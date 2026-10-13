"""Notebook 21: load tests outside the notebook, then verify frozen contents.

Reuse a checked Drive cache. Otherwise load original tests from pinned HF
revisions and saved contest lists from a pinned GitHub commit.
"""
import argparse
import hashlib
import json
import os
import urllib.request
from pathlib import Path


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def download(url, dest, wanted):
    dest=Path(dest)
    if dest.exists() and sha(dest)==wanted:return dest
    temporary=dest.with_suffix(dest.suffix+'.part')
    request=urllib.request.Request(url,headers={'User-Agent':'thesis-notebook-21'})
    with urllib.request.urlopen(request,timeout=60) as response,temporary.open('wb') as f:
        while True:
            part=response.read(1024*1024)
            if not part:break
            f.write(part)
        f.flush();os.fsync(f.fileno())
    if sha(temporary)!=wanted:
        temporary.unlink()
        raise RuntimeError(f'Downloaded data differs from the frozen input: {dest.name}')
    os.replace(temporary,dest)
    return dest


def prepare(manifest_path, templates_path, cache, output):
    manifest=json.loads(Path(manifest_path).read_text())
    templates=json.loads(Path(templates_path).read_text())['problems']
    cache=Path(cache);cache.mkdir(parents=True,exist_ok=True)
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    cached=cache/'problems-464.json'
    if cached.exists() and sha(cached)==manifest['problem_sha256']:
        body=cached.read_bytes()
        output.write_bytes(body)
        print('Reused checked Drive problem set: 464 problems. No dataset download.',flush=True)
        return
    from datasets import load_dataset
    from huggingface_hub import hf_hub_download
    from lcb_data import _unpack
    plus={r['task_id']:r for r in load_dataset('evalplus/humanevalplus',
        revision=manifest['humanevalplus_revision'],split='test')}
    assert len(plus)==164
    original_ids=set(manifest['original_lcb_ids'])
    lcb_path=hf_hub_download('livecodebench/code_generation_lite','test6.jsonl',repo_type='dataset',
                             revision=manifest['livecodebench_revision'])
    original={}
    with open(lcb_path) as f:
        for line in f:
            row=json.loads(line);tid='lcb/'+row['question_id']
            if tid not in original_ids:continue
            tests=json.loads(row['public_test_cases'])+_unpack(row['private_test_cases'])
            original[tid]=[{'input':t['input'],'output':t['output']} for t in tests[:20]]
    if set(original)!=original_ids:raise RuntimeError('Original LiveCodeBench IDs are missing from the frozen release.')
    other={}
    for source in manifest['contest_files']:
        path=download(source['url'],cache/source['name'],source['sha256'])
        for p in json.loads(path.read_text())['problems']:
            if p['task_id'] in other:raise RuntimeError('Duplicate saved contest ID')
            other[p['task_id']]=p['tests']
    full=[]
    for template in templates:
        p=dict(template);tid=p['task_id']
        if p['source']=='humaneval':
            if p['entry_point']!=plus[tid]['entry_point']:raise RuntimeError('HumanEval function name changed')
            p['test_plus']=plus[tid]['test']
        else:
            p['tests']=original[tid] if tid in original_ids else other[tid]
        full.append(p)
    if len(full)!=464 or len({p['task_id'] for p in full})!=464:
        raise RuntimeError('Expected exactly 464 unique problems')
    body=json.dumps({'problems':full},sort_keys=True,separators=(',',':')).encode()
    if hashlib.sha256(body).hexdigest()!=manifest['problem_sha256']:
        raise RuntimeError('Questions/tests differ from the frozen 464-problem set. Stop before model generation.')
    temporary=cached.with_suffix('.tmp')
    with temporary.open('wb') as f:f.write(body);f.flush();os.fsync(f.fileno())
    os.replace(temporary,cached)
    output.write_bytes(body)
    print('Loaded and verified all 464 questions and tests; cached them on Drive.',flush=True)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--manifest',required=True)
    ap.add_argument('--templates',required=True);ap.add_argument('--cache',required=True);ap.add_argument('--out',required=True)
    args=ap.parse_args();prepare(args.manifest,args.templates,args.cache,args.out)

if __name__=='__main__':main()
