#!/usr/bin/env python3
"""Build notebook 18: grade 40 extra problems on the three saved models.

Does not train. Does not write into the old result folders.

Run: python scripts/build_extra_notebook.py
"""

import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "notebooks", "18_extra_problems.ipynb")


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": [l + "\n" for l in text.split("\n")]}


def code(text):
    lines = text.split("\n")
    return {"cell_type": "code", "metadata": {}, "outputs": [], "execution_count": None,
            "source": [l + "\n" for l in lines]}


def build():
    cells = []
    cells.append(md("""# 18 — Extra problems only (do not use notebooks 14–17)

**Runtime → Run all** on an **A100**. No typing needed.

This notebook grades **40 new** LiveCodeBench problems.
It does **not** train. It does **not** redo the old 234.

```text
old notebooks 14–17  →  leave them closed
this notebook        →  writes only to  results/extra/
```

| | |
|---|---|
| Problems | the 40 ids in `results/extra/ids.json` |
| Models | 0.8B, then 2B, then 4B |
| Settings | the same ways each model already has |
| Drive out | `MyDrive/stop-overthinking/results/extra/` |
| Hour cap | **4.5 real hours**, and it always leaves **0.5 hour** spare |
| Stop point | before **every** way, not only before each model |

**Before Run all:** push this project to GitHub, then upload this notebook to Colab.
Colab clones the repo by itself. You do not copy a code folder to Drive.

Answers still go to Drive, so a stopped run can continue.
Add-on weights come from the repo. If one weight file is missing, that one way is skipped.

DECISIONS #86."""))

    cells.append(md("""## 1. Install packages"""))
    cells.append(code("""%%capture
!pip install -q --upgrade unsloth
!pip install -q evalplus datasets flash-linear-attention
print("pip done")
"""))

    cells.append(md("""## 2. GPU, Drive, GitHub

Clones the project from GitHub. Answers go only under Drive `results/extra/`."""))
    cells.append(code("""import os, sys, json, subprocess, time, glob
from IPython import get_ipython

name, mem = subprocess.run(
    ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"],
    capture_output=True, text=True).stdout.strip().split(", ")
GPU, GPU_GB = name, float(mem) / 1024
PRODUCTION_OK = ("A100" in GPU or "H100" in GPU) and GPU_GB > 35
print(f"GPU: {GPU} ({GPU_GB:.0f} GB) · " + ("OK" if PRODUCTION_OK else "NOT an A100 — stop"))

def sh(cmd):
    # A previous run may have deleted the folder we were standing in.
    if not os.path.isdir(os.getcwd()):
        os.chdir("/content")
    get_ipython().system(cmd)
    if get_ipython().user_ns.get("_exit_code", 0) != 0:
        raise RuntimeError(f"FAILED: {cmd[:180]}")

from google.colab import drive
drive.mount("/content/drive")

D = "/content/drive/MyDrive/stop-overthinking/results"
WHEELS = "/content/drive/MyDrive/stop-overthinking/wheels"
os.makedirs(D, exist_ok=True)
os.makedirs(WHEELS, exist_ok=True)

REPO = "https://github.com/mahmudulhaquequdrati/stop-overthinking-thesis.git"
os.chdir("/content")
sh("rm -rf /content/thesis")
sh(f"git clone --depth 1 --branch master {REPO} /content/thesis")
os.chdir("/content/thesis")
sys.path.insert(0, "/content/thesis/scripts")
print("code from GitHub:", REPO)

need = ["scripts/build_extra_problems.py", "scripts/compare_extra.py",
        "scripts/gen_colab.py", "results/extra/ids.json", "results/extra/extra-lcb.json"]
missing = [p for p in need if not os.path.exists(p)]
if missing:
    raise RuntimeError(
        "STOP: GitHub is missing " + ", ".join(missing)
        + ". Push this project to master, then Runtime -> Run all again.")

EXTRA_ROOT = f"{D}/extra"
os.makedirs(EXTRA_ROOT, exist_ok=True)
HOURS = f"{EXTRA_ROOT}/hours.json"
CAP_H = 4.5          # real A100 hours. 4.5 x 6.77 units ≈ 30 units, inside a 50-unit pot
FLOOR_H = 0.5        # never plan a step that would eat this spare time

def save_hours(data):
    tmp = HOURS + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2)
        f.flush(); os.fsync(f.fileno())
    os.replace(tmp, HOURS)

if not os.path.exists(HOURS):
    used = 0.0
    stamps = []
    for root, dirs, files in os.walk(EXTRA_ROOT):
        for name in files:
            if name.endswith(".jsonl") or name.endswith("-graded.csv"):
                stamps.append(os.path.getmtime(os.path.join(root, name)))
    if len(stamps) >= 2:
        used = round(max(0.0, (max(stamps) - min(stamps)) / 3600), 3)
        print(f"hours file was missing — guessed {used:.2f}h from files already saved")
    save_hours(dict(cap_hours=CAP_H, floor_hours=FLOOR_H, used_hours=used, runs={},
                    note="notebook 18 only. Does not touch the old shared ledger."))
else:
    data = json.load(open(HOURS))
    data["cap_hours"] = CAP_H
    data["floor_hours"] = FLOOR_H
    save_hours(data)
print("hour file", HOURS, "cap", CAP_H, "spare", FLOOR_H)
"""))

    cells.append(md("""## 3. Fast path

Must print **FAST PATH ON**. If it stays off, stop. A slow run wastes the hours."""))
    cells.append(code("""def fast_path_ok():
    return subprocess.run(
        [sys.executable, "-c", "import causal_conv1d, fla"],
        capture_output=True).returncode == 0

for attempt in (1, 2):
    if fast_path_ok():
        break
    whl = glob.glob(f"{WHEELS}/causal_conv1d*.whl")
    if not whl:
        print("building causal-conv1d once, then saving the wheel")
        sh(f"pip wheel -q causal-conv1d --no-build-isolation --no-deps -w {WHEELS}")
        whl = glob.glob(f"{WHEELS}/causal_conv1d*.whl")
    if not whl:
        raise RuntimeError("no causal_conv1d wheel")
    sh(f"pip install -q --no-deps {whl[0]}")
    sh("pip install -q --no-deps flash-linear-attention || pip install -q flash-linear-attention")

if not fast_path_ok():
    raise RuntimeError("FAST PATH OFF — Restart session, re-run from the top.")
print("FAST PATH ON")
"""))

    cells.append(md("""## 4. Build the 40 problems and show the lists

The id list in git must match the rebuild. If it does not, the script stops.
Old exam ids and old training ids are refused."""))
    cells.append(code("""import shutil
os.makedirs("data", exist_ok=True)
saved = "results/extra/extra-lcb.json"
if os.path.exists(saved):
    shutil.copy(saved, "data/extra-lcb.json")
    print("using the saved 40 problems — no new download")
else:
    sh("python scripts/build_extra_problems.py")
OLD = json.load(open("results/extra/old-test-ids.json"))
TRAIN = json.load(open("results/extra/old-train-ids.json"))
IDS = json.load(open("results/extra/ids.json"))
assert len(OLD) == 234, len(OLD)
assert len(TRAIN) == 80, len(TRAIN)
assert len(IDS) == 40, len(IDS)
assert not (set(IDS) & set(OLD))
assert not (set(IDS) & set(TRAIN))
probs = json.load(open("data/extra-lcb.json"))["problems"]
assert {p["task_id"] for p in probs} == set(IDS)
print(f"lists OK · old exam {len(OLD)} · old train {len(TRAIN)} · extra {len(IDS)} · total {len(OLD)+len(IDS)}")
print("extra ids:", ", ".join(IDS))
"""))

    cells.append(md("""## 5. Helpers

Every answer file is under `results/extra/<model>/`.
A path outside that folder is refused.
A finished file is skipped, so a dead session can continue."""))
    cells.append(code("""BG = []

def rows(path):
    return sum(1 for l in open(path) if l.strip()) if os.path.exists(path) else 0

def hours_used():
    return float(json.load(open(HOURS)).get("used_hours", 0.0))

def charge(tag, t0):
    data = json.load(open(HOURS))
    spent = (time.time() - t0) / 3600
    data["used_hours"] = round(float(data.get("used_hours", 0.0)) + spent, 3)
    data.setdefault("runs", {})
    data["runs"][tag] = round(float(data["runs"].get(tag, 0.0)) + spent, 3)
    data["cap_hours"] = CAP_H
    save_hours(data)
    print(f"hours used {data['used_hours']:.2f} / {CAP_H} · spare kept {FLOOR_H}")
    return spent

def allow(cost):
    left = CAP_H - hours_used()
    ok = (left - cost) >= FLOOR_H
    print(f"hours left {left:.2f} · this way wants {cost:.2f} · spare {FLOOR_H} · " + ("GO" if ok else "STOP"))
    return ok

def guess_hours(profile, tries, last_hours, last_tries, last_profile):
    # Later ways use the last real time. A bigger model gets a bigger guess.
    scale = {"qwen35_0_8b": 1.0, "qwen35_2b": 2.0, "qwen35_4b": 4.0}
    if last_hours and last_tries and last_profile:
        jump = scale[profile] / scale[last_profile]
        return max(0.08, last_hours * jump * (tries / last_tries) * 1.25)
    first = {"qwen35_0_8b": 0.25, "qwen35_2b": 0.40, "qwen35_4b": 0.60}
    return first[profile]

def out_path(folder, way):
    path = os.path.abspath(f"{folder}/test-{way}-lcb.jsonl")
    root = os.path.abspath(EXTRA_ROOT)
    if os.path.commonpath([path, root]) != root:
        raise RuntimeError("refusing to write outside results/extra: " + path)
    return path

def graded_ok(ans):
    g = ans.replace(".jsonl", "-graded.csv")
    return (os.path.exists(g) and rows(g) - 1 == rows(ans)
            and os.path.getmtime(g) >= os.path.getmtime(ans))

def grade(ans):
    for a, p in BG:
        if a == ans:
            p.wait()
    if graded_ok(ans):
        return
    p = subprocess.Popen(
        [sys.executable, "scripts/grade_lcb.py", "--answers", ans, "--problems", "data/extra-lcb.json"],
        stdout=open(ans + ".grade.log", "w"), stderr=subprocess.STDOUT)
    BG.append((ans, p))

def wait_grading():
    for ans, p in BG:
        p.wait()
        print("  graded", os.path.basename(ans), "code", p.returncode)
        if p.returncode != 0:
            raise RuntimeError("grading failed: " + ans)
    BG.clear()

def batch_for(profile):
    if GPU_GB >= 70:
        return 64 if profile == "qwen35_4b" else 128
    if GPU_GB > 35:
        return 32 if profile == "qwen35_4b" else 64
    return 16

def answer(folder, profile, way, policy, adapter, tries, max_tokens, think_budget, stop_on_repeat):
    out = out_path(folder, way)
    if rows(out) >= 40 * tries:
        print(f"  {way:<12} complete ({rows(out)}) - skipped")
        return out
    cmd = (f'python scripts/gen_colab.py --policy {policy} --label {way} --model {profile} '
           f'--problems data/extra-lcb.json --source lcb --samples {tries} '
           f'--dtype auto --batch {batch_for(profile)} --max-tokens {max_tokens} '
           f'--think-budget {think_budget or 1024} --only-ids results/extra/ids.json '
           f'--out "{out}"')
    if stop_on_repeat:
        cmd += " --stop-on-repeat"
    if adapter:
        if not os.path.exists(os.path.join(adapter, "adapter_model.safetensors")):
            print(f"  {way:<12} SKIP — no weights at {adapter}")
            return None
        cmd += f' --adapter "{adapter}"'
    print(f"  {way:<12} answering ...", flush=True)
    sh(cmd)
    return out

def find_lora(repo_rel, drive_rel):
    # Repo first (after you push). Drive second, in case an old run saved the weights there.
    options = [f"/content/thesis/{repo_rel}", f"{D}/{drive_rel}"]
    for path in options:
        if os.path.exists(os.path.join(path, "adapter_model.safetensors")):
            print("LoRA found:", path)
            return path
    print("LoRA missing, that way will be skipped:", repo_rel)
    return options[0]

# Same settings as the finished runs. 2B limit 2048 stays 1 try.
# Important ways come first, so a stop still has the story.
# 2B main ways do not use stop-on-repeat. That matches notebook 14.
LORA_08 = find_lora("results/0.8b/raw/lora/lora1", "0.8b/raw/lora/lora1")
LORA_4B = find_lora("results/4b/raw/lora/lora1", "4b/raw/lora/lora1")
LORA_2B_1 = find_lora("results/mini/lora/lora100", "mini/lora/lora100")
LORA_2B_2 = find_lora("results/2026-09-24-thesis-run/lora/lora2", "2026-09-24-thesis-run/lora/lora2")
RUNS = [
    ("0.8b", "qwen35_0_8b", [
        ("off", "thinking_off", None, 1, 8192, None, True),
        ("limit512", "limit", None, 1, 8192, 512, True),
        ("on", "thinking_on", None, 1, 8192, None, True),
        ("lora1", "thinking_on", LORA_08, 1, 8192, None, True),
        ("limit1024", "limit", None, 1, 8192, 1024, True),
    ]),
    ("2b", "qwen35_2b", [
        ("limit1024", "limit", None, 2, 8192, 1024, False),
        ("off", "thinking_off", None, 2, 8192, None, False),
        ("on", "thinking_on", None, 2, 8192, None, False),
        ("lora2", "thinking_on", LORA_2B_2, 2, 8192, None, False),
        ("lora1", "thinking_on", LORA_2B_1, 2, 8192, None, False),
        ("limit512", "limit", None, 2, 8192, 512, True),
        ("limit2048", "limit", None, 1, 3072, 2048, True),
        ("brief", "brief", None, 2, 8192, None, False),
    ]),
    ("4b", "qwen35_4b", [
        ("limit2048", "limit", None, 2, 8192, 2048, True),
        ("off", "thinking_off", None, 2, 8192, None, True),
        ("on", "thinking_on", None, 2, 8192, None, True),
        ("lora1", "thinking_on", LORA_4B, 2, 8192, None, True),
        ("limit1024", "limit", None, 2, 8192, 1024, True),
        ("limit512", "limit", None, 2, 8192, 512, True),
        ("limit4096", "limit", None, 2, 8192, 4096, True),
    ]),
]
print("helpers ready · writes only under", EXTRA_ROOT)
"""))

    cells.append(md("""## 6. Grade, then update the score file

One way at a time. After each way the answers are graded and `SUMMARY.md` is rewritten.
The next way starts only if it still leaves 0.5 hour spare under the 4.5 hour cap.
A skipped add-on means the weight file was not on Drive. The free ways still run.
If the clock says stop, finished ways stay saved. Run all again later continues them."""))
    cells.append(code("""def refresh_summary():
    cmd = (f'python scripts/compare_extra.py --extra-dir "{EXTRA_ROOT}" '
           f'--write "{EXTRA_ROOT}/SUMMARY.md"')
    get_ipython().system(cmd)
    if get_ipython().user_ns.get("_exit_code", 0) != 0:
        print("summary update failed — answers are still saved")
    else:
        print("SUMMARY.md updated")

assert PRODUCTION_OK, "Need an A100 or H100"
stopped = False
last_hours, last_tries, last_profile = None, None, None
for tag, profile, ways in RUNS:
    if stopped:
        break
    folder = f"{EXTRA_ROOT}/{tag}"
    os.makedirs(folder, exist_ok=True)
    print()
    print("====", tag, "====")
    for way, policy, adapter, tries, max_tokens, budget, stop in ways:
        out = out_path(folder, way)
        if rows(out) >= 40 * tries and graded_ok(out):
            print(f"  {way:<12} already graded — skipped")
            continue
        need = guess_hours(profile, tries, last_hours, last_tries, last_profile)
        if not allow(need):
            print("STOP before", tag, way, "— spare time would be eaten. Finished ways stay saved.")
            stopped = True
            break
        t0 = time.time()
        ans = answer(folder, profile, way, policy, adapter, tries, max_tokens, budget, stop)
        if ans:
            grade(ans)
            wait_grading()
            spent = charge(tag + "/" + way, t0)
            if rows(ans) > 0:
                last_hours, last_tries, last_profile = spent, tries, profile
        refresh_summary()
        if hours_used() + FLOOR_H >= CAP_H:
            print("STOP — cap reached. Finished ways stay saved.")
            stopped = True
            break

refresh_summary()
print()
print("DONE")
print("Scores:", EXTRA_ROOT + "/SUMMARY.md")
print("Download results/extra/ back into the project. Then we update the thesis docs.")
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
