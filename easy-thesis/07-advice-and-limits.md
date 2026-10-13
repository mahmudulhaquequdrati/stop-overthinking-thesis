# Advice and limits

Try free thinking controls before paying for shortest-correct training.
For the complete 464-problem set, the best observed free controls are:

**0.8B: Thinking OFF 14.7%** · **2B: Limit 1,024 38.6%** · **4B: Limit 2,048 71.9%**

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
