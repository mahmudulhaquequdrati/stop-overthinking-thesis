"""Offline checks for frozen IDs, resume exclusion, metadata, and honest reports."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
import run_lora_missing40 as w

ROOT=Path(__file__).resolve().parents[1]

class Missing40Tests(unittest.TestCase):
    def setUp(self):
        self.items=json.loads((ROOT/'results/extra/extra-lcb.json').read_text())['problems']
        self.problems={p['task_id']:p for p in self.items}
        self.manifest=json.loads((ROOT/'results/lora-missing40/plan-manifest.json').read_text())
        self.manifest['problems_path']=str(ROOT/'results/extra/extra-lcb.json')
    def row(self,tid,model='2b'):
        return dict(task_id=tid,policy='thinking_on',way='lora1',model_profile=w.SETTINGS[model][0],
            sample_index=0,seed=3407,max_new_tokens=8192,think_budget=None,
            stop_on_repeat=w.SETTINGS[model][2],adapter_sha256='known',thinking_tokens=10,
            total_new_tokens=20,hit_limit=False,raw_output='thinking</think>code',answer_text='code')
    def test_actual_missing40_audit(self):
        w.check_inputs(ROOT,self.manifest,self.problems)
    def test_changed_historical_source_rejected(self):
        m=copy.deepcopy(self.manifest);m['models']['2b']['sources'][0]['sha256']='wrong'
        with self.assertRaises(RuntimeError):w.check_inputs(ROOT,m,self.problems)
    def test_training_overlap_rejected(self):
        m=copy.deepcopy(self.manifest);m['training_ids']=[self.items[0]['task_id']]
        with self.assertRaises(RuntimeError):w.check_inputs(ROOT,m,self.problems)
    def test_resume_skips_exact_saved_answers(self):
        done=set(list(self.problems)[:13])
        chunks=w.pending_chunks(self.problems,done,16)
        remaining=[p['task_id'] for c in chunks for p in c]
        self.assertEqual(len(remaining),27);self.assertEqual(set(remaining),set(self.problems)-done)
        self.assertEqual(w.pending_chunks(self.problems,done,16),chunks)
        self.assertFalse(any(w.pending_chunks(self.problems,set(self.problems),16)))
    def test_method_repeat_setting_and_duplicates(self):
        tid=self.items[0]['task_id'];row=self.row(tid)
        self.assertEqual(w.validate([row],'2b',self.problems,'known'),{tid})
        with self.assertRaises(RuntimeError):w.validate([row,row],'2b',self.problems)
        with self.assertRaises(RuntimeError):w.validate([row],'4b',self.problems)
        row['think_budget']=1024
        with self.assertRaises(RuntimeError):w.validate([row],'2b',self.problems)
    def test_changed_settings_cannot_mix(self):
        with tempfile.TemporaryDirectory() as d:
            w.configure(d,{'seed':3407});w.configure(d,{'seed':3407})
            with self.assertRaises(RuntimeError):w.configure(d,{'seed':1})
    def test_zero_answer_failure_is_not_accuracy(self):
        with tempfile.TemporaryDirectory() as d:
            w.atomic_json(Path(d)/'generation-status.json',{'state':'failed','error':'adapter check failed'})
            w.report(SimpleNamespace(out=d,model='2b'),self.problems)
            s=json.loads((Path(d)/'summary.json').read_text())
            self.assertEqual(s['status'],'FAILED');self.assertIsNone(s['accuracy'])
    def test_orphan_grade_rejected(self):
        import csv
        with tempfile.TemporaryDirectory() as d:
            _,path=w.paths(d)
            with path.open('w') as f:
                writer=csv.DictWriter(f,fieldnames=w.FIELDS);writer.writeheader()
                writer.writerow(dict(policy='thinking_on',task_id=self.items[0]['task_id'],sample_index=0,
                    difficulty='easy',passed=True,why_not='',thinking_tokens=10,total_new_tokens=20,hit_limit=False))
            with self.assertRaises(RuntimeError):w.checked_grades(d,'2b',self.problems)
    def test_all_saved_skips_model_download(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/'out';out.mkdir();adapter=Path(d)/'adapter';adapter.mkdir()
            (adapter/'adapter_model.safetensors').write_bytes(b'fixture')
            (adapter/'adapter_config.json').write_text('{}')
            ans,_=w.paths(out)
            rows=[dict(self.row(tid),adapter_sha256=w.digest(adapter/'adapter_model.safetensors')) for tid in self.problems]
            ans.write_text(''.join(json.dumps(r)+'\n' for r in rows))
            args=SimpleNamespace(out=str(out),adapter=str(adapter),model='2b',batch=16,
                problems=str(ROOT/'results/extra/extra-lcb.json'))
            with patch('gen_colab.load_model') as load,patch.object(w,'preflight') as check:
                w.generate(args,self.problems)
                load.assert_not_called();check.assert_not_called()
            self.assertEqual(len(w.read_answers(ans)),40)
    def test_grade_resume_does_not_repeat_candidate(self):
        from unittest.mock import patch
        tid=self.items[0]['task_id']
        with tempfile.TemporaryDirectory() as d:
            ans,_=w.paths(d);ans.write_text(json.dumps(self.row(tid))+'\n')
            args=SimpleNamespace(out=d,model='2b')
            with patch('grade_lcb.run_one',return_value=(True,'',[])) as run:
                w.grade(args,self.problems);w.grade(args,self.problems)
                self.assertEqual(run.call_count,1)
            raw,grades=w.checked_grades(d,'2b',self.problems)
            self.assertEqual(len(grades),1)
    def test_notebook_syntax_and_budget_scope(self):
        n=json.loads((ROOT/'notebooks/22_lora1_missing40_2b_4b.ipynb').read_text())
        code='\n'.join(''.join(c['source']) for c in n['cells'] if c['cell_type']=='code')
        for c in n['cells']:
            if c['cell_type']=='code':compile(''.join(c['source']),'cell','exec')
        self.assertIn('UNIT_CAP = 20.0',code)
        self.assertIn('RUN_READY = False',code)
        self.assertIn('runtime.unassign()',code)
        self.assertNotIn('generate_with_budget',code)

if __name__=='__main__':unittest.main()
