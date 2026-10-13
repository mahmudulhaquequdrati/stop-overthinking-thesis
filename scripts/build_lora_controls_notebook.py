"""Build Notebook24 like21: existing adapters, frozen464, two new limits.
No GPU calls. Small external JSON files keep the notebook readable.
"""
import csv
import json
import hashlib
from pathlib import Path
from combine_results import load_results,training_audit
ROOT=Path(__file__).resolve().parents[1]

def build():
    _,sources,ids=load_results();training_audit(ids)
    old_inputs=ROOT/'results/lora-limit-inputs';inputs=ROOT/'results/lora-controls-inputs'
    inputs.mkdir(exist_ok=True)
    for name in ['problem-templates.json','data-manifest.json']:(inputs/name).write_bytes((old_inputs/name).read_bytes())
    manifest=json.loads((old_inputs/'manifest.json').read_text())
    manifest['files']={};manifest['models']={};manifest['status']='NOTEBOOK READY — not measured'
    manifest['default_unit_cap']=40.0
    names=['run_lora_controls.py','compare_lora_controls.py','run_lora_limit.py','gen_colab.py','prompts.py','models.py',
           'prepare_lora_limit_data.py','grade_humaneval.py','grade_plus.py','grade_lcb.py','build_problem_set.py','lcb_data.py']
    for name in names:manifest['files']['scripts/'+name]=hashlib.sha256((ROOT/'scripts'/name).read_bytes()).hexdigest()
    for size,budget in [('0.8b',512),('2b',1024),('4b',2048)]:
        methods={m:{} for m in ('lora1','off','on',f'limit{budget}')};provenance=[]
        for source in sources:
            if source['model']!=size or source['method'] not in methods:continue
            path=ROOT/source['path'];provenance.append(dict(path=source['path'],sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
            with path.open() as stream:
                for row in csv.DictReader(stream):
                    if int(row['sample_index'])!=0:continue
                    dest=methods[source['method']];tid=row['task_id'];assert tid not in dest
                    dest[tid]=dict(passed=row['passed']=='True',thinking_tokens=float(row['thinking_tokens']),total_new_tokens=float(row['total_new_tokens']))
        assert all(set(v)==ids for v in methods.values())
        (inputs/f'baselines-{size}.json').write_text(json.dumps(dict(methods=methods,sources=provenance),separators=(',',':'))+'\n')
        folder='results/mini/lora/lora100' if size=='2b' else f'results/{size}/raw/lora/lora1'
        manifest['models'][size]=dict(think_budget=budget,adapter_path=folder,
            adapter_sha256=(json.loads((ROOT/'results/lora-limit-2b/completed-464/run-config.json').read_text())['adapter_sha256'] if size=='2b' else hashlib.sha256((ROOT/folder/'adapter_model.safetensors').read_bytes()).hexdigest()),
            config_sha256=hashlib.sha256((ROOT/folder/'adapter_config.json').read_bytes()).hexdigest())
    for path in sorted(inputs.glob('*.json')):
        if path.name!='manifest.json':manifest['files']['data/'+path.name]=hashlib.sha256(path.read_bytes()).hexdigest()
    (inputs/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    previous=json.loads((ROOT/'notebooks/21_2b_lora1_limit1024.ipynb').read_text());cells=[]
    def src(i):return ''.join(previous['cells'][i]['source'])
    def md(t):cells.append(dict(cell_type='markdown',metadata={},source=t.strip()+'\n'))
    def code(t):cells.append(dict(cell_type='code',metadata={},source=t.strip()+'\n',outputs=[],execution_count=None))
    md("""# 24 — Five LoRA controls, one session

Choose **A100 → Run all**, allow Drive, and enter the current compute-unit balance and rate.
Push this notebook, new scripts, and `results/lora-controls-inputs/` first.

All five run sequentially on the same frozen **464 problems**, one attempt each:

1. 0.8B LoRA-1 + thinking OFF.
2. 0.8B LoRA-1 + thinking limit512.
3. 2B LoRA-1 + thinking OFF.
4. 4B LoRA-1 + thinking limit2048.
5. 4B LoRA-1 + thinking OFF.

**2,320 new answers total.** No training or completed2B limit1024 rerun.
LoRA alone in earlier tables means thinking ON with no thinking-token limit.
OFF uses the same adapter with thinking disabled. Limits start thinking ON and force its end marker.
Overall caps:4,096 HumanEval+ and8,192 LiveCodeBench. Seed3407; earlier sampling settings.
Repeat stopping is ON for0.8B/4B and OFF for2B, matching previous model settings.

The2B adapter must be on Drive at:
`MyDrive/stop-overthinking/results/mini/lora/lora100/adapter_model.safetensors`.
The other adapters are already in the project. Both config and weight hashes are checked.

**Question:** do OFF or the same free thinking limit improve the existing adapter?
**Hypothesis:** higher accuracy or comparable accuracy with fewer output tokens.
**Change:** thinking OFF or a limit, keeping the adapter fixed.
**Measure:** code-test passing, thinking/output tokens, and shared-problem uncertainty.
**Compare:** saved first attempts for the same free control, LoRA alone, ON, and OFF.
**Support:** a positive gap interval against the corresponding free control.
**Contradiction:** worse accuracy or extra output without useful benefit.
This is retrospective; existing tests and historical references are reused.

One **Run all** executes all five, grading and saving each before moving on.
Enter the total compute-unit ceiling you want to use; it is limited by your current balance.
Reserve units for grading/reports. Stop when done; the ceiling is not a spending target.
Saved answers and grades resume independently if Colab disconnects.
The final cell downloads a ZIP and releases the GPU.
If an earlier setup cell fails, disconnect manually. New scores remain unmeasured until checked.
""")
    code('''UNIT_CAP = 40.0 # provisional; set from current resource prompts before any installs
RESERVE_UNITS = 1.5
GENERATION_RESERVE_UNITS = 3.0
RUNS = [("0.8b","off"),("0.8b","limit"),("2b","off"),("4b","limit"),("4b","off")]
PREFLIGHT_PASSED = False
PROBLEMS_READY = False
print("Five new LoRA controls •464 each • no training")''')
    md('## 1. GPU, Drive, GitHub, and both adapters\n\nCheck exact saved weights and code revisions before installation.')
    init=src(4)
    a=init.index('ADAPTER_SOURCE =');b=init.index('OUT =',a);init=init[:a]+init[b:]
    init=init.replace('results/lora-limit-2b','results/lora-controls').replace('results/lora-limit-inputs','results/lora-controls-inputs')
    init=init.replace('WORK / "scripts/run_lora_limit.py"','WORK / "scripts/run_lora_controls.py"').replace('WORK / "scripts/compare_lora_limit.py"','WORK / "scripts/compare_lora_controls.py"')
    a=init.index('ADAPTER =');b=init.index('WHEELS =',a)
    init=init[:a]+'''ADAPTERS = {}
for size in ("0.8b","2b","4b"):
    spec=manifest["models"][size]
    source=(DRIVE/spec["adapter_path"]) if size=="2b" else WORK/spec["adapter_path"]
    config_source=WORK/spec["adapter_path"]/"adapter_config.json"
    def sha_file(path):
        h=hashlib.sha256()
        with path.open("rb") as f:
            for part in iter(lambda:f.read(1024*1024),b""):h.update(part)
        return h.hexdigest()
    if sha_file(source/"adapter_model.safetensors")!=spec["adapter_sha256"] or sha_file(config_source)!=spec["config_sha256"]:
        raise RuntimeError("Adapter mismatch: "+size)
    dest=Path("/content/lora-controls-24")/size
    dest.mkdir(parents=True,exist_ok=True)
    shutil.copy2(source/"adapter_model.safetensors",dest/"adapter_model.safetensors")
    shutil.copy2(config_source,dest/"adapter_config.json")
    ADAPTERS[size]=dest
PROBLEMS = Path("/content/lora-controls-24/problems-464.json")
''' +init[b:]
    init=init.replace('Revised workflow only.', 'Notebook24 only.').replace('Revised-run budget used:', 'This notebook budget used:')
    init=init.replace('AVAILABLE_NOW = resource_number("Available compute units right now (the balance, not the rate): ")', 'AVAILABLE_NOW = resource_number("Available compute units right now: ")\nUNIT_CAP = min(resource_number("Total unit ceiling for all five runs (up to your balance): "), AVAILABLE_NOW)')
    code(init)
    md('## 2. Monitored commands and installation\n\nUse the successful Notebook21 package setup, with logs and budget stops.')
    code(src(6));code(src(8));code(src(10).replace('thesis-notebook-21','thesis-notebook-24'))
    md('## 3. Check both adapters on CPU\n\nCheck PEFT injection without downloading a base model. Real tensor mapping is checked during GPU loading.')
    code('''def worker(size,mode,phase):
    way="lora1-off" if mode=="off" else "lora1-limit"+str(manifest["models"][size]["think_budget"])
    folder=OUT/size/way;folder.mkdir(parents=True,exist_ok=True)
    return [sys.executable,str(WORK/"scripts/run_lora_controls.py"),"--model",size,"--mode",mode,
        "--phase",phase,"--problems",str(PROBLEMS),"--out",str(folder),
        "--adapter",str(ADAPTERS[size]),"--batch",str((64 if GPU_GB>=70 else 32) if size=="4b" else BATCH)]
for size in ("0.8b","2b","4b"):
    if not run_process(worker(size,"off","preflight"),"preflight-"+size,180):
        raise RuntimeError("CPU compatibility check stopped: "+size)
PREFLIGHT_PASSED=True''')
    md('## 4. Load and check the frozen464 questions\n\nReuse Notebook21’s verified Drive cache. No new questions or tests are selected.')
    code(src(14)) # Cache stays the exact Notebook21 input set.
    md('''## 5. Generate, grade, and compare each new method

All five runs proceed in one session, each in its own worker process. Saved answers are skipped on resume.
Each model’s first16 technical checks count toward464. There is no accuracy gate.
Each report compares the same shared IDs and saved first attempts.
Different historical environments and batches remain a limitation.''')
    code('''from run_lora_limit import read_answers
for size,mode in RUNS:
    if not globals().get("PREFLIGHT_PASSED",False) or not globals().get("PROBLEMS_READY",False):
        print("STOP: compatibility and data/grader checks must finish first.")
        break
    way="lora1-off" if mode=="off" else "lora1-limit"+str(manifest["models"][size]["think_budget"])
    folder=OUT/size/way
    folder.mkdir(parents=True,exist_ok=True)
    tag=size+"-"+mode
    try:
        ok=run_process(worker(size,mode,"generate"),"generate-"+tag,24*3600,reserve=GENERATION_RESERVE_UNITS)
        if not ok:(folder/"generation-status.json").write_text(json.dumps({"state":"budget_stopped"}))
    except Exception as error:
        (folder/"generation-status.json").write_text(json.dumps({"state":"failed","error":str(error)[-5000:]}))
        print("GENERATION FAILED:",str(error)[-3000:])
    generated=sum(len(read_answers(folder/f"test-{way}-{tag}.jsonl",True)) for tag in ("he","lcb"))
    if generated:
        try:run_process(worker(size,mode,"grade"),"grade-"+tag,24*3600,reserve=RESERVE_UNITS)
        except Exception as error:print("GRADING FAILED:",str(error)[-3000:])
    else:print(size+": zero answers, skip grading. This is not0% accuracy.")
    report=[sys.executable,str(WORK/"scripts/compare_lora_controls.py"),"--model",size,"--mode",mode,
        "--out",str(folder),"--problems",str(PROBLEMS),"--baselines",str(INPUTS/f"baselines-{size}.json")]
    try:
        run_process(report,"compare-"+tag,120,reserve=0.1)
        if (folder/"SUMMARY.md").exists():
            from IPython.display import display,Markdown
            display(Markdown((folder/"SUMMARY.md").read_text()))
    except Exception as error:print("Report unavailable:",str(error)[-2000:])
    if remaining_seconds(GENERATION_RESERVE_UNITS)<120:
        print("Budget stop; resume this same notebook. Saved answers stay on Drive.")
        break
print("Outputs:",OUT)''')
    md('## 6. ZIP and release GPU\n\nSend the ZIP back to update the full464 table. All five new scores remain unmeasured until then.')
    code(src(20).replace('results/lora-limit-2b-download','results/lora-controls-download'))
    for i,c in enumerate(cells):c['id']=f'lora-controls-24-{i:02d}'
    notebook=dict(cells=cells,metadata=previous['metadata'],nbformat=4,nbformat_minor=5)
    notebook['metadata']['colab']['name']='24_lora1_off_and_limits.ipynb'
    path=ROOT/'notebooks/24_lora1_off_and_limits.ipynb';path.write_text(json.dumps(notebook,indent=1)+'\n')
    print(f'Built {path.name}: {len(cells)} cells, {path.stat().st_size/1000:.1f}KB.')
    return notebook

if __name__=='__main__':build()
