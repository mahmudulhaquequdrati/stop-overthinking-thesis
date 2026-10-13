"""Compare Notebook 21 with saved first attempts, on shared problem IDs only."""
import argparse
import csv
import json
import random
import statistics as st
from pathlib import Path
from run_lora_limit import WAY,atomic_json,read_answers,read_grades,validate_answers


def paired_interval(differences, n_boot=2000):
    rng=random.Random(3407)
    values=sorted(st.mean(rng.choices(differences,k=len(differences))) for _ in range(n_boot))
    return [values[49],values[1949]]


def summarize(out, problems_path, baseline_path):
    out=Path(out)
    problems={p['task_id']:p for p in json.loads(Path(problems_path).read_text())['problems']}
    old=json.loads(Path(baseline_path).read_text())
    baseline=old['methods']
    current={};raw={}
    for tag in ('he','lcb'):
        ans=out/f'test-{WAY}-{tag}.jsonl'
        rows=read_answers(ans);validate_answers(rows,problems)
        for r in rows:
            if r['task_id'] in raw:raise RuntimeError('Duplicate raw answer')
            raw[r['task_id']]=r
        for r in read_grades(ans.with_name(ans.stem+'-graded.csv')):
            tid=r['task_id']
            if tid in current or int(r['sample_index'])!=0 or tid not in raw:
                raise RuntimeError('Duplicate or orphan graded row')
            for k in ('thinking_tokens','total_new_tokens'):
                if float(r[k])!=raw[tid][k]:raise RuntimeError('Grade token count differs from raw answer')
            current[tid]=dict(passed=r['passed']=='True',thinking_tokens=float(r['thinking_tokens']),
                total_new_tokens=float(r['total_new_tokens']),hit_limit=r['hit_limit']=='True')
    comparisons=[]
    for way,by_id in baseline.items():
        ids=sorted(current.keys()&by_id.keys())
        if not ids:continue
        delta=[float(current[t]['passed'])-float(by_id[t]['passed']) for t in ids]
        comparisons.append(dict(reference=way,shared_problems=len(ids),
            accuracy=st.mean(float(current[t]['passed']) for t in ids),
            reference_accuracy=st.mean(float(by_id[t]['passed']) for t in ids),
            delta=st.mean(delta),delta_ci=paired_interval(delta),
            total_tokens=st.mean(current[t]['total_new_tokens'] for t in ids),
            reference_total_tokens=st.mean(by_id[t]['total_new_tokens'] for t in ids)))
    status_path=out/'generation-status.json'
    generation_status=json.loads(status_path.read_text()) if status_path.exists() else {}
    status=('COMPLETE' if len(current)==464 else
            'FAILED' if generation_status.get('state')=='failed' else
            'NO ANSWERS' if not raw else 'PARTIAL')
    result=dict(way=WAY,coverage=len(current),generated=len(raw),total_problems=464,
        status=status,generation_status=generation_status,
        complete=len(current)==464,attempts_per_problem=1,comparisons=comparisons,
        accuracy=st.mean(float(r['passed']) for r in current.values()) if current else None,
        baseline_manifest=old['sources'])
    atomic_json(out/'summary.json',result)
    lines=['# 2B LoRA-1 + thinking limit 1,024','',
        f'Generated: **{len(raw)}/464**. Graded coverage: **{len(current)}/464**. One attempt per problem.','',
        'Status: **'+status+('' if result['complete'] else ' — no complete 464-problem score')+'**.','',
        'Only this combination is scheduled for generation. Reference results are saved first attempts.',
        'They are not the previous combined scores that used all available attempts.','',
        '| Reference | Shared problems | Combination | Reference | Gap (points) | 95% gap interval | Total tokens: combination / reference |',
        '|---|---|---|---|---|---|---|']
    for c in comparisons:
        lo,hi=c['delta_ci']
        lines.append(f'| {c["reference"]} | {c["shared_problems"]} | {100*c["accuracy"]:.1f}% | {100*c["reference_accuracy"]:.1f}% | {100*c["delta"]:+.1f} | [{100*lo:+.1f}, {100*hi:+.1f}] | {c["total_tokens"]:.0f} / {c["reference_total_tokens"]:.0f} |')
    if generation_status.get('error'):
        lines+=['','Generation failure: '+generation_status['error']]
    if not comparisons:lines+=['','No accuracy result exists yet. Zero generated answers is an execution failure/stop, not 0% accuracy.']
    lines+=['','## How to read this','',
        'The primary comparison is against **limit1024**, not normal thinking alone.',
        'A positive gap favors the combination. An interval crossing zero is inconclusive.',
        'Intervals resample shared problems 2,000 times with seed 3407. They are unadjusted.',
        'LoRA-1 without the limit covers at most 424 shared problems; missing results are not failures.',
        'Saved references are historical. Package versions and batch layouts can affect sampling.',
        'Matching the seed does not guarantee identical random draws across batches or environments.',
        'This is a retrospective extension, not a fresh held-out evaluation.',
        'Raw answers, adapter hash, run settings, and environment records stay beside this report.','']
    (out/'SUMMARY.md').write_text('\n'.join(lines))
    print('\n'.join(lines[:18]))
    return result


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True)
    ap.add_argument('--problems',required=True);ap.add_argument('--baselines',required=True)
    args=ap.parse_args();summarize(args.out,args.problems,args.baselines)

if __name__=='__main__':main()
