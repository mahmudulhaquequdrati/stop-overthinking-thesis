"""Build Notebook23 like21: existing adapters, frozen464, two new limits.
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
    old_inputs=ROOT/'results/lora-limit-inputs';inputs=ROOT/'results/lora-limit-sizes-inputs'
    inputs.mkdir(exist_ok=True)
    for name in ['problem-templates.json','data-manifest.json']:(inputs/name).write_bytes((old_inputs/name).read_bytes())
    manifest=json.loads((old_inputs/'manifest.json').read_text())
    manifest['files']={};manifest['models']={};manifest['status']='NOTEBOOK READY — not measured'
    manifest['default_unit_cap']=40.0
    names=['run_lora_limit_sizes.py','compare_lora_limit_sizes.py','run_lora_limit.py','gen_colab.py','prompts.py','models.py',
           'prepare_lora_limit_data.py','grade_humaneval.py','grade_plus.py','grade_lcb.py','build_problem_set.py','lcb_data.py']
    for name in names:manifest['files']['scripts/'+name]=hashlib.sha256((ROOT/'scripts'/name).read_bytes()).hexdigest()
    for size,budget in [('0.8b',512),('4b',2048)]:
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
        folder=f'results/{size}/raw/lora/lora1'
        manifest['models'][size]=dict(think_budget=budget,adapter_path=folder,
            adapter_sha256=hashlib.sha256((ROOT/folder/'adapter_model.safetensors').read_bytes()).hexdigest(),
            config_sha256=hashlib.sha256((ROOT/folder/'adapter_config.json').read_bytes()).hexdigest())
    for path in sorted(inputs.glob('*.json')):
        if path.name!='manifest.json':manifest['files']['data/'+path.name]=hashlib.sha256(path.read_bytes()).hexdigest()
    (inputs/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    previous=json.loads((ROOT/'notebooks/21_2b_lora1_limit1024.ipynb').read_text());cells=[]
    def src(i):return ''.join(previous['cells'][i]['source'])
    def md(t):cells.append(dict(cell_type='markdown',metadata={},source=t.strip()+'\n'))
    def code(t):cells.append(dict(cell_type='code',metadata={},source=t.strip()+'\n',outputs=[],execution_count=None))
    md('''# 23 — Existing LoRA + limits:0.8B512 and4B2,048

Like Notebook21: **A100 → Run all**, allow Drive, enter the current rate and balance.
Push this notebook, new scripts, and `results/lora-limit-sizes-inputs/` first.
Readable cells only; no encoded bundle or new training.

**0.8B LoRA-1 + thinking limit512:**464 questions once.
**4B LoRA-1 + thinking limit2,048:**the same464 questions once.
Both adapters are already saved in the project and checked before setup.
The completed2B LoRA + limit1,024 result remains **41.2% (191/464)** and is not rerun.

A LoRA is a trained add-on. A token is a small piece of text.
These new methods start with thinking ON, stop its notes at the chosen token limit,
then allow the remaining output room for code. They are not thinking OFF.
Overall caps:4,096 for HumanEval+ and8,192 for LiveCodeBench.
Seed3407; same sampling as earlier. Repeat stopping stays ON for both sizes.

**Question:** does adding the trained adapter help with the same free limit?
**Hypothesis:** more passing answers or comparable accuracy with fewer output tokens.
**Change:** add LoRA-1 to limit512 or limit2048.
**Measures:** passing tests, thinking/output tokens, and uncertainty from shared problems.
**Compare:** saved first attempts for the same limit, LoRA alone, OFF, and ON.
**Support:** a positive accuracy-gap interval against the same limit alone.
**Contradiction:** worse accuracy, no useful gain, or extra cost without benefit.
**Data:** the existing464 IDs. This is retrospective, not a fresh held-out exam.

Separate total estimated ceiling: **40 compute units** including setup and resumes.
This does not reset old notebooks' ledgers. It ends when done; the ceiling is not a spending target.
Save the final ZIP. If an early setup cell fails, disconnect manually.
No accuracy is filled into the thesis until actual saved results are checked.
''')
    code('''UNIT_CAP = 40.0
RESERVE_UNITS = 1.5
GENERATION_RESERVE_UNITS = 3.0
PREFLIGHT_PASSED = False
PROBLEMS_READY = False
print("0.8B LoRA + limit512, then4B LoRA + limit2048 •464 each • no training")''')
    md('## 1. GPU, Drive, GitHub, and both adapters\n\nCheck exact saved weights and code revisions before installation.')
    init=src(4)
    a=init.index('ADAPTER_SOURCE =');b=init.index('OUT =',a);init=init[:a]+init[b:]
    init=init.replace('results/lora-limit-2b','results/lora-limit-sizes').replace('results/lora-limit-inputs','results/lora-limit-sizes-inputs')
    init=init.replace('WORK / "scripts/run_lora_limit.py"','WORK / "scripts/run_lora_limit_sizes.py"').replace('WORK / "scripts/compare_lora_limit.py"','WORK / "scripts/compare_lora_limit_sizes.py"')
    a=init.index('ADAPTER =');b=init.index('WHEELS =',a)
    init=init[:a]+'''ADAPTERS = {}
for size in ("0.8b","4b"):
    spec=manifest["models"][size]
    source=WORK/spec["adapter_path"]
    def sha_file(path):
        h=hashlib.sha256()
        with path.open("rb") as f:
            for part in iter(lambda:f.read(1024*1024),b""):h.update(part)
        return h.hexdigest()
    if sha_file(source/"adapter_model.safetensors")!=spec["adapter_sha256"] or sha_file(source/"adapter_config.json")!=spec["config_sha256"]:
        raise RuntimeError("Adapter mismatch: "+size)
    dest=Path("/content/lora-limit-23")/size
    dest.mkdir(parents=True,exist_ok=True)
    for name in ("adapter_model.safetensors","adapter_config.json"):shutil.copy2(source/name,dest/name)
    ADAPTERS[size]=dest
PROBLEMS = Path("/content/lora-limit-23/problems-464.json")
''' +init[b:]
    init=init.replace('Revised workflow only.', 'Notebook23 only.').replace('Revised-run budget used:', 'This notebook budget used:')
    code(init)
    md('## 2. Monitored commands and installation\n\nUse the successful Notebook21 package setup, with logs and budget stops.')
    code(src(6));code(src(8));code(src(10).replace('thesis-notebook-21','thesis-notebook-23'))
    md('## 3. Check both adapters on CPU\n\nCheck PEFT injection without downloading a base model. Real tensor mapping is checked during GPU loading.')
    code('''def worker(size,phase):
    folder=OUT/size;folder.mkdir(parents=True,exist_ok=True)
    return [sys.executable,str(WORK/"scripts/run_lora_limit_sizes.py"),"--model",size,
        "--phase",phase,"--problems",str(PROBLEMS),"--out",str(folder),
        "--adapter",str(ADAPTERS[size]),"--batch",str((64 if GPU_GB>=70 else 32) if size=="4b" else BATCH)]
for size in ("0.8b","4b"):
    if not run_process(worker(size,"preflight"),"preflight-"+size,180):
        raise RuntimeError("CPU compatibility check stopped: "+size)
PREFLIGHT_PASSED=True''')
    md('## 4. Load and check the frozen464 questions\n\nReuse Notebook21’s verified Drive cache. No new questions or tests are selected.')
    code(src(14)) # Cache stays the exact Notebook21 input set.
    md('''## 5. Generate, grade, and compare each new method

0.8B runs first, then4B in a separate process. Saved answers are skipped on resume.
Each model’s first16 technical checks count toward464. There is no accuracy gate.
Each report compares the same shared IDs and saved first attempts.
Different historical environments and batches remain a limitation.''')
    code('''from run_lora_limit import read_answers
for size in ("0.8b","4b"):
    if not globals().get("PREFLIGHT_PASSED",False) or not globals().get("PROBLEMS_READY",False):
        print("STOP: compatibility and data/grader checks must finish first.")
        break
    folder=OUT/size
    way="lora1-limit"+str(manifest["models"][size]["think_budget"])
    try:
        ok=run_process(worker(size,"generate"),"generate-"+size,24*3600,reserve=GENERATION_RESERVE_UNITS)
        if not ok:(folder/"generation-status.json").write_text(json.dumps({"state":"budget_stopped"}))
    except Exception as error:
        (folder/"generation-status.json").write_text(json.dumps({"state":"failed","error":str(error)[-5000:]}))
        print("GENERATION FAILED:",str(error)[-3000:])
    generated=sum(len(read_answers(folder/f"test-{way}-{tag}.jsonl",True)) for tag in ("he","lcb"))
    if generated:
        try:run_process(worker(size,"grade"),"grade-"+size,24*3600,reserve=RESERVE_UNITS)
        except Exception as error:print("GRADING FAILED:",str(error)[-3000:])
    else:print(size+": zero answers, skip grading. This is not0% accuracy.")
    report=[sys.executable,str(WORK/"scripts/compare_lora_limit_sizes.py"),"--model",size,
        "--out",str(folder),"--problems",str(PROBLEMS),"--baselines",str(INPUTS/f"baselines-{size}.json")]
    try:
        run_process(report,"compare-"+size,120,reserve=0.1)
        if (folder/"SUMMARY.md").exists():
            from IPython.display import display,Markdown
            display(Markdown((folder/"SUMMARY.md").read_text()))
    except Exception as error:print("Report unavailable:",str(error)[-2000:])
    if remaining_seconds(GENERATION_RESERVE_UNITS)<120:
        print("Budget stop; resume this same notebook. Saved answers stay on Drive.")
        break
print("Outputs:",OUT)''')
    md('## 6. ZIP and release GPU\n\nSend the ZIP back to update the full464 table. Both new scores remain unmeasured until then.')
    code(src(20).replace('results/lora-limit-2b-download','results/lora-limit-sizes-download'))
    for i,c in enumerate(cells):c['id']=f'lora-limit-23-{i:02d}'
    notebook=dict(cells=cells,metadata=previous['metadata'],nbformat=4,nbformat_minor=5)
    notebook['metadata']['colab']['name']='23_lora1_limits_08b_4b.ipynb'
    path=ROOT/'notebooks/23_lora1_limits_08b_4b.ipynb';path.write_text(json.dumps(notebook,indent=1)+'\n')
    print(f'Built {path.name}: {len(cells)} cells, {path.stat().st_size/1000:.1f}KB.')
    return notebook

if __name__=='__main__':build()
