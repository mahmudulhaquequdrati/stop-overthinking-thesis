#!/usr/bin/env python3
"""Build notebook 17: Qwen3.5-2B · limit2048 only · LEAN (1 try, tight max tokens).

Saves compute hours vs a full 2-try / 8k-token run:
  - 1 try only (enough to see if 2048 beats 1024)
  - max_new_tokens = budget + 1024 only (no 8192 LCB waste)
  - stop-on-repeat on
  - no OFF/ON/LoRA/other limits

Run: python scripts/build_2b_limit2048_notebook.py
"""

import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "notebooks", "17_qwen35_2b_limit2048.ipynb")


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": [l + "\n" for l in text.split("\n")]}


def code(text):
    lines = text.split("\n")
    return {"cell_type": "code", "metadata": {}, "outputs": [], "execution_count": None,
            "source": [l + "\n" for l in lines]}


def build():
    cells = []

    cells.append(md("""# 17 — Qwen3.5-2B · limit 2048 only (LEAN)

**Runtime → Run all** on an **A100**. No typing needed.

Question: on 2B, does accuracy keep rising past 1024, or peak?
(We already have limit512 = 45.1% and limit1024 = 49.8%.)

**Cheap on purpose** (you have few compute hours left):

| Save | How |
|---|---|
| ~½ answering cost | **1 try** only (not 2) |
| No long LCB waste | `max_tokens = 2048 + 1024` only (not 8192) |
| Loop cut | `--stop-on-repeat` |
| No extras | only limit2048 — no OFF/ON/LoRA/4096 |

| | |
|---|---|
| Model | `unsloth/Qwen3.5-2B` |
| Way | **limit2048 only** |
| Tries | **1** (lean) |
| Problems | same **234** |
| Drive results | `MyDrive/stop-overthinking/results/2b-limit2048/` |

Caption later: **2B limit2048 = 1 try**; main 2B table stays 2 tries.

**Before Run all:** Drive `stop-overthinking/code/` + `results/shared/hours_budget.json`.

DECISIONS #83."""))

    cells.append(md("""## 1. Install packages"""))
    cells.append(code("""%%capture
!pip install -q --upgrade unsloth
!pip install -q evalplus datasets flash-linear-attention
print("pip done")
"""))

    cells.append(md("""## 2. GPU, Drive, code, budget

Bigger batch when VRAM allows → fewer wall seconds per token."""))
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
assert os.path.exists("scripts/gen_colab.py"), "scripts/gen_colab.py missing"
assert os.path.exists("scripts/hours_budget.py"), "scripts/hours_budget.py missing"

RUN_TAG = "2b_limit2048"
MODEL = "qwen35_2b"
T = f"{D}/2b-limit2048/raw"
SUMMARY = f"{D}/2b-limit2048/SUMMARY.md"
HOURS = f"{D}/shared/hours_budget.json"
os.makedirs(T, exist_ok=True)
os.makedirs(os.path.dirname(HOURS), exist_ok=True)
os.makedirs(os.path.dirname(SUMMARY), exist_ok=True)

if not os.path.exists(HOURS):
    json.dump(dict(cap_hours=58.544, used_hours=0.0, runs={},
                   note="shared pot; keep ≥50h buffer"),
              open(HOURS, "w"), indent=2)

# LEAN: one try; generation capped at budget+1024 (no 8k LCB ceiling).
THINK_BUDGET = 2048
TRIES = 1
MAX_NEW = THINK_BUDGET + 1024   # 3072 — thinking + short answer room
SRC = {"he": "humaneval", "lcb": "lcb"}
N = {"he": 164, "lcb": 70}
WAYS = {"limit2048": ("limit", None)}
# Low hour estimates so the gate does not block a small fill-in.
COST_H = {"smoke": 0.2, "A": 3.5}

import hours_budget as hb
print(f"LEAN model={MODEL} · limit={THINK_BUDGET} · tries={TRIES} · max_new={MAX_NEW}")
print(f"out={T}")
print(f"shared hours left: {hb.left(HOURS):.1f} / {json.load(open(HOURS)).get('cap_hours', '?')}")
"""))

    cells.append(md("""## 3. Fast path (REQUIRED)

Must print **FAST PATH ON ✓**. Without it (~40 tok/s) this run wastes hours — stop."""))
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
        print("building causal-conv1d once (~5–15 min) → Drive wheels")
        sh(f"pip wheel -q causal-conv1d --no-build-isolation --no-deps -w {WHEELS}")
        whl = _glob.glob(f"{WHEELS}/causal_conv1d*.whl")
    if not whl:
        raise RuntimeError("no causal_conv1d*.whl")
    sh(f"pip install -q --no-deps {whl[0]}")
    sh("pip install -q --no-deps flash-linear-attention || pip install -q flash-linear-attention")
    if not fast_path_ok():
        sh("pip install -q flash-linear-attention")
    if not fast_path_ok() and whl:
        for w in whl:
            try: os.remove(w)
            except OSError: pass

import torch
print("torch", torch.__version__, "cuda", torch.version.cuda)
if not fast_path_ok():
    raise RuntimeError("FAST PATH OFF — Restart session, re-run from cell 1.")
print("FAST PATH ON ✓")
"""))

    cells.append(md("""## 4. Problems (needed once)"""))
    cells.append(code("""for c in ["python scripts/test_prompts.py",
           "python scripts/build_problem_set.py",
           "python scripts/mbpp_data.py",
           "python scripts/overlap_check.py"]:
    print(">", c); sh(c)
sh(f"cp -f data/overlap_exclude.json {T}/overlap-exclude.json")
print("problems ready")
"""))

    cells.append(md("""## 5. Helpers (resume-safe, tight max tokens)"""))
    cells.append(code("""BG = []

def ans_path(way, ds, folder=None, prefix="test"):
    return f"{folder or T}/{prefix}-{way}-{ds}.jsonl"

def answer(way, ds, tries, folder=None, n=0, maxtok=None, think_budget=None,
           prefix="test", stop_on_repeat=True, problems="data/problems.json"):
    out = ans_path(way, ds, folder, prefix)
    want = (n or N[ds]) * tries
    if rows(out) >= want:
        print(f"  {way:<12}{ds:<4} complete ({rows(out)}) - skipped"); return out
    policy, _adapter = WAYS[way]
    tb = think_budget if think_budget is not None else THINK_BUDGET
    # LEAN: never open an 8k ceiling — only budget + answer room.
    use_max = maxtok if maxtok is not None else (tb + 1024)
    cmd = (f'python scripts/gen_colab.py --policy {policy} --label {way} --model {MODEL} '
           f'--problems {problems} --source {SRC[ds]} --samples {tries} '
           f'--dtype auto --batch {BATCH} --max-tokens {use_max} '
           f'--think-budget {tb} --out "{out}"')
    if stop_on_repeat:
        cmd += " --stop-on-repeat"
    if n:
        cmd += f" --n {n}"
    print(f"  {way:<12}{ds:<4} answering (max_new={use_max}) ...", flush=True)
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

print("helpers · limit2048 · tries", TRIES, "· max_new", MAX_NEW, "· batch", BATCH)
"""))

    cells.append(md("""## 6. Tiny smoke (2 problems)"""))
    cells.append(code("""assert PRODUCTION_OK, "Need A100/H100 >35GB"
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
            ans = answer("limit2048", ds, 1, folder=SM, n=2, maxtok=256, think_budget=128)
            grade(ans, ds, wait=True)
            r = [json.loads(l) for l in open(ans_path("limit2048", ds, SM))]
            assert any(x["thinking_tokens"] > 0 for x in r), "0 thinking"
            assert graded_ok(ans_path("limit2048", ds, SM))
        open(f"{SM}/PASSED", "w").write("ok")
        print("SMOKE PASSED ✓")
    finally:
        hb.end_stage(HOURS, RUN_TAG, "smoke")
"""))

    cells.append(md("""## 7. Stage A — limit2048 on 234 · **1 try**

Resume-safe. If tokens/s stays under ~100, stop (fast path failed)."""))
    cells.append(code("""assert PRODUCTION_OK
if all(rows(ans_path("limit2048", ds)) >= N[ds] * TRIES and graded_ok(ans_path("limit2048", ds))
       for ds in SRC):
    print("stage A: already complete")
else:
    if not hb.gate(HOURS, RUN_TAG, "A", COST_H["A"]):
        raise RuntimeError("hours gate blocked Stage A — check buffer")
    hb.start_stage(HOURS, RUN_TAG, "A")
    try:
        for ds in SRC:
            grade(answer("limit2048", ds, TRIES), ds)
        wait_grading()
    finally:
        hb.end_stage(HOURS, RUN_TAG, "A")
print("stage A done. Hours left:", round(hb.left(HOURS), 1))
"""))

    cells.append(md("""## 8. SUMMARY on Drive"""))
    cells.append(code("""wait_grading()
for ds in SRC:
    a = ans_path("limit2048", ds)
    if rows(a) and not graded_ok(a):
        grade(a, ds, wait=True)

sh(f'python scripts/make_size_summary.py --dir "{T}" --run 2b-limit2048 --summary "{SUMMARY}"')
print(open(SUMMARY).read())
print("=== hours ===")
print(open(HOURS).read())
print("DONE ✓  Drive: results/2b-limit2048/")
print("Compare to 2B limit1024 = 49.8% (2 tries) — caption this run as 1 try.")
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
    with open(OUT, "w") as f:
        json.dump(nb, f, indent=1)
        f.write("\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
