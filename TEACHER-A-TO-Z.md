# Teacher guide: the completed 464-problem thesis

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

[Every method, benchmark, difficulty, token count and interval](results/CURRENT-RESULTS.md) · [Full easy thesis](easy-thesis/FULL-THESIS.md) · [Full formal Markdown thesis](thesis/THESIS.md).

<!-- CURRENT-STUDY:END -->

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
See [the paired results](easy-thesis/05-results.md) for numbers and limits.

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

[Per-problem values](results/combined/per-problem.csv),
[source files and original counts](results/combined/sources.csv), and
[the full audit](results/combined/results.json).

## Completed LoRA controls

All six combinations are complete, with 464/464 results each.
0.8B: LoRA + OFF **14.0%**, LoRA + limit 512 **14.4%**.
2B: LoRA + OFF **35.6%**, LoRA + limit 1,024 **41.2%**.
4B: LoRA + OFF **64.7%**, LoRA + limit 2,048 **71.6%**.
These use one attempt per problem. Historical controls also have a labelled
first-attempt comparison; their all-attempt scores remain separate.
See [the completed analysis](easy-thesis/11-completed-lora-controls.md) and [benchmark tables](easy-thesis/05-results.md).


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

Read [checked results](results/lora-controls/checked-results.json),
[raw archive and result note](results/lora-controls/README.md), and
[all accuracy, benchmark and token tables](easy-thesis/05-results.md).
