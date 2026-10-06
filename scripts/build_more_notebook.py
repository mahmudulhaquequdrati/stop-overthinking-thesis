#!/usr/bin/env python3
"""Build notebook 19: one file, three models, a problem list that can grow.

Does not train. Does not write into the old result folders.

1. What problem does this solve?  Three models need the same new problems, and
   we may add problems later.
2. Why do we need it?  A separate notebook per model would drift. A frozen list
   cannot grow.
3. What goes in?   The config cell (models, how many problems, hour cap).
4. What comes out? notebooks/19_more_problems.ipynb
5. Why this way?   Same cells as notebook 18. One config cell. Finished ways are skipped.

Run: python scripts/build_more_notebook.py
"""

import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "notebooks", "19_more_problems.ipynb")


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": [l + "\n" for l in text.split("\n")]}


def code(text):
    lines = text.split("\n")
    return {"cell_type": "code", "metadata": {}, "outputs": [], "execution_count": None,
            "source": [l + "\n" for l in lines]}


def build():
    cells = []
    cells.append(md("""# 19 — More problems (one notebook, all three models)

**Runtime → Run all** on an **A100**. Change numbers only in the config cell.

This notebook grades a **growing** LiveCodeBench list on 0.8B, then 2B, then 4B.
It does **not** train. It does **not** redo the old 234 or the extra 40.
LoRA-2 is not in this run. The old LoRA-2 score stays on the 234.

```text
notebooks 14–18   →  leave them closed
this notebook     →  writes only to  results/more/
```

| | |
|---|---|
| Problems | `results/more/ids.json` (append only) |
| Models | the names in the config cell |
| Tries | **1** |
| Hour cap | the compute-hour cap in the config cell |
| Drive out | `MyDrive/stop-overthinking/results/more/` |

**Before Run all:** push this project to GitHub, then upload this notebook to Colab.
This run can use a **new Google account**. That Drive starts empty. That is fine.
Old scores stay on the old account. This notebook does not read them.
To add problems later, raise `N_NEW` and Run all again. Graded problems are skipped.
Lowering `N_NEW` does not delete ids."""))

    cells.append(md("""## 0. Config

This is the only cell you edit.
`N_NEW` is the target size of the new list, not a number to add on top of the old exam.
It is 190 because that is every clean problem left. Raise it later only if you have new problems to append.
`COMPUTE_CAP` is compute hours for this pass, not real hours. About 6.77 compute hours is one real A100 hour."""))
    cells.append(code("""# The only cell you change.
MODELS = ["0.8b", "2b", "4b"]   # remove a name to skip that model
N_NEW = 190                     # every clean problem that is left. Raise it later to append. Lowering does not delete.
COMPUTE_CAP = 100               # stop this pass at 100 compute hours, so a retry still has hours left
COMPUTE_PER_REAL_HOUR = 6.77
print("models", MODELS)
print("new-list target", N_NEW)
print(f"cap {COMPUTE_CAP} compute hours ≈ {COMPUTE_CAP / COMPUTE_PER_REAL_HOUR:.1f} real A100 hours")
"""))

    cells.append(md("""## 1. Install packages"""))
    cells.append(code("""%%capture
!pip install -q --upgrade unsloth
!pip install -q evalplus datasets flash-linear-attention
print("pip done")
"""))

    cells.append(md("""## 2. GPU, Drive, GitHub

Clones the project from GitHub. The problems and the 0.8B and 4B add-ons come from that clone.
A new Google account has an empty Drive. The notebook creates `results/more/` there and saves scores.
It does not need any file from the old account, except the 2B add-on if you want that one way.
If Drive fails, answers stay in `/content/more-out/` and the run continues."""))
    cells.append(code("""import os, sys, json, subprocess, time, glob
from IPython import get_ipython

os.chdir("/content")
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

def try_mount():
    from google.colab import drive
    try:
        drive.mount("/content/drive")
    except Exception as e:
        print("Drive mount failed:", type(e).__name__, e)
        try:
            drive.mount("/content/drive", force_remount=True)
        except Exception as e2:
            print("Drive mount failed again:", type(e2).__name__, e2)
            return False
    return os.path.isdir("/content/drive/MyDrive")

DRIVE_OK = try_mount()
if DRIVE_OK:
    D = "/content/drive/MyDrive/stop-overthinking/results"
    WHEELS = "/content/drive/MyDrive/stop-overthinking/wheels"
    MORE_ROOT = f"{D}/more"
    print("saving scores on Drive:", MORE_ROOT)
    print("A new account's Drive can be empty. Old result folders are not required.")
else:
    D = "/content/more-out"
    WHEELS = "/content/wheels"
    MORE_ROOT = "/content/more-out"
    print("Drive did not mount. Scores stay in /content/more-out.")
    print("A zip is written at the end. Download it before the session ends.")
os.makedirs(D, exist_ok=True)
os.makedirs(WHEELS, exist_ok=True)
os.makedirs(MORE_ROOT, exist_ok=True)

REPO = "https://github.com/mahmudulhaquequdrati/stop-overthinking-thesis.git"
os.chdir("/content")
sh("rm -rf /content/thesis")
sh(f"git clone --depth 1 --branch master {REPO} /content/thesis")
os.chdir("/content/thesis")
sys.path.insert(0, "/content/thesis/scripts")
print("code from GitHub:", REPO)

need = ["scripts/build_more_problems.py", "scripts/compare_more.py",
        "scripts/gen_colab.py", "scripts/grade_lcb.py"]
missing = [p for p in need if not os.path.exists(p)]
if missing:
    raise RuntimeError(
        "STOP: GitHub is missing " + ", ".join(missing)
        + ". Push this project to master, then Runtime -> Run all again.")

HOURS = f"{MORE_ROOT}/hours.json"
CAP_H = COMPUTE_CAP / COMPUTE_PER_REAL_HOUR   # real A100 hours
FLOOR_H = 0.5                                 # do not start a way that would cross the cap

def save_hours(data):
    tmp = HOURS + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2)
        f.flush(); os.fsync(f.fileno())
    os.replace(tmp, HOURS)

if not os.path.exists(HOURS):
    used = 0.0
    stamps = []
    for root, dirs, files in os.walk(MORE_ROOT):
        for fname in files:
            if fname.endswith(".jsonl") or fname.endswith("-graded.csv"):
                stamps.append(os.path.getmtime(os.path.join(root, fname)))
    if len(stamps) >= 2:
        used = round(max(0.0, (max(stamps) - min(stamps)) / 3600), 3)
        print(f"hours file was missing — guessed {used:.2f}h from files already saved")
    save_hours(dict(cap_hours=CAP_H, compute_cap=COMPUTE_CAP, floor_hours=FLOOR_H,
                    used_hours=used, runs={},
                    note="notebook 19 only. Does not touch the old exam or the extra 40."))
else:
    data = json.load(open(HOURS))
    data["cap_hours"] = CAP_H
    data["compute_cap"] = COMPUTE_CAP
    data["floor_hours"] = FLOOR_H
    save_hours(data)
print(f"hour file {HOURS} · cap {CAP_H:.2f} real hours · {COMPUTE_CAP} compute hours · spare {FLOOR_H}")
"""))

    cells.append(md("""## 3. Fast path

Qwen is very slow without two small libraries. This cell installs them.
It downloads the ready-made file that matches **this** Colab's PyTorch.
An old file on Drive is used only when its name matches. A mismatch is deleted.
Must print **FAST PATH ON**. If it stops, copy the error and paste it here."""))
    cells.append(code(FAST_PATH))

    cells.append(md("""## 4. Build or grow the problem list

Notebook 18 failed here once: the cell before it left Python in `/content`, so `scripts/` was not found.
This cell goes back to `/content/thesis` first.

If the saved list is already in the GitHub clone, this cell does **not** download LiveCodeBench.
A download in the middle of a GPU run is how a session dies. Push `results/more/more-lcb.json` before Run all.
If you raised `N_NEW` above the saved list, it appends. It never deletes an id.
The 234, the extra 40, and the 80 training ids are refused.
`LISTS.md` shows the total count. That total is not a new blended score."""))
    cells.append(code("""import shutil
# Same fix as notebook 18 (DECISIONS #88). The fast-path cell stands in /content.
os.chdir("/content/thesis")
if not os.path.isdir("scripts"):
    raise RuntimeError("STOP: scripts/ is not here. Folder is " + os.getcwd()
                       + ". Runtime -> Run all again from the top.")
print("code folder:", os.getcwd())
os.makedirs("data", exist_ok=True)
ids_path = "results/more/ids.json"
probs_path = "results/more/more-lcb.json"
if not (os.path.exists(ids_path) and os.path.exists(probs_path)):
    raise RuntimeError(
        "STOP: results/more/more-lcb.json is not in this GitHub clone. "
        "Push the project to master, then Runtime -> Run all again. "
        "Do not download LiveCodeBench inside this GPU run.")
have = json.load(open(ids_path))
if len(have) >= int(N_NEW):
    print(f"using the saved list — {len(have)} problems, no new download")
else:
    print(f"saved list has {len(have)}. Target is {int(N_NEW)}. Appending.")
    sh(sys.executable + f" scripts/build_more_problems.py --n {int(N_NEW)}")
shutil.copy(probs_path, "data/more-lcb.json")
OLD = json.load(open("results/extra/old-test-ids.json"))
TRAIN = json.load(open("results/extra/old-train-ids.json"))
EXTRA = json.load(open("results/extra/ids.json"))
IDS = json.load(open(ids_path))
assert len(OLD) == 234, len(OLD)
assert len(TRAIN) == 80, len(TRAIN)
assert len(EXTRA) == 40, len(EXTRA)
assert not (set(IDS) & set(OLD))
assert not (set(IDS) & set(TRAIN))
assert not (set(IDS) & set(EXTRA))
probs = json.load(open("data/more-lcb.json"))["problems"]
assert [p["task_id"] for p in probs] == IDS
n_easy = sum(p["difficulty"] == "easy" for p in probs)
n_med = sum(p["difficulty"] == "medium" for p in probs)
total = len(OLD) + len(EXTRA) + len(IDS)
print(f"lists OK · old exam {len(OLD)} · extra {len(EXTRA)} · new {len(IDS)} ({n_easy} easy, {n_med} medium)")
print(f"total problems you can show: {total}")
print("totals file: results/more/LISTS.md")
"""))

    cells.append(md("""## 5. Helpers

Every answer file is under `results/more/<model>/`.
A path outside that folder is refused.
A finished file is skipped, so a dead session can continue.
One try. LoRA-1 only. No LoRA-2."""))
    cells.append(code(HELPERS))

    cells.append(md("""## 6. Grade, then update the score file

One way at a time. After each way the answers are graded and `SUMMARY.md` is rewritten.
The score table has the full new list, then an easy row and a medium row.
It does not mix those scores into 49.8% or 78.2%.
The next way starts only if it still leaves spare time under the compute-hour cap.
A skipped add-on means the weight file was not found. The free ways still run.
If the clock says stop, finished ways stay saved. Run all again later continues them."""))
    cells.append(code(GRADE))

    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "cells": cells,
    }


FAST_PATH = r'''def fast_path_error():
    p = subprocess.run(
        [sys.executable, "-c", "import causal_conv1d, fla"],
        capture_output=True, text=True)
    if p.returncode == 0:
        return ""
    return ((p.stderr or "") + (p.stdout or "")).strip()[-800:]

def fast_path_ok():
    return fast_path_error() == ""

def pip_sh(args):
    # Same Python as the import check. A bare "pip" can install into another Python.
    sh(sys.executable + " -m pip " + args)

def colab_torch():
    # Read versions in a new process, so this notebook does not load torch yet.
    probe = """
import json, sys, torch
ver = torch.__version__.split("+")[0]
parts = ver.split(".")
tags = []
if len(parts) >= 2:
    tags.append(parts[0] + "." + parts[1])
    if parts[0].isdigit() and int(parts[0]) >= 20 and parts[1].isdigit():
        tags.append("%s.%02d" % (parts[0], int(parts[1])))
        tags.append("%s.%d" % (parts[0], int(parts[1])))
seen = []
for t in tags:
    if t and t not in seen:
        seen.append(t)
cuda = (torch.version.cuda or "").split(".")[0]
abi = "TRUE" if torch.compiled_with_cxx11_abi() else "FALSE"
py = "cp%d%d" % (sys.version_info.major, sys.version_info.minor)
print(json.dumps({"ver": ver, "tags": seen, "cuda": cuda, "abi": abi, "py": py}))
"""
    p = subprocess.run([sys.executable, "-c", probe], capture_output=True, text=True)
    if p.returncode != 0:
        print((p.stderr or "")[-800:])
        raise RuntimeError("could not read the PyTorch version. Scroll up.")
    return json.loads(p.stdout.strip().splitlines()[-1])

def wheel_needles(info, abi):
    py = info["py"]
    cu = info["cuda"]
    return [
        f"+cu{cu}torch{tag}cxx11abi{abi}-{py}-{py}-linux_x86_64.whl"
        for tag in info["tags"]
    ]

def find_saved(info):
    paths = glob.glob(f"{WHEELS}/causal_conv1d*.whl")
    order = [info["abi"], "FALSE" if info["abi"] == "TRUE" else "TRUE"]
    for abi in order:
        for needle in wheel_needles(info, abi):
            for path in paths:
                if needle in os.path.basename(path):
                    return path
    return ""

def find_release_url(info):
    import urllib.request
    url = "https://api.github.com/repos/Dao-AILab/causal-conv1d/releases/latest"
    req = urllib.request.Request(url, headers={"User-Agent": "stop-overthinking"})
    with urllib.request.urlopen(req, timeout=60) as r:
        rel = json.load(r)
    order = [info["abi"], "FALSE" if info["abi"] == "TRUE" else "TRUE"]
    for abi in order:
        for needle in wheel_needles(info, abi):
            for asset in rel.get("assets", []):
                if needle in asset.get("name", ""):
                    return asset["browser_download_url"], asset["name"]
    return "", ""

def install_wheel(path):
    pip_sh(f'install -q --no-deps "{path}"')
    pip_sh("install -q flash-linear-attention")

os.chdir("/content")
os.makedirs(WHEELS, exist_ok=True)
print("wheels folder:", WHEELS)
print("fast path at start:", "ON" if fast_path_ok() else "off")

if not fast_path_ok():
    info = colab_torch()
    print("this Colab: torch", info["ver"], "cuda", info["cuda"],
          "python", info["py"], "abi", info["abi"])
    if not info["cuda"]:
        raise RuntimeError("PyTorch has no CUDA. Change the runtime to an A100, then Run all.")
    err = fast_path_error()
    if err:
        print(err)
    # A half-installed copy from "pip install causal-conv1d" blocks the right file.
    subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "causal-conv1d"],
                   capture_output=True, text=True)
    saved = find_saved(info)
    if saved:
        print("using saved wheel", os.path.basename(saved))
        install_wheel(saved)
    if not fast_path_ok():
        for w in glob.glob(f"{WHEELS}/causal_conv1d*.whl"):
            try:
                os.remove(w)
            except OSError:
                pass
        try:
            url, name = find_release_url(info)
        except Exception as e:
            url, name = "", ""
            print("could not list ready wheels:", type(e).__name__, e)
        if url:
            from urllib.request import urlretrieve
            dest = os.path.join(WHEELS, name)
            print("downloading ready wheel (~185 MB):", name)
            try:
                urlretrieve(url, dest)
                install_wheel(dest)
            except Exception as e:
                print("download failed:", type(e).__name__, e)
    if not fast_path_ok():
        for w in glob.glob(f"{WHEELS}/causal_conv1d*.whl"):
            try:
                os.remove(w)
            except OSError:
                pass
        print("no ready wheel loaded. Building. This can take 5-15 min.")
        pip_sh("install -q ninja packaging wheel")
        sh(f"{sys.executable} -m pip wheel causal-conv1d --no-build-isolation --no-deps -w {WHEELS}")
        built = [p for p in glob.glob(f"{WHEELS}/causal_conv1d*.whl")]
        if not built:
            raise RuntimeError("could not build causal-conv1d. Scroll up for the pip error.")
        install_wheel(built[0])

err = fast_path_error()
if err:
    print(err)
    raise RuntimeError(
        "FAST PATH OFF. The speed libraries did not load. "
        "Copy the lines above and paste them here.")
print("FAST PATH ON")
os.chdir("/content/thesis")
print("code folder:", os.getcwd())
'''

HELPERS = r'''# Notebook 18 died when this cell ran from /content. Stay in the project folder.
os.chdir("/content/thesis")
if not os.path.isdir("scripts"):
    raise RuntimeError("STOP: scripts/ is not here. Folder is " + os.getcwd())
print("code folder:", os.getcwd())

BG = []

def rows(path):
    return sum(1 for l in open(path) if l.strip()) if os.path.exists(path) else 0

def n_problems():
    return len(json.load(open("results/more/ids.json")))

def hours_used():
    return float(json.load(open(HOURS)).get("used_hours", 0.0))

def charge(tag, t0):
    data = json.load(open(HOURS))
    spent = (time.time() - t0) / 3600
    data["used_hours"] = round(float(data.get("used_hours", 0.0)) + spent, 3)
    data.setdefault("runs", {})
    data["runs"][tag] = round(float(data["runs"].get(tag, 0.0)) + spent, 3)
    data["cap_hours"] = CAP_H
    data["compute_cap"] = COMPUTE_CAP
    save_hours(data)
    compute = data["used_hours"] * COMPUTE_PER_REAL_HOUR
    print(f"hours used {data['used_hours']:.2f} real / {compute:.1f} compute · cap {COMPUTE_CAP}")
    return spent

def allow(cost):
    left = CAP_H - hours_used()
    ok = (left - cost) >= FLOOR_H
    print(f"real hours left {left:.2f} · this way wants {cost:.2f} · spare {FLOOR_H} · " + ("GO" if ok else "STOP"))
    return ok

def guess_hours(profile, tries, last_hours, last_tries, last_profile):
    # Later ways use the last real time. A bigger model gets a bigger guess.
    # Scale by the problem count, because this list is not the old 40.
    scale = {"qwen35_0_8b": 1.0, "qwen35_2b": 2.0, "qwen35_4b": 4.0}
    size = max(1, n_problems()) / 40.0
    if last_hours and last_tries and last_profile:
        jump = scale[profile] / scale[last_profile]
        return max(0.08, last_hours * jump * (tries / last_tries) * 1.25)
    first = {"qwen35_0_8b": 0.25, "qwen35_2b": 0.40, "qwen35_4b": 0.60}
    return first[profile] * size

def out_path(folder, way):
    path = os.path.abspath(f"{folder}/test-{way}-lcb.jsonl")
    root = os.path.abspath(MORE_ROOT)
    if os.path.commonpath([path, root]) != root:
        raise RuntimeError("refusing to write outside results/more: " + path)
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
        [sys.executable, "scripts/grade_lcb.py", "--answers", ans, "--problems", "data/more-lcb.json"],
        cwd="/content/thesis",
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
    need = n_problems() * tries
    if rows(out) >= need:
        print(f"  {way:<12} complete ({rows(out)}) - skipped")
        return out
    # cd first, and use this cell's Python. Notebook 18's fast path failed when
    # a bare "pip" installed into a different Python. A bare "python" can do the same.
    cmd = (f'cd /content/thesis && {sys.executable} scripts/gen_colab.py --policy {policy} --label {way} '
           f'--model {profile} --problems data/more-lcb.json --source lcb --samples {tries} '
           f'--dtype auto --batch {batch_for(profile)} --max-tokens {max_tokens} '
           f'--think-budget {think_budget or 1024} --only-ids results/more/ids.json '
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
    options = [f"/content/thesis/{repo_rel}", f"{D}/{drive_rel}"]
    for path in options:
        if os.path.exists(os.path.join(path, "adapter_model.safetensors")):
            print("LoRA found:", path)
            return path
    print("LoRA missing, that way will be skipped:", repo_rel)
    print("  A new Google account cannot see the old Drive.")
    print("  0.8B and 4B weights are in the GitHub project. The 2B weights are not.")
    print("  Free ways still run. To include 2B LoRA, copy this folder from the OLD account")
    print("  onto THIS account's Drive, then Run all again:")
    print("  MyDrive/stop-overthinking/results/mini/lora/lora100/")
    return options[0]

# One try. Story ways first, so a stop still has the comparison.
# 2B does not use stop-on-repeat. That matches the locked 2B exam.
LORA_08 = find_lora("results/0.8b/raw/lora/lora1", "0.8b/raw/lora/lora1")
LORA_4B = find_lora("results/4b/raw/lora/lora1", "4b/raw/lora/lora1")
LORA_2B_1 = find_lora("results/mini/lora/lora100", "mini/lora/lora100")
ALL_RUNS = [
    ("0.8b", "qwen35_0_8b", [
        ("off", "thinking_off", None, 1, 8192, None, True),
        ("limit512", "limit", None, 1, 8192, 512, True),
        ("on", "thinking_on", None, 1, 8192, None, True),
        ("lora1", "thinking_on", LORA_08, 1, 8192, None, True),
    ]),
    ("2b", "qwen35_2b", [
        ("limit1024", "limit", None, 1, 8192, 1024, False),
        ("off", "thinking_off", None, 1, 8192, None, False),
        ("on", "thinking_on", None, 1, 8192, None, False),
        ("lora1", "thinking_on", LORA_2B_1, 1, 8192, None, False),
    ]),
    ("4b", "qwen35_4b", [
        ("limit2048", "limit", None, 1, 8192, 2048, True),
        ("off", "thinking_off", None, 1, 8192, None, True),
        ("on", "thinking_on", None, 1, 8192, None, True),
        ("lora1", "thinking_on", LORA_4B, 1, 8192, None, True),
    ]),
]
RUNS = [row for row in ALL_RUNS if row[0] in MODELS]
print("helpers ready · writes only under", MORE_ROOT)
print("models this run:", [row[0] for row in RUNS], "· problems", n_problems())
'''

GRADE = r'''def refresh_summary():
    os.chdir("/content/thesis")
    cmd = (f'cd /content/thesis && {sys.executable} scripts/compare_more.py --more-dir "{MORE_ROOT}" '
           f'--write "{MORE_ROOT}/SUMMARY.md"')
    get_ipython().system(cmd)
    if get_ipython().user_ns.get("_exit_code", 0) != 0:
        print("summary update failed — answers are still saved")
    else:
        print("SUMMARY.md updated")

import shutil
os.chdir("/content/thesis")
if not os.path.isdir("scripts"):
    raise RuntimeError("STOP: scripts/ is not here. Folder is " + os.getcwd())
# Keep the list next to the answers. A dead session can still be read from Drive.
for name in ("ids.json", "LISTS.md", "more-lcb.json"):
    src = os.path.join("results/more", name)
    dest = os.path.join(MORE_ROOT, name)
    if not os.path.exists(src) or os.path.abspath(src) == os.path.abspath(dest):
        continue
    try:
        shutil.copy(src, dest)
    except OSError as e:
        print("could not copy", name, "— grading still uses the project copy:", e)
print("list folder:", MORE_ROOT)

assert PRODUCTION_OK, "Need an A100 or H100"
if not RUNS:
    raise RuntimeError("MODELS is empty. Put at least one of 0.8b, 2b, 4b in the config cell.")
stopped = False
last_hours, last_tries, last_profile = None, None, None
for tag, profile, ways in RUNS:
    if stopped:
        break
    folder = f"{MORE_ROOT}/{tag}"
    os.makedirs(folder, exist_ok=True)
    print()
    print("====", tag, "====")
    for way, policy, adapter, tries, max_tokens, budget, stop in ways:
        out = out_path(folder, way)
        if rows(out) >= n_problems() * tries and graded_ok(out):
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
print("Scores:", MORE_ROOT + "/SUMMARY.md")
print("These scores stay in this folder. They are not mixed into 49.8% or 78.2%.")
if not DRIVE_OK:
    import shutil
    shutil.make_archive("/content/more-out-download", "zip", "/content", "more-out")
    print("Drive was not used. Download /content/more-out-download.zip from the files panel.")
else:
    print("Download Drive results/more/ back into the project when the run finishes.")
'''


def main():
    nb = build()
    with open(OUT, "w") as f:
        json.dump(nb, f, indent=1)
        f.write("\n")
    print("wrote", OUT, "cells", len(nb["cells"]))


if __name__ == "__main__":
    main()
