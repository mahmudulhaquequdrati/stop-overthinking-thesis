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

2B and 4B LoRA-1 now cover all464, after adding their exact extra40 results.
Some limit settings and LoRA-2 also have incomplete coverage.
See [all method coverage](05-results.md) and [the source manifest](../results/combined/sources.csv).

Saved raw results and the formal thesis retain their historical numbers.
Those files document the original experiments. They are not the combined headline.

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
