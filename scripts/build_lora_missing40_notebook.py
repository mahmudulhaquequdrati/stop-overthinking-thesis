"""Build a readable missing40 notebook from the successful Notebook21 setup.
Input: saved grades and extra40 tests. Output: small notebook plus audit manifest.
No model calls, training, or network access during this build.
"""
import hashlib
import json
from pathlib import Path
from combine_results import load_results,training_audit

ROOT=Path(__file__).resolve().parents[1]

def build():
    records,sources,ids=load_results();extra={k[2] for k,v in records.items() if v['cohort']=='extra'}
    assert len(extra)==40
    manifest=json.loads((ROOT/'results/lora-missing40/plan-manifest.json').read_text())
    assert set(manifest['problem_ids'])==extra
    manifest['training_ids']=sorted(json.loads((ROOT/'results/lora-limit-inputs/manifest.json').read_text())['training_ids'])
    training_audit(ids)
    manifest['all_problem_ids']=sorted(ids)
    manifest['problem_sha256']=hashlib.sha256((ROOT/'results/extra/extra-lcb.json').read_bytes()).hexdigest()
    manifest['models']={}
    for model in ('2b','4b'):
        existing={k[2] for k in records if k[:2]==(model,'lora1')}
        assert len(existing)==424 and ids-existing==extra
        manifest['models'][model]=dict(existing_coverage=424,missing_ids=sorted(extra),sources=[
            dict(path=s['path'],sha256=hashlib.sha256((ROOT/s['path']).read_bytes()).hexdigest())
            for s in sources if s['model']==model and s['method']=='lora1'])
    manifest['adapters']={
        '2b':dict(config_path='results/mini/lora/lora100/adapter_config.json',
                  weight_sha256=json.loads((ROOT/'results/lora-limit-2b/completed-464/run-config.json').read_text())['adapter_sha256']),
        '4b':dict(config_path='results/4b/raw/lora/lora1/adapter_config.json',
                  weight_sha256=hashlib.sha256((ROOT/'results/4b/raw/lora/lora1/adapter_model.safetensors').read_bytes()).hexdigest())}
    for a in manifest['adapters'].values():a['config_sha256']=hashlib.sha256((ROOT/a['config_path']).read_bytes()).hexdigest()
    scripts=['run_lora_missing40.py','run_lora_limit.py','gen_colab.py','models.py','prompts.py','grade_lcb.py','grade_humaneval.py','build_problem_set.py','lcb_data.py']
    manifest['script_hashes']={n:hashlib.sha256((ROOT/'scripts'/n).read_bytes()).hexdigest() for n in scripts}
    manifest['default_unit_cap']=20.0
    manifest['status']='NOTEBOOK READY — GPU run not started'
    manifest['planned_new_answers']=80
    (ROOT/'results/lora-missing40/plan-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    old=json.loads((ROOT/'notebooks/21_2b_lora1_limit1024.ipynb').read_text());cells=[]
    def md(t):cells.append(dict(cell_type='markdown',metadata={},source=t.strip()+'\n'))
    def code(t):cells.append(dict(cell_type='code',metadata={},source=t.strip()+'\n',outputs=[],execution_count=None))
    def src(i):return ''.join(old['cells'][i]['source'])
    md('''# 22 — Only the missing40: 2B and4B LoRA-1 alone

Choose **A100 → Run all**, and allow Drive access.
Push the latest scripts, notebook, and `results/lora-missing40/` first.
No encoded bundle, new questions, training, limits, or free-control reruns.

**80 new answers total:** 2B on40, then4B on the same40. One attempt each.
These are exactly the frozen extra40. The existing424 LoRA-alone problems are excluded.
The completed2B LoRA + limit result remains **41.2% (191/464)**.

The2B original adapter must be on Drive:
`MyDrive/stop-overthinking/results/mini/lora/lora100/adapter_model.safetensors`.
The4B adapter is already in the project. Both hashes are checked before setup.

A LoRA is a trained add-on. Both runs use ordinary thinking, with **no thinking-token limit**.
Overall output cap:8,192 tokens. Seed3407.2B repeat stopping OFF;4B ON, matching earlier runs.

**Question:** how does LoRA alone compare with the free control across all464?
**Hypothesis:** completing the missing evidence may change the observed gap.
**Change:** apply the existing adapter with ordinary thinking.
**Measure:** passing code tests and output tokens.
**Compare:** saved2B limit1024 and4B limit2048 on identical IDs.
**Data:** the missing40 existing questions, not a new held-out test.
**Support/contradiction:** higher/lower LoRA accuracy, with problem-based uncertainty.

Default ceiling: **20 estimated compute units total for this notebook**, including setup and resumes.
This is a separate ledger; it does not reset Notebook21 or reuse its45-unit allowance.
Enter Colab's current units-per-hour rate and available balance.
The notebook saves a ZIP and releases the GPU at the end.
If setup stops early, disconnect manually; saved results are safe.
''')
    code('''UNIT_CAP = 20.0
RESERVE_UNITS = 1.0
GENERATION_RESERVE_UNITS = 2.0
RUN_READY = False
print("2B and4B LoRA-1 alone •40 each • no training •20-unit estimated ceiling")''')
    md('''## 1. GPU, Drive, GitHub, and frozen IDs

Check both adapters and completed-result IDs before package setup.
The exact extra40 contents and original424 source hashes must match.
No already completed LoRA-alone problem can enter this run.''')
    code('''import os, sys, json, time, math, subprocess, hashlib, signal, shutil
from pathlib import Path
os.chdir("/content")
checked = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"], capture_output=True, text=True)
if checked.returncode: raise RuntimeError("Choose A100 GPU first.")
GPU, MEMORY = [x.strip() for x in checked.stdout.strip().splitlines()[0].split(",")]
GPU_GB = float(MEMORY)/1024
if "A100" not in GPU or GPU_GB < 35: raise RuntimeError("Expected A100 with at least40GB.")
from google.colab import drive
drive.mount("/content/drive")
DRIVE = Path("/content/drive/MyDrive/stop-overthinking")
OUT = DRIVE / "results/lora-missing40"
OUT.mkdir(parents=True, exist_ok=True)
probe = OUT / ".write-check"; probe.write_text("ok"); probe.unlink()

def resource_number(prompt):
    value = float(input(prompt).strip())
    if not math.isfinite(value) or value <= 0: raise RuntimeError("Enter a positive Colab resource number.")
    return value
UNIT_RATE = resource_number("Compute units per hour (previous A100 rate6.77): ")
AVAILABLE_NOW = resource_number("Available compute units right now: ")
LEDGER = OUT / "compute-ledger.json"
if LEDGER.exists():
    budget = json.loads(LEDGER.read_text())
    BASE_USED = max(float(budget.get("estimated_units",0)), float(budget["initial_balance"])-AVAILABLE_NOW,0.0)
else:
    budget = {"version":2,"initial_balance":AVAILABLE_NOW,"sessions":0}
    BASE_USED = 0.0
SESSION_START = time.monotonic()
budget.update(estimated_units=BASE_USED,unit_rate=UNIT_RATE,unit_cap=UNIT_CAP,
    sessions=budget.get("sessions",0)+1,gpu=GPU,active=True)
def save_ledger(value):
    tmp = LEDGER.with_suffix(".tmp")
    with tmp.open("w") as f:
        json.dump(value,f,indent=2); f.flush(); os.fsync(f.fileno())
    os.replace(tmp,LEDGER)
def tick():
    budget["estimated_units"] = BASE_USED+(time.monotonic()-SESSION_START)/3600*UNIT_RATE
    save_ledger(budget)
def remaining_seconds(reserve=RESERVE_UNITS):
    tick()
    return max(0.0,(min(UNIT_CAP-budget["estimated_units"],AVAILABLE_NOW-(budget["estimated_units"]-BASE_USED))-reserve)/UNIT_RATE*3600)
save_ledger(budget)
if remaining_seconds()<60: raise RuntimeError("Budget too low; saved work remains safe.")
WORK = Path("/content/thesis")
REPO = "https://github.com/mahmudulhaquequdrati/stop-overthinking-thesis.git"
if not (WORK/".git").exists():
    subprocess.run(["git","clone","--depth","1","--branch","master",REPO,str(WORK)],check=True,timeout=300)
else:
    subprocess.run(["git","-C",str(WORK),"pull","--ff-only","origin","master"],check=True,timeout=300)
os.chdir(WORK); sys.path.insert(0,str(WORK/"scripts"))
MANIFEST = WORK/"results/lora-missing40/plan-manifest.json"
PROBLEMS = WORK/"results/extra/extra-lcb.json"
manifest = json.loads(MANIFEST.read_text())
for name,sha in manifest["script_hashes"].items():
    if hashlib.sha256((WORK/"scripts"/name).read_bytes()).hexdigest()!=sha: raise RuntimeError("Script revision mismatch: "+name)
from run_lora_missing40 import check_inputs
items = json.loads(PROBLEMS.read_text())["problems"]
assert len(items)==len({p["task_id"] for p in items})==40
manifest["problems_path"] = str(PROBLEMS)
check_inputs(WORK,manifest,{p["task_id"]:p for p in items})
ADAPTERS = {}
for model in ("2b","4b"):
    spec = manifest["adapters"][model]
    weights = DRIVE/"results/mini/lora/lora100/adapter_model.safetensors" if model=="2b" else WORK/"results/4b/raw/lora/lora1/adapter_model.safetensors"
    config = WORK/spec["config_path"]
    if not weights.exists(): raise RuntimeError("Missing adapter: "+str(weights))
    def sha_file(path):
        h=hashlib.sha256()
        with path.open("rb") as f:
            for part in iter(lambda:f.read(1024*1024),b""):h.update(part)
        return h.hexdigest()
    if sha_file(weights)!=spec["weight_sha256"] or sha_file(config)!=spec["config_sha256"]: raise RuntimeError("Adapter hash mismatch: "+model)
    dest=Path("/content/lora-missing40")/model
    dest.mkdir(parents=True,exist_ok=True)
    shutil.copy2(weights,dest/"adapter_model.safetensors")
    shutil.copy2(config,dest/"adapter_config.json")
    ADAPTERS[model]=dest
WHEELS = DRIVE/"wheels"; WHEELS.mkdir(parents=True,exist_ok=True)
print("Both adapters verified; exactly40 missing IDs per model. Existing424 excluded.")''')
    md('## 2. Monitored commands and package setup\n\nReuse the successful Notebook21 setup. Logs and budget stay on Drive.')
    code(src(6));code(src(8));code(src(10).replace('thesis-notebook-21','thesis-notebook-22'))
    md('## 3. Check both adapters on CPU\n\nExercise PEFT injection before base-model downloads. No2B or4B inference yet.')
    code('''def worker(model,phase):
    folder=OUT/model; folder.mkdir(parents=True,exist_ok=True)
    return [sys.executable,str(WORK/"scripts/run_lora_missing40.py"),"--phase",phase,
        "--model",model,"--adapter",str(ADAPTERS[model]),"--problems",str(PROBLEMS),
        "--manifest",str(MANIFEST),"--root",str(WORK),"--out",str(folder),
        "--batch",str((64 if GPU_GB>=70 else32) if model=="4b" else(128 if GPU_GB>=70 else64))]
for model in ("2b","4b"):
    if not run_process(worker(model,"preflight"),"preflight-"+model,180):
        raise RuntimeError("CPU adapter check stopped: "+model)
RUN_READY=True
print("Both CPU compatibility checks passed.")'''.replace('else32','else 32').replace('else64','else 64'))
    md('''## 4. Run2B, then4B, grade, and report

Each model runs in a separate process, freeing GPU memory when it ends.
First4 answers measure execution speed and count toward40.
Saved answers and grades are skipped on resume. A partial run is labelled partial.
The results here are40-problem subset scores; the464 scores are recalculated later.''')
    code('''from run_lora_missing40 import paths,read_answers
for model in ("2b","4b"):
    if not globals().get("RUN_READY",False):
        print("STOP: setup/CPU checks did not finish. No generation started.")
        break
    try:
        ok=run_process(worker(model,"generate"),"generate-"+model,24*3600,reserve=GENERATION_RESERVE_UNITS)
        if not ok:
            (OUT/model/"generation-status.json").write_text(json.dumps({"state":"budget_stopped"}))
        ans,_=paths(OUT/model)
        if read_answers(ans,True):
            run_process(worker(model,"grade"),"grade-"+model,24*3600,reserve=RESERVE_UNITS)
        else: print(model+": zero answers; skip grading. This is not0% accuracy.")
    except Exception as error:
        print(model+" FAILED:",str(error)[-4000:])
    try:
        run_process(worker(model,"report"),"report-"+model,120,reserve=0.1)
        report=OUT/model/"SUMMARY.md"
        if report.exists():
            from IPython.display import display,Markdown
            display(Markdown(report.read_text()))
    except Exception as error: print("Report unavailable:",str(error)[-2000:])
    if remaining_seconds(GENERATION_RESERVE_UNITS)<120:
        print("Budget stop. Reopen this notebook to resume saved work.")
        break
print("All available work saved:",OUT)''')
    md('## 5. ZIP and disconnect\n\nDownload the ZIP and send it back for checked464-problem updates. The Drive copy stays saved.')
    code(src(20).replace('results/lora-limit-2b-download','results/lora-missing40-download'))
    for i,c in enumerate(cells):c['id']=f'lora-missing40-22-{i:02d}'
    notebook=dict(cells=cells,metadata=old['metadata'],nbformat=4,nbformat_minor=5)
    notebook['metadata']['colab']['name']='22_lora1_missing40_2b_4b.ipynb'
    path=ROOT/'notebooks/22_lora1_missing40_2b_4b.ipynb';path.write_text(json.dumps(notebook,indent=1)+'\n')
    print(f'Built {path.name}: {len(cells)} cells, {path.stat().st_size/1000:.1f}KB.')
    return notebook

if __name__=='__main__':build()
