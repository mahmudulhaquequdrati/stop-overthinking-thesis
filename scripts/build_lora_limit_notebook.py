"""Build standalone Notebook 21 with frozen data, scripts, and first-attempt scores.

The notebook needs only Colab, Drive, and the existing LoRA-1 weight file.
No repository clone, training, or dataset download is required.
"""
import base64
import csv
import hashlib
import io
import json
import zlib
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'notebooks/21_2b_lora1_limit1024.ipynb'
SCRIPT_NAMES=['models.py','prompts.py','build_problem_set.py','gen_colab.py',
    'grade_humaneval.py','grade_plus.py','grade_lcb.py','lcb_data.py',
    'run_lora_limit.py','compare_lora_limit.py']


def make_payload():
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
    files['data/problems-464.json']=json.dumps(frozen,separators=(',',':')).encode()
    files['data/baselines-first-attempt.json']=json.dumps(baselines,separators=(',',':')).encode()
    files['data/adapter_config.json']=(ROOT/'results/mini/lora/lora100/adapter_config.json').read_bytes()
    files['data/manifest.json']=json.dumps({'files':{k:hashlib.sha256(v).hexdigest() for k,v in files.items()},
        'problem_ids':sorted(ids),'training_ids':sorted(training),'created':'2026-10-14',
        'humanevalplus_revision':he_revision},indent=2).encode()
    buf=io.BytesIO()
    with zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
        for name,body in sorted(files.items()):
            info=zipfile.ZipInfo(name,date_time=(2026,10,14,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(info,body,compresslevel=6)
    return buf.getvalue()


def build():
    payload=make_payload();encoded=base64.b64encode(payload).decode()
    cells=[]
    def md(text):cells.append({'cell_type':'markdown','metadata':{},'source':text.strip()+'\n'})
    def code(text):cells.append({'cell_type':'code','metadata':{},'execution_count':None,'outputs':[],'source':text.strip()+'\n'})
    md('''# 21 — 2B LoRA-1 + thinking limit 1,024

Choose **A100 GPU**, then **Runtime → Run all**.
This asks one new way on **464 unique problems**, once each. It does no training.
A *LoRA* is a small trained add-on. A *token* is a small piece of text.

Before starting, put your existing **LoRA-1** weight file here:

`MyDrive/stop-overthinking/results/mini/lora/lora100/adapter_model.safetensors`

Use the file from the original **lora100** training run, not LoRA-2.
The correct adapter configuration is included. Do not rename a different adapter's weights.
This notebook includes its own scripts, questions, tests, and saved comparison scores.
It is larger than earlier notebooks because it carries the complete frozen test data.
No GitHub push or extra code upload is required.

Allow Drive access when asked. Enter Colab's displayed **compute units per hour** when asked.
You do not need to edit code. The run has a **15-unit estimated cap**, including setup.
Colab's balance cannot be read here; the cap uses the rate you enter.
Use a fresh runtime. Saved outputs let interrupted runs continue.

```text
Existing LoRA-1 → thinking capped at 1,024 → Python code → tests → comparison report
```

**Research question:** does LoRA + limit beat the original 2B + the same limit?
**Hypothesis:** combining them raises accuracy or saves total tokens at similar accuracy.
**What changes:** load the existing LoRA; keep the limit and generation rules.
**What we measure:** test passing, total tokens, thinking tokens, and shared-problem gaps.
**Comparison:** saved first attempts for limit, LoRA without limit, OFF, and ON.
**Data:** 464 problems; LoRA without limit has 424 reference results.
**Metric:** one attempt per problem; compare on shared problem IDs, with uncertainty.
**Support:** an accuracy gain with a positive interval, or comparable accuracy with fewer tokens.
**Contradiction:** no gain, worse accuracy, or higher cost without useful accuracy gains.

We are in **EXPERIMENT → DATA → RESULTS**. This is a retrospective extension.
Package versions and batch layouts differ from historical runs; the same seed does not erase that limitation.
''')
    md('''## 1. Check GPU, Drive, weights, and budget

**Problem:** avoid downloading a model when the weight file or GPU is missing.
**Why:** these failures previously wasted setup time.
**Input:** your A100, Drive folder, and displayed unit rate.
**Output:** checked paths and a saved budget ledger.
**Choice:** stop early instead of silently switching to temporary storage.''')
    code('''import os, sys, json, time, math, subprocess, hashlib, signal
from pathlib import Path
STARTED = time.time()
GPU_INFO = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"], capture_output=True, text=True)
if GPU_INFO.returncode != 0:
    raise RuntimeError("No NVIDIA GPU. Choose Runtime → Change runtime type → A100 GPU.")
GPU, MEMORY = [x.strip() for x in GPU_INFO.stdout.strip().splitlines()[0].split(",")]
GPU_GB = float(MEMORY) / 1024
if "A100" not in GPU or GPU_GB < 35:
    raise RuntimeError(f"This notebook is checked for A100, but got {GPU} ({GPU_GB:.0f} GB). Select A100.")
print(f"GPU: {GPU} ({GPU_GB:.0f} GB)")
from google.colab import drive
drive.mount("/content/drive")
DRIVE = Path("/content/drive/MyDrive/stop-overthinking")
ADAPTER_SOURCE = DRIVE / "results/mini/lora/lora100/adapter_model.safetensors"
if not ADAPTER_SOURCE.is_file() or ADAPTER_SOURCE.stat().st_size < 1024:
    raise RuntimeError("Missing LoRA-1 weights. Copy the original lora100 adapter_model.safetensors to: " + str(ADAPTER_SOURCE))
OUT = DRIVE / "results/lora-limit-2b"
OUT.mkdir(parents=True, exist_ok=True)
PROBE = OUT / ".write-check"
PROBE.write_text("ok"); PROBE.unlink()
raw_rate = input("Enter compute units per hour shown by Colab for this A100: ").strip()
try:
    UNIT_RATE = float(raw_rate)
except ValueError:
    raise RuntimeError("Enter the displayed numeric rate, for example 6.77. Then rerun this cell.")
if not math.isfinite(UNIT_RATE) or not 0 < UNIT_RATE <= 120:
    raise RuntimeError("The rate must be a positive number from Colab's resource display.")
UNIT_CAP = 15.0
RESERVE_UNITS = 1.5  # Save time for reports and closing the session.
GENERATION_RESERVE_UNITS = 3.0  # Keep grading time available.
BATCH = 128 if GPU_GB >= 70 else 64
LEDGER = OUT / "compute-ledger.json"
def save_ledger(value):
    tmp = LEDGER.with_suffix(".tmp")
    with tmp.open("w") as f:
        json.dump(value, f, indent=2); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, LEDGER)
if LEDGER.exists():
    budget = json.loads(LEDGER.read_text())
    if budget.get("active"):
        # If the last session vanished, conservatively count the unobserved interval.
        budget["estimated_units"] = min(UNIT_CAP, budget["estimated_units"] + max(0, STARTED - budget["last_tick"]) / 3600 * budget["unit_rate"])
else:
    budget = {"estimated_units": 0.0, "sessions": 0, "active": False}
budget.update(unit_rate=UNIT_RATE, unit_cap=UNIT_CAP, last_tick=STARTED, active=True,
              sessions=budget.get("sessions", 0) + 1, gpu=GPU, note="Estimated wall-clock usage, not Colab's billing balance.")
save_ledger(budget)
def tick():
    now = time.time()
    budget["estimated_units"] += max(0, now - budget["last_tick"]) / 3600 * UNIT_RATE
    budget["last_tick"] = now
    save_ledger(budget)
def remaining_seconds(reserve=RESERVE_UNITS):
    tick()
    return max(0.0, (UNIT_CAP - reserve - budget["estimated_units"]) / UNIT_RATE * 3600)
if remaining_seconds() < 60:
    budget["active"] = False; save_ledger(budget)
    raise RuntimeError("This experiment's budget is exhausted. Saved answers are safe; do not reset the ledger to bypass the cap.")
print(f"LoRA-1 found. Estimated used: {budget['estimated_units']:.2f}/{UNIT_CAP:.0f} units. Batch: {BATCH}.")
''')
    md('''## 2. Unpack this notebook's frozen files

**Problem:** GitHub code or local data can be missing.
**Why:** the notebook should work without a repository update.
**Input:** the compressed bundle included below.
**Output:** checked scripts and exactly 464 frozen problems in `/content/lora-limit-21`.
**Choice:** compare file hashes before using data, then copy the weight locally.''')
    code('''import base64, io, zipfile, shutil
WORK = Path("/content/lora-limit-21")
WORK.mkdir(parents=True, exist_ok=True)
BUNDLE = "'''+encoded+'''"
PAYLOAD_SHA256 = "'''+hashlib.sha256(payload).hexdigest()+'''"
packed = base64.b64decode(BUNDLE)
if hashlib.sha256(packed).hexdigest() != PAYLOAD_SHA256:
    raise RuntimeError("Notebook bundle is incomplete. Upload the original notebook again.")
with zipfile.ZipFile(io.BytesIO(packed)) as archive:
    for member in archive.infolist():
        dest = (WORK / member.filename).resolve()
        if not dest.is_relative_to(WORK.resolve()):
            raise RuntimeError("Unsafe bundle path")
    archive.extractall(WORK)
manifest = json.loads((WORK / "data/manifest.json").read_text())
for name, wanted in manifest["files"].items():
    if hashlib.sha256((WORK / name).read_bytes()).hexdigest() != wanted:
        raise RuntimeError("Bundled file failed its check: " + name)
PROBLEMS = WORK / "data/problems-464.json"
BASELINES = WORK / "data/baselines-first-attempt.json"
problems = json.loads(PROBLEMS.read_text())["problems"]
ids = {p["task_id"] for p in problems}
assert len(problems) == len(ids) == 464
assert ids == set(manifest["problem_ids"])
assert not ids.intersection(manifest["training_ids"])
assert sum(p["source"] == "humaneval" for p in problems) == 164
assert all(p.get("test_plus") for p in problems if p["source"] == "humaneval")
assert all(0 < len(p["tests"]) <= 20 for p in problems if p["source"] == "lcb")
ADAPTER = WORK / "adapter-lora1"
ADAPTER.mkdir(exist_ok=True)
shutil.copy2(ADAPTER_SOURCE, ADAPTER / "adapter_model.safetensors")
shutil.copy2(WORK / "data/adapter_config.json", ADAPTER / "adapter_config.json")
sys.path.insert(0, str(WORK / "scripts"))
os.chdir(WORK)
print("Checked 464 unique problems, their tests, comparison files, and scripts. Training ID overlap: zero.")
''')
    md('''## 3. Install and check inference packages

**Problem:** slow or mismatched GPU libraries can waste the budget.
**Why:** Qwen3.5 needs fast linear-attention and convolution kernels.
**Input:** the current Colab Python, PyTorch, and cached wheels.
**Output:** fresh-process import checks and a saved package list.
**Choice:** use the existing successful notebook's wheel repair approach, with time limits.
Only inference and grading packages are installed. Training libraries are unnecessary.''')
    code('''def run_process(command, tag, timeout=1200, reserve=RESERVE_UNITS):
    allowed = min(timeout, remaining_seconds(reserve))
    if allowed < 30:
        print(f"Budget stop before {tag}; saved work is safe.")
        return False
    log = OUT / (tag + ".log")
    print("Starting", tag, "• maximum", round(allowed / 60, 1), "minutes", flush=True)
    with log.open("a", buffering=1) as stream:
        position = log.stat().st_size
        proc = subprocess.Popen(command, cwd=WORK, stdout=stream, stderr=subprocess.STDOUT, start_new_session=True)
        started = time.monotonic()
        try:
            while proc.poll() is None:
                tick()
                if time.monotonic() - started >= allowed or remaining_seconds(reserve) <= 0:
                    os.killpg(proc.pid, signal.SIGTERM)
                    try:
                        proc.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        os.killpg(proc.pid, signal.SIGKILL); proc.wait()
                    print(f"Stopped {tag} at the time/budget limit. Log: {log}")
                    return False
                with log.open() as reader:
                    reader.seek(position); tail = reader.read(); position = reader.tell()
                if tail:
                    print(tail[-3000:], end="", flush=True)
                time.sleep(3)
        except BaseException:
            if proc.poll() is None:
                os.killpg(proc.pid, signal.SIGTERM)
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(proc.pid, signal.SIGKILL); proc.wait()
            raise
        finally:
            tick()
    if proc.returncode != 0:
        tail = log.read_text(errors="replace")[-5000:]
        raise RuntimeError(f"{tag} failed. Saved work is safe. Last log lines:\\n{tail}")
    return True

def pip_install(*packages, timeout=900):
    if not run_process([sys.executable, "-m", "pip", "install", "--disable-pip-version-check", *packages], "install-packages", timeout):
        raise RuntimeError("Setup stopped at its budget/time limit. Inspect the saved log before resuming.")

pip_install("transformers==5.15.0", "peft>=0.20.0,<0.21", "accelerate", "safetensors", "evalplus", "flash-linear-attention", "ninja", "packaging", "wheel")
WHEELS = DRIVE / "wheels"
WHEELS.mkdir(parents=True, exist_ok=True)
probe = subprocess.run([sys.executable, "-c", "import json, sys, torch; print(json.dumps(dict(torch=torch.__version__.split('+')[0], cuda=torch.version.cuda, abi=str(torch.compiled_with_cxx11_abi()).upper(), py='cp%d%d'%sys.version_info[:2])))"], capture_output=True, text=True)
if probe.returncode != 0:
    raise RuntimeError("PyTorch check failed: " + probe.stderr[-1000:])
info = json.loads(probe.stdout.strip().splitlines()[-1])
if not info["cuda"]:
    raise RuntimeError("PyTorch has no CUDA. Reconnect with an A100 runtime.")
tag = ".".join(info["torch"].split(".")[:2])
needle = f"+cu{info['cuda'].split('.')[0]}torch{tag}cxx11abi{info['abi']}-{info['py']}-{info['py']}-linux_x86_64.whl"
def fast_check():
    return subprocess.run([sys.executable, "-c", "import causal_conv1d, fla; from transformers.models.qwen3_5.modeling_qwen3_5 import Qwen3_5ForCausalLM"], capture_output=True, text=True)
check = fast_check()
if check.returncode != 0:
    candidates = sorted(p for p in WHEELS.glob("causal_conv1d*.whl") if needle in p.name)
    if not candidates:
        try:
            import urllib.request
            request = urllib.request.Request("https://api.github.com/repos/Dao-AILab/causal-conv1d/releases/latest", headers={"User-Agent": "thesis-notebook-21"})
            with urllib.request.urlopen(request, timeout=30) as response:
                release = json.load(response)
            asset = next((a for a in release.get("assets", []) if needle in a["name"]), None)
            if asset:
                dest = WHEELS / asset["name"]
                download_code = "import urllib.request; urllib.request.urlretrieve(" + repr(asset["browser_download_url"]) + ", " + repr(str(dest)) + ")"
                if run_process([sys.executable, "-c", download_code], "download-wheel", 300):
                    candidates = [dest]
        except Exception as error:
            print("Ready-wheel lookup failed:", type(error).__name__, str(error)[:200])
    if candidates:
        pip_install("--no-deps", str(candidates[0]))
    check = fast_check()
    if check.returncode != 0:
        print("Building a matching convolution wheel; maximum 10 minutes.")
        if not run_process([sys.executable, "-m", "pip", "wheel", "causal-conv1d", "--no-build-isolation", "--no-deps", "-w", str(WHEELS)], "build-wheel", 600):
            raise RuntimeError("Fast-kernel build exceeded its setup budget. See build-wheel.log; no model answers were requested.")
        candidates = sorted(p for p in WHEELS.glob("causal_conv1d*.whl") if needle in p.name)
        if not candidates:
            raise RuntimeError("The wheel built, but its PyTorch/CUDA tag does not match this runtime.")
        pip_install("--no-deps", str(candidates[0]))
check = fast_check()
if check.returncode != 0:
    raise RuntimeError("Fast GPU libraries failed to import. Model generation stopped to avoid a slow run. " + check.stderr[-1500:])
if not run_process([sys.executable, "-m", "pip", "freeze"], "package-versions", 60):
    raise RuntimeError("Budget exhausted during package checks.")
print("FAST PATH ON. Qwen3.5 imports correctly.")
if not run_process([sys.executable, str(WORK / "scripts/grade_plus.py"), "--problems", str(PROBLEMS), "--source", "humaneval", "--check-official", "8"], "check-grader", 300):
    raise RuntimeError("No time for the official-solution grader check; generation will not start.")
''')
    md('''## 4. Run the one new combination

**Problem:** find whether the trained add-on benefits from the same thinking limit.
**Why:** this tests the missing combination without training again.
**Input:** frozen problems, existing LoRA-1, and a 1,024-token thinking budget.
**Output:** raw answers saved individually to Drive.
**Choice:** check the first 16 across task types, then continue automatically.
Those 16 count toward the 464; no extra pilot answers are bought.
Resuming skips saved answers. Different resumed batch layouts can change later random draws.''')
    code('''GENERATION_COMPLETE = False
worker = [sys.executable, str(WORK / "scripts/run_lora_limit.py"), "--problems", str(PROBLEMS), "--out", str(OUT), "--batch", str(BATCH)]
try:
    GENERATION_COMPLETE = run_process(worker + ["--phase", "generate", "--adapter", str(ADAPTER)], "generate", timeout=24*3600, reserve=GENERATION_RESERVE_UNITS)
except Exception as error:
    print("Generation stopped:", str(error)[-5000:])
    print("The next cells will grade saved answers and make a partial report.")
print("Generation completed:", GENERATION_COMPLETE)
''')
    md('''## 5. Grade saved answers and compare

**Problem:** saved text alone cannot establish accuracy.
**Why:** only benchmark tests can mark the code.
**Input:** saved answers and the bundled benchmark tests.
**Output:** resumable graded CSVs, `SUMMARY.md`, and `summary.json`.
**Choice:** grade code in separate timed processes, and compare first attempts on shared IDs.
HumanEval+ uses the plus tests; LiveCodeBench uses the original saved tests, up to 20 per problem.''')
    code('''GRADING_COMPLETE = False
try:
    GRADING_COMPLETE = run_process(worker + ["--phase", "grade"], "grade", timeout=24*3600, reserve=RESERVE_UNITS)
except Exception as error:
    print("Grading stopped:", str(error)[-5000:])
    print("Finished grades remain saved; the report will show partial coverage.")
report_command = [sys.executable, str(WORK / "scripts/compare_lora_limit.py"), "--out", str(OUT), "--problems", str(PROBLEMS), "--baselines", str(BASELINES)]
if not run_process(report_command, "compare", timeout=120, reserve=0.1):
    print("No time for the comparison report. Saved raw answers and grades can be analyzed later without GPU generation.")
summary_file = OUT / "SUMMARY.md"
if summary_file.exists():
    from IPython.display import display, Markdown
    display(Markdown(summary_file.read_text()))
print("Outputs saved:", OUT)
''')
    md('''## 6. Save a download and release the GPU

**Problem:** leaving a paid runtime connected wastes units.
**Why:** the data is already saved on Drive.
**Input:** this experiment's outputs and its budget ledger.
**Output:** a ZIP on Drive, a download prompt, and a disconnected GPU.
**Choice:** release the runtime automatically after saving the report.
If an earlier setup cell fails, choose **Runtime → Disconnect and delete runtime** yourself.
If the last session ended unexpectedly, the ledger conservatively counts the unobserved interval.''')
    code('''tick()
budget["active"] = False
save_ledger(budget)
ZIP_BASE = DRIVE / "results/lora-limit-2b-download"
try:
    shutil.make_archive(str(ZIP_BASE), "zip", root_dir=OUT)
    from google.colab import files
    print("Results ZIP:", str(ZIP_BASE) + ".zip")
    files.download(str(ZIP_BASE) + ".zip")
except Exception as error:
    print("Download was not started:", type(error).__name__, str(error)[:200])
    print("Your results are still saved on Drive:", OUT)
finally:
    print(f"Estimated charged time: {budget['estimated_units']:.2f}/{UNIT_CAP:.0f} units at the rate you entered.")
    print("Disconnecting this GPU runtime now. Reopen the same notebook to resume a partial run.")
    from google.colab import runtime
    runtime.unassign()
''')
    notebook={'cells':cells,'metadata':{'accelerator':'GPU','colab':{'name':OUT.name,'provenance':[]},
        'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},
        'language_info':{'name':'python'},'gpuClass':'premium'},'nbformat':4,'nbformat_minor':5}
    for i,cell in enumerate(cells):cell['id']=f'lora-limit-21-{i:02d}'
    OUT.write_text(json.dumps(notebook,indent=1)+'\n')
    print(f'Built {OUT.name}: {len(cells)} cells, {OUT.stat().st_size/1e6:.1f} MB; frozen bundle {len(payload)/1e6:.1f} MB.')
    return notebook

if __name__=='__main__':build()
