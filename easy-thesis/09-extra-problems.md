# Collection history and coverage

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

The main easy-thesis view is now **464 unique problems**.
This page records where they came from; it is not a separate results story.

The original collection had 234 problems. Later collections added 40 and 190.
Their IDs are disjoint. The combined total contains 164 HumanEval+ and 300 LiveCodeBench problems.
The combined view was chosen on 13 October 2026, after results were available.
It should not be described as a single pre-registered test set.

0.8B used one attempt per problem. The main 2B and 4B runs used two attempts.
The 190-problem collection used one attempt. Some limit fill-ins also used one.
All available attempts contribute, but every problem has equal weight.

2B and 4B LoRA-1 now cover all 464, after adding their exact extra 40 results.
Some limit settings and LoRA-2 also have incomplete coverage.
See [all method coverage](05-results.md) and [the source manifest](../results/combined/sources.csv).

Saved raw results retain their historical numbers. The dated Markdown archive
preserves the original thesis. Both current thesis versions use the combined results.

## Completed LoRA controls

All six combinations are complete, with 464/464 results each.
0.8B: LoRA + OFF **14.0%**, LoRA + limit 512 **14.4%**.
2B: LoRA + OFF **35.6%**, LoRA + limit 1,024 **41.2%**.
4B: LoRA + OFF **64.7%**, LoRA + limit 2,048 **71.6%**.
These use one attempt per problem. Historical controls also have a labelled
first-attempt comparison; their all-attempt scores remain separate.
See [the completed analysis](11-completed-lora-controls.md) and [benchmark tables](05-results.md).
