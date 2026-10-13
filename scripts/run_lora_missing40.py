"""Fill only the extra40 LoRA-alone gaps. No training or completed-answer repeats.

Input: frozen40 IDs, saved424 provenance, existing adapters.
Output: independently resumable raw answers, grades, and honest subset reports.
Uses the existing generator and grader to preserve earlier experiment settings.
"""
import argparse
import csv
import json
import os
import random
import time
from pathlib import Path
from run_lora_limit import atomic_json,digest,read_answers,read_grades,FIELDS

SETTINGS={'2b':('qwen35_2b','unsloth/Qwen3.5-2B',False),
          '4b':('qwen35_4b','unsloth/Qwen3.5-4B',True)}


def check_inputs(root, manifest, problems):
    root=Path(root)
    expected=set(manifest['problem_ids'])
    if len(expected)!=40 or len(problems)!=40 or set(problems)!=expected:
        raise RuntimeError('Expected exactly the frozen40 problem IDs.')
    if expected & set(manifest['training_ids']):raise RuntimeError('Training ID overlap')
    if digest(manifest['problems_path'])!=manifest['problem_sha256']:
        raise RuntimeError('Problem contents changed')
    for model in SETTINGS:
        existing=set()
        attempts=set()
        for source in manifest['models'][model]['sources']:
            path=root/source['path']
            if digest(path)!=source['sha256']:raise RuntimeError('Saved424 source changed: '+str(path))
            with path.open() as stream:
                for row in csv.DictReader(stream):
                    key=(row['task_id'],int(row['sample_index']))
                    if key in attempts:raise RuntimeError('Duplicate historical attempt')
                    attempts.add(key);existing.add(key[0])
        if len(existing)!=424 or set(manifest['all_problem_ids'])-existing!=expected:
            raise RuntimeError('Missing set is no longer exactly40 for '+model)
        if existing & expected:raise RuntimeError('Would repeat completed LoRA-alone problems')
    if any(p['source']!='lcb' or not 0<len(p['tests'])<=20 for p in problems.values()):
        raise RuntimeError('Expected saved LiveCodeBench tests')


def validate(rows, model, problems, adapter_hash=None):
    profile,_,repeat=SETTINGS[model];seen=set()
    expected=dict(policy='thinking_on',way='lora1',model_profile=profile,sample_index=0,
        seed=3407,max_new_tokens=8192,think_budget=None,stop_on_repeat=repeat)
    for row in rows:
        tid=row['task_id']
        if tid not in problems or tid in seen:raise RuntimeError('Unexpected or duplicate answer ID: '+tid)
        seen.add(tid)
        for k,v in expected.items():
            if row.get(k)!=v:raise RuntimeError('Wrong saved '+k)
        if adapter_hash and row.get('adapter_sha256')!=adapter_hash:raise RuntimeError('Adapter hash changed')
        if row['thinking_tokens']<0 or row['total_new_tokens']<row['thinking_tokens']:
            raise RuntimeError('Invalid token counts')
    return seen


def paths(out):
    a=Path(out)/'test-lora1-lcb.jsonl'
    return a,a.with_name(a.stem+'-graded.csv')


def configure(out, config):
    path=Path(out)/'run-config.json'
    if path.exists() and json.loads(path.read_text())!=config:
        raise RuntimeError('Run settings changed; preserve the existing run, do not mix revisions.')
    atomic_json(path,config)


def preflight(adapter, model):
    from peft import PeftConfig,get_peft_model
    from peft.import_utils import is_torchao_available
    from transformers import LlamaConfig,LlamaForCausalLM
    from safetensors import safe_open
    is_torchao_available()
    cfg=PeftConfig.from_pretrained(adapter)
    if cfg.base_model_name_or_path!=SETTINGS[model][1]:raise RuntimeError('Wrong adapter model')
    with safe_open(str(Path(adapter)/'adapter_model.safetensors'),framework='pt',device='cpu') as f:
        keys=f.keys()
        if not any('lora_A' in k for k in keys) or not any('lora_B' in k for k in keys):
            raise RuntimeError('Adapter has no A/B weights')
    tiny=LlamaForCausalLM(LlamaConfig(vocab_size=32,hidden_size=32,intermediate_size=64,
        num_hidden_layers=1,num_attention_heads=4,num_key_value_heads=2))
    checked=get_peft_model(tiny,cfg)
    if not any('lora_B' in n for n,_ in checked.named_parameters()):raise RuntimeError('Adapter injection failed')
    print(model+' CPU adapter-injection check passed; real weight mapping checked during model load.',flush=True)


def pending_chunks(problems, done, batch):
    if batch < 1:raise RuntimeError('Batch must be positive')
    ordered=sorted(problems.values(),key=lambda p:p['task_id'])
    random.Random(3407).shuffle(ordered)
    chunks=[ordered[:4]]+[ordered[i:i+batch] for i in range(4,len(ordered),batch)]
    return [[p for p in chunk if p['task_id'] not in done] for chunk in chunks]


def generate(args, problems):
    import models,prompts
    from gen_colab import load_model,add_adapter,generate_safe,generate as ordinary_generate
    profile_name,_,repeat=SETTINGS[args.model]
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    ah=digest(Path(args.adapter)/'adapter_model.safetensors')
    config=dict(model=args.model,way='lora1',seed=3407,samples=1,think_budget=None,
        max_new_tokens=8192,stop_on_repeat=repeat,adapter_sha256=ah,
        adapter_config_sha256=digest(Path(args.adapter)/'adapter_config.json'),
        problem_sha256=digest(args.problems),worker_sha256=digest(__file__),
        generator_sha256=digest(Path(__file__).with_name('gen_colab.py')),
        prompts_sha256=digest(Path(__file__).with_name('prompts.py')))
    configure(out,config)
    ans,_=paths(out);done=validate(read_answers(ans,True),args.model,problems,ah)
    if len(done)==40:
        print('All40 saved; skip GPU model load.',flush=True);return
    preflight(args.adapter,args.model)
    profile=models.get(profile_name);model,tok=load_model(profile)
    prompts.check_prompt_has_switch(tok,profile);model=add_adapter(model,args.adapter);model.eval()
    import torch,platform,importlib.metadata as metadata
    atomic_json(out/f'environment-{time.time_ns()}.json',dict(python=platform.python_version(),
        gpu=torch.cuda.get_device_name(),dtype=str(model.dtype),batch=args.batch,
        packages={n:metadata.version(n) for n in ('torch','transformers','peft','flash-linear-attention','causal-conv1d')}))
    # First4 measure execution speed; they are part of the40, not extra questions.
    for chunk in pending_chunks(problems,done,args.batch):
        if not chunk:continue
        texts=[prompts.make_prompt(tok,p['question'],'thinking_on') for p in chunk]
        start=time.monotonic()
        outputs,cuts=generate_safe(lambda t:ordinary_generate(model,tok,t,8192,profile,3407,repeat),texts)
        if len(outputs)!=len(chunk) or len(cuts)!=len(chunk):raise RuntimeError('Wrong batch length')
        seconds=time.monotonic()-start
        for p,raw,cut in zip(chunk,outputs,cuts):
            thinking,answer=prompts.split_thinking(tok,raw,'thinking_on',profile)
            row=dict(task_id=p['task_id'],policy='thinking_on',way='lora1',model_profile=profile_name,
                model_id=profile['hf_id'],sample_index=0,seed=3407,max_new_tokens=8192,
                think_budget=None,stop_on_repeat=repeat,adapter_sha256=ah,adapter=args.adapter,
                dataset='lcb',difficulty=p['difficulty'],dtype=str(model.dtype),
                thinking_tokens=thinking,total_new_tokens=prompts.n_tokens(tok,raw),hit_limit=bool(cut),
                raw_output=raw,answer_text=answer,batch_size=len(chunk),batch_seconds=round(seconds,3))
            validate([row],args.model,problems,ah)
            with ans.open('a') as f:
                f.write(json.dumps(row)+'\n');f.flush();os.fsync(f.fileno())
            done.add(p['task_id'])
        print(f'{args.model}: saved {len(done)}/40; batch {seconds:.1f}s. Remaining answers: {40-len(done)}.',flush=True)


def checked_grades(out, model, problems):
    ans,grades=paths(out);rows=read_answers(ans,True);validate(rows,model,problems)
    raw={r['task_id']:r for r in rows};graded=read_grades(grades,True);seen=set()
    for r in graded:
        tid=r['task_id']
        if tid not in raw or tid in seen or int(r['sample_index'])!=0:raise RuntimeError('Duplicate/orphan grade')
        if r['policy']!='thinking_on':raise RuntimeError('Wrong grade method')
        for k in ('thinking_tokens','total_new_tokens'):
            if float(r[k])!=raw[tid][k]:raise RuntimeError('Grade token mismatch')
        if (r['hit_limit']=='True')!=raw[tid]['hit_limit']:raise RuntimeError('Grade cap mismatch')
        seen.add(tid)
    return raw,graded


def grade(args, problems):
    from grade_lcb import run_one,extract_code
    import tempfile
    raw,graded=checked_grades(args.out,args.model,problems);done={r['task_id'] for r in graded}
    _,path=paths(args.out)
    with tempfile.TemporaryDirectory(prefix='missing40-grade-') as wd:
        for tid,row in raw.items():
            if tid in done:continue
            p=problems[tid];passed,why,_=run_one(extract_code(row['answer_text']),p,wd)
            new=not path.exists()
            with path.open('a',newline='') as f:
                w=csv.DictWriter(f,fieldnames=FIELDS)
                if new:w.writeheader()
                w.writerow(dict(policy='thinking_on',task_id=tid,sample_index=0,difficulty=p['difficulty'],
                    passed=passed,why_not=' '.join(str(why).splitlines()),thinking_tokens=row['thinking_tokens'],
                    total_new_tokens=row['total_new_tokens'],hit_limit=row['hit_limit']))
                f.flush();os.fsync(f.fileno())
            done.add(tid);print(f'{args.model}: graded {len(done)}/{len(raw)}',flush=True)


def report(args, problems):
    raw,graded=checked_grades(args.out,args.model,problems)
    passed=sum(r['passed']=='True' for r in graded)
    result=dict(model=args.model,method='lora1',generated=len(raw),coverage=len(graded),
        expected=40,passed=passed,accuracy=passed/len(graded) if graded else None,
        status='COMPLETE' if len(graded)==40 else 'PARTIAL' if raw else 'NO ANSWERS')
    status=Path(args.out)/'generation-status.json'
    state=json.loads(status.read_text()) if status.exists() else {}
    result['generation_status']=state
    if result['status']!='COMPLETE' and state.get('state')=='failed':result['status']='FAILED'
    atomic_json(Path(args.out)/'summary.json',result)
    text=f"# {args.model} LoRA-1 alone: missing40\n\nStatus: **{result['status']}**. Generated {len(raw)}/40; graded {len(graded)}/40.\n\n"
    if graded:text+=f"Subset accuracy: **{100*result['accuracy']:.1f}% ({passed}/{len(graded)})**.\n\n"
    if state.get('error'):text+='Execution failure: '+state['error']+'\n\n'
    text+='This is the extra40 subset, not a464-problem score. One attempt each.\nCombine with saved424 only after checking both result sets. Missing rows are not failures.\n'
    (Path(args.out)/'SUMMARY.md').write_text(text);print(text)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--phase',choices=['preflight','generate','grade','report','audit'],required=True)
    ap.add_argument('--model',choices=list(SETTINGS),required=True);ap.add_argument('--adapter')
    ap.add_argument('--problems',required=True);ap.add_argument('--manifest',required=True)
    ap.add_argument('--root',required=True);ap.add_argument('--out',required=True);ap.add_argument('--batch',type=int,default=32)
    args=ap.parse_args();manifest=json.loads(Path(args.manifest).read_text())
    manifest['problems_path']=args.problems
    items=json.loads(Path(args.problems).read_text())['problems'];problems={p['task_id']:p for p in items}
    if len(items)!=len(problems):raise RuntimeError('Duplicate problem IDs')
    check_inputs(args.root,manifest,problems)
    Path(args.out).mkdir(parents=True,exist_ok=True)
    if args.phase=='audit':print('Exact missing40 confirmed for both models; no existing LoRA-alone overlap.');return
    if args.phase=='preflight':preflight(args.adapter,args.model);return
    if args.phase=='generate':
        status=Path(args.out)/'generation-status.json';atomic_json(status,dict(state='running'))
        try:generate(args,problems)
        except BaseException as e:
            atomic_json(status,dict(state='failed',error=f'{type(e).__name__}: {e}'));raise
        atomic_json(status,dict(state='finished'))
    elif args.phase=='grade':grade(args,problems)
    else:report(args,problems)

if __name__=='__main__':main()
