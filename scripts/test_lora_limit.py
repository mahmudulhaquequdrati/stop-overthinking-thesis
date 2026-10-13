"""Offline regression checks for Notebook 21's resume and comparison behavior."""
import csv
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from run_lora_limit import FIELDS,WAY,read_answers,read_grades,schedule,validate_answers,ensure_run_config
from compare_lora_limit import summarize
from prepare_lora_limit_data import prepare,download


def problem(tid,source='humaneval',difficulty='easy'):
    return dict(task_id=tid,source=source,difficulty=difficulty)


def answer(tid,source='humaneval'):
    return dict(task_id=tid,sample_index=0,seed=3407,policy='limit',way=WAY,
        model_profile='qwen35_2b',think_budget=1024,max_new_tokens=4096 if source=='humaneval' else 8192,
        thinking_tokens=2,total_new_tokens=10,hit_limit=False,raw_output='notes</think>code',answer_text='code')


class ResumeTests(unittest.TestCase):
    def test_notebook_does_not_grade_after_zero_answer_failure(self):
        import sys,types
        notebook=Path(__file__).resolve().parents[1]/'notebooks/21_2b_lora1_limit1024.ipynb'
        cells=json.loads(notebook.read_text())['cells']
        gen=next(c['source'] for c in cells if c['cell_type']=='code' and c['source'].startswith('GENERATION_COMPLETE'))
        grading=next(c['source'] for c in cells if c['cell_type']=='code' and c['source'].startswith('GRADING_COMPLETE'))
        with tempfile.TemporaryDirectory() as wd:
            out=Path(wd);ps=out/'problems.json';base=out/'base.json'
            ps.write_text('{"problems":[]}');base.write_text('{"methods":{},"sources":[]}')
            calls=[]
            def command(cmd,tag,**kwargs):
                calls.append(tag)
                if tag=='generate':raise RuntimeError('TorchAO conflict')
                if tag=='compare':summarize(out,ps,base)
                return True
            fake_display=types.ModuleType('IPython.display')
            fake_display.display=lambda _:None;fake_display.Markdown=lambda value:value
            scope=dict(sys=sys,json=json,OUT=out,WORK=out,PROBLEMS=ps,BASELINES=base,ADAPTER=out,
                BATCH=64,WAY=WAY,GENERATION_RESERVE_UNITS=3,RESERVE_UNITS=1.5,run_process=command,
                PREFLIGHT_PASSED=True,PROBLEMS_READY=True)
            with patch.dict('sys.modules',{'IPython.display':fake_display}),patch('builtins.print'):
                exec(compile(gen,'generation-cell','exec'),scope)
                exec(compile(grading,'grading-cell','exec'),scope)
            self.assertEqual(calls,['generate','compare'])
            self.assertFalse(scope['GENERATION_COMPLETE'])
            self.assertFalse(scope['GRADING_COMPLETE'])
            self.assertEqual(json.loads((out/'summary.json').read_text())['status'],'FAILED')

    def test_zero_answer_failure_can_adopt_fixed_worker(self):
        with tempfile.TemporaryDirectory() as wd:
            out=Path(wd);path=out/'run-config.json'
            path.write_text(json.dumps({'worker_sha256':'failed-revision'}))
            with patch('builtins.print'):
                ensure_run_config(out,{'worker_sha256':'fixed-revision'})
            self.assertEqual(json.loads(path.read_text())['worker_sha256'],'fixed-revision')
            backup=list(out.glob('run-config.previous-*.json'))
            self.assertEqual(len(backup),1)
            self.assertEqual(json.loads(backup[0].read_text())['worker_sha256'],'failed-revision')

    def test_fixed_worker_cannot_mix_with_existing_answers(self):
        with tempfile.TemporaryDirectory() as wd:
            out=Path(wd);path=out/'run-config.json'
            path.write_text(json.dumps({'worker_sha256':'old'}))
            (out/f'test-{WAY}-he.jsonl').write_text(json.dumps(answer('a'))+'\n')
            with self.assertRaises(RuntimeError):ensure_run_config(out,{'worker_sha256':'new'})
            self.assertEqual(json.loads(path.read_text())['worker_sha256'],'old')

    def test_zero_answer_generation_failure_has_no_accuracy(self):
        with tempfile.TemporaryDirectory() as wd:
            out=Path(wd)
            (out/'problems.json').write_text('{"problems":[]}')
            (out/'base.json').write_text('{"methods":{},"sources":[]}')
            (out/'generation-status.json').write_text(json.dumps({'state':'failed','error':'TorchAO version conflict'}))
            with patch('builtins.print'):
                report=summarize(out,out/'problems.json',out/'base.json')
            self.assertEqual(report['status'],'FAILED')
            self.assertIsNone(report['accuracy'])
            self.assertEqual(report['generated'],0)
            self.assertIn('TorchAO version conflict',(out/'SUMMARY.md').read_text())
            self.assertNotIn('Only this new combination was generated',(out/'SUMMARY.md').read_text())

    def test_verified_problem_cache_needs_no_dataset_package(self):
        import hashlib
        with tempfile.TemporaryDirectory() as wd:
            root=Path(wd);cache=root/'cache';cache.mkdir()
            body=b'{"problems":[]}'
            (cache/'problems-464.json').write_bytes(body)
            (root/'manifest.json').write_text(json.dumps({'problem_sha256':hashlib.sha256(body).hexdigest()}))
            (root/'templates.json').write_text('{"problems":[]}')
            with patch.dict('sys.modules',{'datasets':None}),patch('builtins.print'):
                prepare(root/'manifest.json',root/'templates.json',cache,root/'out.json')
            self.assertEqual((root/'out.json').read_bytes(),body)

    def test_changed_download_does_not_replace_saved_source(self):
        import io
        with tempfile.TemporaryDirectory() as wd:
            path=Path(wd)/'data.json';path.write_bytes(b'original')
            with patch('urllib.request.urlopen',return_value=io.BytesIO(b'changed')):
                with self.assertRaises(RuntimeError):download('https://example.org/data',path,'wrong-hash')
            self.assertEqual(path.read_bytes(),b'original')
            self.assertFalse(path.with_suffix('.json.part').exists())

    def test_interrupted_final_answer_is_archived_and_repaired(self):
        with tempfile.TemporaryDirectory() as wd:
            p=Path(wd)/'answers.jsonl';row=answer('a')
            p.write_text(json.dumps(row)+'\n'+ '{"task_id":')
            self.assertEqual(read_answers(p,True),[row])
            self.assertTrue(list(Path(wd).glob('*.interrupted-*')))
            with p.open('a') as f:f.write(json.dumps(answer('b'))+'\n')
            self.assertEqual(len(read_answers(p)),2)

    def test_interior_corruption_is_not_discarded(self):
        with tempfile.TemporaryDirectory() as wd:
            p=Path(wd)/'answers.jsonl';p.write_text('bad\n'+json.dumps(answer('a'))+'\n')
            with self.assertRaises(RuntimeError):read_answers(p,True)

    def test_duplicate_or_changed_settings_rejected(self):
        ps={'a':problem('a')};row=answer('a')
        with self.assertRaises(RuntimeError):validate_answers([row,row],ps)
        row['think_budget']=512
        with self.assertRaises(RuntimeError):validate_answers([row],ps)

    def test_partial_grade_tail_is_repaired(self):
        with tempfile.TemporaryDirectory() as wd:
            p=Path(wd)/'grades.csv'
            p.write_text(','.join(FIELDS)+'\nlimit,a,0,easy,True,,2,10,False\nlimit,b,0')
            self.assertEqual(len(read_grades(p,True)),1)
            self.assertTrue(list(Path(wd).glob('*.interrupted-*')))

    def test_finished_final_answer_without_newline_can_resume(self):
        with tempfile.TemporaryDirectory() as wd:
            p=Path(wd)/'answers.jsonl';p.write_text(json.dumps(answer('a')))
            read_answers(p,True)
            with p.open('a') as f:f.write(json.dumps(answer('b'))+'\n')
            self.assertEqual(len(read_answers(p)),2)

    def test_every_scheduled_problem_occurs_once(self):
        ps={}
        for source,diff,n in [('humaneval','easy',164),('lcb','easy',166),('lcb','medium',134)]:
            for i in range(n):
                p=problem(f'{source}-{diff}-{i}',source,diff);ps[p['task_id']]=p
        chunks=schedule(ps,64)
        ids=[p['task_id'] for chunk in chunks for p in chunk]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertEqual(set(ids),set(ps))
        self.assertEqual(sum(map(len,chunks[:3])),16)
        self.assertTrue(all(len({p['source'] for p in chunk})==1 for chunk in chunks))

    def test_partial_comparison_uses_intersection_not_missing_failures(self):
        with tempfile.TemporaryDirectory() as wd:
            out=Path(wd);ps=out/'problems.json';base=out/'base.json'
            ps.write_text(json.dumps({'problems':[problem('a'),problem('b'),problem('c')]}))
            old={t:dict(passed=False,total_new_tokens=20) for t in ['a','b','c']}
            base.write_text(json.dumps({'methods':{'limit1024':old,'lora1':{'a':old['a']}},'sources':[]}))
            ans=out/f'test-{WAY}-he.jsonl';ans.write_text('\n'.join(json.dumps(answer(t)) for t in ['a','b'])+'\n')
            with ans.with_name(ans.stem+'-graded.csv').open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader()
                for t in ['a','b']:
                    w.writerow(dict(policy='limit',task_id=t,sample_index=0,difficulty='easy',passed=t=='a',
                        why_not='',thinking_tokens=2,total_new_tokens=10,hit_limit=False))
            with patch('builtins.print'):
                report=summarize(out,ps,base)
            self.assertFalse(report['complete']);self.assertEqual(report['coverage'],2)
            c={x['reference']:x for x in report['comparisons']}
            self.assertEqual(c['limit1024']['shared_problems'],2)
            self.assertEqual(c['limit1024']['accuracy'],0.5)
            self.assertEqual(c['lora1']['shared_problems'],1)
            self.assertEqual(c['lora1']['accuracy'],1)
            self.assertIn('PARTIAL', (out/'SUMMARY.md').read_text())

if __name__=='__main__':unittest.main()
