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

## Completed extension: 2B LoRA-1 + limit 1,024

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
