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
| 0.8B | Thinking OFF | 14.7% | 464/464 | 464 |
| 0.8B | Thinking ON | 4.1% | 464/464 | 464 |
| 2B | Think briefly | 6.4% | 274/464 | 548 |
| 2B | Limit 1,024 | 38.6% | 464/464 | 738 |
| 2B | Limit 2,048 | 40.9% | 274/464 | 274 |
| 2B | Limit 512 | 39.4% | 274/464 | 548 |
| 2B | LoRA-1 | 34.4% | 464/464 | 698 |
| 2B | LoRA-2 | 45.1% | 234/464 | 468 |
| 2B | Thinking OFF | 31.8% | 464/464 | 738 |
| 2B | Thinking ON | 26.8% | 464/464 | 738 |
| 4B | Limit 1,024 | 76.5% | 234/464 | 468 |
| 4B | Limit 2,048 | 71.9% | 464/464 | 738 |
| 4B | Limit 4,096 | 76.7% | 234/464 | 468 |
| 4B | Limit 512 | 75.4% | 234/464 | 468 |
| 4B | LoRA-1 | 56.8% | 464/464 | 698 |
| 4B | Thinking OFF | 66.5% | 464/464 | 738 |
| 4B | Thinking ON | 50.0% | 464/464 | 738 |


Coverage means unique problems with results. A missing result is not counted as a failure. Only compare scores directly when they use the same problems.

The combined inputs contain **11,196 saved attempts** across all methods and sizes.
That is not a count of independent test problems.

![Matched LoRA comparison](figures/combined-lora.svg)

| Model | Free control | Shared problems | Free accuracy | LoRA-1 accuracy | Gap (points) | 95% gap interval |
|---|---|---|---|---|---|---|
| 0.8B | Thinking OFF | 464 | 14.7% | 12.3% | +2.4 | [-0.4, +5.2] |
| 2B | Limit 1,024 | 464 | 38.6% | 34.4% | +4.2 | [+0.8, +7.8] |
| 4B | Limit 2,048 | 464 | 71.9% | 56.8% | +15.1 | [+11.3, +19.0] |


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
