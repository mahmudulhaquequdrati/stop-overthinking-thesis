"""Check completed Notebook 24 data and reproduce first-attempt comparisons.

Reads saved answers and grades only; never executes generated code or models.
"""
import csv
import hashlib
import json
import statistics as st
from pathlib import Path

import run_lora_controls as worker
from compare_lora_controls import paired_interval

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'results/lora-controls'
INPUTS = ROOT/'results/lora-controls-inputs'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    manifest = json.loads((INPUTS/'manifest.json').read_text())
    problems = {p['task_id']:p for p in json.loads((INPUTS/'problem-templates.json').read_text())['problems']}
    assert len(problems) == 464 and set(problems) == set(manifest['problem_ids'])
    assert not set(problems) & set(manifest['training_ids'])
    results = []
    for size,mode in [('0.8b','off'),('0.8b','limit'),('2b','off'),('4b','limit'),('4b','off')]:
        worker.select_model(size,mode)
        folder = OUT/'completed-464'/size/worker.WAY
        config = json.loads((folder/'run-config.json').read_text())
        archived = json.loads((folder/'summary.json').read_text())
        assert config['adapter_sha256'] == manifest['models'][size]['adapter_sha256']
        assert config['adapter_config_sha256'] == manifest['models'][size]['config_sha256']
        assert config['problem_sha256'] == 'b7a8a88e867a670f7022932a76d39eafc996225581bd61eb10bc1f5d90be1953'
        for key,path in [('worker_sha256','scripts/run_lora_controls.py'),
                         ('generator_sha256','scripts/gen_colab.py'),('prompts_sha256','scripts/prompts.py')]:
            assert config[key] == manifest['files'][path] == sha(ROOT/path)
        raw,grades = [],[]
        for tag,count in [('he',164),('lcb',300)]:
            path = folder/f'test-{worker.WAY}-{tag}.jsonl'
            rr = [json.loads(line) for line in path.read_text().splitlines()]
            gg = list(csv.DictReader(path.with_name(path.stem+'-graded.csv').open()))
            assert len(rr) == len(gg) == count
            raw.extend(rr); grades.extend(gg)
        assert len(worker.validate_answers(raw,problems,config['adapter_sha256'])) == 464
        by_id = {r['task_id']:r for r in raw}
        g = {r['task_id']:r for r in grades}
        assert len(g) == len(grades) == 464 and set(g) == set(problems)
        for tid,r in g.items():
            assert r['policy'] == config['policy'] and int(r['sample_index']) == 0
            assert r['passed'] in ('True','False')
            for key in ('thinking_tokens','total_new_tokens'):
                assert float(r[key]) == by_id[tid][key]
        baseline = json.loads((INPUTS/f'baselines-{size}.json').read_text())
        for source in baseline['sources']:
            assert sha(ROOT/source['path']) == source['sha256']
        comparisons = []
        for c in archived['comparisons']:
            b = baseline['methods'][c['reference']]
            assert set(b) == set(g)
            ids = sorted(g)
            delta = [int(g[t]['passed']=='True')-int(b[t]['passed']) for t in ids]
            assert st.mean(delta) == c['delta'] and paired_interval(delta) == c['delta_ci']
            comparisons.append(c)
        passed = sum(r['passed']=='True' for r in grades)
        assert archived['accuracy'] == passed/464 and archived['complete']
        groups = []
        for source,difficulty in [('humaneval','easy'),('lcb','easy'),('lcb','medium')]:
            selected = [r for t,r in g.items() if (problems[t]['source'],problems[t]['difficulty']) == (source,difficulty)]
            groups.append(dict(source=source,difficulty=difficulty,coverage=len(selected),
                passed=sum(r['passed']=='True' for r in selected)))
        results.append(dict(model=size,method=worker.WAY,coverage=464,attempts=464,passed=passed,
            accuracy=passed/464,comparisons=comparisons,groups=groups,config=config,
            total_tokens=st.mean(float(r['total_new_tokens']) for r in grades)))
    data = dict(total_problems=464,new_answers=2320,exact_training_id_overlap=[],
        sampling_unit='problem',bootstrap_replicates=2000,seed=3407,results=results,
        zip_sha256=sha(ROOT/'lora-controls-download.zip'),
        ledger=json.loads((OUT/'completed-464/compute-ledger-v2.json').read_text()))
    (OUT/'checked-results.json').write_text(json.dumps(data,indent=2)+'\n')
    print('Checked five configurations: 2,320 answers and grades, frozen IDs, source hashes, paired intervals.')


if __name__ == '__main__':
    main()
