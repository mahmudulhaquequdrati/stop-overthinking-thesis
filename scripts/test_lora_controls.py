"""Offline checks for the five new configurations and report/resume boundaries."""
import csv,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import run_lora_controls as w
import compare_lora_controls as c
ROOT=Path(__file__).resolve().parents[1]
RUNS=[('0.8b','off'),('0.8b','limit'),('2b','off'),('4b','limit'),('4b','off')]
class Controls(unittest.TestCase):
    def setUp(self):
        self.problems={p['task_id']:p for p in json.loads((ROOT/'results/lora-controls-inputs/problem-templates.json').read_text())['problems']}
    def row(self,tid):
        return dict(task_id=tid,sample_index=0,seed=3407,policy=w.POLICY,way=w.WAY,
            model_profile=w.MODEL,think_budget=w.THINK_BUDGET,stop_on_repeat=w.STOP_ON_REPEAT,
            max_new_tokens=4096 if self.problems[tid]['source']=='humaneval' else 8192,
            thinking_tokens=0 if w.POLICY=='thinking_off' else w.THINK_BUDGET,
            total_new_tokens=3000,raw_output='code' if w.POLICY=='thinking_off' else 'notes</think>code',
            hit_limit=False,adapter_sha256='known',answer_text='code')
    def test_all_five_settings(self):
        for size,mode in RUNS:
            w.select_model(size,mode);tid=next(iter(self.problems));r=self.row(tid)
            self.assertEqual(w.validate_answers([r],self.problems,'known'),{(tid,0)})
            self.assertEqual(w.STOP_ON_REPEAT,size!='2b')
            with self.assertRaises(RuntimeError):w.validate_answers([r,r],self.problems)
        with self.assertRaises(RuntimeError):w.select_model('2b','limit')
    def test_off_uses_ordinary_generation(self):
        for size in ['0.8b','2b','4b']:
            w.select_model(size,'off')
            with patch('gen_colab.generate_safe',side_effect=lambda fn,texts:fn(texts)),patch('gen_colab.generate',return_value=(['code'],[False])) as ordinary,patch('gen_colab.generate_with_budget') as limited:
                w.sample_outputs(None,None,['prompt'],4096,{})
                ordinary.assert_called_once();limited.assert_not_called()
                self.assertEqual(ordinary.call_args.args[3],4096)
    def test_limits_use_correct_budgets(self):
        for size,budget in [('0.8b',512),('4b',2048)]:
            w.select_model(size,'limit')
            with patch('gen_colab.generate_safe',side_effect=lambda fn,texts:fn(texts)),patch('gen_colab.generate') as ordinary,patch('gen_colab.generate_with_budget',return_value=(['notes</think>code'],[False])) as limited:
                w.sample_outputs(None,None,['prompt'],8192,{})
                ordinary.assert_not_called();self.assertEqual(limited.call_args.args[3],budget)
    def test_off_cannot_claim_thinking_tokens(self):
        w.select_model('2b','off');r=self.row(next(iter(self.problems)));r['thinking_tokens']=1
        with self.assertRaises(RuntimeError):w.validate_answers([r],self.problems)
    def test_changed_mode_cannot_mix_outputs(self):
        w.select_model('0.8b','limit');r=self.row(next(iter(self.problems)))
        w.select_model('0.8b','off')
        with self.assertRaises(RuntimeError):w.validate_answers([r],self.problems)
    def test_no_answer_report_has_no_accuracy(self):
        for size,mode in RUNS:
            w.select_model(size,mode);c.WAY=w.WAY
            with tempfile.TemporaryDirectory() as d:
                w.atomic_json(Path(d)/'generation-status.json',dict(state='failed',error='fixture'))
                result=c.summarize(d,ROOT/'results/lora-controls-inputs/problem-templates.json',ROOT/f'results/lora-controls-inputs/baselines-{size}.json',size,w.THINK_BUDGET,mode)
                self.assertEqual(result['status'],'FAILED');self.assertIsNone(result['accuracy'])
    def test_frozen_ids_and_baselines(self):
        m=json.loads((ROOT/'results/lora-controls-inputs/manifest.json').read_text())
        self.assertEqual(len(self.problems),464);self.assertEqual(set(self.problems),set(m['problem_ids']))
        self.assertFalse(set(self.problems)&set(m['training_ids']))
        for size in ['0.8b','2b','4b']:
            b=json.loads((ROOT/f'results/lora-controls-inputs/baselines-{size}.json').read_text())
            self.assertTrue(all(set(rows)==set(self.problems) for rows in b['methods'].values()))
    def test_schedule_no_duplicates(self):
        chunks=w.schedule(self.problems,64);ids=[p['task_id'] for chunk in chunks for p in chunk]
        self.assertEqual(len(ids),464);self.assertEqual(set(ids),set(self.problems))
    def test_notebook_syntax_scope(self):
        n=json.loads((ROOT/'notebooks/24_lora1_off_and_limits.ipynb').read_text())
        cells=[''.join(c['source']) for c in n['cells'] if c['cell_type']=='code']
        for source in cells:compile(source,'cell','exec')
        self.assertIn('for size,mode in RUNS:', '\n'.join(cells))
        self.assertIn('UNIT_CAP = min(resource_number', '\n'.join(cells))
        self.assertIn('runtime.unassign()', '\n'.join(cells))
if __name__=='__main__':unittest.main()
