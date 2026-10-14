# What the results suggest

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

[Every method, benchmark, difficulty, token count and interval](../results/CURRENT-RESULTS.md) · [Full easy thesis](../easy-thesis/FULL-THESIS.md) · [Full formal Markdown thesis](THESIS.md).

<!-- CURRENT-STUDY:END -->

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
For exact numbers and paired intervals, see [the combined results](../easy-thesis/05-results.md).

LoRA-1 and LoRA-2 differ in training data and coverage.
A result for one is not a result for the other.
The best observed full-coverage controls also differ by model size.
Incomplete limit sweeps do not establish a globally optimal budget.

## Other historical checks

One “think briefly” wording conflicted with the code-only instruction in saved examples.
That does not show that every short-thinking prompt fails.
A longer-output retry changed both the available token room and the evaluated conditions.
Keep its original scope in [the formal analysis](06-analysis.md).
Neither check is a newly calculated 464-problem result.

## Completed LoRA controls

All six combinations are complete, with 464/464 results each.
0.8B: LoRA + OFF **14.0%**, LoRA + limit 512 **14.4%**.
2B: LoRA + OFF **35.6%**, LoRA + limit 1,024 **41.2%**.
4B: LoRA + OFF **64.7%**, LoRA + limit 2,048 **71.6%**.
These use one attempt per problem. Historical controls also have a labelled
first-attempt comparison; their all-attempt scores remain separate.
See [the completed analysis](../easy-thesis/11-completed-lora-controls.md) and [benchmark tables](../easy-thesis/05-results.md).


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
[all accuracy, benchmark and token tables](../easy-thesis/05-results.md).
