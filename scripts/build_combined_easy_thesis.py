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
       **{f'limit{n}':f'Limit {n:,}' for n in (512,1024,2048,4096)},
       'lora1-off':'LoRA-1 + OFF', **{f'lora1-limit{n}':f'LoRA-1 + limit {n:,}' for n in (512,1024,2048)}}
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
for summary in D['summaries']:
    if summary['coverage']==464:
        full_rows.append([summary['model'].upper(),LABEL[summary['method']],pct(summary['accuracy']),
            ci(summary['accuracy_ci']),'464/464',summary['attempts']])
full_table=table(['Model','Way','Accuracy','95% interval','Coverage','Attempts'],full_rows)
all_table=table(['Model','Way','Accuracy','Coverage','Attempts'],[[s['model'].upper(),LABEL[s['method']],pct(s['accuracy']),f'{s["coverage"]}/464',s['attempts']] for s in D['summaries']])
paired_table=table(['Model','Way vs reference','Shared problems','Way accuracy','Reference accuracy','Gap (points)','95% gap interval'],[
    [c['model'].upper(),f'{LABEL[c["method"]]} vs {LABEL[c["reference"]]}',c['coverage'],pct(c['accuracy']),pct(c['reference_accuracy']),points(c['delta']),ci(c['delta_ci'],False)] for c in D['comparisons']])
lora_table=table(['Model','Free control','Shared problems','Free accuracy','LoRA-1 accuracy','Gap (points)','95% gap interval'],[
    [c['model'].upper(),LABEL[c['method']],c['coverage'],pct(c['accuracy']),pct(c['reference_accuracy']),points(c['delta']),ci(c['delta_ci'],False)] for c in D['comparisons'] if c['reference']=='lora1' and not c['method'].startswith('lora1-')])
token_table=table(['Model','Way','Coverage','Thinking tokens','All tokens','Hit output cap'],[
    [s['model'].upper(),LABEL[s['method']],f'{s["coverage"]}/464',f'{s["thinking_tokens"]:,.0f}',f'{s["total_new_tokens"]:,.0f}',pct(s['hit_limit'])]
    for s in D['summaries']])
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
            f'<text x="24" y="{height-12}" font-size="11">Source: saved graded runs, Sep–Oct 2026. Equal weight per problem; updated 14 Oct 2026.</text>', '</g></svg>']
    (E/'figures'/name).write_text('\n'.join(out)+'\n')
chart('combined-accuracy.svg','Accuracy across 464 unique problems','Model and way • only methods with complete coverage',[
    (f'{r[0]} · {r[1]}',float(r[2][:-1]),r[2]) for r in full_rows])
chart('combined-lora.svg','Free control versus LoRA-1','Each pair uses the same problems; pair coverage is shown',[
    row for c in D['comparisons'] if c['reference']=='lora1' and not c['method'].startswith('lora1-') for row in (
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
The 2B and 4B gaps have positive intervals. Both compare the same 464 problems.
These are retrospective, unadjusted comparisons, not proof of a universal winner.

## How to read the result

Each problem gets equal weight, whether it has one attempt or two.
For each problem, average its pass/fail results. Then average across problems.
2B and 4B LoRA-1 now cover 464/464 problems after the missing40 fill-in. Do not treat missing results as wrong answers.
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
The completed extensions generated new answers using existing LoRA-1 add-ons.
No new training was run. This document rebuild uses saved results only.
The Notebook 24 ledger records about 57.0 estimated Colab units for its five runs.
Recalculating the tables locally spends no Colab units.

## What changes between methods

- Thinking OFF: answer without thinking notes.
- Thinking ON: allow notes until the overall output cap.
- Thinking limit: end the notes at a fixed token budget, then generate the answer.
- Think briefly: ask for shorter notes in the prompt.
- LoRA-1 alone: use the trained add-on with thinking ON and no thinking limit.
- LoRA-1 + OFF: use that add-on with thinking notes switched off.
- LoRA-1 + limit: use that add-on and end thinking at the stated limit.
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
Raw results remain unchanged. The pre-update Markdown files are preserved in
[the dated archive](../archive/2026-10-14-before-complete-md-sync/markdown-originals.tar.gz).
The formal Markdown thesis now uses the same checked 464-problem results.

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

These are the best observed free controls among methods covering the full set.
The completed trained combinations are also included below.
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

## Selected free controls by problem group

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
Among the main free controls, thinking OFF uses the fewest output tokens on each size.
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
The 2B and 4B gaps have positive intervals, now using 464 shared problems.
No result proves that all LoRA training methods are ineffective.
The original LoRA-2 experiment remains a 234-problem finding.

## Limits of the combined study

- The analysis is retrospective. We combined runs after seeing their results.
- Attempt counts differ. Equal problem weights address weighting, not all measurement noise.
- 2B and 4B LoRA-1 now cover 464/464 problems after the missing40 fill-in. Some other methods cover still fewer.
- Only one model family and code tasks were tested. No hard contest problems or math.
- LiveCodeBench grading used up to 20 tests per problem.
- Exact training/test ID overlap is zero, but text similarity and pretraining exposure remain possible.
- Intervals are unadjusted for multiple comparisons and method selection.
- Token counts do not directly measure time, money, or energy.
- A hitting-the-cap flag is not the same as a detected loop.

## What to test next

All six planned LoRA combinations are now complete on 464 problems each.
The five Notebook 24 runs and earlier 2B limit run need no rerun.
LoRA + OFF did not consistently improve on OFF without training.
LoRA + limits improved on LoRA alone, but gains over the matching free limit
remain uncertain for 2B and 4B. See the completed comparison below.
Training on correct answers generated under a limit remains untested.
This documentation rebuild used saved results and no Colab units.
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

## Why did older LoRA reports show 424/464?

Those reports preceded the extra 40 fill-in. Both 2B and 4B LoRA-1 now cover 464/464.
Missing results are not failures. We compare LoRA with controls on shared IDs only.
The 0.8B LoRA-1 covers all 464. LoRA-2 covers 234.

## Does the free limit beat LoRA alone?

The selected free controls have higher observed scores on shared problems.
The 0.8B gap is uncertain. The 2B and 4B intervals are positive.
See [the paired results](05-results.md) for numbers and limits.

## Were all problems selected before the experiment?

No. This is a retrospective combined view of saved runs.
The original study was selected earlier; later collections extended it.
We retain this history in the methods, without making separate headline stories.

## Do the old loop percentages apply to 464 problems?

No. They apply to the original 234-problem 2B analysis.
We did not rerun loop detection for the combined set.

## Did the completed experiments use GPU budget?

Yes. Notebook 24 records about 57.0 estimated compute units, not hours.
This document rebuild only reads saved scores and uses no GPU budget.

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

2B and 4B LoRA-1 now cover all 464, after adding their exact extra 40 results.
Some limit settings and LoRA-2 also have incomplete coverage.
See [all method coverage](05-results.md) and [the source manifest](../results/combined/sources.csv).

Saved raw results retain their historical numbers. The dated Markdown archive
preserves the original thesis. Both current thesis versions use the combined results.
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
The completed LoRA + OFF and LoRA + limit results are included for all three sizes.

Start with [PAPER.md](PAPER.md) for a teacher-ready summary.
Read [FULL-THESIS.md](FULL-THESIS.md) for all chapters, including every benchmark table, or [00-one-page.md](00-one-page.md) for the short version.

- [Method](03-how-we-did-it.md): weighting, grading, and intervals.
- [Datasets](04-the-datasets.md): test and training counts.
- [Results](05-results.md): accuracy, tokens, coverage, and shared-problem comparisons.
- [Explanation](06-why-it-works.md): historical loop evidence, clearly scoped.
- [Limitations](07-advice-and-limits.md).
- [Questions](08-all-answers.md).
- [Collection history](09-extra-problems.md).
- [All counts](10-all-counts.md).
- [Words](WORDS.md).

The [formal Markdown thesis](../thesis/THESIS.md) uses the same updated results.
The original study text is preserved in the dated Markdown archive.
The [combined audit](../results/combined/README.md) is the source for this version.

Rebuild from the project root:

```sh
.venv/bin/python scripts/audit_lora_controls.py
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
# Completed combinations: keep the all-attempt and first-attempt views explicit.
C=json.loads((ROOT/'results/lora-controls/checked-results.json').read_text())
assert C['new_answers']==2320 and len(C['results'])==5
combinations=[(m,method) for m in MODELS for method in ('lora1-off',f'lora1-limit{512 if m=="0.8b" else 1024 if m=="2b" else 2048}')]
combo_rows=[]
first_rows=[]
first_groups=[]
first_methods={}
for m in MODELS:
    base=json.loads((ROOT/f'results/lora-controls-inputs/baselines-{m}.json').read_text())['methods']
    for method,by_id in base.items():
        assert len(by_id)==464
        first_methods[m,method]=by_id
    for size,method in combinations:
        if size!=m:continue
        folder=(ROOT/'results/lora-limit-2b/completed-464' if m=='2b' and method=='lora1-limit1024'
                else ROOT/f'results/lora-controls/completed-464/{m}/{method}')
        rows=[r for path in sorted(folder.glob('*-graded.csv')) for r in __import__('csv').DictReader(path.open())]
        assert len(rows)==464 and len({r['task_id'] for r in rows})==464
        first_methods[m,method]={r['task_id']:dict(passed=r['passed']=='True',
            thinking_tokens=float(r['thinking_tokens']),total_new_tokens=float(r['total_new_tokens'])) for r in rows}
        summary=S[m,method]
        passed=sum(r['passed']=='True' for r in rows)
        assert summary['accuracy']==passed/464
        combo_rows.append([m.upper(),LABEL[method],passed,'464/464',pct(summary['accuracy']),ci(summary['accuracy_ci']),f'{summary["total_new_tokens"]:,.0f}'])
    for (model,method),by_id in first_methods.items():
        if model!=m:continue
        passed=sum(r['passed'] for r in by_id.values())
        first_rows.append([m.upper(),LABEL[method],f'{passed}/464',pct(passed/464),f'{sum(r["total_new_tokens"] for r in by_id.values())/464:,.0f}'])
combo_table=table(['Model','Combination','Passed','Coverage','Accuracy','95% interval','Mean total tokens'],combo_rows)
first_table=table(['Model','Way','Passed / tested','First-attempt accuracy','Mean total tokens'],first_rows)
from combine_results import interval
first_pairs=[]
for m,method in combinations:
    a=first_methods[m,method]
    control='off' if method.endswith('-off') else method.split('-')[1]
    for ref in dict.fromkeys((control,'lora1','off')):
        b=first_methods[m,ref];ids=sorted(a)
        diffs=[float(a[t]['passed'])-float(b[t]['passed']) for t in ids]
        first_pairs.append([m.upper(),LABEL[method]+' vs '+LABEL[ref],464,
            points(sum(diffs)/464),ci(interval(diffs),False)])
# Directly answer whether switching LoRA thinking off beats its limited mode.
for m in MODELS:
    limit=f'lora1-limit{512 if m=="0.8b" else 1024 if m=="2b" else 2048}'
    a,b=first_methods[m,limit],first_methods[m,'lora1-off'];ids=sorted(a)
    diffs=[float(a[t]['passed'])-float(b[t]['passed']) for t in ids]
    first_pairs.append([m.upper(),LABEL[limit]+' vs LoRA-1 + OFF',464,points(sum(diffs)/464),ci(interval(diffs),False)])
first_pair_table=table(['Model','First-attempt comparison','Shared problems','Gap (points)','95% gap interval'],first_pairs)
# Every saved method is broken down by benchmark and difficulty, with its own denominator.
group_rows=[]
for summary in D['summaries']:
    groups=list(summary['groups'])
    lcb=[g for g in groups if g['source']=='LiveCodeBench']
    n=sum(g['coverage'] for g in lcb)
    if n:
        groups.insert(1,dict(source='LiveCodeBench',difficulty='all',coverage=n,
            accuracy=sum(g['coverage']*g['accuracy'] for g in lcb)/n))
    for g in groups:
        group_rows.append([summary['model'].upper(),LABEL[summary['method']],g['source'],g['difficulty'],g['coverage'],pct(g['accuracy'])])
all_group_table=table(['Model','Way','Benchmark','Difficulty','Problems tested','Accuracy (all attempts, equal problem weight)'],group_rows)
# The same benchmark split for the first-attempt view, including historical controls.
problem_info={p['task_id']:p for p in json.loads((ROOT/'results/lora-controls-inputs/problem-templates.json').read_text())['problems']}
for (m,method),by_id in first_methods.items():
    for source,difficulty in [('humaneval','easy'),('lcb','all'),('lcb','easy'),('lcb','medium')]:
        rows=[r for tid,r in by_id.items() if problem_info[tid]['source']==source and (difficulty=='all' or problem_info[tid]['difficulty']==difficulty)]
        n=len(rows);passed=sum(r['passed'] for r in rows)
        first_groups.append([m.upper(),LABEL[method],'HumanEval+' if source=='humaneval' else 'LiveCodeBench',difficulty,f'{passed}/{n}',pct(passed/n)])
first_group_table=table(['Model','Way','Benchmark','Difficulty','Passed / tested','First-attempt accuracy'],first_groups)
chart('lora-combinations.svg','Completed LoRA combinations: 464 problems each',
      'One attempt per problem; existing trained adapters; no new training',
      [(f'{m.upper()} · {LABEL[method]}',100*S[m,method]['accuracy'],pct(S[m,method]['accuracy'])) for m,method in combinations])
chart('first-attempt-controls.svg','Free controls and trained combinations',
      'First attempts only; 464 identical problems for every bar',
      [(f'{m.upper()} · {LABEL[method]}',100*sum(r['passed'] for r in by_id.values())/464,
        pct(sum(r['passed'] for r in by_id.values())/464)) for (m,method),by_id in first_methods.items()])
interpretation='''### What the completed tests show

- **0.8B:** LoRA + OFF passes 65/464 (14.0%); LoRA + limit 512 passes 67/464 (14.4%).
  OFF without LoRA passes 68/464 (14.7%). There is no clear gain over OFF.
  LoRA + limit improves on the matching free limit by 3.9 points, interval +0.6 to +7.1.
- **2B:** LoRA + OFF passes 165/464 (35.6%); LoRA + limit 1,024 passes 191/464 (41.2%).
  The limit combination beats LoRA + OFF by 5.6 points, interval +1.1 to +9.9.
  Its 2.6-point gain over limit alone remains uncertain, interval −1.5 to +6.7.
- **4B:** LoRA + OFF passes 300/464 (64.7%); LoRA + limit 2,048 passes 332/464 (71.6%).
  Limit alone passes 330/464 (71.1%). The two-pass gain is inconclusive,
  interval −3.0 to +3.7 points. The combination uses about 11.4% fewer output tokens.

These are same-problem, first-attempt comparisons with historical references.
Intervals are unadjusted for multiple comparisons. They are not proof of universal wins.
Shorter output does not directly establish lower GPU time, energy, or money.
'''
brief='''## Completed LoRA combinations — all three sizes

LoRA alone means **thinking ON, with no thinking-token limit**.
LoRA + OFF and LoRA + limit use the same saved trained add-on.
No new training was done for these six combinations.

'''+combo_table+'\n'+interpretation
put('00-one-page.md',(E/'00-one-page.md').read_text()+'\n'+brief)
put('05-results.md',(E/'05-results.md').read_text()+'''\n## Completed LoRA combinations

![Completed combinations](figures/lora-combinations.svg)

'''+combo_table+'''\n## Same 464 problems, first attempts only

![First-attempt controls and combinations](figures/first-attempt-controls.svg)

Older methods can have two attempts per problem. For this comparison we use
only their first saved attempts, matching the new runs' single attempt.
This explains 2B LoRA alone: **34.9% first attempts versus 34.4% all attempts**.
Likewise, 4B limit alone is **71.1% first attempts versus 71.9% all attempts**.
These are two calculations from the same saved results, not contradictory scores.

'''+first_table+'\n'+first_pair_table+'\n'+interpretation+'''\n## Every benchmark and difficulty: all available methods

Each row averages attempts within a problem, then gives every problem equal weight.
Denominators are shown. Incomplete methods must not be ranked against full coverage.

'''+all_group_table+'''\n## Every benchmark and difficulty: first attempts

Every method below has all 464 test IDs: 164 HumanEval+, 166 LiveCodeBench easy,
and 134 LiveCodeBench medium. Counts show successes, not coverage alone.

'''+first_group_table)
put('11-completed-lora-controls.md','''# Completed LoRA controls: evidence and conclusion

We are at RESULTS → ANALYSIS → CONCLUSION.
The question is whether an existing trained add-on helps when thinking is off or limited.
For example, a student can use the same learned skill with or without written planning.
We change the thinking setting, then measure passing tests and answer length.
The main reference is the same setting without the trained add-on.
A gain over normal thinking alone is not enough to establish a benefit from training.

## All six planned combinations are finished

Notebook 21 supplied 2B LoRA + limit 1,024.
Notebook 24 supplied the other five configurations, with 2,320 new answers.
Each configuration has one answer and one grade for each of the same 464 IDs.
Notebook 23 is superseded by Notebook 24; do not run both.

'''+combo_table+'\n'+interpretation+'''
## Settings and checks

The models are Qwen3.5-0.8B, Qwen3.5-2B, and Qwen3.5-4B.
Existing adapter weight hashes match the settings recorded alongside the raw outputs.
Sampling used seed 3407, temperature 0.6, top-p 0.95, and top-k 20.
The total output caps were 4,096 tokens for HumanEval+ and 8,192 for LiveCodeBench.
The limit is for thinking only. It does not cap the complete answer at 512/1,024/2,048.
Thinking OFF records zero thinking tokens.
Repeat stopping was enabled for 0.8B and 4B; 2B retained its original handling.
The saved environment records Python 3.13.15, PyTorch 2.9.1+cu128,
Transformers 5.18.0, PEFT 0.21.1, Flash Linear Attention 0.5.2,
and causal-conv1d 1.7.0. Model calculations used bfloat16 precision.
Notebook 24 requested batch size 128; generation could reduce batches if needed.
The full environment files and package list remain with each saved run.
The Notebook 24 ledger records an A100 80GB GPU and about 57.0 estimated units.
The earlier Notebook 21 ledger is separate; 57.0 is not the whole project's spend.
Actual billed units must be checked in Colab, not inferred as hours.

Checked: 464 unique IDs per configuration; no duplicate attempts; every answer graded;
no unexpected IDs; zero exact overlap with saved training IDs; grade/raw token agreement;
reference source hashes; generation settings; and recalculated problem-based intervals.
No new model generation, training, or generated-code execution was needed for this audit.
Grades were read from the saved benchmark runs, rather than re-executed in this update.

The new runs use historical references from earlier packages and batch layouts.
A matching seed does not guarantee identical random draws in different environments.
The combined analysis remains retrospective. It is not a new pre-registered evaluation.
We did not claim that the model never saw benchmark text during pretraining.

## Practical conclusion

OFF without training remains the simplest observed choice for 0.8B.
The 2B LoRA + limit combination has the highest observed full-set accuracy for 2B.
It has not established a reliable gain over the free 1,024-token limit.
The 4B combination nearly matches the free limit while generating fewer output tokens.
LoRA + OFF does not show a consistent accuracy benefit over OFF without training.
No new run is required to complete these six planned configurations.

## Reproduce without GPU spending

```sh
.venv/bin/python scripts/audit_lora_controls.py
python3 scripts/combine_results.py
python3 scripts/build_combined_easy_thesis.py
```

Read [checked results](../results/lora-controls/checked-results.json),
[raw archive and result note](../results/lora-controls/README.md), and
[all accuracy, benchmark and token tables](05-results.md).
''')
for name in ('03-how-we-did-it.md','04-the-datasets.md','06-why-it-works.md',
             '07-advice-and-limits.md','08-all-answers.md','09-extra-problems.md','10-all-counts.md','README.md','01-who-should-use-it.md'):
    put(name,(E/name).read_text()+'''\n## Completed LoRA controls

All six combinations are complete, with 464/464 results each.
0.8B: LoRA + OFF **14.0%**, LoRA + limit 512 **14.4%**.
2B: LoRA + OFF **35.6%**, LoRA + limit 1,024 **41.2%**.
4B: LoRA + OFF **64.7%**, LoRA + limit 2,048 **71.6%**.
These use one attempt per problem. Historical controls also have a labelled
first-attempt comparison; their all-attempt scores remain separate.
See [the completed analysis](11-completed-lora-controls.md) and [benchmark tables](05-results.md).
''')
# The motivation chapter preserves its original text across rebuilds.
t=(E/'02-the-problem.md').read_text()
if '## Latest completed extension' in t:
    t=t.split('## Latest completed extension')[0]
put('02-the-problem.md',t)

chapters=['00-one-page.md','10-all-counts.md','01-who-should-use-it.md','02-the-problem.md','03-how-we-did-it.md','04-the-datasets.md','05-results.md','06-why-it-works.md','07-advice-and-limits.md','08-all-answers.md','09-extra-problems.md','11-completed-lora-controls.md','WORDS.md']
put('FULL-THESIS.md','# Stop Overthinking, Keep Passing the Tests\n\nEasy-language thesis: retrospective combined analysis of **464 unique problems**.\nUpdated 14 October 2026 with all six completed LoRA combinations.\n\nRead in order: summary → counts → motivation → methods → datasets → results → analysis → limits → teacher questions → collection history → completed LoRA controls → glossary.\nAll benchmark, difficulty, token and comparison tables are included below.\n\n'+'\n\n---\n\n'.join((E/p).read_text() for p in chapters))
put('PAPER.md','# Stop Overthinking, Keep Passing the Tests\n\nTeacher and paper draft: **464 unique code problems**, with explicit method coverage.\n\n'+'\n\n---\n\n'.join((E/p).read_text() for p in ['00-one-page.md','03-how-we-did-it.md','04-the-datasets.md','05-results.md','06-why-it-works.md','07-advice-and-limits.md','11-completed-lora-controls.md']))
combined=f'''# Combined results: 464 unique problems

Retrospective presentation chosen 13 October 2026; results updated 14 October 2026. Equal weight per problem.
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
- [sources.csv](sources.csv): the {len(D["sources"])} exact input files and their original pass counts.
- [Easy thesis](../../easy-thesis/PAPER.md): reader-facing combined account.

Checked: 464 distinct IDs, disjoint collections, no duplicate method/problem/attempt rows,
and zero overlap with {D['audit']['training_ids_checked']} saved training-pool IDs.
Original headline pass counts are reconciled before output is written.
Text similarity and pretraining exposure are not ruled out by this ID check.
Intervals resample problems 2,000 times with seed 3407; they are unadjusted percentile intervals.
Partial coverage is not imputed. Never rank a subset score against a full-set score.
'''
(ROOT/'results/combined/README.md').write_text(combined + '\n## Completed combinations\n\n' + combo_table + '\n' + interpretation + '\nFull first-attempt and benchmark tables: [easy thesis](../../easy-thesis/05-results.md).\n')
print('Built easy-thesis chapters, PAPER.md, FULL-THESIS.md, seven SVG charts, and combined README.')
# Refresh the formal thesis and notices too, so a normal rebuild cannot leave them stale.
if (ROOT/'scripts/sync_thesis_markdown.py').exists() and (ROOT/'archive/2026-10-14-before-complete-md-sync/markdown-originals.tar.gz').exists():
    import subprocess
    import sys
    subprocess.run([sys.executable,str(ROOT/'scripts/sync_thesis_markdown.py')],cwd=ROOT,check=True)
