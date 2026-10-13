# Advice and limits

Try free thinking controls before paying for shortest-correct training.
For the complete 464-problem set, the best observed free controls are:

**0.8B: Thinking OFF 14.7%** · **2B: Limit 1,024 38.6%** · **4B: Limit 2,048 71.9%**

“Best” here is limited to the methods with full coverage.
The partially tested limits cannot establish a better full-set score.

## What we can say about training

On shared problems, the selected free controls score higher than LoRA-1.
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
