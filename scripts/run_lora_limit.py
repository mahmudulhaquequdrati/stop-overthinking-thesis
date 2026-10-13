"""Notebook 21 worker: one existing 2B LoRA, one 1,024-token limit.

Generate with the existing thesis functions, then grade in a separate process.
Raw answers and graded rows resume independently. No training is performed.
"""
import argparse
import csv
import hashlib
import json
import os
import random
import time
from pathlib import Path

MODEL = 'qwen35_2b'
WAY = 'lora1-limit1024'
FIELDS = ['policy','task_id','sample_index','difficulty','passed','why_not',
          'thinking_tokens','total_new_tokens','hit_limit']


def digest(path):
    h = hashlib.sha256()
    with open(path,'rb') as f:
        for part in iter(lambda:f.read(1024*1024),b''):
            h.update(part)
    return h.hexdigest()


def atomic_json(path, value):
    path=Path(path)
    tmp=path.with_suffix(path.suffix+'.tmp')
    with tmp.open('w') as f:
        json.dump(value,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)


def read_answers(path, repair_tail=False):
    """A disconnect can leave one incomplete final line; archive it before repair."""
    path=Path(path)
    if not path.exists():return []
    data=path.read_bytes();lines=data.splitlines(keepends=True);rows=[]
    offset=0
    for i,line in enumerate(lines):
        try:
            row=json.loads(line)
        except (ValueError,UnicodeDecodeError):
            if i!=len(lines)-1 or not repair_tail:
                raise RuntimeError(f'Invalid answer line {i+1}: {path}')
            backup=path.with_name(path.name+f'.interrupted-{time.time_ns()}')
            backup.write_bytes(data[offset:])
            with path.open('r+b') as f:
                f.truncate(offset);f.flush();os.fsync(f.fileno())
            print(f'Repaired incomplete final line; saved its bytes to {backup.name}',flush=True)
            break
        rows.append(row);offset+=len(line)
    if rows and path.stat().st_size and not path.read_bytes().endswith(b'\n'):
        with path.open('ab') as f:f.write(b'\n');f.flush();os.fsync(f.fileno())
    return rows


def read_grades(path, repair_tail=False):
    path=Path(path)
    if not path.exists():return []
    lines=path.read_text().splitlines(keepends=True)
    if not lines or next(csv.reader([lines[0]]))!=FIELDS:
        raise RuntimeError(f'Invalid grade header: {path}')
    rows=[];valid=lines[:1]
    for i,line in enumerate(lines[1:],1):
        cols=next(csv.reader([line]))
        good=len(cols)==len(FIELDS) and cols[4] in ('True','False') and cols[8] in ('True','False')
        if not good:
            if i!=len(lines)-1 or not repair_tail:
                raise RuntimeError(f'Invalid grade row {i+1}: {path}')
            path.with_name(path.name+f'.interrupted-{time.time_ns()}').write_text(line)
            path.write_text(''.join(valid));break
        rows.append(dict(zip(FIELDS,cols)));valid.append(line)
    if rows and not path.read_bytes().endswith(b'\n'):
        with path.open('ab') as f:f.write(b'\n');f.flush();os.fsync(f.fileno())
    return rows


def validate_answers(rows, problems, adapter_hash=None):
    seen=set()
    for r in rows:
        key=(r['task_id'],r['sample_index'])
        if key in seen:raise RuntimeError(f'Duplicate answer: {key}')
        seen.add(key)
        p=problems.get(r['task_id'])
        if not p:raise RuntimeError(f'Unexpected problem: {key}')
        cap=4096 if p['source']=='humaneval' else 8192
        expected={'sample_index':0,'seed':3407,'policy':'limit','way':WAY,
                  'model_profile':MODEL,'think_budget':1024,'max_new_tokens':cap}
        for k,v in expected.items():
            if r.get(k)!=v:raise RuntimeError(f'Wrong saved {k} for {key}: {r.get(k)}')
        if adapter_hash and r.get('adapter_sha256')!=adapter_hash:
            raise RuntimeError('Saved answer uses different adapter weights.')
        if '</think>' not in r['raw_output']:
            raise RuntimeError(f'Missing thinking end marker: {key}')
        # Marker tokenization can cause a tiny decoded-text count difference.
        if not 0<=r['thinking_tokens']<=1028:
            raise RuntimeError(f'Thinking exceeded the budget: {key}')
    return seen


def schedule(problems, batch):
    """First 16 span task types; their outputs count toward the full 464."""
    rng=random.Random(3407)
    groups={}
    for key in [('humaneval','easy'),('lcb','easy'),('lcb','medium')]:
        group=sorted([p for p in problems.values() if (p['source'],p['difficulty'])==key],key=lambda p:p['task_id'])
        rng.shuffle(group);groups[key]=group
    chunks=[]
    for key,n in [(('humaneval','easy'),8),(('lcb','easy'),4),(('lcb','medium'),4)]:
        group=groups[key];chunks.append(group[:n]);groups[key]=group[n:]
    rest_he=groups['humaneval','easy']
    rest_lcb=groups['lcb','easy']+groups['lcb','medium']
    for group in (rest_he,rest_lcb):
        chunks.extend(group[i:i+batch] for i in range(0,len(group),batch))
    return [c for c in chunks if c]


def ensure_run_config(out, config):
    """A failed zero-answer attempt can adopt a fix; existing samples cannot."""
    out=Path(out)
    path=out/'run-config.json'
    if path.exists() and json.loads(path.read_text())!=config:
        for tag in ('he','lcb'):
            ans=out/f'test-{WAY}-{tag}.jsonl'
            if read_answers(ans) or read_grades(ans.with_name(ans.stem+'-graded.csv')):
                raise RuntimeError('Saved run settings differ and answers/grades already exist. Do not mix revisions.')
        backup=out/f'run-config.previous-{time.time_ns()}.json'
        os.replace(path,backup)
        print('Previous attempt saved no answers. Archived its configuration before applying the fix.',flush=True)
    atomic_json(path,config)


def preflight(adapter):
    """Exercise PEFT adapter injection on a tiny CPU model, before 2B loading."""
    import torch
    from peft import PeftConfig,get_peft_model
    from peft.import_utils import is_torchao_available
    from transformers import LlamaConfig,LlamaForCausalLM
    from safetensors import safe_open
    # PEFT checks this optional backend even for ordinary Linear layers.
    is_torchao_available()
    cfg=PeftConfig.from_pretrained(adapter)
    if cfg.base_model_name_or_path!='unsloth/Qwen3.5-2B':
        raise RuntimeError('Adapter configuration is not for the expected 2B model.')
    with safe_open(str(Path(adapter)/'adapter_model.safetensors'),framework='pt',device='cpu') as weights:
        keys=weights.keys()
        if not keys or not any('lora_A' in k for k in keys) or not any('lora_B' in k for k in keys):
            raise RuntimeError('Adapter weight file has no LoRA A/B tensors.')
    tiny=LlamaForCausalLM(LlamaConfig(vocab_size=32,hidden_size=32,intermediate_size=64,
        num_hidden_layers=1,num_attention_heads=4,num_key_value_heads=2))
    checked=get_peft_model(tiny,cfg)
    if not any('lora_B' in name for name,_ in checked.named_parameters()):
        raise RuntimeError('PEFT did not inject the adapter in its CPU compatibility check.')
    del checked,tiny
    print(f'CPU LoRA compatibility check passed; {len(keys)} saved tensors. No 2B model download.',flush=True)


def generate(args, problems):
    import models,prompts
    from gen_colab import load_model,add_adapter,generate_safe,generate_with_budget
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    cfg=json.loads((Path(args.adapter)/'adapter_config.json').read_text())
    if cfg.get('base_model_name_or_path')!='unsloth/Qwen3.5-2B' or cfg.get('peft_type')!='LORA':
        raise RuntimeError('This is not the expected Qwen3.5-2B LoRA adapter.')
    weight_hash=digest(Path(args.adapter)/'adapter_model.safetensors')
    config=dict(way=WAY,model_profile=MODEL,seed=3407,samples=1,think_budget=1024,
        problem_sha256=digest(args.problems),adapter_sha256=weight_hash,
        generator_sha256=digest(Path(__file__).with_name('gen_colab.py')),
        worker_sha256=digest(__file__),stop_on_repeat=False)
    ensure_run_config(out,config)
    done=set()
    for source in ('he','lcb'):
        done|=validate_answers(read_answers(out/f'test-{WAY}-{source}.jsonl',True),problems,weight_hash)
    if len(done)==len(problems):
        print('All answers already saved; no GPU model load needed.',flush=True);return
    preflight(args.adapter)
    profile=models.get(MODEL)
    model,tok=load_model(profile)
    prompts.check_prompt_has_switch(tok,profile)
    model=add_adapter(model,args.adapter)
    model.eval()
    import importlib.metadata as metadata,platform,torch
    env=dict(python=platform.python_version(),gpu=torch.cuda.get_device_name(),dtype=str(model.dtype),batch_requested=args.batch,
        packages={name:metadata.version(name) for name in ('torch','transformers','peft','flash-linear-attention','causal-conv1d')})
    atomic_json(out/f'environment-{time.time_ns()}.json',env)
    chunks=schedule(problems,args.batch)
    for chunk_index,full_chunk in enumerate(chunks):
        chunk=[p for p in full_chunk if (p['task_id'],0) not in done]
        if not chunk:continue
        source=chunk[0]['source'];cap=4096 if source=='humaneval' else 8192
        texts=[prompts.make_prompt(tok,p['question'],'limit') for p in chunk]
        t0=time.monotonic()
        outputs,cuts=generate_safe(lambda t:generate_with_budget(model,tok,t,1024,cap,profile,3407,False),texts)
        if len(outputs)!=len(chunk) or len(cuts)!=len(chunk):raise RuntimeError('Wrong generation batch size')
        elapsed=time.monotonic()-t0
        source_tag='he' if source=='humaneval' else 'lcb'
        for p,raw,cut in zip(chunk,outputs,cuts):
            thinking,answer=prompts.split_thinking(tok,raw,'limit',profile)
            row=dict(task_id=p['task_id'],policy='limit',way=WAY,adapter=args.adapter,
                adapter_sha256=weight_hash,sample_index=0,seed=3407,model_id=profile['hf_id'],
                model_profile=MODEL,dataset=source,difficulty=p['difficulty'],dtype=str(model.dtype),
                max_new_tokens=cap,think_budget=1024,thinking_tokens=thinking,
                total_new_tokens=prompts.n_tokens(tok,raw),hit_limit=bool(cut),
                batch_size=len(chunk),batch_seconds=round(elapsed,3),raw_output=raw,answer_text=answer,
                timestamp=time.strftime('%Y-%m-%d %H:%M:%S'))
            validate_answers([row],problems,weight_hash)
            with (out/f'test-{WAY}-{source_tag}.jsonl').open('a') as f:
                f.write(json.dumps(row)+'\n');f.flush();os.fsync(f.fileno())
            done.add((p['task_id'],0))
        print(f'Saved {len(done)}/464 • {elapsed:.1f}s this batch',flush=True)
        if chunk_index==2:print('First 16 technical checks passed. Continuing; no accuracy gate.',flush=True)
    print('Generation complete: 464/464.',flush=True)


def grade(args, problems):
    from grade_plus import run_one as run_he
    from grade_humaneval import extract_code as extract_he
    from grade_lcb import run_one as run_lcb,extract_code as extract_lcb
    import tempfile
    out=Path(args.out)
    for tag in ('he','lcb'):
        ans=out/f'test-{WAY}-{tag}.jsonl';graded=ans.with_name(ans.stem+'-graded.csv')
        rows=read_answers(ans,True);validate_answers(rows,problems)
        raw={r['task_id']:r for r in rows}
        previous=read_grades(graded,True);seen=set()
        for r in previous:
            key=(r['task_id'],int(r['sample_index']))
            if key in seen or key[0] not in raw or key[1]!=0:raise RuntimeError('Duplicate or orphan grade')
            original=raw[key[0]]
            for k in ('thinking_tokens','total_new_tokens'):
                if float(r[k])!=original[k]:raise RuntimeError('Grade does not match saved answer')
            if r['policy']!='limit' or (r['hit_limit']=='True')!=original['hit_limit']:
                raise RuntimeError('Grade metadata differs from saved answer')
            seen.add(key)
        with tempfile.TemporaryDirectory(prefix='lora-limit-grade-') as wd:
            for row in rows:
                if (row['task_id'],0) in seen:continue
                p=problems[row['task_id']]
                if tag=='he':passed,why=run_he(extract_he(row['answer_text']),p,wd)
                else:passed,why,_=run_lcb(extract_lcb(row['answer_text']),p,wd)
                new=not graded.exists()
                with graded.open('a',newline='') as f:
                    w=csv.DictWriter(f,fieldnames=FIELDS)
                    if new:w.writeheader()
                    w.writerow(dict(policy='limit',task_id=row['task_id'],sample_index=0,
                        difficulty=p['difficulty'],passed=passed,why_not=' '.join(str(why).splitlines()),
                        thinking_tokens=row['thinking_tokens'],total_new_tokens=row['total_new_tokens'],hit_limit=row['hit_limit']))
                    f.flush();os.fsync(f.fileno())
                seen.add((row['task_id'],0))
                print(f'Graded {tag} {len(seen)}/{len(rows)}: {row["task_id"]} {"PASS" if passed else "FAIL"}',flush=True)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--phase',choices=['preflight','generate','grade'],required=True)
    ap.add_argument('--problems',required=True);ap.add_argument('--adapter')
    ap.add_argument('--out',required=True);ap.add_argument('--batch',type=int,default=32)
    args=ap.parse_args()
    if args.phase=='preflight':
        if not args.adapter:ap.error('--adapter is required for preflight')
        preflight(args.adapter)
        return
    problems_list=json.loads(Path(args.problems).read_text())['problems']
    problems={p['task_id']:p for p in problems_list}
    if len(problems_list)!=464 or len(problems)!=464:raise RuntimeError('Expected 464 unique problems')
    status=Path(args.out)/'generation-status.json'
    if args.phase=='generate':
        if not args.adapter:ap.error('--adapter is required for generation')
        status.parent.mkdir(parents=True,exist_ok=True)
        atomic_json(status,dict(state='running'))
        try:
            generate(args,problems)
        except BaseException as error:
            atomic_json(status,dict(state='failed',error=f'{type(error).__name__}: {error}'))
            raise
        atomic_json(status,dict(state='finished'))
    else:grade(args,problems)

if __name__=='__main__':main()
