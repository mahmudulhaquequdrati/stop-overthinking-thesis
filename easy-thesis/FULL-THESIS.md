# Stop Overthinking, Keep Passing the Tests

<!-- CURRENT-STUDY:START -->

**Current study — 14 October 2026:** **464 unique test problems**.
Benchmarks: **164 HumanEval+**, **166 LiveCodeBench easy**, **134 LiveCodeBench medium**.
All six planned LoRA combinations are complete, one attempt per problem:

- **0.8B:** LoRA + OFF **14.0% (65/464)**; LoRA + limit 512 **14.4% (67/464)**.
- **2B:** LoRA + OFF **35.6% (165/464)**; LoRA + limit 1,024 **41.2% (191/464)**.
- **4B:** LoRA + OFF **64.7% (300/464)**; LoRA + limit 2,048 **71.6% (332/464)**.

LoRA alone means thinking ON without a thinking-token limit.
Older methods' all-attempt averages and first-attempt comparisons are labelled separately.
LoRA + OFF does not consistently improve on free OFF; the 2B/4B gains over free limits remain uncertain.

[Every method, benchmark, difficulty, token count and interval](../results/CURRENT-RESULTS.md) · [Full easy thesis](FULL-THESIS.md) · [Full formal Markdown thesis](../thesis/THESIS.md).

<!-- CURRENT-STUDY:END -->

Easy-language thesis: retrospective combined analysis of **464 unique problems**.
Updated 14 October 2026 with all six completed LoRA combinations.

Read in order: summary → counts → motivation → methods → datasets → results → analysis → limits → teacher questions → collection history → completed LoRA controls → glossary.
All benchmark, difficulty, token and comparison tables are included below.

# The thesis in one page

We studied **464 unique code problems** using three small Qwen3.5 models.
The question: does training the model to think shorter beat free thinking controls?
A *LoRA* is a small trained add-on. A *token* is a small piece of text.

**0.8B: Thinking OFF 14.7%** · **2B: Limit 1,024 38.6%** · **4B: Limit 2,048 71.9%**

These are the best observed free controls with **464/464 coverage**.
“Free” means no additional training; generating answers still uses compute.

![Best full-coverage controls](figures/best-free.svg)

## What training added

| Model | Free control | Shared problems | Free accuracy | LoRA-1 accuracy | Gap (points) | 95% gap interval |
|---|---|---|---|---|---|---|
| 0.8B | Thinking OFF | 464 | 14.7% | 12.3% | +2.4 | [-0.4, +5.2] |
| 2B | Limit 1,024 | 464 | 38.6% | 34.4% | +4.2 | [+0.8, +7.8] |
| 4B | Limit 2,048 | 464 | 71.9% | 56.8% | +15.1 | [+11.3, +19.0] |


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

Source: [combined results](../results/combined/README.md), calculated from saved graded answers. No model was run again.

## Completed LoRA combinations — all three sizes

LoRA alone means **thinking ON, with no thinking-token limit**.
LoRA + OFF and LoRA + limit use the same saved trained add-on.
No new training was done for these six combinations.

| Model | Combination | Passed | Coverage | Accuracy | 95% interval | Mean total tokens |
|---|---|---|---|---|---|---|
| 0.8B | LoRA-1 + OFF | 65 | 464/464 | 14.0% | [11.0%, 17.0%] | 1,278 |
| 0.8B | LoRA-1 + limit 512 | 67 | 464/464 | 14.4% | [11.2%, 17.5%] | 4,979 |
| 2B | LoRA-1 + OFF | 165 | 464/464 | 35.6% | [31.2%, 39.7%] | 1,445 |
| 2B | LoRA-1 + limit 1,024 | 191 | 464/464 | 41.2% | [36.6%, 45.7%] | 4,072 |
| 4B | LoRA-1 + OFF | 300 | 464/464 | 64.7% | [59.9%, 69.0%] | 882 |
| 4B | LoRA-1 + limit 2,048 | 332 | 464/464 | 71.6% | [67.5%, 75.6%] | 3,511 |

### What the completed tests show

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


---

# All problems and all available scores

**464 unique test problems** is the main count.
Training pools and the early pilot are excluded.

![Problem counts](figures/counts.svg)

| Group | Unique problems |
|---|---|
| HumanEval+ easy | 164 |
| LiveCodeBench easy | 166 |
| LiveCodeBench medium | 134 |
| Test total | 464 |


LoRA-1's original training pool had 100 problems.
LoRA-2's pool had 280 problems; 157 retained examples were used for training.
These are training counts, not extra test problems. The pools must not be summed as disjoint sets.

## Every method with its actual coverage

| Model | Way | Accuracy | Coverage | Attempts |
|---|---|---|---|---|
| 0.8B | Limit 1,024 | 11.3% | 274/464 | 274 |
| 0.8B | Limit 512 | 10.6% | 464/464 | 464 |
| 0.8B | LoRA-1 | 12.3% | 464/464 | 464 |
| 0.8B | LoRA-1 + limit 512 | 14.4% | 464/464 | 464 |
| 0.8B | LoRA-1 + OFF | 14.0% | 464/464 | 464 |
| 0.8B | Thinking OFF | 14.7% | 464/464 | 464 |
| 0.8B | Thinking ON | 4.1% | 464/464 | 464 |
| 2B | Think briefly | 6.4% | 274/464 | 548 |
| 2B | Limit 1,024 | 38.6% | 464/464 | 738 |
| 2B | Limit 2,048 | 40.9% | 274/464 | 274 |
| 2B | Limit 512 | 39.4% | 274/464 | 548 |
| 2B | LoRA-1 | 34.4% | 464/464 | 698 |
| 2B | LoRA-1 + limit 1,024 | 41.2% | 464/464 | 464 |
| 2B | LoRA-1 + OFF | 35.6% | 464/464 | 464 |
| 2B | LoRA-2 | 45.1% | 234/464 | 468 |
| 2B | Thinking OFF | 31.8% | 464/464 | 738 |
| 2B | Thinking ON | 26.8% | 464/464 | 738 |
| 4B | Limit 1,024 | 76.5% | 234/464 | 468 |
| 4B | Limit 2,048 | 71.9% | 464/464 | 738 |
| 4B | Limit 4,096 | 76.7% | 234/464 | 468 |
| 4B | Limit 512 | 75.4% | 234/464 | 468 |
| 4B | LoRA-1 | 56.8% | 464/464 | 698 |
| 4B | LoRA-1 + limit 2,048 | 71.6% | 464/464 | 464 |
| 4B | LoRA-1 + OFF | 64.7% | 464/464 | 464 |
| 4B | Thinking OFF | 66.5% | 464/464 | 738 |
| 4B | Thinking ON | 50.0% | 464/464 | 738 |


Coverage means unique problems with results. A missing result is not counted as a failure. Only compare scores directly when they use the same problems.

The combined inputs contain **13,980 saved attempts** across all methods and sizes.
That is not a count of independent test problems.

![Matched LoRA comparison](figures/combined-lora.svg)

| Model | Free control | Shared problems | Free accuracy | LoRA-1 accuracy | Gap (points) | 95% gap interval |
|---|---|---|---|---|---|---|
| 0.8B | Thinking OFF | 464 | 14.7% | 12.3% | +2.4 | [-0.4, +5.2] |
| 2B | Limit 1,024 | 464 | 38.6% | 34.4% | +4.2 | [+0.8, +7.8] |
| 4B | Limit 2,048 | 464 | 71.9% | 56.8% | +15.1 | [+11.3, +19.0] |


Source: [combined results](../results/combined/README.md), calculated from saved graded answers. No model was run again.

## Completed LoRA controls

All six combinations are complete, with 464/464 results each.
0.8B: LoRA + OFF **14.0%**, LoRA + limit 512 **14.4%**.
2B: LoRA + OFF **35.6%**, LoRA + limit 1,024 **41.2%**.
4B: LoRA + OFF **64.7%**, LoRA + limit 2,048 **71.6%**.
These use one attempt per problem. Historical controls also have a labelled
first-attempt comparison; their all-attempt scores remain separate.
See [the completed analysis](11-completed-lora-controls.md) and [benchmark tables](05-results.md).


---

# Who should use this, and why

This study helps people choosing settings for small Python code models.
It covers Qwen3.5-0.8B, 2B, and 4B, run on a Colab GPU.
A GPU is the chip doing the model's calculations.

Imagine asking a student to plan a solution before writing code.
Some planning helps. Repeating the plan without finishing wastes time.
Our free controls either skip the notes or stop them at a fixed length.

## What to try first

**0.8B: Thinking OFF 14.7%** · **2B: Limit 1,024 38.6%** · **4B: Limit 2,048 71.9%**

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

## Completed LoRA controls

All six combinations are complete, with 464/464 results each.
0.8B: LoRA + OFF **14.0%**, LoRA + limit 512 **14.4%**.
2B: LoRA + OFF **35.6%**, LoRA + limit 1,024 **41.2%**.
4B: LoRA + OFF **64.7%**, LoRA + limit 2,048 **71.6%**.
These use one attempt per problem. Historical controls also have a labelled
first-attempt comparison; their all-attempt scores remain separate.
See [the completed analysis](11-completed-lora-controls.md) and [benchmark tables](05-results.md).


---

# The problem, the gap, and the question

We are in this box:

```text
PROBLEM → GAP → QUESTION → HYPOTHESIS → EXPERIMENT → … → CONCLUSION
   ▲         ▲        ▲           ▲
  here     here     here        here
```

## 1. The problem

New code models "think" before they answer.
Thinking means they write notes to themselves, then the code.
Thinking can help.
It also costs tokens and time.
A *token* is a small piece of text, about three quarters of a word.

On a small model, those notes are often far longer than the code.
People call that overthinking.
Our later results show a sharper name: **getting stuck in a loop.**

Everyday picture: the student writes five pages for "2 + 2", then copies the same paragraph until the bell rings.

## 2. Two ways to fix it

```text
Question
   │
   ├─ Free ways (no training)
   │     1. Thinking OFF
   │     2. Stop thinking at a fixed length
   │     3. Ask in words: "think briefly"
   │
   └─ Training
         Teach a small add-on (a LoRA) using the model's own shortest correct answers
```

A *LoRA* is a small add-on.
The rest of the model stays frozen.
Free ways need no training.
Training needs GPU time and careful data.

## 3. The gap

Other papers have trained models to think shorter.
Other papers have tried a thinking switch or a length cap.
We did not find a study that did **both** on one small code model that has a real ON/OFF switch.
That comparison is the gap.
If a free switch is as good as training, training is not worth it.

## 4. The question

**On a small model with a thinking switch, is training it to think shorter better than the free options?**

## 5. What we expected

We wrote this down **before** the main run.

| Part | We needed | Plain meaning |
|---|---|---|
| H1 | Thinking length ≤ 0.75× normal thinking | It should get clearly shorter |
| H2 | Accuracy loss ≤ 3 points | It should not get much worse |
| H3 | Better than each free way | Training should beat OFF, the limit, and "think briefly" |

What would support it: shorter thinking, accuracy held, and a win over the free ways.
What would reject it: thinking not shorter, or a free way that scores higher.

## 6. What we actually did, in one line

We evaluated three Qwen3.5 sizes across **464 unique code problems**.
We compared free thinking controls with shortest-correct LoRA training.
Coverage differs by method, so trained models are compared on shared problems.
The combined analysis is retrospective; the original hypotheses applied to LoRA-2's 234-problem experiment.

The method is in [03-how-we-did-it.md](03-how-we-did-it.md).
The combined scores are in [05-results.md](05-results.md).


---

# How we did it

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

Coverage means unique problems with results. A missing result is not counted as a failure. Only compare scores directly when they use the same problems.

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

Source: [combined results](../results/combined/README.md), calculated from saved graded answers. No model was run again.

## Completed LoRA controls

All six combinations are complete, with 464/464 results each.
0.8B: LoRA + OFF **14.0%**, LoRA + limit 512 **14.4%**.
2B: LoRA + OFF **35.6%**, LoRA + limit 1,024 **41.2%**.
4B: LoRA + OFF **64.7%**, LoRA + limit 2,048 **71.6%**.
These use one attempt per problem. Historical controls also have a labelled
first-attempt comparison; their all-attempt scores remain separate.
See [the completed analysis](11-completed-lora-controls.md) and [benchmark tables](05-results.md).


---

# The datasets, and how we checked them

The combined study has **464 distinct test problems**.
Training problems are not part of this total.

![Problem counts](figures/counts.svg)

| Dataset and difficulty | Problems |
|---|---|
| HumanEval+ easy functions | 164 |
| LiveCodeBench easy | 166 |
| LiveCodeBench medium | 134 |
| Total | 464 |


HumanEval+ asks for Python functions. LiveCodeBench includes contest programs and class methods.
There are no hard problems in this study.
We checked IDs across all collection lists and found no duplicate test problems.
The combined total is 164 function problems and 300 contest problems.

## The training set

Training problems are **not** the test problems.
LoRA-1 used a pool of **100** easy functions.
LoRA-2 used the bigger pool below.

| Pool | Problems | Why this pool |
|---|---|---|
| MBPP+ | 200 | Easy Python functions with strong tests. The early test showed they work. |
| Older LiveCodeBench | 80 (40 easy + 40 medium) | Older contest training problems from release v1. Distinct IDs were checked against the combined test set; dates alone do not establish separation. |

```text
200 MBPP+  +  80 older LiveCodeBench  =  280 problems
        │
        ▼
4 thinking-ON tries each
        │
        ▼
keep the shortest correct answer
(never shorter than half the middle correct length)
        │
        ▼
157 training examples  →  LoRA-2
133 from MBPP+   +   24 from older LiveCodeBench
```

![Training data funnel](../results/full-results/figures/fig7-training-data-funnel.svg)

| | MBPP+ | Older LiveCodeBench |
|---|---|---|
| Problems | 200 | 80 |
| Answers (4 tries) | 800 | 320 |
| Correct answers | 357 (44.6%) | 44 (13.8%) |
| Kept examples | 133 | 24 |
| Middle thinking length of kept examples | 515 tokens | **4,709 tokens** |

The LiveCodeBench training examples were already long.
There was almost nothing short to learn there.
The kept length divided by the average correct length was **0.83** on MBPP+ and **0.99** on older LiveCodeBench.

LoRA-2 trained on those 157 examples for 3 passes.
That took about 6 minutes.
The loss fell from about 0.25 to about 0.16, so the add-on did learn the examples.
The later chapter explains why that still did not shorten test thinking.

## Overlap and limitations

The combined audit compares all 464 test IDs with **280 saved training-pool IDs**.
Exact ID overlap is **zero**. It also checks IDs in saved training-answer and retained-example files.
The source list is in [the audit](../results/combined/results.json).
This update does not repeat a full text-similarity audit.
Different IDs can still hide related wording or equivalent tasks.

Earlier runs used function-name and 5-word text-overlap exclusions.
Those historical exclusions are preserved, not rewritten by this update.
We cannot prove the base model never saw these benchmarks during pretraining.
A problem's release date alone is not proof of unseen data.

## Completed LoRA controls

All six combinations are complete, with 464/464 results each.
0.8B: LoRA + OFF **14.0%**, LoRA + limit 512 **14.4%**.
2B: LoRA + OFF **35.6%**, LoRA + limit 1,024 **41.2%**.
4B: LoRA + OFF **64.7%**, LoRA + limit 2,048 **71.6%**.
These use one attempt per problem. Historical controls also have a labelled
first-attempt comparison; their all-attempt scores remain separate.
See [the completed analysis](11-completed-lora-controls.md) and [benchmark tables](05-results.md).


---

# The combined results

**464 unique problems** form the main results view.
Accuracy gives each problem equal weight, using all its available attempts.

**0.8B: Thinking OFF 14.7%** · **2B: Limit 1,024 38.6%** · **4B: Limit 2,048 71.9%**

These are the best observed free controls among methods covering the full set.
The completed trained combinations are also included below.
A higher score on an incomplete subset does not establish a better method.

## Methods with complete coverage

![Combined accuracy](figures/combined-accuracy.svg)

| Model | Way | Accuracy | 95% interval | Coverage | Attempts |
|---|---|---|---|---|---|
| 0.8B | Limit 512 | 10.6% | [7.8%, 13.6%] | 464/464 | 464 |
| 0.8B | LoRA-1 | 12.3% | [9.3%, 15.3%] | 464/464 | 464 |
| 0.8B | LoRA-1 + limit 512 | 14.4% | [11.2%, 17.5%] | 464/464 | 464 |
| 0.8B | LoRA-1 + OFF | 14.0% | [11.0%, 17.0%] | 464/464 | 464 |
| 0.8B | Thinking OFF | 14.7% | [11.6%, 17.9%] | 464/464 | 464 |
| 0.8B | Thinking ON | 4.1% | [2.4%, 6.0%] | 464/464 | 464 |
| 2B | Limit 1,024 | 38.6% | [34.4%, 42.8%] | 464/464 | 738 |
| 2B | LoRA-1 | 34.4% | [30.3%, 38.4%] | 464/464 | 698 |
| 2B | LoRA-1 + limit 1,024 | 41.2% | [36.6%, 45.7%] | 464/464 | 464 |
| 2B | LoRA-1 + OFF | 35.6% | [31.2%, 39.7%] | 464/464 | 464 |
| 2B | Thinking OFF | 31.8% | [27.7%, 36.0%] | 464/464 | 738 |
| 2B | Thinking ON | 26.8% | [23.2%, 30.6%] | 464/464 | 738 |
| 4B | Limit 2,048 | 71.9% | [67.9%, 75.6%] | 464/464 | 738 |
| 4B | LoRA-1 | 56.8% | [52.5%, 61.0%] | 464/464 | 698 |
| 4B | LoRA-1 + limit 2,048 | 71.6% | [67.5%, 75.6%] | 464/464 | 464 |
| 4B | LoRA-1 + OFF | 64.7% | [59.9%, 69.0%] | 464/464 | 464 |
| 4B | Thinking OFF | 66.5% | [62.3%, 70.5%] | 464/464 | 738 |
| 4B | Thinking ON | 50.0% | [45.9%, 54.3%] | 464/464 | 738 |


## Training versus free controls on shared problems

![Matched LoRA comparison](figures/combined-lora.svg)

| Model | Free control | Shared problems | Free accuracy | LoRA-1 accuracy | Gap (points) | 95% gap interval |
|---|---|---|---|---|---|---|
| 0.8B | Thinking OFF | 464 | 14.7% | 12.3% | +2.4 | [-0.4, +5.2] |
| 2B | Limit 1,024 | 464 | 38.6% | 34.4% | +4.2 | [+0.8, +7.8] |
| 4B | Limit 2,048 | 464 | 71.9% | 56.8% | +15.1 | [+11.3, +19.0] |


The 0.8B free control's lead is uncertain: its interval includes zero.
The 2B interval is narrowly positive, and the 4B interval is positive.
These intervals are descriptive and unadjusted for selecting comparisons after results.
Do not describe these as universal or definitive wins.

## All available methods, with coverage

Coverage means unique problems with results. A missing result is not counted as a failure. Only compare scores directly when they use the same problems.

| Model | Way | Accuracy | Coverage | Attempts |
|---|---|---|---|---|
| 0.8B | Limit 1,024 | 11.3% | 274/464 | 274 |
| 0.8B | Limit 512 | 10.6% | 464/464 | 464 |
| 0.8B | LoRA-1 | 12.3% | 464/464 | 464 |
| 0.8B | LoRA-1 + limit 512 | 14.4% | 464/464 | 464 |
| 0.8B | LoRA-1 + OFF | 14.0% | 464/464 | 464 |
| 0.8B | Thinking OFF | 14.7% | 464/464 | 464 |
| 0.8B | Thinking ON | 4.1% | 464/464 | 464 |
| 2B | Think briefly | 6.4% | 274/464 | 548 |
| 2B | Limit 1,024 | 38.6% | 464/464 | 738 |
| 2B | Limit 2,048 | 40.9% | 274/464 | 274 |
| 2B | Limit 512 | 39.4% | 274/464 | 548 |
| 2B | LoRA-1 | 34.4% | 464/464 | 698 |
| 2B | LoRA-1 + limit 1,024 | 41.2% | 464/464 | 464 |
| 2B | LoRA-1 + OFF | 35.6% | 464/464 | 464 |
| 2B | LoRA-2 | 45.1% | 234/464 | 468 |
| 2B | Thinking OFF | 31.8% | 464/464 | 738 |
| 2B | Thinking ON | 26.8% | 464/464 | 738 |
| 4B | Limit 1,024 | 76.5% | 234/464 | 468 |
| 4B | Limit 2,048 | 71.9% | 464/464 | 738 |
| 4B | Limit 4,096 | 76.7% | 234/464 | 468 |
| 4B | Limit 512 | 75.4% | 234/464 | 468 |
| 4B | LoRA-1 | 56.8% | 464/464 | 698 |
| 4B | LoRA-1 + limit 2,048 | 71.6% | 464/464 | 464 |
| 4B | LoRA-1 + OFF | 64.7% | 464/464 | 464 |
| 4B | Thinking OFF | 66.5% | 464/464 | 738 |
| 4B | Thinking ON | 50.0% | 464/464 | 738 |


For example, 2B Limit 2,048 covers only 274 problems.
Its score cannot be ranked directly against Limit 1,024 on 464 problems.
LoRA-2 covers only its original 234 problems; it is not a full-study result.

## Paired comparisons

Positive gaps favor the first method. Every row uses identical shared problem IDs.

| Model | Way vs reference | Shared problems | Way accuracy | Reference accuracy | Gap (points) | 95% gap interval |
|---|---|---|---|---|---|---|
| 0.8B | Thinking OFF vs Thinking ON | 464 | 14.7% | 4.1% | +10.6 | [+7.5, +13.8] |
| 0.8B | Thinking OFF vs LoRA-1 | 464 | 14.7% | 12.3% | +2.4 | [-0.4, +5.2] |
| 2B | Limit 1,024 vs Thinking ON | 464 | 38.6% | 26.8% | +11.7 | [+8.5, +15.1] |
| 2B | Limit 1,024 vs LoRA-1 | 464 | 38.6% | 34.4% | +4.2 | [+0.8, +7.8] |
| 2B | Limit 1,024 vs Thinking OFF | 464 | 38.6% | 31.8% | +6.8 | [+3.2, +10.5] |
| 4B | Limit 2,048 vs Thinking ON | 464 | 71.9% | 50.0% | +21.9 | [+18.3, +25.5] |
| 4B | Limit 2,048 vs LoRA-1 | 464 | 71.9% | 56.8% | +15.1 | [+11.3, +19.0] |
| 4B | Limit 2,048 vs Thinking OFF | 464 | 71.9% | 66.5% | +5.4 | [+1.6, +9.1] |
| 0.8B | LoRA-1 + limit 512 vs Limit 512 | 464 | 14.4% | 10.6% | +3.9 | [+0.6, +7.1] |
| 0.8B | LoRA-1 + limit 512 vs LoRA-1 | 464 | 14.4% | 12.3% | +2.2 | [-0.4, +5.0] |
| 0.8B | LoRA-1 + limit 512 vs Thinking OFF | 464 | 14.4% | 14.7% | -0.2 | [-3.0, +3.0] |
| 0.8B | LoRA-1 + OFF vs Thinking OFF | 464 | 14.0% | 14.7% | -0.6 | [-3.2, +2.2] |
| 0.8B | LoRA-1 + OFF vs LoRA-1 | 464 | 14.0% | 12.3% | +1.7 | [-0.9, +4.5] |
| 2B | LoRA-1 + limit 1,024 vs Limit 1,024 | 464 | 41.2% | 38.6% | +2.6 | [-1.4, +6.5] |
| 2B | LoRA-1 + limit 1,024 vs LoRA-1 | 464 | 41.2% | 34.4% | +6.8 | [+2.9, +10.7] |
| 2B | LoRA-1 + limit 1,024 vs Thinking OFF | 464 | 41.2% | 31.8% | +9.4 | [+5.4, +13.5] |
| 2B | LoRA-1 + OFF vs Thinking OFF | 464 | 35.6% | 31.8% | +3.8 | [+0.2, +7.3] |
| 2B | LoRA-1 + OFF vs LoRA-1 | 464 | 35.6% | 34.4% | +1.2 | [-2.6, +5.1] |
| 4B | LoRA-1 + limit 2,048 vs Limit 2,048 | 464 | 71.6% | 71.9% | -0.3 | [-3.7, +2.8] |
| 4B | LoRA-1 + limit 2,048 vs LoRA-1 | 464 | 71.6% | 56.8% | +14.8 | [+10.8, +19.0] |
| 4B | LoRA-1 + limit 2,048 vs Thinking OFF | 464 | 71.6% | 66.5% | +5.1 | [+0.9, +9.2] |
| 4B | LoRA-1 + OFF vs Thinking OFF | 464 | 64.7% | 66.5% | -1.8 | [-5.4, +1.6] |
| 4B | LoRA-1 + OFF vs LoRA-1 | 464 | 64.7% | 56.8% | +7.9 | [+3.6, +12.2] |


## Tokens and output caps

A token is a small piece of text. These are averages of per-problem means.
All tokens include both thinking and the final answer.
“Hit output cap” comes from the saved flag; it is not a loop detector or the pass/fail rule.
Token counts describe output length, not measured GPU time.

![Combined token use](figures/combined-tokens.svg)

| Model | Way | Coverage | Thinking tokens | All tokens | Hit output cap |
|---|---|---|---|---|---|
| 0.8B | Limit 1,024 | 274/464 | 975 | 4,794 | 72.3% |
| 0.8B | Limit 512 | 464/464 | 510 | 5,920 | 80.2% |
| 0.8B | LoRA-1 | 464/464 | 5,150 | 5,256 | 68.1% |
| 0.8B | LoRA-1 + limit 512 | 464/464 | 503 | 4,979 | 61.6% |
| 0.8B | LoRA-1 + OFF | 464/464 | 0 | 1,278 | 13.6% |
| 0.8B | Thinking OFF | 464/464 | 0 | 1,781 | 19.0% |
| 0.8B | Thinking ON | 464/464 | 6,147 | 6,206 | 86.4% |
| 2B | Think briefly | 274/464 | 5,484 | 5,507 | 92.3% |
| 2B | Limit 1,024 | 464/464 | 923 | 4,337 | 45.3% |
| 2B | Limit 2,048 | 274/464 | 1,453 | 1,978 | 37.6% |
| 2B | Limit 512 | 274/464 | 495 | 3,388 | 37.2% |
| 2B | LoRA-1 | 464/464 | 4,414 | 4,735 | 52.6% |
| 2B | LoRA-1 + limit 1,024 | 464/464 | 892 | 4,072 | 40.5% |
| 2B | LoRA-1 + OFF | 464/464 | 0 | 1,445 | 14.4% |
| 2B | LoRA-2 | 234/464 | 3,252 | 3,392 | 41.0% |
| 2B | Thinking OFF | 464/464 | 0 | 1,337 | 12.4% |
| 2B | Thinking ON | 464/464 | 5,169 | 5,331 | 60.6% |
| 4B | Limit 1,024 | 234/464 | 763 | 2,185 | 16.7% |
| 4B | Limit 2,048 | 464/464 | 1,603 | 3,921 | 29.2% |
| 4B | Limit 4,096 | 234/464 | 1,915 | 2,821 | 16.7% |
| 4B | Limit 512 | 234/464 | 481 | 2,168 | 17.1% |
| 4B | LoRA-1 | 464/464 | 4,661 | 4,797 | 38.5% |
| 4B | LoRA-1 + limit 2,048 | 464/464 | 1,512 | 3,511 | 23.1% |
| 4B | LoRA-1 + OFF | 464/464 | 0 | 882 | 5.6% |
| 4B | Thinking OFF | 464/464 | 0 | 943 | 5.3% |
| 4B | Thinking ON | 464/464 | 5,064 | 5,188 | 45.7% |


## Selected free controls by problem group

| Model | Way | Problem group | Coverage | Accuracy |
|---|---|---|---|---|
| 0.8B | Thinking OFF | HumanEval+ easy | 164 | 25.6% |
| 0.8B | Thinking OFF | LiveCodeBench easy | 166 | 15.7% |
| 0.8B | Thinking OFF | LiveCodeBench medium | 134 | 0.0% |
| 2B | Limit 1,024 | HumanEval+ easy | 164 | 60.4% |
| 2B | Limit 1,024 | LiveCodeBench easy | 166 | 43.4% |
| 2B | Limit 1,024 | LiveCodeBench medium | 134 | 6.0% |
| 4B | Limit 2,048 | HumanEval+ easy | 164 | 86.9% |
| 4B | Limit 2,048 | LiveCodeBench easy | 166 | 85.2% |
| 4B | Limit 2,048 | LiveCodeBench medium | 134 | 36.9% |


Different difficulty mixes change the overall score. Report these groups alongside the headline.

## Earlier focused checks

LoRA-2's original 234-problem experiment reported a thinking-length ratio of x1.00
and 45.1% accuracy. These were not rerun on all 464 problems.
The earlier MBPP+ pilot used 100 separate test problems. It is excluded here.
Its 65% LoRA accuracy versus 50% thinking ON is an earlier transfer check, not a combined score.
Loop and longer-output checks retain their original coverage in [the explanation](06-why-it-works.md).

Source: [combined results](../results/combined/README.md), calculated from saved graded answers. No model was run again.

## Completed LoRA combinations

![Completed combinations](figures/lora-combinations.svg)

| Model | Combination | Passed | Coverage | Accuracy | 95% interval | Mean total tokens |
|---|---|---|---|---|---|---|
| 0.8B | LoRA-1 + OFF | 65 | 464/464 | 14.0% | [11.0%, 17.0%] | 1,278 |
| 0.8B | LoRA-1 + limit 512 | 67 | 464/464 | 14.4% | [11.2%, 17.5%] | 4,979 |
| 2B | LoRA-1 + OFF | 165 | 464/464 | 35.6% | [31.2%, 39.7%] | 1,445 |
| 2B | LoRA-1 + limit 1,024 | 191 | 464/464 | 41.2% | [36.6%, 45.7%] | 4,072 |
| 4B | LoRA-1 + OFF | 300 | 464/464 | 64.7% | [59.9%, 69.0%] | 882 |
| 4B | LoRA-1 + limit 2,048 | 332 | 464/464 | 71.6% | [67.5%, 75.6%] | 3,511 |

## Same 464 problems, first attempts only

![First-attempt controls and combinations](figures/first-attempt-controls.svg)

Older methods can have two attempts per problem. For this comparison we use
only their first saved attempts, matching the new runs' single attempt.
This explains 2B LoRA alone: **34.9% first attempts versus 34.4% all attempts**.
Likewise, 4B limit alone is **71.1% first attempts versus 71.9% all attempts**.
These are two calculations from the same saved results, not contradictory scores.

| Model | Way | Passed / tested | First-attempt accuracy | Mean total tokens |
|---|---|---|---|---|
| 0.8B | LoRA-1 | 57/464 | 12.3% | 5,256 |
| 0.8B | Thinking OFF | 68/464 | 14.7% | 1,781 |
| 0.8B | Thinking ON | 19/464 | 4.1% | 6,206 |
| 0.8B | Limit 512 | 49/464 | 10.6% | 5,920 |
| 0.8B | LoRA-1 + OFF | 65/464 | 14.0% | 1,278 |
| 0.8B | LoRA-1 + limit 512 | 67/464 | 14.4% | 4,979 |
| 2B | LoRA-1 | 162/464 | 34.9% | 4,701 |
| 2B | Thinking OFF | 151/464 | 32.5% | 1,366 |
| 2B | Thinking ON | 121/464 | 26.1% | 5,369 |
| 2B | Limit 1,024 | 179/464 | 38.6% | 4,348 |
| 2B | LoRA-1 + OFF | 165/464 | 35.6% | 1,445 |
| 2B | LoRA-1 + limit 1,024 | 191/464 | 41.2% | 4,072 |
| 4B | LoRA-1 | 264/464 | 56.9% | 4,779 |
| 4B | Thinking OFF | 308/464 | 66.4% | 941 |
| 4B | Thinking ON | 231/464 | 49.8% | 5,186 |
| 4B | Limit 2,048 | 330/464 | 71.1% | 3,965 |
| 4B | LoRA-1 + OFF | 300/464 | 64.7% | 882 |
| 4B | LoRA-1 + limit 2,048 | 332/464 | 71.6% | 3,511 |

| Model | First-attempt comparison | Shared problems | Gap (points) | 95% gap interval |
|---|---|---|---|---|
| 0.8B | LoRA-1 + OFF vs Thinking OFF | 464 | -0.6 | [-3.2, +2.2] |
| 0.8B | LoRA-1 + OFF vs LoRA-1 | 464 | +1.7 | [-0.9, +4.5] |
| 0.8B | LoRA-1 + limit 512 vs Limit 512 | 464 | +3.9 | [+0.6, +7.1] |
| 0.8B | LoRA-1 + limit 512 vs LoRA-1 | 464 | +2.2 | [-0.4, +5.0] |
| 0.8B | LoRA-1 + limit 512 vs Thinking OFF | 464 | -0.2 | [-3.0, +3.0] |
| 2B | LoRA-1 + OFF vs Thinking OFF | 464 | +3.0 | [-0.6, +6.9] |
| 2B | LoRA-1 + OFF vs LoRA-1 | 464 | +0.6 | [-3.4, +4.7] |
| 2B | LoRA-1 + limit 1,024 vs Limit 1,024 | 464 | +2.6 | [-1.5, +6.7] |
| 2B | LoRA-1 + limit 1,024 vs LoRA-1 | 464 | +6.2 | [+2.4, +10.1] |
| 2B | LoRA-1 + limit 1,024 vs Thinking OFF | 464 | +8.6 | [+4.5, +12.9] |
| 4B | LoRA-1 + OFF vs Thinking OFF | 464 | -1.7 | [-5.6, +1.9] |
| 4B | LoRA-1 + OFF vs LoRA-1 | 464 | +7.8 | [+3.2, +12.1] |
| 4B | LoRA-1 + limit 2,048 vs Limit 2,048 | 464 | +0.4 | [-3.0, +3.7] |
| 4B | LoRA-1 + limit 2,048 vs LoRA-1 | 464 | +14.7 | [+10.3, +19.0] |
| 4B | LoRA-1 + limit 2,048 vs Thinking OFF | 464 | +5.2 | [+0.6, +9.5] |
| 0.8B | LoRA-1 + limit 512 vs LoRA-1 + OFF | 464 | +0.4 | [-2.4, +3.2] |
| 2B | LoRA-1 + limit 1,024 vs LoRA-1 + OFF | 464 | +5.6 | [+1.1, +9.9] |
| 4B | LoRA-1 + limit 2,048 vs LoRA-1 + OFF | 464 | +6.9 | [+2.8, +11.2] |

### What the completed tests show

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

## Every benchmark and difficulty: all available methods

Each row averages attempts within a problem, then gives every problem equal weight.
Denominators are shown. Incomplete methods must not be ranked against full coverage.

| Model | Way | Benchmark | Difficulty | Problems tested | Accuracy (all attempts, equal problem weight) |
|---|---|---|---|---|---|
| 0.8B | Limit 1,024 | HumanEval+ | easy | 164 | 17.1% |
| 0.8B | Limit 1,024 | LiveCodeBench | all | 110 | 2.7% |
| 0.8B | Limit 1,024 | LiveCodeBench | easy | 48 | 6.2% |
| 0.8B | Limit 1,024 | LiveCodeBench | medium | 62 | 0.0% |
| 0.8B | Limit 512 | HumanEval+ | easy | 164 | 22.6% |
| 0.8B | Limit 512 | LiveCodeBench | all | 300 | 4.0% |
| 0.8B | Limit 512 | LiveCodeBench | easy | 166 | 6.6% |
| 0.8B | Limit 512 | LiveCodeBench | medium | 134 | 0.7% |
| 0.8B | LoRA-1 | HumanEval+ | easy | 164 | 22.0% |
| 0.8B | LoRA-1 | LiveCodeBench | all | 300 | 7.0% |
| 0.8B | LoRA-1 | LiveCodeBench | easy | 166 | 12.0% |
| 0.8B | LoRA-1 | LiveCodeBench | medium | 134 | 0.7% |
| 0.8B | LoRA-1 + limit 512 | HumanEval+ | easy | 164 | 26.8% |
| 0.8B | LoRA-1 + limit 512 | LiveCodeBench | all | 300 | 7.7% |
| 0.8B | LoRA-1 + limit 512 | LiveCodeBench | easy | 166 | 12.7% |
| 0.8B | LoRA-1 + limit 512 | LiveCodeBench | medium | 134 | 1.5% |
| 0.8B | LoRA-1 + OFF | HumanEval+ | easy | 164 | 25.0% |
| 0.8B | LoRA-1 + OFF | LiveCodeBench | all | 300 | 8.0% |
| 0.8B | LoRA-1 + OFF | LiveCodeBench | easy | 166 | 13.9% |
| 0.8B | LoRA-1 + OFF | LiveCodeBench | medium | 134 | 0.7% |
| 0.8B | Thinking OFF | HumanEval+ | easy | 164 | 25.6% |
| 0.8B | Thinking OFF | LiveCodeBench | all | 300 | 8.7% |
| 0.8B | Thinking OFF | LiveCodeBench | easy | 166 | 15.7% |
| 0.8B | Thinking OFF | LiveCodeBench | medium | 134 | 0.0% |
| 0.8B | Thinking ON | HumanEval+ | easy | 164 | 10.4% |
| 0.8B | Thinking ON | LiveCodeBench | all | 300 | 0.7% |
| 0.8B | Thinking ON | LiveCodeBench | easy | 166 | 0.6% |
| 0.8B | Thinking ON | LiveCodeBench | medium | 134 | 0.7% |
| 2B | Think briefly | HumanEval+ | easy | 164 | 3.7% |
| 2B | Think briefly | LiveCodeBench | all | 110 | 10.5% |
| 2B | Think briefly | LiveCodeBench | easy | 48 | 24.0% |
| 2B | Think briefly | LiveCodeBench | medium | 62 | 0.0% |
| 2B | Limit 1,024 | HumanEval+ | easy | 164 | 60.4% |
| 2B | Limit 1,024 | LiveCodeBench | all | 300 | 26.7% |
| 2B | Limit 1,024 | LiveCodeBench | easy | 166 | 43.4% |
| 2B | Limit 1,024 | LiveCodeBench | medium | 134 | 6.0% |
| 2B | Limit 2,048 | HumanEval+ | easy | 164 | 57.3% |
| 2B | Limit 2,048 | LiveCodeBench | all | 110 | 16.4% |
| 2B | Limit 2,048 | LiveCodeBench | easy | 48 | 37.5% |
| 2B | Limit 2,048 | LiveCodeBench | medium | 62 | 0.0% |
| 2B | Limit 512 | HumanEval+ | easy | 164 | 54.9% |
| 2B | Limit 512 | LiveCodeBench | all | 110 | 16.4% |
| 2B | Limit 512 | LiveCodeBench | easy | 48 | 33.3% |
| 2B | Limit 512 | LiveCodeBench | medium | 62 | 3.2% |
| 2B | LoRA-1 | HumanEval+ | easy | 164 | 56.4% |
| 2B | LoRA-1 | LiveCodeBench | all | 300 | 22.3% |
| 2B | LoRA-1 | LiveCodeBench | easy | 166 | 38.6% |
| 2B | LoRA-1 | LiveCodeBench | medium | 134 | 2.2% |
| 2B | LoRA-1 + limit 1,024 | HumanEval+ | easy | 164 | 60.4% |
| 2B | LoRA-1 + limit 1,024 | LiveCodeBench | all | 300 | 30.7% |
| 2B | LoRA-1 + limit 1,024 | LiveCodeBench | easy | 166 | 49.4% |
| 2B | LoRA-1 + limit 1,024 | LiveCodeBench | medium | 134 | 7.5% |
| 2B | LoRA-1 + OFF | HumanEval+ | easy | 164 | 51.2% |
| 2B | LoRA-1 + OFF | LiveCodeBench | all | 300 | 27.0% |
| 2B | LoRA-1 + OFF | LiveCodeBench | easy | 166 | 45.2% |
| 2B | LoRA-1 + OFF | LiveCodeBench | medium | 134 | 4.5% |
| 2B | LoRA-2 | HumanEval+ | easy | 164 | 56.4% |
| 2B | LoRA-2 | LiveCodeBench | all | 70 | 18.6% |
| 2B | LoRA-2 | LiveCodeBench | easy | 31 | 38.7% |
| 2B | LoRA-2 | LiveCodeBench | medium | 39 | 2.6% |
| 2B | Thinking OFF | HumanEval+ | easy | 164 | 47.3% |
| 2B | Thinking OFF | LiveCodeBench | all | 300 | 23.3% |
| 2B | Thinking OFF | LiveCodeBench | easy | 166 | 38.0% |
| 2B | Thinking OFF | LiveCodeBench | medium | 134 | 5.2% |
| 2B | Thinking ON | HumanEval+ | easy | 164 | 55.2% |
| 2B | Thinking ON | LiveCodeBench | all | 300 | 11.3% |
| 2B | Thinking ON | LiveCodeBench | easy | 166 | 18.4% |
| 2B | Thinking ON | LiveCodeBench | medium | 134 | 2.6% |
| 4B | Limit 1,024 | HumanEval+ | easy | 164 | 85.1% |
| 4B | Limit 1,024 | LiveCodeBench | all | 70 | 56.4% |
| 4B | Limit 1,024 | LiveCodeBench | easy | 31 | 82.3% |
| 4B | Limit 1,024 | LiveCodeBench | medium | 39 | 35.9% |
| 4B | Limit 2,048 | HumanEval+ | easy | 164 | 86.9% |
| 4B | Limit 2,048 | LiveCodeBench | all | 300 | 63.7% |
| 4B | Limit 2,048 | LiveCodeBench | easy | 166 | 85.2% |
| 4B | Limit 2,048 | LiveCodeBench | medium | 134 | 36.9% |
| 4B | Limit 4,096 | HumanEval+ | easy | 164 | 86.9% |
| 4B | Limit 4,096 | LiveCodeBench | all | 70 | 52.9% |
| 4B | Limit 4,096 | LiveCodeBench | easy | 31 | 79.0% |
| 4B | Limit 4,096 | LiveCodeBench | medium | 39 | 32.1% |
| 4B | Limit 512 | HumanEval+ | easy | 164 | 84.1% |
| 4B | Limit 512 | LiveCodeBench | all | 70 | 55.0% |
| 4B | Limit 512 | LiveCodeBench | easy | 31 | 83.9% |
| 4B | Limit 512 | LiveCodeBench | medium | 39 | 32.1% |
| 4B | LoRA-1 | HumanEval+ | easy | 164 | 85.1% |
| 4B | LoRA-1 | LiveCodeBench | all | 300 | 41.3% |
| 4B | LoRA-1 | LiveCodeBench | easy | 166 | 67.5% |
| 4B | LoRA-1 | LiveCodeBench | medium | 134 | 9.0% |
| 4B | LoRA-1 + limit 2,048 | HumanEval+ | easy | 164 | 84.1% |
| 4B | LoRA-1 + limit 2,048 | LiveCodeBench | all | 300 | 64.7% |
| 4B | LoRA-1 + limit 2,048 | LiveCodeBench | easy | 166 | 86.1% |
| 4B | LoRA-1 + limit 2,048 | LiveCodeBench | medium | 134 | 38.1% |
| 4B | LoRA-1 + OFF | HumanEval+ | easy | 164 | 79.3% |
| 4B | LoRA-1 + OFF | LiveCodeBench | all | 300 | 56.7% |
| 4B | LoRA-1 + OFF | LiveCodeBench | easy | 166 | 74.7% |
| 4B | LoRA-1 + OFF | LiveCodeBench | medium | 134 | 34.3% |
| 4B | Thinking OFF | HumanEval+ | easy | 164 | 78.7% |
| 4B | Thinking OFF | LiveCodeBench | all | 300 | 59.8% |
| 4B | Thinking OFF | LiveCodeBench | easy | 166 | 79.5% |
| 4B | Thinking OFF | LiveCodeBench | medium | 134 | 35.4% |
| 4B | Thinking ON | HumanEval+ | easy | 164 | 80.5% |
| 4B | Thinking ON | LiveCodeBench | all | 300 | 33.3% |
| 4B | Thinking ON | LiveCodeBench | easy | 166 | 56.6% |
| 4B | Thinking ON | LiveCodeBench | medium | 134 | 4.5% |

## Every benchmark and difficulty: first attempts

Every method below has all 464 test IDs: 164 HumanEval+, 166 LiveCodeBench easy,
and 134 LiveCodeBench medium. Counts show successes, not coverage alone.

| Model | Way | Benchmark | Difficulty | Passed / tested | First-attempt accuracy |
|---|---|---|---|---|---|
| 0.8B | LoRA-1 | HumanEval+ | easy | 36/164 | 22.0% |
| 0.8B | LoRA-1 | LiveCodeBench | all | 21/300 | 7.0% |
| 0.8B | LoRA-1 | LiveCodeBench | easy | 20/166 | 12.0% |
| 0.8B | LoRA-1 | LiveCodeBench | medium | 1/134 | 0.7% |
| 0.8B | Thinking OFF | HumanEval+ | easy | 42/164 | 25.6% |
| 0.8B | Thinking OFF | LiveCodeBench | all | 26/300 | 8.7% |
| 0.8B | Thinking OFF | LiveCodeBench | easy | 26/166 | 15.7% |
| 0.8B | Thinking OFF | LiveCodeBench | medium | 0/134 | 0.0% |
| 0.8B | Thinking ON | HumanEval+ | easy | 17/164 | 10.4% |
| 0.8B | Thinking ON | LiveCodeBench | all | 2/300 | 0.7% |
| 0.8B | Thinking ON | LiveCodeBench | easy | 1/166 | 0.6% |
| 0.8B | Thinking ON | LiveCodeBench | medium | 1/134 | 0.7% |
| 0.8B | Limit 512 | HumanEval+ | easy | 37/164 | 22.6% |
| 0.8B | Limit 512 | LiveCodeBench | all | 12/300 | 4.0% |
| 0.8B | Limit 512 | LiveCodeBench | easy | 11/166 | 6.6% |
| 0.8B | Limit 512 | LiveCodeBench | medium | 1/134 | 0.7% |
| 0.8B | LoRA-1 + OFF | HumanEval+ | easy | 41/164 | 25.0% |
| 0.8B | LoRA-1 + OFF | LiveCodeBench | all | 24/300 | 8.0% |
| 0.8B | LoRA-1 + OFF | LiveCodeBench | easy | 23/166 | 13.9% |
| 0.8B | LoRA-1 + OFF | LiveCodeBench | medium | 1/134 | 0.7% |
| 0.8B | LoRA-1 + limit 512 | HumanEval+ | easy | 44/164 | 26.8% |
| 0.8B | LoRA-1 + limit 512 | LiveCodeBench | all | 23/300 | 7.7% |
| 0.8B | LoRA-1 + limit 512 | LiveCodeBench | easy | 21/166 | 12.7% |
| 0.8B | LoRA-1 + limit 512 | LiveCodeBench | medium | 2/134 | 1.5% |
| 2B | LoRA-1 | HumanEval+ | easy | 95/164 | 57.9% |
| 2B | LoRA-1 | LiveCodeBench | all | 67/300 | 22.3% |
| 2B | LoRA-1 | LiveCodeBench | easy | 63/166 | 38.0% |
| 2B | LoRA-1 | LiveCodeBench | medium | 4/134 | 3.0% |
| 2B | Thinking OFF | HumanEval+ | easy | 79/164 | 48.2% |
| 2B | Thinking OFF | LiveCodeBench | all | 72/300 | 24.0% |
| 2B | Thinking OFF | LiveCodeBench | easy | 63/166 | 38.0% |
| 2B | Thinking OFF | LiveCodeBench | medium | 9/134 | 6.7% |
| 2B | Thinking ON | HumanEval+ | easy | 88/164 | 53.7% |
| 2B | Thinking ON | LiveCodeBench | all | 33/300 | 11.0% |
| 2B | Thinking ON | LiveCodeBench | easy | 30/166 | 18.1% |
| 2B | Thinking ON | LiveCodeBench | medium | 3/134 | 2.2% |
| 2B | Limit 1,024 | HumanEval+ | easy | 99/164 | 60.4% |
| 2B | Limit 1,024 | LiveCodeBench | all | 80/300 | 26.7% |
| 2B | Limit 1,024 | LiveCodeBench | easy | 73/166 | 44.0% |
| 2B | Limit 1,024 | LiveCodeBench | medium | 7/134 | 5.2% |
| 2B | LoRA-1 + OFF | HumanEval+ | easy | 84/164 | 51.2% |
| 2B | LoRA-1 + OFF | LiveCodeBench | all | 81/300 | 27.0% |
| 2B | LoRA-1 + OFF | LiveCodeBench | easy | 75/166 | 45.2% |
| 2B | LoRA-1 + OFF | LiveCodeBench | medium | 6/134 | 4.5% |
| 2B | LoRA-1 + limit 1,024 | HumanEval+ | easy | 99/164 | 60.4% |
| 2B | LoRA-1 + limit 1,024 | LiveCodeBench | all | 92/300 | 30.7% |
| 2B | LoRA-1 + limit 1,024 | LiveCodeBench | easy | 82/166 | 49.4% |
| 2B | LoRA-1 + limit 1,024 | LiveCodeBench | medium | 10/134 | 7.5% |
| 4B | LoRA-1 | HumanEval+ | easy | 140/164 | 85.4% |
| 4B | LoRA-1 | LiveCodeBench | all | 124/300 | 41.3% |
| 4B | LoRA-1 | LiveCodeBench | easy | 112/166 | 67.5% |
| 4B | LoRA-1 | LiveCodeBench | medium | 12/134 | 9.0% |
| 4B | Thinking OFF | HumanEval+ | easy | 127/164 | 77.4% |
| 4B | Thinking OFF | LiveCodeBench | all | 181/300 | 60.3% |
| 4B | Thinking OFF | LiveCodeBench | easy | 134/166 | 80.7% |
| 4B | Thinking OFF | LiveCodeBench | medium | 47/134 | 35.1% |
| 4B | Thinking ON | HumanEval+ | easy | 132/164 | 80.5% |
| 4B | Thinking ON | LiveCodeBench | all | 99/300 | 33.0% |
| 4B | Thinking ON | LiveCodeBench | easy | 94/166 | 56.6% |
| 4B | Thinking ON | LiveCodeBench | medium | 5/134 | 3.7% |
| 4B | Limit 2,048 | HumanEval+ | easy | 141/164 | 86.0% |
| 4B | Limit 2,048 | LiveCodeBench | all | 189/300 | 63.0% |
| 4B | Limit 2,048 | LiveCodeBench | easy | 139/166 | 83.7% |
| 4B | Limit 2,048 | LiveCodeBench | medium | 50/134 | 37.3% |
| 4B | LoRA-1 + OFF | HumanEval+ | easy | 130/164 | 79.3% |
| 4B | LoRA-1 + OFF | LiveCodeBench | all | 170/300 | 56.7% |
| 4B | LoRA-1 + OFF | LiveCodeBench | easy | 124/166 | 74.7% |
| 4B | LoRA-1 + OFF | LiveCodeBench | medium | 46/134 | 34.3% |
| 4B | LoRA-1 + limit 2,048 | HumanEval+ | easy | 138/164 | 84.1% |
| 4B | LoRA-1 + limit 2,048 | LiveCodeBench | all | 194/300 | 64.7% |
| 4B | LoRA-1 + limit 2,048 | LiveCodeBench | easy | 143/166 | 86.1% |
| 4B | LoRA-1 + limit 2,048 | LiveCodeBench | medium | 51/134 | 38.1% |


---

# What the results suggest

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

## Completed LoRA controls

All six combinations are complete, with 464/464 results each.
0.8B: LoRA + OFF **14.0%**, LoRA + limit 512 **14.4%**.
2B: LoRA + OFF **35.6%**, LoRA + limit 1,024 **41.2%**.
4B: LoRA + OFF **64.7%**, LoRA + limit 2,048 **71.6%**.
These use one attempt per problem. Historical controls also have a labelled
first-attempt comparison; their all-attempt scores remain separate.
See [the completed analysis](11-completed-lora-controls.md) and [benchmark tables](05-results.md).


---

# Advice and limits

Try free thinking controls before paying for shortest-correct training.
For the complete 464-problem set, the best observed free controls are:

**0.8B: Thinking OFF 14.7%** · **2B: Limit 1,024 38.6%** · **4B: Limit 2,048 71.9%**

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

## Completed LoRA controls

All six combinations are complete, with 464/464 results each.
0.8B: LoRA + OFF **14.0%**, LoRA + limit 512 **14.4%**.
2B: LoRA + OFF **35.6%**, LoRA + limit 1,024 **41.2%**.
4B: LoRA + OFF **64.7%**, LoRA + limit 2,048 **71.6%**.
These use one attempt per problem. Historical controls also have a labelled
first-attempt comparison; their all-attempt scores remain separate.
See [the completed analysis](11-completed-lora-controls.md) and [benchmark tables](05-results.md).


---

# Questions a teacher may ask

## How many test problems?

**464 unique problems:** 164 HumanEval+ and 300 LiveCodeBench.
Training and the early pilot are excluded.

## What are the main scores?

**0.8B: Thinking OFF 14.7%** · **2B: Limit 1,024 38.6%** · **4B: Limit 2,048 71.9%**

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

## Completed LoRA controls

All six combinations are complete, with 464/464 results each.
0.8B: LoRA + OFF **14.0%**, LoRA + limit 512 **14.4%**.
2B: LoRA + OFF **35.6%**, LoRA + limit 1,024 **41.2%**.
4B: LoRA + OFF **64.7%**, LoRA + limit 2,048 **71.6%**.
These use one attempt per problem. Historical controls also have a labelled
first-attempt comparison; their all-attempt scores remain separate.
See [the completed analysis](11-completed-lora-controls.md) and [benchmark tables](05-results.md).


---

# Collection history and coverage

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

## Completed LoRA controls

All six combinations are complete, with 464/464 results each.
0.8B: LoRA + OFF **14.0%**, LoRA + limit 512 **14.4%**.
2B: LoRA + OFF **35.6%**, LoRA + limit 1,024 **41.2%**.
4B: LoRA + OFF **64.7%**, LoRA + limit 2,048 **71.6%**.
These use one attempt per problem. Historical controls also have a labelled
first-attempt comparison; their all-attempt scores remain separate.
See [the completed analysis](11-completed-lora-controls.md) and [benchmark tables](05-results.md).


---

# Completed LoRA controls: evidence and conclusion

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

| Model | Combination | Passed | Coverage | Accuracy | 95% interval | Mean total tokens |
|---|---|---|---|---|---|---|
| 0.8B | LoRA-1 + OFF | 65 | 464/464 | 14.0% | [11.0%, 17.0%] | 1,278 |
| 0.8B | LoRA-1 + limit 512 | 67 | 464/464 | 14.4% | [11.2%, 17.5%] | 4,979 |
| 2B | LoRA-1 + OFF | 165 | 464/464 | 35.6% | [31.2%, 39.7%] | 1,445 |
| 2B | LoRA-1 + limit 1,024 | 191 | 464/464 | 41.2% | [36.6%, 45.7%] | 4,072 |
| 4B | LoRA-1 + OFF | 300 | 464/464 | 64.7% | [59.9%, 69.0%] | 882 |
| 4B | LoRA-1 + limit 2,048 | 332 | 464/464 | 71.6% | [67.5%, 75.6%] | 3,511 |

### What the completed tests show

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


---

# Words used in this folder

Each word is used in the easy thesis.
The longer list is [../GLOSSARY.md](../GLOSSARY.md).

| Word | Meaning |
|---|---|
| Token | A small piece of text, about three quarters of a word. The model writes one token at a time. |
| Thinking | Notes the model writes to itself before the code. Thinking uses tokens and time. |
| Thinking ON | The normal way. The model may think as long as the token room allows. |
| Thinking OFF | The switch is off. The model writes the answer with no thinking notes. |
| Thinking limit | We stop the thinking notes at a fixed length, then the model must answer. |
| Think briefly | We add one sentence that asks for short thinking. |
| LoRA | A small trained add-on. The big model stays frozen. |
| LoRA-1 | The add-on from the small early test (easy problems only). |
| LoRA-2 | The add-on from the main 2B run. This was the main trained way, chosen before we saw scores. |
| Accuracy | Average of each problem’s share of passing attempts. |
| Pass | The code passes every test for that problem. One failed test means fail. |
| Points | The gap between two accuracies. 40% minus 30% is +10 points. |
| Error bar | An uncertainty interval from resampling problems; it does not prove a universal result. |
| Cut off | The saved output reached its cap. The grader still determines whether extracted code passes. |
| Loop | The model repeats the same lines until the room runs out. |
| Dataset | A fixed list of problems, with tests. |
| Overlap | A training problem that is too close to a test problem. We remove those. |
| Median | The middle value after you sort the numbers. A few huge answers do not pull it up. |
| GPU | The chip that runs the model. We used a Google Colab A100. |
| 0.8B / 2B / 4B | About 0.8, 2, or 4 billion numbers inside the model. Bigger usually means stronger and heavier. |
| Coverage | How many unique problems have results for one method. |
| Retrospective | Chosen after the results were available. |
| Equal problem weight | Each problem contributes equally, even when attempt counts differ. |
| Paired comparison | Compare two methods on exactly the same problems. |
| Bootstrap | Repeat the calculation on resampled problems to estimate uncertainty. |
