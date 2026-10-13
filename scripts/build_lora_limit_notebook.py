"""Build Notebook 21 in the same readable GitHub/Drive style as notebooks 18–20.

The notebook needs only Colab, Drive, and the existing LoRA-1 weight file.
Tests are loaded externally, as in the earlier notebooks, and cached on Drive.
"""
import csv
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'notebooks/21_2b_lora1_limit1024.ipynb'
SCRIPT_NAMES=['models.py','prompts.py','build_problem_set.py','gen_colab.py',
    'grade_humaneval.py','grade_plus.py','grade_lcb.py','lcb_data.py',
    'run_lora_limit.py','compare_lora_limit.py','prepare_lora_limit_data.py']


def make_inputs():
    problems=[]
    for relative in ['data/problems.json','results/extra/extra-lcb.json','results/more/more-lcb.json']:
        problems+=json.loads((ROOT/relative).read_text())['problems']
    ids={p['task_id'] for p in problems}
    assert len(problems)==len(ids)==464
    assert sum(p['source']=='humaneval' for p in problems)==164
    assert sum(p['source']=='lcb' for p in problems)==300
    # The local problem file predates the plus-test upgrade. Read the cached
    # official HF dataset, without networking or modifying the original data.
    he_revision = 'already-in-problems-file'
    if not all(p.get('test_plus') for p in problems if p['source']=='humaneval'):
        import pyarrow.ipc as ipc
        cache = Path.home()/'.cache/huggingface/datasets/evalplus___humanevalplus'
        matches = sorted(cache.rglob('humanevalplus-test.arrow'))
        if len(matches) != 1:
            raise RuntimeError('Expected one cached official HumanEval+ dataset; cannot silently use original tests.')
        with matches[0].open('rb') as stream:
            plus = {r['task_id']:r for r in ipc.open_stream(stream).read_all().to_pylist()}
        assert len(plus) == 164
        he_revision = matches[0].parent.name
        for p in problems:
            if p['source']=='humaneval':
                p['test_plus'] = plus[p['task_id']]['test']
                assert p['entry_point'] == plus[p['task_id']]['entry_point']
                p['canonical_solution'] = plus[p['task_id']]['prompt'] + plus[p['task_id']]['canonical_solution']
    assert all(p.get('test_plus') for p in problems if p['source']=='humaneval')
    assert all(0<len(p['tests'])<=20 for p in problems if p['source']=='lcb')
    training=set(json.loads((ROOT/'results/extra/old-train-ids.json').read_text()))
    for name in ['results/2026-09-24-thesis-run/train-set-v2.jsonl','results/2026-09-24-thesis-run/train-mbpp.jsonl']:
        training|={json.loads(line)['task_id'] for line in (ROOT/name).read_text().splitlines() if line.strip()}
    assert not (training&ids)
    # Preserve all grading inputs verbatim; remove only display-only fields.
    keep={'task_id','source','difficulty','question','run_as','entry_point','test','test_plus',
          'tests','func_name','canonical_solution'}
    frozen={'problems':[{k:v for k,v in p.items() if k in keep} for p in problems]}
    combined=json.loads((ROOT/'results/combined/results.json').read_text())
    baselines={'methods':{m:{} for m in ('limit1024','lora1','off','on')},'sources':[]}
    for src in combined['sources']:
        if src['model']!='2b' or src['method'] not in baselines['methods']:continue
        dest=baselines['methods'][src['method']]
        path=ROOT/src['path']
        for r in csv.DictReader(path.open()):
            if int(r['sample_index'])!=0:continue
            assert r['task_id'] not in dest
            dest[r['task_id']]={k:float(r[k]) for k in ('thinking_tokens','total_new_tokens')}
            dest[r['task_id']]['passed']=r['passed']=='True'
        baselines['sources'].append(dict(path=src['path'],sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    assert {k:len(v) for k,v in baselines['methods'].items()}=={'limit1024':464,'lora1':424,'off':464,'on':464}
    files={f'scripts/{name}':(ROOT/'scripts'/name).read_bytes() for name in SCRIPT_NAMES}
    full_body=json.dumps(frozen,sort_keys=True,separators=(',',':')).encode()
    thin={'problems':[{k:v for k,v in p.items() if k not in ('test_plus','tests')} for p in frozen['problems']]}
    files['data/problem-templates.json']=json.dumps(thin,separators=(',',':')).encode()
    data_commit='5ff583e6ed2b950636342d2b3583f7420fb9ed4b'
    contest_files=[]
    for name,relative in [('extra-lcb.json','results/extra/extra-lcb.json'),('more-lcb.json','results/more/more-lcb.json')]:
        contest_files.append(dict(name=name,sha256=hashlib.sha256((ROOT/relative).read_bytes()).hexdigest(),
            url=f'https://raw.githubusercontent.com/mahmudulhaquequdrati/stop-overthinking-thesis/{data_commit}/{relative}'))
    lcb_revision=(Path.home()/'.cache/huggingface/hub/datasets--livecodebench--code_generation_lite/refs/main').read_text().strip()
    files['data/data-manifest.json']=json.dumps(dict(problem_sha256=hashlib.sha256(full_body).hexdigest(),
        humanevalplus_revision=he_revision,livecodebench_revision=lcb_revision,
        original_lcb_ids=[p['task_id'] for p in json.loads((ROOT/'data/problems.json').read_text())['problems'] if p['source']=='lcb'],
        contest_files=contest_files),indent=2).encode()
    files['data/baselines-first-attempt.json']=json.dumps(baselines,separators=(',',':')).encode()
    files['data/adapter_config.json']=(ROOT/'results/mini/lora/lora100/adapter_config.json').read_bytes()
    files['data/manifest.json']=json.dumps({'files':{k:hashlib.sha256(v).hexdigest() for k,v in files.items()},
        'problem_ids':sorted(ids),'training_ids':sorted(training),'created':'2026-10-14',
        'humanevalplus_revision':he_revision},indent=2).encode()
    return files

def build():
    files=make_inputs()
    inputs=ROOT/'results/lora-limit-inputs'
    inputs.mkdir(parents=True,exist_ok=True)
    for name,body in files.items():
        if name.startswith('data/'):
            (inputs/name.removeprefix('data/')).write_bytes(body)
    previous=json.loads((ROOT/'notebooks/21_2b_lora1_limit1024.ipynb').read_text())
    # Keep the tested worker/report/disconnect cells, without any embedded bundle.
    old_code={}
    for i,c in enumerate(previous['cells']):
        if c['cell_type']=='code':
            source=''.join(c['source'])
            if source.startswith('GENERATION_COMPLETE'):old_code['generate']=source
            if source.startswith('GRADING_COMPLETE'):old_code['grade']=source
            if 'ZIP_BASE = ' in source:old_code['finish']=source
    cells=[]
    def md(text):cells.append(dict(cell_type='markdown',metadata={},source=text.strip()+'\n'))
    def code(text):cells.append(dict(cell_type='code',metadata={},source=text.strip()+'\n',outputs=[],execution_count=None))
    md('''# 21 — 2B LoRA-1 + thinking limit 1,024

Use **A100 → Runtime → Run all**, like notebooks 18, 19, and 20.
The cells are readable. There is no Base64 bundle or large string.
The notebook gets code and frozen input files from the project on GitHub.
**Push the latest notebook, scripts, and `results/lora-limit-inputs/` first.**

It answers **464 unique problems, one attempt each**, using existing LoRA-1.
A LoRA is a trained add-on. A token is a small piece of text.
No new training or other model is run.

The original lora100 weight file must be here:

`MyDrive/stop-overthinking/results/mini/lora/lora100/adapter_model.safetensors`

Allow Drive access. Enter the units-per-hour rate and your current unit balance.
The rate in your screenshot was **6.77**, not the remaining balance.
This revised workflow has a **45-unit total estimated ceiling**, approved for completing all 464 problems.
Recorded usage from the failed LoRA-loading attempt is retained. Older setup costs remain documented separately.
The run ends when work finishes; it does not aim to spend the full allowance.
It keeps the old ledger for reference and uses a new ledger with actual balance checks.
On resumes, it accounts for balance changes instead of guessing disconnected hours.

Setup removes unused TorchAO, checks LoRA injection on CPU, and uses compatible installed packages and ready GPU-library wheels.
If the newest PyTorch has no wheel, it uses PyTorch 2.9.1 + CUDA 12.8 with a published wheel.
It does not attempt a long source compilation. Package installation is not inference-tested locally.

```text
GPU + Drive → GitHub → install → fast-library check → frozen problems
            → existing LoRA + limit → tests → comparison → saved ZIP
```

**Question:** does LoRA + limit improve on original 2B + the same limit?
**Hypothesis:** higher accuracy, or similar accuracy with fewer total tokens.
**What changes:** add LoRA-1 to the existing 1,024-token limit.
**Measures:** passing tests, thinking/total tokens, and paired uncertainty.
**Main comparison:** saved first attempts from original 2B + limit.
**Data:** 464 problems; uncapped LoRA-1 has 424 reference problems.
**Support:** positive accuracy-gap interval, or useful token savings with similar accuracy.
**Contradiction:** no useful gain, worse accuracy, or more cost without improvement.

This is a retrospective extension. Historical package versions and batches can differ.
Matching seeds does not make those differences disappear.
''')
    md('''## 0. Fixed experiment settings

**Problem:** avoid accidentally running training or another model.
**Why:** test only the new combination at low cost.
**Input:** the agreed model, limit, and budget.
**Output:** fixed settings for every later cell.
**Choice:** one attempt, one model, and one thinking limit.''')
    code('''MODEL_PROFILE = "qwen35_2b"
WAY = "lora1-limit1024"
THINK_BUDGET = 1024
N_PROBLEMS = 464
TRIES = 1
UNIT_CAP = 45.0
RESERVE_UNITS = 1.5
GENERATION_RESERVE_UNITS = 3.0
PREFLIGHT_PASSED = False
PROBLEMS_READY = False
print("2B LoRA-1 + limit1024 only • 464 problems • one attempt • no training")
''')
    md('''## 1. GPU, Drive, and GitHub

**Problem:** missing weights, code, or Drive caused earlier failures.
**Why:** check them before downloading the model.
**Input:** your A100, original LoRA-1, and current Colab resource values.
**Output:** the project checkout and persistent result/budget paths.
**Choice:** follow the GitHub/Drive pattern of notebook 20 and stop on missing inputs.''')
    code('''import os, sys, json, time, math, subprocess, hashlib, signal, shutil
from pathlib import Path
os.chdir("/content")
gpu_check = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"], capture_output=True, text=True)
if gpu_check.returncode:
    raise RuntimeError("Choose A100 GPU in Runtime → Change runtime type.")
GPU, MEMORY = [x.strip() for x in gpu_check.stdout.strip().splitlines()[0].split(",")]
GPU_GB = float(MEMORY) / 1024
if "A100" not in GPU or GPU_GB < 35:
    raise RuntimeError(f"Expected A100, got {GPU} ({GPU_GB:.0f} GB).")
BATCH = 128 if GPU_GB >= 70 else 64
print(f"GPU: {GPU} ({GPU_GB:.0f} GB) • batch {BATCH}")
from google.colab import drive
drive.mount("/content/drive")
DRIVE = Path("/content/drive/MyDrive/stop-overthinking")
ADAPTER_SOURCE = DRIVE / "results/mini/lora/lora100/adapter_model.safetensors"
if not ADAPTER_SOURCE.is_file() or ADAPTER_SOURCE.stat().st_size < 1024:
    raise RuntimeError("Missing original lora100 weight file: " + str(ADAPTER_SOURCE))
OUT = DRIVE / "results/lora-limit-2b"
OUT.mkdir(parents=True, exist_ok=True)
probe = OUT / ".write-check"; probe.write_text("ok"); probe.unlink()

def resource_number(prompt):
    try:
        value = float(input(prompt).strip())
    except ValueError:
        raise RuntimeError("Enter the number shown by Colab, then rerun this cell.")
    if not math.isfinite(value) or value <= 0:
        raise RuntimeError("Enter a positive number shown by Colab.")
    return value
UNIT_RATE = resource_number("Compute units per hour (your screenshot showed 6.77): ")
AVAILABLE_NOW = resource_number("Available compute units right now (the balance, not the rate): ")
LEDGER = OUT / "compute-ledger-v2.json"
OLD_LEDGER = OUT / "compute-ledger.json"
if OLD_LEDGER.exists():
    print("Keeping the previous attempt ledger unchanged:", OLD_LEDGER)
if LEDGER.exists():
    budget = json.loads(LEDGER.read_text())
    # The user's fresh resource balance includes idle/disconnected usage.
    BASE_USED = max(float(budget.get("estimated_units", 0)), float(budget["initial_balance"]) - AVAILABLE_NOW, 0.0)
else:
    budget = {"version": 2, "initial_balance": AVAILABLE_NOW, "sessions": 0}
    BASE_USED = 0.0
SESSION_START = time.monotonic()
budget.update(estimated_units=BASE_USED, unit_rate=UNIT_RATE, unit_cap=UNIT_CAP,
              sessions=budget.get("sessions", 0) + 1, gpu=GPU, active=True,
              note="Revised workflow only. Estimate includes current-session time and confirmed balance changes on resume.")
def save_ledger(value):
    tmp = LEDGER.with_suffix(".tmp")
    with tmp.open("w") as f:
        json.dump(value, f, indent=2); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, LEDGER)
def tick():
    budget["estimated_units"] = BASE_USED + (time.monotonic() - SESSION_START) / 3600 * UNIT_RATE
    save_ledger(budget)
def remaining_seconds(reserve=RESERVE_UNITS):
    tick()
    return max(0.0, (min(UNIT_CAP - budget["estimated_units"], AVAILABLE_NOW - (budget["estimated_units"] - BASE_USED)) - reserve) / UNIT_RATE * 3600)
save_ledger(budget)
if remaining_seconds() < 60:
    raise RuntimeError("Not enough budget left for this run. Saved work is safe; review the ledger and Colab balance.")

REPO = "https://github.com/mahmudulhaquequdrati/stop-overthinking-thesis.git"
WORK = Path("/content/thesis")
if not (WORK / ".git").exists():
    subprocess.run(["git", "clone", "--depth", "1", "--branch", "master", REPO, str(WORK)], check=True, timeout=300)
else:
    subprocess.run(["git", "-C", str(WORK), "pull", "--ff-only", "origin", "master"], check=True, timeout=300)
INPUTS = WORK / "results/lora-limit-inputs"
need = [WORK / "scripts/run_lora_limit.py", WORK / "scripts/prepare_lora_limit_data.py",
        WORK / "scripts/compare_lora_limit.py", INPUTS / "manifest.json"]
if any(not p.exists() for p in need):
    raise RuntimeError("GitHub is missing this revision's input files/scripts. Push the latest project changes, then reopen this notebook.")
manifest = json.loads((INPUTS / "manifest.json").read_text())
for name, wanted in manifest["files"].items():
    path = WORK / name if name.startswith("scripts/") else INPUTS / Path(name).name
    if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != wanted:
        raise RuntimeError("GitHub code/input revision does not match its manifest: " + name)
ADAPTER = Path("/content/lora-limit-21/adapter-lora1")
ADAPTER.mkdir(parents=True, exist_ok=True)
shutil.copy2(ADAPTER_SOURCE, ADAPTER / "adapter_model.safetensors")
shutil.copy2(INPUTS / "adapter_config.json", ADAPTER / "adapter_config.json")
PROBLEMS = Path("/content/lora-limit-21/problems-464.json")
BASELINES = INPUTS / "baselines-first-attempt.json"
WHEELS = DRIVE / "wheels"; WHEELS.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(WORK / "scripts"))
os.chdir(WORK)
print("GitHub, Drive, LoRA weights, and input manifest checked.")
print(f"Revised-run budget used: {budget['estimated_units']:.2f}/{UNIT_CAP:.0f} units.")
''')
    md('''## 2. Helpers with logs and a budget stop

**Problem:** an install or GPU job can run longer than expected.
**Why:** protect the remaining compute balance.
**Input:** commands and their time estimates.
**Output:** logs on Drive and saved budget updates.
**Choice:** monitor worker processes and preserve completed work on a stop.''')
    # Reuse the already tested supervisor, with no package-install side effects here.
    import ast
    supervisor_source=''
    for c in previous['cells']:
        text=''.join(c['source'])
        if c['cell_type']=='code' and text.startswith('def run_process('):
            tree=ast.parse(text)
            node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='run_process')
            supervisor_source=ast.get_source_segment(text,node);break
    if not supervisor_source:
        raise RuntimeError('Cannot locate the tested subprocess supervisor in Notebook 21.')
    code(supervisor_source+'''

def pip_install(*packages, tag="install-packages", timeout=1200):
    command = [sys.executable, "-m", "pip", "install", "-q", "--disable-pip-version-check", *packages]
    if not run_process(command, tag, timeout):
        raise RuntimeError("Setup stopped at the time/budget limit. Read " + str(OUT / (tag + ".log")))
''')
    md('''## 3. Install packages

**Problem:** the earlier install downgraded working packages and pulled unrelated API dependencies.
**Why:** we need inference, datasets, and the saved-test graders only.
**Input:** Colab's installed packages.
**Output:** compatible inference/data libraries.
**Choice:** keep supported installed versions; EvalPlus is not needed to run our saved plus-test programs.''')
    code('''pip_install("transformers>=5.15,<6", "peft>=0.20,<0.22", "accelerate", "safetensors",
            "datasets", "flash-linear-attention", "ninja", "packaging", "wheel")
# TorchAO is optional and unused by this 16-bit, unquantized inference run.
# Colab's old copy causes PEFT adapter injection to fail before generation.
if not run_process([sys.executable, "-m", "pip", "uninstall", "-y", "torchao"], "remove-unused-torchao", 120):
    raise RuntimeError("Not enough time to remove the incompatible optional TorchAO backend.")
print("Package installation finished. Model download has not started.")
''')
    md('''## 4. Fast path — cached or released wheel, like notebook 20

**Problem:** the latest PyTorch/CUDA combination may have no ready convolution wheel.
**Why:** source compilation used the remaining setup time in your log.
**Input:** Python, PyTorch, CUDA, and saved/released wheel files.
**Output:** working fast libraries, checked in fresh processes.
**Choice:** try the current environment first; use a published compatible PyTorch stack if needed.
No source build is started.''')
    code('''import urllib.request

def torch_info():
    probe = "import json,sys,torch; print(json.dumps(dict(ver=torch.__version__.split('+')[0], cuda=(torch.version.cuda or '').split('.')[0], abi=str(torch.compiled_with_cxx11_abi()).upper(), py='cp%d%d'%sys.version_info[:2])))"
    checked = subprocess.run([sys.executable, "-c", probe], capture_output=True, text=True, timeout=90)
    if checked.returncode:
        raise RuntimeError("PyTorch check failed: " + checked.stderr[-1500:])
    info = json.loads(checked.stdout.strip().splitlines()[-1])
    info["tag"] = ".".join(info["ver"].split(".")[:2])
    if not info["cuda"]:
        raise RuntimeError("PyTorch has no CUDA. Choose a fresh A100 runtime.")
    return info

def fast_check():
    probe = "import causal_conv1d, fla; from transformers.models.qwen3_5.modeling_qwen3_5 import Qwen3_5ForCausalLM"
    return subprocess.run([sys.executable, "-c", probe], capture_output=True, text=True, timeout=120)

def wheel_tail(info):
    return f"+cu{info['cuda']}torch{info['tag']}cxx11abi{info['abi']}-{info['py']}-{info['py']}-linux_x86_64.whl"

request = urllib.request.Request("https://api.github.com/repos/Dao-AILab/causal-conv1d/releases/tags/v1.7.0", headers={"User-Agent": "thesis-notebook-21"})
assets = None
def released_wheel(info):
    global assets
    if assets is None:
        with urllib.request.urlopen(request, timeout=30) as response:
            assets = json.load(response).get("assets", [])
    return next((a for a in assets if wheel_tail(info) in a["name"]), None)

def install_ready(info):
    saved = sorted(p for p in WHEELS.glob("causal_conv1d*.whl") if wheel_tail(info) in p.name)
    if saved:
        try:
            pip_install("--no-deps", str(saved[0]), tag="install-convolution")
            if fast_check().returncode == 0:
                return True
        except RuntimeError as error:
            print("Saved wheel did not load:", str(error)[-500:])
    asset = released_wheel(info)
    if not asset:
        return False
    dest = WHEELS / asset["name"]
    temporary = str(dest) + ".part"
    download = "import urllib.request,os; urllib.request.urlretrieve(" + repr(asset["browser_download_url"]) + ", " + repr(temporary) + "); os.replace(" + repr(temporary) + ", " + repr(str(dest)) + ")"
    if not run_process([sys.executable, "-c", download], "download-wheel", 300):
        raise RuntimeError("Wheel download exceeded the remaining setup time.")
    pip_install("--no-deps", str(dest), tag="install-convolution")
    return fast_check().returncode == 0

info = torch_info()
print("Current environment:", info)
check = fast_check()
if check.returncode != 0 and not install_ready(info):
    print("No compatible ready wheel for this PyTorch/CUDA. Selecting a published ready-wheel stack.")
    target = dict(ver="2.9.1", tag="2.9", cuda="12", abi="TRUE", py=info["py"])
    if not released_wheel(target):
        raise RuntimeError("No published wheel for this Python version. Stop here; no source compilation is attempted.")
    pip_install("torch==2.9.1", "torchvision==0.24.1", "torchaudio==2.9.1",
                "--index-url", "https://download.pytorch.org/whl/cu128", tag="compatible-pytorch")
    info = torch_info()
    print("Compatible environment:", info)
    if not install_ready(info):
        raise RuntimeError("The compatible wheel did not load. See saved logs; model generation has not started.")
check = fast_check()
if check.returncode != 0:
    raise RuntimeError("FAST PATH OFF: " + check.stderr[-2000:])
print("FAST PATH ON")
run_process([sys.executable, "-m", "pip", "freeze"], "package-versions", 60)
os.chdir(WORK)
''')
    md('''## 4a. Check LoRA compatibility before downloading the model

**Problem:** an optional library can break PEFT even after the model loads.
**Why:** catch the exact adapter-injection error without paying for the 2B download.
**Input:** the adapter configuration and weight-file headers.
**Output:** a CPU-only compatibility check using a tiny model.
**Choice:** exercise PEFT injection, not just import its package. The real 2B weight loading is still checked later.''')
    code('''preflight_command = [sys.executable, str(WORK / "scripts/run_lora_limit.py"), "--phase", "preflight",
    "--adapter", str(ADAPTER), "--problems", str(PROBLEMS), "--out", str(OUT)]
if not run_process(preflight_command, "check-lora-compatibility", 180):
    raise RuntimeError("The compatibility check did not finish. Do not start model generation.")
PREFLIGHT_PASSED = True
print("CPU LoRA compatibility check passed.")
''')
    md('''## 5. Load the same 464 problems

**Problem:** downloaded lists or tests must not change the exam.
**Why:** compare the same questions with the original saved results.
**Input:** frozen project IDs/questions, pinned datasets, and the Drive cache.
**Output:** verified HumanEval+ and LiveCodeBench tests.
**Choice:** load external problem files like earlier notebooks, check them, and reuse the cache.''')
    code('''DATA_CACHE = DRIVE / "results/lora-limit-2b-inputs"
prepare_command = [sys.executable, str(WORK / "scripts/prepare_lora_limit_data.py"),
    "--manifest", str(INPUTS / "data-manifest.json"), "--templates", str(INPUTS / "problem-templates.json"),
    "--cache", str(DATA_CACHE), "--out", str(PROBLEMS)]
if not run_process(prepare_command, "prepare-data", 900):
    raise RuntimeError("Problem loading stopped; cached files and saved results are safe.")
problems = json.loads(PROBLEMS.read_text())["problems"]
assert len(problems) == len({p["task_id"] for p in problems}) == 464
assert set(p["task_id"] for p in problems) == set(manifest["problem_ids"])
assert not set(manifest["problem_ids"]).intersection(manifest["training_ids"])
assert all(p.get("test_plus") for p in problems if p["source"] == "humaneval")
assert all(0 < len(p["tests"]) <= 20 for p in problems if p["source"] == "lcb")
if not run_process([sys.executable, str(WORK / "scripts/grade_plus.py"), "--problems", str(PROBLEMS), "--source", "humaneval", "--check-official", "8"], "check-grader", 300):
    raise RuntimeError("Not enough time for the official-solution check.")
PROBLEMS_READY = True
print("464 problems checked. Official-solution grader check passed.")
''')
    md('''## 6. Answer the new combination only

**Problem:** measure LoRA-1 with the same limit as the free control.
**Why:** a win over unlimited thinking alone would not establish training's added value.
**Input:** the existing adapter and 464 checked problems.
**Output:** raw answers saved individually to Drive.
**Choice:** first 16 check execution; they count toward the total. Saved answers are skipped on resume.''')
    code('''GENERATION_COMPLETE = False
GENERATION_ERROR = None
worker = [sys.executable, str(WORK / "scripts/run_lora_limit.py"), "--problems", str(PROBLEMS), "--out", str(OUT), "--batch", str(BATCH)]
try:
    if not globals().get("PREFLIGHT_PASSED", False) or not globals().get("PROBLEMS_READY", False):
        raise RuntimeError("LoRA compatibility and problem/grader checks must pass before generation.")
    GENERATION_COMPLETE = run_process(worker + ["--phase", "generate", "--adapter", str(ADAPTER)], "generate", timeout=24*3600, reserve=GENERATION_RESERVE_UNITS)
    if not GENERATION_COMPLETE:
        (OUT / "generation-status.json").write_text(json.dumps({"state": "budget_stopped"}))
except Exception as error:
    GENERATION_ERROR = str(error)
    (OUT / "generation-status.json").write_text(json.dumps({"state": "failed", "error": GENERATION_ERROR[-5000:]}))
    print("GENERATION FAILED. There is no new accuracy result unless saved answers were graded.")
    print(GENERATION_ERROR[-5000:])
print("Generation completed:", GENERATION_COMPLETE)
''')
    md('''## 7. Grade and compare

**Problem:** text alone cannot establish correctness.
**Why:** benchmark tests decide whether code passes.
**Input:** saved raw answers and the actual tests.
**Output:** resumable grades and a comparison report using shared problem IDs.
**Choice:** use separate timed processes and saved first attempts for the references.''')
    code('''GRADING_COMPLETE = False
from run_lora_limit import read_answers
generated_count = sum(len(read_answers(OUT / f"test-{WAY}-{tag}.jsonl", True)) for tag in ("he", "lcb"))
if generated_count == 0:
    print("SKIP GRADING: zero answers were generated. This is not an accuracy result.")
else:
    try:
        GRADING_COMPLETE = run_process(worker + ["--phase", "grade"], "grade", timeout=24*3600, reserve=RESERVE_UNITS)
    except Exception as error:
        print("GRADING FAILED:", str(error)[-5000:])
        print("Completed grades are preserved; the report shows actual coverage.")
report_command = [sys.executable, str(WORK / "scripts/compare_lora_limit.py"), "--out", str(OUT), "--problems", str(PROBLEMS), "--baselines", str(BASELINES)]
if not run_process(report_command, "compare", timeout=120, reserve=0.1):
    print("No time to produce a report. Saved raw answers/grades can be analyzed later without GPU generation.")
summary_file = OUT / "SUMMARY.md"
if summary_file.exists():
    from IPython.display import display, Markdown
    display(Markdown(summary_file.read_text()))
print("Outputs saved:", OUT)
''')
    md('''## 8. Save a ZIP and release the GPU

**Problem:** leaving a paid session connected uses units.
**Why:** Drive already holds the completed work.
**Input:** raw outputs, grades, reports, and the revised-run ledger.
**Output:** a results ZIP and a released GPU.
**Choice:** disconnect automatically after successful completion. If an earlier cell fails, disconnect manually.''')
    code(old_code['finish'])
    for i,c in enumerate(cells):c['id']=f'lora-limit-21-{i:02d}'
    notebook=dict(cells=cells,metadata={'accelerator':'GPU','colab':{'name':OUT.name,'provenance':[]},
        'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},
        'language_info':{'name':'python'},'gpuClass':'premium'},nbformat=4,nbformat_minor=5)
    OUT.write_text(json.dumps(notebook,indent=1)+'\n')
    print(f'Built readable Notebook 21: {len(cells)} cells, {OUT.stat().st_size/1000:.1f} KB; input files external.')
    return notebook

if __name__=='__main__':build()
