"""Offline regression checks for Notebook 21's resume and comparison behavior."""
import csv
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from run_lora_limit import FIELDS,WAY,read_answers,read_grades,schedule,validate_answers
from compare_lora_limit import summarize
from prepare_lora_limit_data import prepare,download


def problem(tid,source='humaneval',difficulty='easy'):
    return dict(task_id=tid,source=source,difficulty=difficulty)


def answer(tid,source='humaneval'):
    return dict(task_id=tid,sample_index=0,seed=3407,policy='limit',way=WAY,
        model_profile='qwen35_2b',think_budget=1024,max_new_tokens=4096 if source=='humaneval' else 8192,
        thinking_tokens=2,total_new_tokens=10,hit_limit=False,raw_output='notes</think>code',answer_text='code')


class ResumeTests(unittest.TestCase):
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
