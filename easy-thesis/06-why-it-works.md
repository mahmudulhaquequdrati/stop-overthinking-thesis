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

[Every method, benchmark, difficulty, token count and interval](../results/CURRENT-RESULTS.md) · [Full easy thesis](FULL-THESIS.md) · [Full formal Markdown thesis](../thesis/THESIS.md).

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
