"""Render the easy thesis from the checked combined results (no GPU calls).

The input is results/combined/results.json. Outputs are readable Markdown and
SVG charts. Numbers share one source so chapters cannot drift apart.
"""
import html
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
E=ROOT/'easy-thesis'
D=json.loads((ROOT/'results/combined/results.json').read_text())
S={(s['model'],s['method']):s for s in D['summaries']}
LABEL={'off':'Thinking OFF','on':'Thinking ON','lora1':'LoRA-1','lora2':'LoRA-2','brief':'Think briefly',
       **{f'limit{n}':f'Limit {n:,}' for n in (512,1024,2048,4096)}}
MODELS=('0.8b','2b','4b')
BEST={'0.8b':'off','2b':'limit1024','4b':'limit2048'}
def pct(v):return f'{100*v:.1f}%'
def points(v):return f'{100*v:+.1f}'
def ci(v,percent=True):return '['+', '.join(pct(x) if percent else points(x) for x in v)+']'
def table(headers,rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','|'+'|'.join('---' for _ in headers)+'|']+['| '+' | '.join(map(str,r))+' |' for r in rows])+'\n'
def put(name,content): (E/name).write_text(content.strip()+'\n')
headline=' · '.join(f'**{m.upper()}: {LABEL[BEST[m]]} {pct(S[m,BEST[m]]["accuracy"])}**' for m in MODELS)
source='Source: [combined results](../results/combined/README.md), calculated from saved graded answers. No model was run again.'
coverage_note='Coverage means unique problems with results. A missing result is not counted as a failure. Only compare scores directly when they use the same problems.'
full_rows=[]
for m in MODELS:
    for method in ('off','on',BEST[m],'lora1'):
        if any(r[0]==m.upper() and r[1]==LABEL[method] for r in full_rows):continue
        s=S[m,method]
        if s['coverage']==464:
            full_rows.append([m.upper(),LABEL[method],pct(s['accuracy']),ci(s['accuracy_ci']),f'{s["coverage"]}/464',s['attempts']])
full_table=table(['Model','Way','Accuracy','95% interval','Coverage','Attempts'],full_rows)
all_table=table(['Model','Way','Accuracy','Coverage','Attempts'],[[s['model'].upper(),LABEL[s['method']],pct(s['accuracy']),f'{s["coverage"]}/464',s['attempts']] for s in D['summaries']])
paired_table=table(['Model','Way vs reference','Shared problems','Way accuracy','Reference accuracy','Gap (points)','95% gap interval'],[
    [c['model'].upper(),f'{LABEL[c["method"]]} vs {LABEL[c["reference"]]}',c['coverage'],pct(c['accuracy']),pct(c['reference_accuracy']),points(c['delta']),ci(c['delta_ci'],False)] for c in D['comparisons']])
lora_table=table(['Model','Free control','Shared problems','Free accuracy','LoRA-1 accuracy','Gap (points)','95% gap interval'],[
    [c['model'].upper(),LABEL[c['method']],c['coverage'],pct(c['accuracy']),pct(c['reference_accuracy']),points(c['delta']),ci(c['delta_ci'],False)] for c in D['comparisons'] if c['reference']=='lora1'])
token_table=table(['Model','Way','Coverage','Thinking tokens','All tokens','Hit output cap'],[
    [s['model'].upper(),LABEL[s['method']],f'{s["coverage"]}/464',f'{s["thinking_tokens"]:,.0f}',f'{s["total_new_tokens"]:,.0f}',pct(s['hit_limit'])]
    for s in D['summaries'] if s['method'] in ('off','on','lora1',BEST[s['model']])])
group_table=table(['Model','Way','Problem group','Coverage','Accuracy'],[
    [m.upper(),LABEL[BEST[m]],g['source']+' '+g['difficulty'],g['coverage'],pct(g['accuracy'])]
    for m in MODELS for g in S[m,BEST[m]]['groups']])

# Flat, labelled SVGs. Horizontal bars leave room for readable method labels.
def chart(name,title,subtitle,rows,max_value=100,unit='Accuracy (%)'):
    width,height=960,155+len(rows)*40
    left,span=260,530
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{html.escape(title)}">',
         '<rect width="100%" height="100%" fill="#fafaf7"/>',
         '<g font-family="Arial, sans-serif" fill="#202d32">',
         f'<text x="24" y="32" font-size="22" font-weight="bold">{html.escape(title)}</text>',
         f'<text x="24" y="56" font-size="13">{html.escape(subtitle)}</text>']
    for i,(label,value,detail) in enumerate(rows):
        y=83+i*40
        out += [f'<text x="24" y="{y+18}" font-size="14">{html.escape(label)}</text>',
                f'<rect x="{left}" y="{y}" width="{span*value/max_value:.2f}" height="25" fill="#286b70"/>',
                f'<text x="{left+span*value/max_value+8:.2f}" y="{y+18}" font-size="13">{html.escape(detail)}</text>']
    y=90+len(rows)*40
    for tick in range(5):
        val=tick*max_value/4
        out.append(f'<text x="{left+tick*span/4}" y="{y}" font-size="12">{val:,.0f}</text>')
    out += [f'<text x="{left}" y="{y+23}" font-size="13">{html.escape(unit)}</text>',
            f'<text x="24" y="{height-12}" font-size="11">Source: saved graded runs, Sep–Oct 2026. Equal weight per problem; analysis 13 Oct 2026.</text>', '</g></svg>']
    (E/'figures'/name).write_text('\n'.join(out)+'\n')
chart('combined-accuracy.svg','Accuracy across 464 unique problems','Model and way • only methods with complete coverage',[
    (f'{r[0]} · {r[1]}',float(r[2][:-1]),r[2]) for r in full_rows])
chart('combined-lora.svg','Free control versus LoRA-1','Each pair uses the same problems; pair coverage is shown',[
    row for c in D['comparisons'] if c['reference']=='lora1' for row in (
        (f'{c["model"].upper()} · {LABEL[c["method"]]}',100*c['accuracy'],f'{pct(c["accuracy"])} · n={c["coverage"]}'),
        (f'{c["model"].upper()} · LoRA-1',100*c['reference_accuracy'],f'{pct(c["reference_accuracy"])} · n={c["coverage"]}'))])
chart('combined-tokens.svg','Average total tokens per answer','Model and way • per-problem means • complete coverage',[
    (f'{m.upper()} · {LABEL[method]}',S[m,method]['total_new_tokens'],f'{S[m,method]["total_new_tokens"]:,.0f}')
    for m in MODELS for method in dict.fromkeys(('off','on',BEST[m]))],max_value=8000,unit='All generated tokens (thinking + answer)')
chart('counts.svg','464 unique test problems','Problem groups • training problems are excluded',[
    ('HumanEval+ easy',164,'164'),('LiveCodeBench easy',166,'166'),('LiveCodeBench medium',134,'134')],max_value=200,unit='Unique problems')
chart('best-free.svg','Best observed full-coverage free controls','464 problems per bar • not a claim about untested settings',[
    (f'{m.upper()} · {LABEL[BEST[m]]}',100*S[m,BEST[m]]['accuracy'],pct(S[m,BEST[m]]['accuracy'])) for m in MODELS])
# Retire the old cohort chart rather than leave an obsolete headline asset.
(E/'figures/more-190-ways.svg').unlink(missing_ok=True)

put('00-one-page.md',f'''# The thesis in one page

We studied **464 unique code problems** using three small Qwen3.5 models.
The question: does training the model to think shorter beat free thinking controls?
A *LoRA* is a small trained add-on. A *token* is a small piece of text.

{headline}

These are the best observed free controls with **464/464 coverage**.
“Free” means no additional training; generating answers still uses compute.

![Best full-coverage controls](figures/best-free.svg)

## What training added

{lora_table}

In the earlier all-attempt analysis, all three free controls score higher than LoRA-1 alone on shared problems.
The 0.8B interval crosses zero, so its small lead is uncertain.
The 2B lead has an interval only just above zero. The 4B lead is clearer.
These are retrospective, unadjusted comparisons, not proof of a universal winner.

## How to read the result

Each problem gets equal weight, whether it has one attempt or two.
For each problem, average its pass/fail results. Then average across problems.
2B and 4B LoRA-1 cover 424/464 problems. Do not treat missing results as wrong answers.
Earlier LoRA-2 and loop checks cover only 234 problems.

The combined view was chosen after the runs. It was not a single preselected exam.
Collection details stay in the methods note; the main story uses all 464 problems.

{source}
''')
put('01-who-should-use-it.md',f'''# Who should use this, and why

This study helps people choosing settings for small Python code models.
It covers Qwen3.5-0.8B, 2B, and 4B, run on a Colab GPU.
A GPU is the chip doing the model's calculations.

Imagine asking a student to plan a solution before writing code.
Some planning helps. Repeating the plan without finishing wastes time.
Our free controls either skip the notes or stop them at a fixed length.

## What to try first

{headline}

These scores use 464 problems each. Try the same controls on your own tasks.
No additional training is needed. Answer generation still costs compute.

![Accuracy and coverage](figures/combined-accuracy.svg)

## Cost matters too

Thinking OFF uses fewer total tokens than normal thinking on every tested size.
The limits on 2B and 4B also reduce total tokens relative to normal thinking.
See the exact counts and coverage in [the results](05-results.md).

We did not test larger models, hard contest problems, math, or privacy attacks.
Local deployment can keep prompts on your machine, but this is not a security evaluation.
A result on these benchmarks does not promise the same accuracy on your code.
''')
# Keep the original motivation and hypotheses, replacing only the obsolete study scope.
p=E/'02-the-problem.md'
t=p.read_text(); start=t.index('## 6. What we actually did')
t=t[:start]+'''## 6. What we actually did, in one line

We evaluated three Qwen3.5 sizes across **464 unique code problems**.
We compared free thinking controls with shortest-correct LoRA training.
Coverage differs by method, so trained models are compared on shared problems.
The combined analysis is retrospective; the original hypotheses applied to LoRA-2's 234-problem experiment.

The method is in [03-how-we-did-it.md](03-how-we-did-it.md).
The combined scores are in [05-results.md](05-results.md).
''';put(p.name,t)
put('03-how-we-did-it.md',f'''# How we did it

We combined saved graded results for **464 unique problems**.
No new answers were generated. No training was run.
This update spends no Colab units.

## What changes between methods

- Thinking OFF: answer without thinking notes.
- Thinking ON: allow notes until the overall output cap.
- Thinking limit: end the notes at a fixed token budget, then generate the answer.
- Think briefly: ask for shorter notes in the prompt.
- LoRA-1: use a small add-on trained on shortest correct answers.
- LoRA-2: use the original 2B study's larger training set; coverage is 234/464.

A token is a small piece of text. LoRA trains an add-on while keeping the base model fixed.
The reported limits refer to thinking tokens, not the whole answer.
The original output caps were 4,096 for HumanEval+ and 8,192 for LiveCodeBench.
The saved runs used temperature 0.6, top-p 0.95, and top-k 20.
Repeat stopping was used in the size extensions; 2B retained its original handling.
This is a summary of existing runs, not a newly standardized experiment.

## How accuracy is calculated

For each problem, count the share of its attempts that passed.
Then average those shares across covered problems.

```text
Problem A: 1 pass from 2 attempts → 0.5
Problem B: 1 pass from 1 attempt  → 1.0
Combined accuracy: (0.5 + 1.0) / 2 = 75%
```

Pooling the three attempts would give 66.7%. That would give A twice the weight.
Our combined score gives each problem equal weight.
We do not average rounded percentages from the old summaries.

{coverage_note}

## Tests and uncertainty

An answer passes when it passes every test actually used by the saved grader.
HumanEval+ used its extended tests. LiveCodeBench used up to 20 tests per problem.
Thus these results do not establish success on every available LiveCodeBench hidden test.
Generated code was checked in a separate process with time limits.
This update reads scores only; it does not execute generated code.

For a comparison, use the intersection of both methods' problem IDs.
Resample whole problems 2,000 times with seed 3407.
The reported 95% intervals are percentile bootstrap intervals.
Both methods remain paired on each sampled problem; attempts are not independent problems.
Intervals reflect variation across problems, not all training or generation randomness.
They are unadjusted for multiple comparisons and post-result method selection.

## A retrospective combined view

The 464 problems came from several runs with different attempt counts.
The original 234 were selected before their results; later collections added 40 and 190.
We chose to combine them on 13 October 2026, after seeing results.
This history matters for interpreting claims, but it does not prevent a labelled combined summary.
Raw files and the original formal thesis remain unchanged.

{source}
''')
# Retain the original training explanation and examples, with bounded claims.
old=(E/'04-the-datasets.md').read_text()
training=old[old.index('## The training set'):].split('## The overlap check')[0].split('## Overlap and limitations')[0].strip()
put('04-the-datasets.md',f'''# The datasets, and how we checked them

The combined study has **464 distinct test problems**.
Training problems are not part of this total.

![Problem counts](figures/counts.svg)

{table(['Dataset and difficulty','Problems'],[['HumanEval+ easy functions',164],['LiveCodeBench easy',166],['LiveCodeBench medium',134],['Total',464]])}

HumanEval+ asks for Python functions. LiveCodeBench includes contest programs and class methods.
There are no hard problems in this study.
We checked IDs across all collection lists and found no duplicate test problems.
The combined total is 164 function problems and 300 contest problems.

{training}

## Overlap and limitations

The combined audit compares all 464 test IDs with **{D['audit']['training_ids_checked']} saved training-pool IDs**.
Exact ID overlap is **zero**. It also checks IDs in saved training-answer and retained-example files.
The source list is in [the audit](../results/combined/results.json).
This update does not repeat a full text-similarity audit.
Different IDs can still hide related wording or equivalent tasks.

Earlier runs used function-name and 5-word text-overlap exclusions.
Those historical exclusions are preserved, not rewritten by this update.
We cannot prove the base model never saw these benchmarks during pretraining.
A problem's release date alone is not proof of unseen data.
''')
put('05-results.md',f'''# The combined results

**464 unique problems** form the main results view.
Accuracy gives each problem equal weight, using all its available attempts.

{headline}

These are the best observed controls among methods covering the full set.
A higher score on an incomplete subset does not establish a better method.

## Methods with complete coverage

![Combined accuracy](figures/combined-accuracy.svg)

{full_table}

## Training versus free controls on shared problems

![Matched LoRA comparison](figures/combined-lora.svg)

{lora_table}

The 0.8B free control's lead is uncertain: its interval includes zero.
The 2B interval is narrowly positive, and the 4B interval is positive.
These intervals are descriptive and unadjusted for selecting comparisons after results.
Do not describe these as universal or definitive wins.

## All available methods, with coverage

{coverage_note}

{all_table}

For example, 2B Limit 2,048 covers only 274 problems.
Its score cannot be ranked directly against Limit 1,024 on 464 problems.
LoRA-2 covers only its original 234 problems; it is not a full-study result.

## Paired comparisons

Positive gaps favor the first method. Every row uses identical shared problem IDs.

{paired_table}

## Tokens and output caps

A token is a small piece of text. These are averages of per-problem means.
All tokens include both thinking and the final answer.
“Hit output cap” comes from the saved flag; it is not a loop detector or the pass/fail rule.
Token counts describe output length, not measured GPU time.

![Combined token use](figures/combined-tokens.svg)

{token_table}

## Full-coverage recommended controls by problem group

{group_table}

Different difficulty mixes change the overall score. Report these groups alongside the headline.

## Earlier focused checks

LoRA-2's original 234-problem experiment reported a thinking-length ratio of x1.00
and 45.1% accuracy. These were not rerun on all 464 problems.
The earlier MBPP+ pilot used 100 separate test problems. It is excluded here.
Its 65% LoRA accuracy versus 50% thinking ON is an earlier transfer check, not a combined score.
Loop and longer-output checks retain their original coverage in [the explanation](06-why-it-works.md).

{source}
''')
put('06-why-it-works.md','''# What the results suggest

A thinking limit can interrupt repeated notes and leave room for code.
Thinking OFF avoids those notes altogether.
This is a plausible explanation for the combined results, not proof of one cause.

Imagine a student copying the same plan until the exam ends.
Stopping the notes can leave time to write an answer.
But it cannot supply a missing solution.

## Earlier loop analysis: 234 problems only

The original 2B run had 468 attempts per method.
Normal thinking hit the output cap on 190 attempts (40.6%).
Of those capped attempts, 69.5% met the study's loop rule.
LoRA-2 hit the cap on 192 attempts (41.0%).
Of those, 88.5% met the loop rule.
These are historical measurements, not estimates for all 464 problems.

![Original 234-problem loop analysis](../results/full-results/figures/fig3-cutoffs-and-loops.svg)

On HumanEval+, completed normal-thinking answers had a median of 672 thinking tokens.
This suggests unfinished repetitions contributed strongly to long output.
Training on finished correct answers did not explicitly teach recovery from loops.
That may explain its limited transfer, but does not prove such training can never help.

## Earlier LoRA-2 result: 234 problems only

The thinking-length ratio versus normal thinking was x1.00 [0.94, 1.06].
The original study did not find the hoped-for shortening.
This result must not be extended to all models or all 464 problems.
The original training and loop evidence remains in the formal thesis.

## What the combined analysis adds

The full-coverage 2B and 4B limits score higher than normal thinking and use fewer total tokens.
Thinking OFF is the cheapest of the main full-coverage controls on each size.
For exact numbers and paired intervals, see [the combined results](05-results.md).

LoRA-1 and LoRA-2 differ in training data and coverage.
A result for one is not a result for the other.
The best observed full-coverage controls also differ by model size.
Incomplete limit sweeps do not establish a globally optimal budget.

## Other historical checks

One “think briefly” wording conflicted with the code-only instruction in saved examples.
That does not show that every short-thinking prompt fails.
A longer-output retry changed both the available token room and the evaluated conditions.
Keep its original scope in [the formal analysis](../thesis/06-analysis.md).
Neither check is a newly calculated 464-problem result.
''')
put('07-advice-and-limits.md',f'''# Advice and limits

Try free thinking controls before paying for shortest-correct training.
For the complete 464-problem set, the best observed free controls are:

{headline}

“Best” here is limited to the methods with full coverage.
The partially tested limits cannot establish a better full-set score.

## What we can say about training

In the earlier all-attempt analysis, the selected free controls score higher than LoRA-1 alone on shared problems.
The small 0.8B difference remains uncertain.
The 2B gap has a narrowly positive interval; the 4B gap is clearer.
No result proves that all LoRA training methods are ineffective.
The original LoRA-2 experiment remains a 234-problem finding.

## Limits of the combined study

- The analysis is retrospective. We combined runs after seeing their results.
- Attempt counts differ. Equal problem weights address weighting, not all measurement noise.
- 2B and 4B LoRA-1 cover 424/464 problems. Some other methods cover still fewer.
- Only one model family and code tasks were tested. No hard contest problems or math.
- LiveCodeBench grading used up to 20 tests per problem.
- Exact training/test ID overlap is zero, but text similarity and pretraining exposure remain possible.
- Intervals are unadjusted for multiple comparisons and method selection.
- Token counts do not directly measure time, money, or energy.
- A hitting-the-cap flag is not the same as a detected loop.

## What to test next

A useful next question is whether LoRA plus the same thinking limit improves accuracy.
Another is whether training on correct answers generated under a limit helps.
Those experiments are not part of this update. No Colab units were spent.
Keep future training, development, and test problems separate.

## One recommendation

Start with the observed free control for your model size, then test it on your own tasks.
''')
put('08-all-answers.md',f'''# Questions a teacher may ask

## How many test problems?

**464 unique problems:** 164 HumanEval+ and 300 LiveCodeBench.
Training and the early pilot are excluded.

## What are the main scores?

{headline}

Each headline uses all 464 problems. These are full-coverage free controls.

## Why not add all correct answers and divide by all attempts?

Some problems have two attempts and others have one.
That would give the former twice the weight.
We average within each problem first, then across problems.

## Why does LoRA sometimes show 424/464?

2B and 4B LoRA-1 have no saved results on 40 test problems.
Missing results are not failures. We compare LoRA with controls on shared IDs only.
The 0.8B LoRA-1 covers all 464. LoRA-2 covers 234.

## Does the limit beat training?

The selected free controls have higher observed scores on shared problems.
The 0.8B gap is uncertain. The 2B interval is narrowly positive; the 4B interval is positive.
See [the paired results](05-results.md) for numbers and limits.

## Were all problems selected before the experiment?

No. This is a retrospective combined view of saved runs.
The original study was selected earlier; later collections extended it.
We retain this history in the methods, without making separate headline stories.

## Do the old loop percentages apply to 464 problems?

No. They apply to the original 234-problem 2B analysis.
We did not rerun loop detection for the combined set.

## Did this update use any GPU budget?

No. It reads graded CSV files and calculates statistics locally.

## Where can someone check the calculations?

[Per-problem values](../results/combined/per-problem.csv),
[source files and original counts](../results/combined/sources.csv), and
[the full audit](../results/combined/results.json).
''')
put('09-extra-problems.md','''# Collection history and coverage

The main easy-thesis view is now **464 unique problems**.
This page records where they came from; it is not a separate results story.

The original collection had 234 problems. Later collections added 40 and 190.
Their IDs are disjoint. The combined total contains 164 HumanEval+ and 300 LiveCodeBench problems.
The combined view was chosen on 13 October 2026, after results were available.
It should not be described as a single pre-registered test set.

0.8B used one attempt per problem. The main 2B and 4B runs used two attempts.
The 190-problem collection used one attempt. Some limit fill-ins also used one.
All available attempts contribute, but every problem has equal weight.

2B and 4B LoRA-1 each lack 40 results. Their coverage is 424/464.
Some limit settings and LoRA-2 also have incomplete coverage.
See [all method coverage](05-results.md) and [the source manifest](../results/combined/sources.csv).

Saved raw results and the formal thesis retain their historical numbers.
Those files document the original experiments. They are not the combined headline.
''')
put('10-all-counts.md',f'''# All problems and all available scores

**464 unique test problems** is the main count.
Training pools and the early pilot are excluded.

![Problem counts](figures/counts.svg)

{table(['Group','Unique problems'],[['HumanEval+ easy',164],['LiveCodeBench easy',166],['LiveCodeBench medium',134],['Test total',464]])}

LoRA-1's original training pool had 100 problems.
LoRA-2's pool had 280 problems; 157 retained examples were used for training.
These are training counts, not extra test problems. The pools must not be summed as disjoint sets.

## Every method with its actual coverage

{all_table}

{coverage_note}

The combined inputs contain **{sum(s['attempts'] for s in D['summaries']):,} saved attempts** across all methods and sizes.
That is not a count of independent test problems.

![Matched LoRA comparison](figures/combined-lora.svg)

{lora_table}

{source}
''')
put('README.md','''# Easy thesis — start here

This version presents **464 unique test problems** as one combined study view.
Accuracy gives every problem equal weight. Every method shows its actual coverage.

Start with [PAPER.md](PAPER.md) for a teacher-ready summary.
Read [FULL-THESIS.md](FULL-THESIS.md) for all chapters, or [00-one-page.md](00-one-page.md) for the short version.

- [Method](03-how-we-did-it.md): weighting, grading, and intervals.
- [Datasets](04-the-datasets.md): test and training counts.
- [Results](05-results.md): accuracy, tokens, coverage, and shared-problem comparisons.
- [Explanation](06-why-it-works.md): historical loop evidence, clearly scoped.
- [Limitations](07-advice-and-limits.md).
- [Questions](08-all-answers.md).
- [Collection history](09-extra-problems.md).
- [All counts](10-all-counts.md).
- [Words](WORDS.md).

The [formal thesis](../thesis/THESIS.md) preserves the original study.
Its historical scores differ from the retrospective combined analysis here.
The [combined audit](../results/combined/README.md) is the source for this version.

Rebuild from the project root:

```sh
python3 scripts/combine_results.py
python3 scripts/build_combined_easy_thesis.py
```

No model calls or Colab units are needed.
''')
# Correct definitions that previously implied pooled attempts or certainty.
words=(E/'WORDS.md').read_text()
words=words.replace('The share of answers that pass every test.', 'Average of each problem’s share of passing attempts.')
words=words.replace('49.8% minus 42.1% is +7.7 points.', '40% minus 30% is +10 points.')
words=words.replace('A range for the true gap. If the range does not include 0, we call the gap proven on this test.', 'An uncertainty interval from resampling problems; it does not prove a universal result.')
words=words.replace('The answer hit the token room before it finished. It counts as wrong.', 'The saved output reached its cap. The grader still determines whether extracted code passes.')
for key,definition in [('Coverage','How many unique problems have results for one method.'),('Retrospective','Chosen after the results were available.'),('Equal problem weight','Each problem contributes equally, even when attempt counts differ.'),('Paired comparison','Compare two methods on exactly the same problems.'),('Bootstrap','Repeat the calculation on resampled problems to estimate uncertainty.')]:
    if f'| {key} |' not in words:words+=f'| {key} | {definition} |\n'
put('WORDS.md',words)
# Keep the completed extension separate from historical all-attempt tables.
completed = json.loads((ROOT/'results/lora-limit-2b/completed-464/summary.json').read_text())
assert completed['complete'] and completed['coverage'] == completed['generated'] == 464
assert completed['attempts_per_problem'] == 1 and completed['accuracy'] == 191/464
assert completed['comparisons'][0]['reference'] == 'limit1024'
assert completed['comparisons'][0]['reference_accuracy'] == 179/464
extension = """## Completed extension: 2B LoRA-1 + limit 1,024

**41.2% accuracy — 191/464 passed. Coverage: 464/464, one attempt per problem.**
This uses Qwen3.5-2B and the existing LoRA-1 trained add-on.

On the same 464 first attempts, limit alone scores 38.6% (179/464).
The combination gains 2.6 points and uses 6.4% fewer total output tokens.
The 95% gap interval is −1.5 to +6.7 points. A reliable gain is not established.
On the 424 shared first attempts, the combination scores 43.9%, versus LoRA-1 alone at 38.0%.
That gain is 5.9 points, with an interval of +1.4 to +10.4.

Earlier tables use all attempts per problem; LoRA-1 alone is 37.4% under that rule.
Do not confuse that number with the 38.0% first-attempt reference.
The extension is retrospective, with historical references and unadjusted intervals.
It does not prove training universally beats free controls.

2B and 4B LoRA-1 alone still each miss the same extra 40 problems.
Only these two gaps are planned next: 80 new answers, no training or completed-run repeats.
Other partial methods retain their stated coverage.

Checked 14 October 2026. Source: [completed result](../results/lora-limit-2b/README.md).
Next: [missing-40 plan](../results/lora-missing40/PLAN.md).
"""
for name in ('00-one-page.md', '03-how-we-did-it.md', '05-results.md',
             '07-advice-and-limits.md', '08-all-answers.md', '09-extra-problems.md',
             '10-all-counts.md', 'README.md'):
    put(name, (E/name).read_text() + '\n' + extension)

for name in ('01-who-should-use-it.md', '02-the-problem.md', '04-the-datasets.md', '06-why-it-works.md'):
    put(name, (E/name).read_text() + "\n## Latest completed extension\n\n2B LoRA-1 + limit 1,024: **41.2% (191/464)**, one attempt per problem.\nThe +2.6-point gain over limit alone remains inconclusive.\nSee [the completed evidence](../results/lora-limit-2b/README.md) and [the missing-40 plan](../results/lora-missing40/PLAN.md).\n")

chapters=['00-one-page.md','10-all-counts.md','01-who-should-use-it.md','02-the-problem.md','03-how-we-did-it.md','04-the-datasets.md','05-results.md','06-why-it-works.md','07-advice-and-limits.md','08-all-answers.md','09-extra-problems.md','WORDS.md']
put('FULL-THESIS.md','# Stop Overthinking, Keep Passing the Tests\n\nEasy-language thesis: retrospective combined analysis of **464 unique problems**.\n\n'+'\n\n---\n\n'.join((E/p).read_text() for p in chapters))
put('PAPER.md','# Stop Overthinking, Keep Passing the Tests\n\nTeacher and paper draft: **464 unique code problems**, with explicit method coverage.\n\n'+'\n\n---\n\n'.join((E/p).read_text() for p in ['00-one-page.md','03-how-we-did-it.md','04-the-datasets.md','05-results.md','06-why-it-works.md','07-advice-and-limits.md']))
combined=f'''# Combined results: 464 unique problems

Retrospective analysis, 13 October 2026. Equal weight per problem.
Main complete-coverage controls: {headline}

{coverage_note}

{all_table}

## Shared-problem comparisons

{paired_table}

## Reproduce and audit

Run `python3 scripts/combine_results.py`, then `python3 scripts/build_combined_easy_thesis.py`.
No GPU calls are made. Original graded files remain unchanged.

- [results.json](results.json): full metrics, 95% intervals, problem IDs, and training ID audit.
- [per-problem.csv](per-problem.csv): success fractions and token means before averaging.
- [sources.csv](sources.csv): the 66 exact input files and their original pass counts.
- [Easy thesis](../../easy-thesis/PAPER.md): reader-facing combined account.

Checked: 464 distinct IDs, disjoint collections, no duplicate method/problem/attempt rows,
and zero overlap with {D['audit']['training_ids_checked']} saved training-pool IDs.
Original headline pass counts are reconciled before output is written.
Text similarity and pretraining exposure are not ruled out by this ID check.
Intervals resample problems 2,000 times with seed 3407; they are unadjusted percentile intervals.
Partial coverage is not imputed. Never rank a subset score against a full-set score.
'''
(ROOT/'results/combined/README.md').write_text(combined + '\n' + extension.replace('../results/lora-limit-2b/', '../lora-limit-2b/').replace('../results/lora-missing40/', '../lora-missing40/'))
print('Built easy-thesis chapters, PAPER.md, FULL-THESIS.md, five SVG charts, and combined README.')
