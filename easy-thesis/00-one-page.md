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
The 2B and4B gaps have positive intervals. Both compare the same464 problems.
These are retrospective, unadjusted comparisons, not proof of a universal winner.

## How to read the result

Each problem gets equal weight, whether it has one attempt or two.
For each problem, average its pass/fail results. Then average across problems.
2B and 4B LoRA-1 now cover 464/464 problems after the missing40 fill-in. Do not treat missing results as wrong answers.
Earlier LoRA-2 and loop checks cover only 234 problems.

The combined view was chosen after the runs. It was not a single preselected exam.
Collection details stay in the methods note; the main story uses all 464 problems.

Source: [combined results](../results/combined/README.md), calculated from saved graded answers. No model was run again.

## Completed extension: 2B LoRA-1 + limit 1,024

**41.2% accuracy — 191/464 passed. Coverage: 464/464, one attempt per problem.**
This uses Qwen3.5-2B and the existing LoRA-1 trained add-on.

The missing40 LoRA-alone runs are complete: 2B passed 1/40; 4B passed 12/40.
Their all-attempt, equal-problem-weight scores now cover all 464:
**2B LoRA-1 alone 34.4%; 4B LoRA-1 alone 56.8%.**

On the same 464 first attempts, the 2B comparison is:
**LoRA + limit 41.2% (191/464), LoRA alone 34.9% (162/464), OFF 32.5% (151/464).**
The combination gains 6.2 points over LoRA alone, interval +2.4 to +10.1.
It gains 8.6 points over OFF, interval +4.5 to +12.9.
LoRA alone's 2.4-point lead over OFF is inconclusive: interval −1.7 to +6.7.
The combination uses 13.4% fewer output tokens than LoRA alone.
OFF uses 66.5% fewer output tokens than the combination.

Limit alone remains 38.6% (179/464). The combination gains 2.6 points,
interval −1.5 to +6.7. A reliable gain over the free limit is not established.

Earlier tables use all attempts per problem; 2B LoRA alone is 34.4% under that rule.
The 34.9% reference above uses first attempts, matching the combination's one attempt.
Archived 424-problem reports retain their original numbers as history.
The extension is retrospective, with historical references and unadjusted intervals.
No result proves a universal winner. Other incomplete methods retain their coverage.

Checked 14 October 2026. Source: [completed result](../results/lora-limit-2b/README.md).
Updated comparison: [missing40 results](../results/lora-missing40/README.md).
