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

Those reports preceded the extra40 fill-in. Both2B and4B LoRA-1 now cover464/464.
Missing results are not failures. We compare LoRA with controls on shared IDs only.
The 0.8B LoRA-1 covers all 464. LoRA-2 covers 234.

## Does the limit beat training?

The selected free controls have higher observed scores on shared problems.
The 0.8B gap is uncertain. The 2B and4B intervals are positive.
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
