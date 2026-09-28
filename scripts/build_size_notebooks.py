#!/usr/bin/env python3
"""Build notebooks 15a (0.8B) and 15b (4B) from one template. Run: python scripts/build_size_notebooks.py"""

import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB_DIR = os.path.join(ROOT, "notebooks")

CONFIGS = {
    "15a_qwen35_0_8b.ipynb": dict(
        title="15a — Qwen3.5-0.8B size × limit × LoRA-1",
        run_tag="0.8b",
        model_profile="qwen35_0_8b",
        hf_id="unsloth/Qwen3.5-0.8B",
        drive_sub="0.8b",
        suggested_hours=60,
        order="SECOND (after 4B)",
    ),
    "15b_qwen35_4b.ipynb": dict(
        title="15b — Qwen3.5-4B size × limit × LoRA-1",
        run_tag="4b",
        model_profile="qwen35_4b",
        hf_id="unsloth/Qwen3.5-4B",
        drive_sub="4b",
        suggested_hours=90,
        order="FIRST",
    ),
}

# Estimated A100 hours per stage (shared 150h pot). Soft; real wall time is logged.
COST_H = {
    "smoke": 0.5,
    "A": 25.0,      # free ways × 234 × 1 try (OFF + ON + 4 limits)
    "B1": 12.0,     # MBPP+ train answers × 4 tries (LoRA-1 data)
    "B2": 1.5,      # train LoRA-1
    "B3": 5.0,      # test LoRA-1 try 1
    "C": 30.0,      # second try (optional)
}


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": [l + "\n" for l in text.split("\n")]}


def code(text):
    return {"cell_type": "code", "metadata": {}, "outputs": [], "execution_count": None,
            "source": [l + "\n" for l in text.split("\n")]}


def build(cfg):
    t = cfg
    cells = []

    cells.append(md(f"""# {t['title']}

**In one sentence:** on **{t['hf_id']}**, compare thinking OFF · ON · limits 512/1024/2048/4096 · and **LoRA-1** (full MBPP+ shortest-correct), on the same **234** test problems as the 2B thesis.

**Run order:** {t['order']}. Shared hour pot with the other size notebook: **≤150 hours combined**.

| | |
|---|---|
| Model profile | `{t['model_profile']}` |
| Drive folder | `MyDrive/stop-overthinking/results/{t['drive_sub']}/` |
| LoRA | **LoRA-1 only** (no LoRA-2) |
| Suggested hours for this run | ≤ {t['suggested_hours']} of the shared 150 |
| Dropped | "think briefly" (already explained on 2B) |

**Problem this solves:** the teacher asks "why only one model / why only 1024?".  
**Why:** same family, change only size + thinking limit + LoRA-1.  
**In:** 234 test problems + MBPP+ train for LoRA-1. **Out:** raw JSONL + graded CSV in this model's folder only.  
**Why this way:** 2B results stay untouched; each size has its own Colab and folder (DECISIONS #72)."""))

    cells.append(md("""## 1. Install

**Problem:** Colab starts empty. **Why:** Unsloth for LoRA-1, evalplus for grading."""))
    cells.append(code("""%%capture
!pip install -q unsloth
!pip install -q evalplus datasets flash-linear-attention"""))

    cells.append(md("""## 2. Config, GPU, Drive, shared hour pot

**Problem:** every path and the 150h cap must live in one place.  
**In:** hours left in the shared pot (read from Drive). **Out:** `T` folder for this model only."""))

    cells.append(code(f'''import os, sys, json, shutil, subprocess, time
from IPython import get_ipython

name, mem = subprocess.run(
    ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"],
    capture_output=True, text=True).stdout.strip().split(", ")
GPU, GPU_GB = name, float(mem) / 1024
PRODUCTION_OK = ("A100" in GPU or "H100" in GPU) and GPU_GB > 35
BATCH = 128 if GPU_GB > 35 else 16
print(f"GPU: {{GPU}} ({{GPU_GB:.0f}} GB) · batch {{BATCH}} · "
      + ("OK for the real run" if PRODUCTION_OK else "NOT an A100: only the smoke test will run"))

def rows(path):
    return sum(1 for l in open(path) if l.strip()) if os.path.exists(path) else 0

def sh(cmd):
    get_ipython().system(cmd)
    if get_ipython().user_ns.get("_exit_code", 0) != 0:
        raise RuntimeError(f"FAILED (read the lines above): {{cmd[:120]}}")

from google.colab import drive
drive.mount("/content/drive")
REPO = "https://github.com/mahmudulhaquequdrati/stop-overthinking-thesis.git"
if not os.path.isdir("/content/thesis"):
    sh(f"git clone -q {{REPO}} /content/thesis")
else:
    sh("cd /content/thesis && git pull -q")
os.chdir("/content/thesis"); sys.path.insert(0, "/content/thesis/scripts")

# --- THIS RUN ONLY (do not write into the 2B thesis/ folder) ---
RUN_TAG   = "{t['run_tag']}"
MODEL     = "{t['model_profile']}"
D         = "/content/drive/MyDrive/stop-overthinking/results"
T         = f"{{D}}/{t['drive_sub']}/raw"          # answers + LoRA for this size
SUMMARY   = f"{{D}}/{t['drive_sub']}/SUMMARY.md"
HOURS     = f"{{D}}/shared/hours_budget.json"      # shared 150h pot
LORA1     = f"{{T}}/lora/lora1"
WHEELS    = "/content/drive/MyDrive/stop-overthinking/wheels"
os.makedirs(T, exist_ok=True)
os.makedirs(LORA1, exist_ok=True)
os.makedirs(os.path.dirname(HOURS), exist_ok=True)
os.makedirs(WHEELS, exist_ok=True)

# Seed the shared pot on Drive if missing (first Colab to run).
if not os.path.exists(HOURS):
    json.dump(dict(cap_hours=150, used_hours=0.0, runs={{}},
                   note="shared pot for 0.8B + 4B; keep ≥50h of the 200 as buffer"),
              open(HOURS, "w"), indent=2)

MAXTOK = {{"he": 4096, "lcb": 8192}}
LIMITS = [512, 1024, 2048, 4096]          # the limit sweep (answers "why only 1024?")
SRC    = {{"he": "humaneval", "lcb": "lcb"}}
N      = {{"he": 164, "lcb": 70}}          # same 234 as notebook 14

# Ways: free options + LoRA-1. No "brief", no LoRA-2.
WAYS = {{"off": ("thinking_off", None), "on": ("thinking_on", None)}}
for L in LIMITS:
    WAYS[f"limit{{L}}"] = ("limit", None)   # think-budget set per call
WAYS["lora1"] = ("thinking_on", LORA1)

COST_H = {json.dumps(COST_H)}

import hours_budget as hb
print(f"model={{MODEL}} · folder={{T}}")
print(f"shared hours left: {{hb.left(HOURS):.1f}} of 150")
print("Type the SHARED hours already used by the OTHER size run (0 if first):")
# Soft check only — the JSON on Drive is the real ledger.
_ = input("(press Enter to continue; ledger on Drive is authoritative) ")
'''))

    cells.append(md("""## 3. Fast path (causal-conv1d), once per machine

**Problem:** without the fast kernel, answering is much slower. Same as notebook 14."""))
    cells.append(code("""import glob as _glob

def fast_path_ok():
    return subprocess.run([sys.executable, "-c", "import causal_conv1d"],
                          capture_output=True).returncode == 0

if fast_path_ok():
    print("fast path already importable")
else:
    found = _glob.glob(f"{WHEELS}/causal_conv1d*.whl")
    if found:
        sh(f"pip install -q {found[0]}")
    else:
        print("building/installing causal-conv1d (may be slow) ...")
        sh("pip install -q causal-conv1d || true")
    print("fast path OK" if fast_path_ok() else
          "WARNING: fast path missing — run will be slower but still correct")
"""))

    cells.append(md("""## 4. Problems, overlap check, prompt switch check

**Problem:** same 234 test set; LoRA-1 trains on **all MBPP+ train problems** (100), full kept set."""))
    cells.append(code("""for c in ["python scripts/test_prompts.py",
           "python scripts/build_problem_set.py",
           "python scripts/mbpp_data.py",
           "python scripts/overlap_check.py"]:
    print(">", c); sh(c)
# Copy the exclude list into this run's folder (do not share with 2B Drive tree).
sh(f"cp data/overlap_exclude.json {T}/overlap-exclude.json")
print("problem set + overlap list ready")
"""))

    cells.append(md("""## 5. Helpers (answer, grade, stage, hours)

**Problem:** same steps for every way; skip finished work; log hours into the shared pot."""))
    cells.append(code('''BG = []

def ans_path(way, ds, folder=None, prefix="test"):
    return f"{folder or T}/{prefix}-{way}-{ds}.jsonl"

def answer(way, ds, tries, folder=None, n=0, maxtok=None, think_budget=None,
           only_ids=None, prefix="test", stop_on_repeat=True, problems="data/problems.json"):
    out = ans_path(way, ds, folder, prefix)
    want = (len(json.load(open(only_ids))) if only_ids else (n or N[ds])) * tries
    if rows(out) >= want:
        print(f"  {way:<10}{ds:<4} complete ({rows(out)}) - skipped"); return out
    policy, adapter = WAYS[way]
    if way.startswith("limit") and think_budget is None:
        think_budget = int(way.replace("limit", ""))
    cmd = (f'python scripts/gen_colab.py --policy {policy} --label {way} --model {MODEL} '
           f'--problems {problems} --source {SRC[ds]} --samples {tries} '
           f'--dtype auto --batch {BATCH} --max-tokens {maxtok or MAXTOK[ds]} '
           f'--think-budget {think_budget or 1024} --out "{out}"')
    if stop_on_repeat: cmd += " --stop-on-repeat"
    if n: cmd += f" --n {n}"
    if adapter:
        if not os.path.exists(f"{adapter}/adapter_config.json"):
            raise RuntimeError(f"LoRA missing at {adapter} — train it before testing lora1")
        cmd += f' --adapter "{adapter}"'
    if only_ids: cmd += f' --only-ids "{only_ids}"'
    print(f"  {way:<10}{ds:<4} answering ...", flush=True)
    sh(cmd)
    return out

def graded_ok(ans):
    g = ans.replace(".jsonl", "-graded.csv")
    return os.path.exists(g) and rows(g) - 1 == rows(ans) and os.path.getmtime(g) >= os.path.getmtime(ans)

def grade(ans, ds, problems="data/problems.json", wait=False):
    for a, p in BG:
        if a == ans: p.wait()
    if graded_ok(ans): return
    if ds == "mbpp":
        script = "grade_mbpp.py"
    elif ds in ("he",):
        script = "grade_plus.py"
    else:
        script = "grade_lcb.py"
    p = subprocess.Popen([sys.executable, f"scripts/{script}", "--answers", ans, "--problems", problems],
                         stdout=open(ans + ".grade.log", "w"), stderr=subprocess.STDOUT)
    if wait: p.wait(); print("  graded", ans)
    else: BG.append((ans, p))

def wait_grading():
    for ans, p in BG:
        p.wait(); print("  graded", ans)
    BG.clear()

def free_ways():
    return ["off", "on"] + [f"limit{L}" for L in LIMITS]

def stage(name, ways, tries, cost_key=None):
    todo = [(w, ds) for w in ways for ds in SRC if rows(ans_path(w, ds)) < N[ds] * tries]
    if not todo:
        print(f"stage {name}: already complete"); return
    assert PRODUCTION_OK, "Production stages need the A100 (step 2)."
    cost = COST_H[cost_key or name]
    if not hb.gate(HOURS, RUN_TAG, name, cost): return
    hb.start_stage(HOURS, RUN_TAG, name)
    try:
        for w, ds in todo:
            grade(answer(w, ds, tries), ds)
    finally:
        hb.end_stage(HOURS, RUN_TAG, name)
print("helpers ready · free ways:", free_ways())
'''))

    cells.append(md("""## 6. Smoke test (~0.5 h)

**Problem:** catch a broken switch / grader before burning hours."""))
    cells.append(code("""SM = f"{T}/smoke"
if os.path.exists(f"{SM}/PASSED"):
    print("smoke already passed - skipped")
elif hb.gate(HOURS, RUN_TAG, "smoke", COST_H["smoke"]):
    hb.start_stage(HOURS, RUN_TAG, "smoke")
    try:
        shutil.rmtree(SM, ignore_errors=True); os.makedirs(SM)
        for w in free_ways():
            for ds in SRC:
                grade(answer(w, ds, 1, folder=SM, n=2, maxtok=256, think_budget=128), ds, wait=True)
        for w in free_ways():
            for ds in SRC:
                r = [json.loads(l) for l in open(ans_path(w, ds, SM))]
                assert len(r) == 2, f"{w} {ds}: expected 2"
                if w == "off":
                    assert all(x["thinking_tokens"] == 0 for x in r), "OFF has thinking - STOP"
                else:
                    assert any(x["thinking_tokens"] > 0 for x in r), f"{w} counted 0 thinking - STOP"
                assert graded_ok(ans_path(w, ds, SM)), f"{w} {ds} not graded"
        open(f"{SM}/PASSED", "w").write("ok")
        print("SMOKE PASSED")
    finally:
        hb.end_stage(HOURS, RUN_TAG, "smoke")
"""))

    cells.append(md("""## 7. Stage A — free ways on all 234 (try 1)

**Problem:** the teacher's table: OFF · ON · limits 512/1024/2048/4096."""))
    cells.append(code("""stage("A", free_ways(), tries=1, cost_key="A")
wait_grading()
print("stage A done (or skipped). Hours left:", round(hb.left(HOURS), 1))
"""))

    cells.append(md("""## 8. Stage B — LoRA-1 only (all MBPP+ train problems, 100%)

**Problem:** rebuild the mini-thesis LoRA-1 recipe on **this** model. No LiveCodeBench train data.

```text
100 MBPP+ train → 4 tries ON → keep shortest correct → train LoRA on ALL kept → test on 234
```
"""))
    cells.append(code("""TR_ANS = f"{T}/train-mbpp-on.jsonl"
TRAIN  = f"{T}/train-set-lora1.jsonl"
EXCLUDE = f"{T}/overlap-exclude.json"

# B1: generate training answers (all MBPP+ train split, 4 tries)
if hb.gate(HOURS, RUN_TAG, "B1", COST_H["B1"]):
    hb.start_stage(HOURS, RUN_TAG, "B1")
    try:
        n_train = sum(1 for p in json.load(open("data/mbpp.json"))["problems"]
                      if p.get("split") == "train")
        want = n_train * 4
        print(f"MBPP+ train problems: {n_train} · want {want} answers")
        if rows(TR_ANS) < want:
            cmd = (f'python scripts/gen_colab.py --policy thinking_on --label on --model {MODEL} '
                   f'--problems data/mbpp.json --source mbpp --split train --samples 4 '
                   f'--dtype auto --batch {BATCH} --max-tokens 4096 --stop-on-repeat '
                   f'--out "{TR_ANS}"')
            print(cmd); sh(cmd)
        # grade with MBPP grader
        if not graded_ok(TR_ANS):
            sh(f'python scripts/grade_mbpp.py --answers "{TR_ANS}" --problems data/mbpp.json')
    finally:
        hb.end_stage(HOURS, RUN_TAG, "B1")

# B2: make train set + train LoRA-1 on ALL kept examples (fraction 1.0)
if os.path.exists(f"{LORA1}/adapter_config.json"):
    print("B2: LoRA-1 already trained - skipped")
elif hb.gate(HOURS, RUN_TAG, "B2", COST_H["B2"]):
    hb.start_stage(HOURS, RUN_TAG, "B2")
    try:
        sh(f'python scripts/make_train_set.py --answers "{TR_ANS}" --problems data/mbpp.json '
           f'--splits train --exclude "{EXCLUDE}" --out "{TRAIN}"')
        sh(f'python scripts/train_lora.py --train "{TRAIN}" --fraction 1.0 --epochs 3 '
           f'--model {MODEL} --out "{LORA1}"')
        assert os.path.exists(f"{LORA1}/adapter_config.json"), "LoRA-1 save failed"
    finally:
        hb.end_stage(HOURS, RUN_TAG, "B2")

# B3: test LoRA-1 on 234, try 1
if os.path.exists(f"{LORA1}/adapter_config.json"):
    stage("B3", ["lora1"], tries=1, cost_key="B3")
    wait_grading()
else:
    print("B3 skipped: no LoRA-1 adapter")
"""))

    cells.append(md("""## 9. Stage C — second try (only if hours remain)

**Problem:** tighter error bars. Skip if the shared pot is tight."""))
    cells.append(code("""ways_c = free_ways() + (["lora1"] if os.path.exists(f"{LORA1}/adapter_config.json") else [])
stage("C", ways_c, tries=2, cost_key="C")
wait_grading()
print("hours left:", round(hb.left(HOURS), 1))
"""))

    cells.append(md("""## 10. Finish grading + local summary table

**Problem:** write SUMMARY.md for this model; later join into ALL-RESULTS."""))
    cells.append(code("""wait_grading()
for way in free_ways() + (["lora1"] if os.path.exists(f"{LORA1}/adapter_config.json") else []):
    for ds in SRC:
        a = ans_path(way, ds)
        if rows(a) and not graded_ok(a):
            grade(a, ds, wait=True)

sh(f'python scripts/make_size_summary.py --dir "{T}" --run {RUN_TAG} --summary "{SUMMARY}"')
print("\\n=== hours budget ===")
print(open(HOURS).read())
print(f"\\nDone. Copy Drive results/{RUN_TAG}/ into the git repo when finished.")
print("Then locally: python scripts/make_all_results.py")
"""))

    return {"nbformat": 4, "nbformat_minor": 5,
            "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                         "language_info": {"name": "python"}},
            "cells": cells}


def main():
    for name, cfg in CONFIGS.items():
        path = os.path.join(NB_DIR, name)
        with open(path, "w") as f:
            json.dump(build(cfg), f, indent=1)
        print("wrote", path)


if __name__ == "__main__":
    main()
