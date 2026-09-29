#!/usr/bin/env python3
"""Build notebook 16: Qwen3.5-2B · limit512 only · 234 problems · 2 tries.

Run: python scripts/build_2b_limit512_notebook.py
"""

import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "notebooks", "16_qwen35_2b_limit512.ipynb")


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": [l + "\n" for l in text.split("\n")]}


def code(text):
    lines = text.split("\n")
    return {"cell_type": "code", "metadata": {}, "outputs": [], "execution_count": None,
            "source": [l + "\n" for l in lines]}


def build():
    cells = []

    cells.append(md("""# 16 — Qwen3.5-2B · limit 512 only

**Runtime → Run all** on an **A100** (40GB or 80GB). No typing needed.

Fills the empty cell in the size table: **2B × Limit 512**.  
Nothing else: no OFF/ON, no other limits, no LoRA, no Stage C beyond 2 tries in one pass.

| | |
|---|---|
| Model | `unsloth/Qwen3.5-2B` (`qwen35_2b`) |
| Way | **limit512 only** |
| Tries | **2** (same as main 2B thesis) |
| Problems | same **234** (HumanEval+ 164 + LiveCodeBench 70) |
| Drive results | `MyDrive/stop-overthinking/results/2b-limit512/` |
| Does not touch | finished 2B thesis folder `results/2026-09-24-thesis-run/` |

**Before Run all:** put latest scripts on Drive:

```text
MyDrive/stop-overthinking/code/
```

Also copy `results/shared/hours_budget.json` to Drive.

DECISIONS #81."""))

    cells.append(md("""## 1. Install packages"""))
    cells.append(code("""%%capture
!pip install -q --upgrade unsloth
!pip install -q evalplus datasets flash-linear-attention
print("pip done")
"""))

    cells.append(md("""## 2. GPU, Drive, latest code, budget

Picks batch size from GPU memory. Prefer Drive code mirror."""))
    cells.append(code("""import os, sys, json, shutil, subprocess, time, glob
from IPython import get_ipython

name, mem = subprocess.run(
    ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"],
    capture_output=True, text=True).stdout.strip().split(", ")
GPU, GPU_GB = name, float(mem) / 1024
PRODUCTION_OK = ("A100" in GPU or "H100" in GPU) and GPU_GB > 35

MODEL_PROFILE = "qwen35_2b"
if GPU_GB >= 70:
    BATCH = 128
elif GPU_GB > 35:
    BATCH = 64
else:
    BATCH = 16
print(f"GPU: {GPU} ({GPU_GB:.0f} GB) · batch {BATCH} · "
      + ("OK for the real run" if PRODUCTION_OK else "NOT an A100/H100 — stop"))

def rows(path):
    return sum(1 for l in open(path) if l.strip()) if os.path.exists(path) else 0

def sh(cmd):
    get_ipython().system(cmd)
    if get_ipython().user_ns.get("_exit_code", 0) != 0:
        raise RuntimeError(f"FAILED: {cmd[:140]}")

from google.colab import drive
drive.mount("/content/drive")

D = "/content/drive/MyDrive/stop-overthinking/results"
WHEELS = "/content/drive/MyDrive/stop-overthinking/wheels"
DRIVE_CODE = "/content/drive/MyDrive/stop-overthinking/code"
os.makedirs(D, exist_ok=True)
os.makedirs(WHEELS, exist_ok=True)

if os.path.isdir(f"{DRIVE_CODE}/scripts"):
    print("Using Drive code mirror:", DRIVE_CODE)
    sh("rm -rf /content/thesis && mkdir -p /content/thesis")
    sh(f"cp -a {DRIVE_CODE}/. /content/thesis/")
else:
    print("WARNING: no Drive mirror at", DRIVE_CODE)
    REPO = "https://github.com/mahmudulhaquequdrati/stop-overthinking-thesis.git"
    if not os.path.isdir("/content/thesis"):
        sh(f"git clone -q {REPO} /content/thesis")
    else:
        sh("cd /content/thesis && git pull -q || true")

os.chdir("/content/thesis")
sys.path.insert(0, "/content/thesis/scripts")
assert os.path.exists("scripts/gen_colab.py"), "scripts/gen_colab.py missing — fix code sync"
assert os.path.exists("scripts/hours_budget.py"), "scripts/hours_budget.py missing — fix code sync"

RUN_TAG = "2b_limit512"
MODEL = "qwen35_2b"
T = f"{D}/2b-limit512/raw"
SUMMARY = f"{D}/2b-limit512/SUMMARY.md"
HOURS = f"{D}/shared/hours_budget.json"
os.makedirs(T, exist_ok=True)
os.makedirs(os.path.dirname(HOURS), exist_ok=True)
os.makedirs(os.path.dirname(SUMMARY), exist_ok=True)

if not os.path.exists(HOURS):
    json.dump(dict(cap_hours=58.544, used_hours=0.0, runs={},
                   note="shared pot; keep ≥50h buffer"),
              open(HOURS, "w"), indent=2)

MAXTOK = {"he": 4096, "lcb": 8192}
THINK_BUDGET = 512
TRIES = 2
SRC = {"he": "humaneval", "lcb": "lcb"}
N = {"he": 164, "lcb": 70}
WAYS = {"limit512": ("limit", None)}
COST_H = {"smoke": 0.3, "A": 6.0}

import hours_budget as hb
print(f"model={MODEL} · out={T} · limit={THINK_BUDGET} · tries={TRIES}")
print(f"shared hours left: {hb.left(HOURS):.1f} / {json.load(open(HOURS)).get('cap_hours', '?')}")
"""))

    cells.append(md("""## 3. Fast path (REQUIRED)

Without `causal-conv1d` + `fla`, Qwen3.5 runs at ~40 tok/s. This cell **stops** if fast path is off."""))
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
        sh(f"pip wheel -q causal-conv1d --no-build-isolation --no-deps -w {WHEELS}")
        whl = _glob.glob(f"{WHEELS}/causal_conv1d*.whl")
    if not whl:
        raise RuntimeError("pip wheel produced no causal_conv1d*.whl — see errors above")
    sh(f"pip install -q --no-deps {whl[0]}")
    sh("pip install -q --no-deps flash-linear-attention || pip install -q flash-linear-attention")
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
        "Runtime → Restart session, re-run from cell 1.")
print("FAST PATH ON ✓")
print("If answering shows <100 tok/s, stop and check: import causal_conv1d, fla")
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
    cells.append(code("""BG = []

def ans_path(way, ds, folder=None, prefix="test"):
    return f"{folder or T}/{prefix}-{way}-{ds}.jsonl"

def answer(way, ds, tries, folder=None, n=0, maxtok=None, think_budget=None,
           only_ids=None, prefix="test", stop_on_repeat=True, problems="data/problems.json"):
    out = ans_path(way, ds, folder, prefix)
    want = (len(json.load(open(only_ids))) if only_ids else (n or N[ds])) * tries
    if rows(out) >= want:
        print(f"  {way:<10}{ds:<4} complete ({rows(out)}) - skipped"); return out
    policy, adapter = WAYS[way]
    if think_budget is None:
        think_budget = THINK_BUDGET
    use_max = maxtok or MAXTOK[ds]
    use_max = max(use_max, think_budget + 1024)
    cmd = (f'python scripts/gen_colab.py --policy {policy} --label {way} --model {MODEL} '
           f'--problems {problems} --source {SRC[ds]} --samples {tries} '
           f'--dtype auto --batch {BATCH} --max-tokens {use_max} '
           f'--think-budget {think_budget} --out "{out}"')
    if stop_on_repeat:
        cmd += " --stop-on-repeat"
    if n:
        cmd += f" --n {n}"
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
    script = "grade_plus.py" if ds == "he" else "grade_lcb.py"
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

print("helpers ready · way: limit512 · batch", BATCH)
"""))

    cells.append(md("""## 6. Smoke (2 problems)

Sanity check only. Accuracy here means nothing."""))
    cells.append(code("""assert PRODUCTION_OK, "Need A100/H100 with >35GB"
SM = f"{T}/smoke"
os.makedirs(SM, exist_ok=True)

if os.path.exists(f"{SM}/PASSED"):
    print("smoke already PASSED - skipped")
else:
    if not hb.gate(HOURS, RUN_TAG, "smoke", COST_H["smoke"]):
        raise RuntimeError("hours gate blocked smoke")
    hb.start_stage(HOURS, RUN_TAG, "smoke")
    try:
        for ds in SRC:
            ans = answer("limit512", ds, 1, folder=SM, n=2, maxtok=256, think_budget=128)
            grade(ans, ds, wait=True)
            r = [json.loads(l) for l in open(ans_path("limit512", ds, SM))]
            assert any(x["thinking_tokens"] > 0 for x in r), "limit512 0 thinking"
            assert graded_ok(ans_path("limit512", ds, SM)), f"limit512 {ds} not graded"
        open(f"{SM}/PASSED", "w").write("ok")
        print("SMOKE PASSED ✓")
    finally:
        hb.end_stage(HOURS, RUN_TAG, "smoke")
"""))

    cells.append(md("""## 7. Stage A — limit512 on 234 · 2 tries

Resume-safe. Skips finished files."""))
    cells.append(code("""assert PRODUCTION_OK
todo = [(ds,) for ds in SRC if rows(ans_path("limit512", ds)) < N[ds] * TRIES]
if not todo and all(graded_ok(ans_path("limit512", ds)) for ds in SRC):
    print("stage A: already complete")
else:
    if not hb.gate(HOURS, RUN_TAG, "A", COST_H["A"]):
        raise RuntimeError("hours gate blocked Stage A")
    hb.start_stage(HOURS, RUN_TAG, "A")
    try:
        for ds in SRC:
            grade(answer("limit512", ds, TRIES), ds)
        wait_grading()
    finally:
        hb.end_stage(HOURS, RUN_TAG, "A")
print("stage A done. Hours left:", round(hb.left(HOURS), 1))
"""))

    cells.append(md("""## 8. Finish + SUMMARY.md on Drive"""))
    cells.append(code("""wait_grading()
for ds in SRC:
    a = ans_path("limit512", ds)
    if rows(a) and not graded_ok(a):
        grade(a, ds, wait=True)

sh(f'python scripts/make_size_summary.py --dir "{T}" --run 2b-limit512 --summary "{SUMMARY}"')
print("=== hours ===")
print(open(HOURS).read())
print("DONE ✓  results in Drive: results/2b-limit512/")
print("Next: zip that folder into the laptop repo and fill SIZE-COMPARISON.md")
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
    nb = build()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(nb, f, indent=1)
        f.write("\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
