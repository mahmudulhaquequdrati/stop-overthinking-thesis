"""Recalculate full464 2B comparisons after filling LoRA-alone extra40.
No generation. First attempts and all-attempt problem means remain separate.
"""
import csv
import json
import statistics as st
from pathlib import Path
from compare_lora_limit import paired_interval
from combine_results import load_results,aggregate,interval
from run_lora_limit import digest
ROOT=Path(__file__).resolve().parents[1]

def main():
    records,sources,ids=load_results();_,methods,summaries=aggregate(records)
    first={name:{} for name in ('lora1','off','limit1024')};provenance=[]
    for source in sources:
        if source['model']!='2b' or source['method'] not in first:continue
        path=ROOT/source['path'];provenance.append(dict(path=source['path'],sha256=digest(path)))
        with path.open() as stream:
            for row in csv.DictReader(stream):
                if int(row['sample_index'])!=0:continue
                assert row['task_id'] not in first[source['method']]
                first[source['method']][row['task_id']]=dict(accuracy=float(row['passed']=='True'),total_new_tokens=float(row['total_new_tokens']))
    combo={}
    for tag in ('he','lcb'):
        path=ROOT/f'results/lora-limit-2b/completed-464/test-lora1-limit1024-{tag}-graded.csv'
        provenance.append(dict(path=str(path.relative_to(ROOT)),sha256=digest(path)))
        with path.open() as stream:
            for row in csv.DictReader(stream):
                assert row['task_id'] not in combo and int(row['sample_index'])==0
                combo[row['task_id']]=dict(accuracy=float(row['passed']=='True'),total_new_tokens=float(row['total_new_tokens']))
    first['lora1-limit1024']=combo
    assert all(set(rows)==ids for rows in first.values())
    all_attempt={name:methods['2b',name] for name in ('lora1','off','limit1024')}
    all_attempt['lora1-limit1024']=combo
    result=dict(coverage=464,retrospective=True,bootstrap_replicates=2000,seed=3407,sources=provenance)
    for label,ways in [('first_attempts',first),('all_attempts_equal_problem_weight',all_attempt)]:
        sums={name:dict(accuracy=st.mean(r['accuracy'] for r in rows.values()),
            accuracy_ci=interval([r['accuracy'] for r in rows.values()]),
            mean_total_tokens=st.mean(r['total_new_tokens'] for r in rows.values())) for name,rows in ways.items()}
        if label=='first_attempts':
            for name,rows in ways.items():sums[name]['passed']=int(sum(r['accuracy'] for r in rows.values()))
        comparisons=[]
        for a,b in [('lora1-limit1024','lora1'),('lora1-limit1024','off'),('lora1','off'),('lora1-limit1024','limit1024')]:
            delta=[ways[a][t]['accuracy']-ways[b][t]['accuracy'] for t in sorted(ids)]
            comparisons.append(dict(method=a,reference=b,shared_problems=464,delta=st.mean(delta),delta_ci=paired_interval(delta)))
        result[label]=dict(summaries=sums,comparisons=comparisons)
    out=ROOT/'results/lora-missing40/comparison-2b-464.json'
    out.write_text(json.dumps(result,indent=2)+'\n')
    for label in ('first_attempts','all_attempts_equal_problem_weight'):
        print(label)
        for name,s in result[label]['summaries'].items():print(name,s)
        for c in result[label]['comparisons']:print(c)
    return result

if __name__=='__main__':main()
