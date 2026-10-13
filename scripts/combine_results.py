"""Rebuild the retrospective 464-problem analysis without model calls.

Reads explicit graded-result directories; emits coverage, per-problem metrics,
paired problem-bootstrap intervals and a provenance audit. Equal problem weights
avoid giving two-attempt runs twice the influence of one-attempt runs.
"""
import csv
import json
import random
import statistics as st
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results/combined'
SEED, BOOTSTRAPS = 3407, 2000
BASES = {'0.8b': 'results/0.8b/raw', '2b': 'results/2026-09-24-thesis-run',
         '4b': 'results/4b/raw'}
METRICS = ('accuracy', 'thinking_tokens', 'total_new_tokens', 'hit_limit')


def mean(values):
    return st.mean(values)


def interval(values):
    rng = random.Random(SEED)
    n = len(values)
    samples = sorted(mean(rng.choices(values, k=n)) for _ in range(BOOTSTRAPS))
    return [samples[49], samples[1949]]


def load_results():
    records, sources, union = {}, [], set()
    cohorts = defaultdict(set)
    for model, base in BASES.items():
        directories = [('original', base), ('extra', f'results/extra/{model}'),
                       ('more', f'results/more/{model}')]
        if model == '2b':
            directories += [('original', 'results/2b-limit512/raw'),
                            ('original', 'results/2b-limit2048/raw')]
        for cohort, folder in directories:
            for path in sorted((ROOT / folder).glob('test-*-graded.csv')):
                method = path.name.split('-')[1]
                if method == 'limit':
                    method = 'limit1024'
                rows = list(csv.DictReader(path.open()))
                ids = set()
                for row in rows:
                    expected = {'off': 'thinking_off', 'on': 'thinking_on',
                                'brief': 'brief'}.get(method)
                    if method.startswith('limit'):
                        expected = 'limit'
                    elif method.startswith('lora'):
                        expected = 'thinking_on'
                    # Brief files use the generator's canonical thinking_brief name.
                    if method == 'brief':
                        assert row['policy'] in ('brief', 'thinking_brief'), (path, row['policy'])
                    else:
                        assert row['policy'] == expected, (path, row['policy'], expected)
                    assert row['passed'] in ('True', 'False')
                    assert row['hit_limit'] in ('True', 'False')
                    task = row['task_id']
                    key = (model, method, task, int(row['sample_index']))
                    assert key not in records, f'Duplicate attempt: {key}'
                    records[key] = dict(accuracy=float(row['passed'] == 'True'),
                        thinking_tokens=float(row['thinking_tokens']),
                        total_new_tokens=float(row['total_new_tokens']),
                        hit_limit=float(row['hit_limit'] == 'True'),
                        difficulty=row['difficulty'], cohort=cohort,
                        source='HumanEval+' if task.startswith('HumanEval/') else 'LiveCodeBench')
                    assert records[key]['total_new_tokens'] >= records[key]['thinking_tokens'] >= 0
                    ids.add(task)
                sources.append(dict(model=model, method=method, cohort=cohort,
                    path=str(path.relative_to(ROOT)), problems=len(ids), attempts=len(rows),
                    passed=sum(r['passed'] == 'True' for r in rows),
                    original_accuracy=100*mean([r['passed'] == 'True' for r in rows])))
                cohorts[cohort].update(ids)
                union.update(ids)
    assert len(union) == 464, len(union)
    assert {c: len(ids) for c, ids in cohorts.items()} == {'original':234,'extra':40,'more':190}
    assert sum(map(len, cohorts.values())) == len(union), 'Overlapping collection lists'
    return records, sources, union


def aggregate(records):
    groups = defaultdict(list)
    for (model, method, task, sample), row in records.items():
        groups[model, method, task].append(row)
    per_problem, methods = [], defaultdict(dict)
    for (model, method, task), rows in sorted(groups.items()):
        assert len({(r['difficulty'], r['source'], r['cohort']) for r in rows}) == 1
        p = dict(model=model, method=method, task_id=task, attempts=len(rows),
                 difficulty=rows[0]['difficulty'], source=rows[0]['source'], cohort=rows[0]['cohort'])
        p.update({metric:mean([r[metric] for r in rows]) for metric in METRICS})
        per_problem.append(p)
        methods[model,method][task] = p
    summaries = []
    for (model, method), problems in sorted(methods.items()):
        ps = list(problems.values())
        summary = dict(model=model, method=method, coverage=len(ps), attempts=sum(p['attempts'] for p in ps))
        summary.update({m:mean([p[m] for p in ps]) for m in METRICS})
        summary['accuracy_ci'] = interval([p['accuracy'] for p in ps])
        summary['groups'] = []
        for source,difficulty in sorted({(p['source'],p['difficulty']) for p in ps}):
            selected = [p for p in ps if (p['source'],p['difficulty']) == (source,difficulty)]
            summary['groups'].append(dict(source=source,difficulty=difficulty,coverage=len(selected),
                accuracy=mean([p['accuracy'] for p in selected])))
        summaries.append(summary)
    return per_problem, methods, summaries


def comparisons(methods):
    results=[]
    for model, limit in [('0.8b','off'),('2b','limit1024'),('4b','limit2048')]:
        for other in ('on','lora1', 'off'):
            if other == limit:
                continue
            a,b = methods[model,limit],methods[model,other]
            ids=sorted(a.keys() & b.keys())
            delta=[a[t]['accuracy']-b[t]['accuracy'] for t in ids]
            results.append(dict(model=model, method=limit, reference=other, coverage=len(ids),
                accuracy=mean([a[t]['accuracy'] for t in ids]),
                reference_accuracy=mean([b[t]['accuracy'] for t in ids]),
                delta=mean(delta), delta_ci=interval(delta),
                total_tokens=mean([a[t]['total_new_tokens'] for t in ids]),
                reference_total_tokens=mean([b[t]['total_new_tokens'] for t in ids])))
    return results


def training_audit(test_ids):
    train_ids=set(json.loads((ROOT/'results/extra/old-train-ids.json').read_text()))
    files=[]
    for folder in ('results/mini', 'results/2026-09-24-thesis-run', 'results/0.8b/raw', 'results/4b/raw'):
        for path in sorted((ROOT/folder).glob('train*.jsonl')):
            rows=[json.loads(line) for line in path.read_text().splitlines() if line.strip()]
            ids={r['task_id'] for r in rows}
            train_ids.update(ids)
            files.append(dict(path=str(path.relative_to(ROOT)), unique_ids=len(ids)))
    overlap=sorted(train_ids & test_ids)
    assert not overlap, f'Training ID overlap: {overlap}'
    return dict(training_ids_checked=len(train_ids), exact_id_overlap=overlap, files=files,
        limitation='ID checks do not rule out paraphrases or pretraining contamination. Existing text-overlap exclusions are preserved.')


def write_csv(path, rows):
    with path.open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)


def main():
    records,sources,ids=load_results()
    per_problem,methods,summaries=aggregate(records)
    audit=training_audit(ids)
    # Reconcile familiar original headline counts, independently of combined weighting.
    for model,method,expected in [('2b','limit1024',233),('4b','limit2048',366),('0.8b','off',48)]:
        assert sum(s['passed'] for s in sources if (s['model'],s['method'],s['cohort']) == (model,method,'original')) == expected
    data=dict(total_problems=len(ids),seed=SEED,bootstrap_replicates=BOOTSTRAPS,
        weighting='Mean of each problem’s success fraction; missing problems omitted, never scored zero.',
        summaries=summaries, comparisons=comparisons(methods), sources=sources,
        audit=audit, problem_ids=sorted(ids))
    OUT.mkdir(exist_ok=True)
    (OUT/'results.json').write_text(json.dumps(data,indent=2)+'\n')
    write_csv(OUT/'per-problem.csv',per_problem)
    write_csv(OUT/'sources.csv',sources)
    print(f'Checked {len(ids)} unique problems, {len(records)} attempts, {len(sources)} input files.')
    print(f'Training IDs checked: {audit["training_ids_checked"]}; exact overlap: 0.')
    for s in summaries:
        print(s['model'],s['method'],s['coverage'],f'{100*s["accuracy"]:.1f}%')


if __name__ == '__main__':
    main()
