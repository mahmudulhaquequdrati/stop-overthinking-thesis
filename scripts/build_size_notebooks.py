#!/usr/bin/env python3
"""Build notebooks 15a (0.8B) and 15b (4B). Run: python scripts/build_size_notebooks.py

Designed for Colab Runtime → Run all:
  - no input() prompts
  - fast path (causal-conv1d + fla) is required
  - batch size picks itself from GPU GB (40 vs 80)
  - prefers Drive mirror of the repo so latest scripts are used
"""

import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB_DIR = os.path.join(ROOT, "notebooks")

CONFIGS = {
    "15a_qwen35_0_8b.ipynb": dict(
        title="15a — Qwen3.5-0.8B (lean: best free ways + LoRA-1)",
        run_tag="0.8b",
        model_profile="qwen35_0_8b",
        hf_id="unsloth/Qwen3.5-0.8B",
        drive_sub="0.8b",
        suggested_hours=50,
        order="NEXT (after 4B; ≤50 compute hours)",
        # Lean plan (DECISIONS #74): enough for the teacher, fits the 50h buffer rule.
        limits=[512, 1024, 2048],   # drop 4096 (not best on 4B; costly)
        stage_a_tries=1,            # one try (drop Stage C)
        run_stage_c=False,
        cost_h={"smoke": 0.4, "A": 12.0, "B1": 8.0, "B2": 1.0, "B3": 3.0},
    ),
    "15b_qwen35_4b.ipynb": dict(
        title="15b — Qwen3.5-4B size × limit × LoRA-1",
        run_tag="4b",
        model_profile="qwen35_4b",
        hf_id="unsloth/Qwen3.5-4B",
        drive_sub="4b",
        suggested_hours=90,
        order="FIRST (done)",
        limits=[512, 1024, 2048, 4096],
        stage_a_tries=1,
        run_stage_c=True,
        cost_h={"smoke": 0.5, "A": 18.0, "B1": 10.0, "B2": 1.5, "B3": 4.0, "C": 22.0},
    ),
}


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": [l + "\n" for l in text.split("\n")]}


def code(text):
    # Avoid a trailing empty line becoming an extra "" cell line with only \n noise
    lines = text.split("\n")
    return {"cell_type": "code", "metadata": {}, "outputs": [], "execution_count": None,
            "source": [l + "\n" for l in lines]}


def build(cfg):
    t = cfg
    profile = t["model_profile"]
    limits = t["limits"]
    limits_txt = "/".join(str(x) for x in limits)
    cost_h = t["cost_h"]
    run_stage_c = t.get("run_stage_c", True)
    stage_a_tries = t.get("stage_a_tries", 1)
    cells = []

    lean_note = ""
    if t["run_tag"] == "0.8b":
        lean_note = """
**Lean plan (≤50 compute hours):** OFF · ON · limits **512 / 1024 / 2048** · LoRA-1 · **1 try** · **no Stage C**.
Dropped limit4096 (not best on 4B) and the second try (saves ~half the answering cost).
Same 234 problems. Enough to answer: smaller size × best free ways × does LoRA beat them?
"""

    cells.append(md(f"""# {t['title']}

**Runtime → Run all** on an **A100** (40GB or 80GB). No typing needed.
{lean_note}
| | |
|---|---|
| Model | `{t['hf_id']}` (`{t['model_profile']}`) |
| Order | **{t['order']}** |
| Drive results | `MyDrive/stop-overthinking/results/{t['drive_sub']}/` |
| Ways | OFF · ON · limit {limits_txt} · **LoRA-1 only** |
| Tries | **{stage_a_tries}** (Stage C: {"yes" if run_stage_c else "NO — skipped to save hours"}) |
| Hour rule | Colab ~100 left; keep ≥50; this run ≤50 more |
| Test set | same **234** problems as the 2B thesis |

**Before Run all:** put latest scripts on Drive:

```text
MyDrive/stop-overthinking/code/
```

Also copy `results/shared/hours_budget.json` to Drive so the 50h cap is enforced.

DECISIONS #72 · #73 · #74."""))

    cells.append(md("""## 1. Install packages

Unsloth (LoRA) + graders + flash-linear-attention (part of the fast path)."""))
    cells.append(code("""%%capture
!pip install -q --upgrade unsloth
!pip install -q evalplus datasets flash-linear-attention
print("pip done")
"""))

    cells.append(md("""## 2. GPU, Drive, latest code, budget

Picks batch size from GPU memory. **80GB → larger batch. 40GB → safer batch.**
Loads code from Drive mirror if present (recommended), else git clone.
**No input()** — safe for Run all."""))

    cells.append(code(f'''import os, sys, json, shutil, subprocess, time, glob
from IPython import get_ipython

name, mem = subprocess.run(
    ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"],
    capture_output=True, text=True).stdout.strip().split(", ")
GPU, GPU_GB = name, float(mem) / 1024
PRODUCTION_OK = ("A100" in GPU or "H100" in GPU) and GPU_GB > 35

# Batch: big enough to be fast, small enough to avoid OOM-split storms on LCB.
# 4B needs more memory per sequence than 0.8B / 2B.
MODEL_PROFILE = "{profile}"
if GPU_GB >= 70:          # A100 80GB
    BATCH = 64 if MODEL_PROFILE == "qwen35_4b" else 128
elif GPU_GB > 35:         # A100 40GB
    BATCH = 32 if MODEL_PROFILE == "qwen35_4b" else 64
else:
    BATCH = 16
print(f"GPU: {{GPU}} ({{GPU_GB:.0f}} GB) · batch {{BATCH}} · "
      + ("OK for the real run" if PRODUCTION_OK else "NOT an A100/H100 — stop"))

def rows(path):
    return sum(1 for l in open(path) if l.strip()) if os.path.exists(path) else 0

def sh(cmd):
    get_ipython().system(cmd)
    if get_ipython().user_ns.get("_exit_code", 0) != 0:
        raise RuntimeError(f"FAILED: {{cmd[:140]}}")

from google.colab import drive
drive.mount("/content/drive")

D = "/content/drive/MyDrive/stop-overthinking/results"
WHEELS = "/content/drive/MyDrive/stop-overthinking/wheels"
DRIVE_CODE = "/content/drive/MyDrive/stop-overthinking/code"
os.makedirs(D, exist_ok=True)
os.makedirs(WHEELS, exist_ok=True)

# Prefer Drive copy of the repo (has your latest scripts). Fallback: GitHub.
if os.path.isdir(f"{{DRIVE_CODE}}/scripts"):
    print("Using Drive code mirror:", DRIVE_CODE)
    sh(f"rm -rf /content/thesis && mkdir -p /content/thesis")
    sh(f"cp -a {{DRIVE_CODE}}/. /content/thesis/")
else:
    print("WARNING: no Drive mirror at", DRIVE_CODE)
    print("  → cloning GitHub (may be older). For latest: upload this repo to that folder.")
    REPO = "https://github.com/mahmudulhaquequdrati/stop-overthinking-thesis.git"
    if not os.path.isdir("/content/thesis"):
        sh(f"git clone -q {{REPO}} /content/thesis")
    else:
        sh("cd /content/thesis && git pull -q || true")

os.chdir("/content/thesis")
sys.path.insert(0, "/content/thesis/scripts")
assert os.path.exists("scripts/gen_colab.py"), "scripts/gen_colab.py missing — fix code sync"
assert os.path.exists("scripts/hours_budget.py"), "scripts/hours_budget.py missing — fix code sync"

RUN_TAG = "{t['run_tag']}"
MODEL = "{profile}"
T = f"{{D}}/{t['drive_sub']}/raw"
SUMMARY = f"{{D}}/{t['drive_sub']}/SUMMARY.md"
HOURS = f"{{D}}/shared/hours_budget.json"
LORA1 = f"{{T}}/lora/lora1"
os.makedirs(T, exist_ok=True)
os.makedirs(LORA1, exist_ok=True)
os.makedirs(os.path.dirname(HOURS), exist_ok=True)

if not os.path.exists(HOURS):
    json.dump(dict(cap_hours=150, used_hours=0.0, runs={{}},
                   note="shared pot for 0.8B + 4B; keep ≥50h of 200 as buffer"),
              open(HOURS, "w"), indent=2)

MAXTOK = {{"he": 4096, "lcb": 8192}}
LIMITS = {limits!r}
SRC = {{"he": "humaneval", "lcb": "lcb"}}
N = {{"he": 164, "lcb": 70}}
WAYS = {{"off": ("thinking_off", None), "on": ("thinking_on", None)}}
for L in LIMITS:
    WAYS[f"limit{{L}}"] = ("limit", None)
WAYS["lora1"] = ("thinking_on", LORA1)
COST_H = {json.dumps(cost_h)}
STAGE_A_TRIES = {stage_a_tries}
RUN_STAGE_C = {run_stage_c!r}

import hours_budget as hb
print(f"model={{MODEL}} · out={{T}}")
print(f"limits={{LIMITS}} · stage_a_tries={{STAGE_A_TRIES}} · stage_c={{RUN_STAGE_C}}")
print(f"shared hours left: {{hb.left(HOURS):.1f}} / {{json.load(open(HOURS)).get('cap_hours', '?')}}")
'''))

    cells.append(md("""## 3. Fast path (REQUIRED)

Without `causal-conv1d` + `fla`, Qwen3.5 runs at ~40 tok/s and burns the hour pot.
With them (2B thesis) we saw hundreds–1000+ tok/s.
This cell **stops the notebook** if the fast path is still off — do not skip it."""))

    cells.append(code("""import glob as _glob

def fast_path_ok():
    return subprocess.run(
        [sys.executable, "-c", "import causal_conv1d, fla"],
        capture_output=True).returncode == 0

for attempt in (1, 2):
    if fast_path_ok():
        break
    whl = _glob.glob(f"{WHEELS}/causal_conv1d*.whl")
    if not whl:
        print("building causal-conv1d once (~5–15 min) → saved on Drive for next time")
        # --no-deps: do NOT let pip pull a newer torch (that breaks Unsloth)
        sh(f"pip wheel -q causal-conv1d --no-build-isolation --no-deps -w {WHEELS}")
        whl = _glob.glob(f"{WHEELS}/causal_conv1d*.whl")
    if not whl:
        raise RuntimeError("pip wheel produced no causal_conv1d*.whl — see errors above")
    # CRITICAL: --no-deps so torch/cuda stay as Unsloth installed them
    sh(f"pip install -q --no-deps {whl[0]}")
    sh("pip install -q --no-deps flash-linear-attention || pip install -q flash-linear-attention")
    # fla may need its own small deps; if import still fails, try with deps once (not torch)
    if not fast_path_ok():
        sh("pip install -q flash-linear-attention")
    if not fast_path_ok() and whl:
        print("wheel did not import with current torch — deleting bad wheel, rebuild once")
        for w in whl:
            try: os.remove(w)
            except OSError: pass

import torch
print("torch", torch.__version__, "cuda", torch.version.cuda, "py", sys.version.split()[0])
if not fast_path_ok():
    raise RuntimeError(
        "FAST PATH OFF. Do not Run all further. "
        "Runtime → Restart session, re-run from cell 1. "
        "Paste the torch/cuda/py line into the chat if it fails again.")
print("FAST PATH ON ✓")
# Quick speed sanity: if someone later sees ~40 tok/s, fast path silently failed at generate time.
print("If Stage A shows <100 tok/s, stop and check: import causal_conv1d, fla")
"""))

    cells.append(md("""## 4. Problems + overlap check"""))
    cells.append(code("""for c in ["python scripts/test_prompts.py",
           "python scripts/build_problem_set.py",
           "python scripts/mbpp_data.py",
           "python scripts/overlap_check.py"]:
    print(">", c); sh(c)
sh(f"cp -f data/overlap_exclude.json {T}/overlap-exclude.json")
print("problems ready")
"""))

    cells.append(md("""## 5. Helpers (resume-safe)"""))
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
    # Limit ways need think_budget + room for code. Else limit4096 + max=4096 → 0 answer tokens.
    use_max = maxtok or MAXTOK[ds]
    if policy == "limit":
        use_max = max(use_max, (think_budget or 1024) + 1024)
    cmd = (f'python scripts/gen_colab.py --policy {policy} --label {way} --model {MODEL} '
           f'--problems {problems} --source {SRC[ds]} --samples {tries} '
           f'--dtype auto --batch {BATCH} --max-tokens {use_max} '
           f'--think-budget {think_budget or 1024} --out "{out}"')
    if stop_on_repeat:
        cmd += " --stop-on-repeat"
    if n:
        cmd += f" --n {n}"
    if adapter:
        if not os.path.exists(f"{adapter}/adapter_config.json"):
            raise RuntimeError(f"LoRA missing at {adapter}")
        cmd += f' --adapter "{adapter}"'
    if only_ids:
        cmd += f' --only-ids "{only_ids}"'
    print(f"  {way:<10}{ds:<4} answering ...", flush=True)
    sh(cmd)
    return out

def graded_ok(ans):
    g = ans.replace(".jsonl", "-graded.csv")
    return (os.path.exists(g) and rows(g) - 1 == rows(ans)
            and os.path.getmtime(g) >= os.path.getmtime(ans))

def grade(ans, ds, problems="data/problems.json", wait=False):
    for a, p in BG:
        if a == ans:
            p.wait()
    if graded_ok(ans):
        return
    if ds == "mbpp":
        script = "grade_mbpp.py"
    elif ds == "he":
        script = "grade_plus.py"
    else:
        script = "grade_lcb.py"
    p = subprocess.Popen(
        [sys.executable, f"scripts/{script}", "--answers", ans, "--problems", problems],
        stdout=open(ans + ".grade.log", "w"), stderr=subprocess.STDOUT)
    if wait:
        p.wait(); print("  graded", ans)
    else:
        BG.append((ans, p))

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
    assert PRODUCTION_OK, "Need A100/H100 with >35GB for production stages"
    cost = COST_H[cost_key or name]
    if not hb.gate(HOURS, RUN_TAG, name, cost):
        return
    hb.start_stage(HOURS, RUN_TAG, name)
    try:
        for w, ds in todo:
            grade(answer(w, ds, tries), ds)
    finally:
        hb.end_stage(HOURS, RUN_TAG, name)

print("helpers ready · free ways:", free_ways(), "· batch", BATCH)
'''))

    cells.append(md("""## 6. Smoke test

Tiny check: every free way answers, counts thinking, grades. Then we know Run all is safe."""))
    cells.append(code("""SM = f"{T}/smoke"
if os.path.exists(f"{SM}/PASSED"):
    print("smoke already passed - skipped")
elif hb.gate(HOURS, RUN_TAG, "smoke", COST_H["smoke"]):
    hb.start_stage(HOURS, RUN_TAG, "smoke")
    try:
        shutil.rmtree(SM, ignore_errors=True); os.makedirs(SM)
        for w in free_ways():
            for ds in SRC:
                grade(answer(w, ds, 1, folder=SM, n=2, maxtok=256, think_budget=128),
                      ds, wait=True)
        for w in free_ways():
            for ds in SRC:
                r = [json.loads(l) for l in open(ans_path(w, ds, SM))]
                assert len(r) == 2, f"{w} {ds}: expected 2"
                if w == "off":
                    assert all(x["thinking_tokens"] == 0 for x in r), "OFF has thinking"
                else:
                    assert any(x["thinking_tokens"] > 0 for x in r), f"{w} 0 thinking"
                assert graded_ok(ans_path(w, ds, SM)), f"{w} {ds} not graded"
        open(f"{SM}/PASSED", "w").write("ok")
        print("SMOKE PASSED ✓")
    finally:
        hb.end_stage(HOURS, RUN_TAG, "smoke")
"""))

    stage_a_note = (
        "OFF · ON · the limits listed above. **1 try** (lean plan). Skips finished files."
        if not run_stage_c
        else "OFF · ON · the limits listed above. **1 try** here; Stage C adds a second try later."
    )
    cells.append(md(f"""## 7. Stage A — free ways on 234

{stage_a_note}"""))
    cells.append(code("""assert PRODUCTION_OK
stage("A", free_ways(), tries=STAGE_A_TRIES, cost_key="A")
wait_grading()
print("stage A done. Hours left:", round(hb.left(HOURS), 1))
"""))

    cells.append(md("""## 8. Stage B — LoRA-1 (full MBPP+ train, all kept examples)

No LoRA-2. Resume-safe."""))
    cells.append(code("""TR_ANS = f"{T}/train-mbpp-on.jsonl"
TRAIN = f"{T}/train-set-lora1.jsonl"
EXCLUDE = f"{T}/overlap-exclude.json"

if hb.gate(HOURS, RUN_TAG, "B1", COST_H["B1"]):
    hb.start_stage(HOURS, RUN_TAG, "B1")
    try:
        n_train = sum(1 for p in json.load(open("data/mbpp.json"))["problems"]
                      if p.get("split") == "train")
        want = n_train * 4
        print(f"MBPP+ train: {n_train} problems · want {want} answers")
        if rows(TR_ANS) < want:
            cmd = (f'python scripts/gen_colab.py --policy thinking_on --label on --model {MODEL} '
                   f'--problems data/mbpp.json --source mbpp --split train --samples 4 '
                   f'--dtype auto --batch {BATCH} --max-tokens 4096 --stop-on-repeat '
                   f'--out "{TR_ANS}"')
            print(cmd); sh(cmd)
        if not graded_ok(TR_ANS):
            sh(f'python scripts/grade_mbpp.py --answers "{TR_ANS}" --problems data/mbpp.json')
    finally:
        hb.end_stage(HOURS, RUN_TAG, "B1")

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

if os.path.exists(f"{LORA1}/adapter_config.json"):
    stage("B3", ["lora1"], tries=1, cost_key="B3")
    wait_grading()
else:
    print("B3 skipped: no LoRA-1")
"""))

    if run_stage_c:
        cells.append(md("""## 9. Stage C — second try (if hours remain)

Skipped automatically when the shared pot is too low."""))
        cells.append(code("""ways_c = free_ways() + (["lora1"] if os.path.exists(f"{LORA1}/adapter_config.json") else [])
stage("C", ways_c, tries=2, cost_key="C")
wait_grading()
print("hours left:", round(hb.left(HOURS), 1))
"""))
    else:
        cells.append(md("""## 9. Stage C — skipped on purpose

**0.8B lean plan:** no second try. Saves about half the answering cost. One try is enough to compare ways."""))
        cells.append(code("""print("Stage C skipped (lean 0.8B plan, DECISIONS #74). Hours left:", round(hb.left(HOURS), 1))
"""))

    cells.append(md("""## 10. Finish + SUMMARY.md on Drive"""))
    cells.append(code("""wait_grading()
for way in free_ways() + (["lora1"] if os.path.exists(f"{LORA1}/adapter_config.json") else []):
    for ds in SRC:
        a = ans_path(way, ds)
        if rows(a) and not graded_ok(a):
            grade(a, ds, wait=True)

sh(f'python scripts/make_size_summary.py --dir "{T}" --run {RUN_TAG} --summary "{SUMMARY}"')
print("=== hours ===")
print(open(HOURS).read())
print(f"DONE ✓  results in Drive: results/{RUN_TAG}/")
"""))

    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "cells": cells,
    }


def main():
    for name, cfg in CONFIGS.items():
        path = os.path.join(NB_DIR, name)
        with open(path, "w") as f:
            json.dump(build(cfg), f, indent=1)
            f.write("\n")
        print("wrote", path)


if __name__ == "__main__":
    main()
