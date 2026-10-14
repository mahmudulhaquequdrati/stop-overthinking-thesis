# 4B: all saved configurations

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

[Every method, benchmark, difficulty, token count and interval](../CURRENT-RESULTS.md) · [Full easy thesis](../../easy-thesis/FULL-THESIS.md) · [Full formal Markdown thesis](../../thesis/THESIS.md).

<!-- CURRENT-STUDY:END -->

Accuracy uses all saved attempts, with equal weight per problem.
First-attempt comparisons are separately labelled in the complete result page.

| Way | Accuracy | Coverage | Attempts | Mean thinking tokens | Mean total tokens |
|---|---|---|---|---|---|
| Limit 1,024 | 76.5% | 234/464 | 468 | 763 | 2,185 |
| Limit 2,048 | 71.9% | 464/464 | 738 | 1,603 | 3,921 |
| Limit 4,096 | 76.7% | 234/464 | 468 | 1,915 | 2,821 |
| Limit 512 | 75.4% | 234/464 | 468 | 481 | 2,168 |
| LoRA-1 alone (ON) | 56.8% | 464/464 | 698 | 4,661 | 4,797 |
| LoRA-1 + limit 2,048 | 71.6% | 464/464 | 464 | 1,512 | 3,511 |
| LoRA-1 + OFF | 64.7% | 464/464 | 464 | 0 | 882 |
| Thinking OFF | 66.5% | 464/464 | 738 | 0 | 943 |
| Thinking ON | 50.0% | 464/464 | 738 | 5,064 | 5,188 |

| Way | Benchmark | Difficulty | Coverage | Accuracy |
|---|---|---|---|---|
| Limit 1,024 | HumanEval+ | easy | 164 | 85.1% |
| Limit 1,024 | LiveCodeBench | easy | 31 | 82.3% |
| Limit 1,024 | LiveCodeBench | medium | 39 | 35.9% |
| Limit 2,048 | HumanEval+ | easy | 164 | 86.9% |
| Limit 2,048 | LiveCodeBench | easy | 166 | 85.2% |
| Limit 2,048 | LiveCodeBench | medium | 134 | 36.9% |
| Limit 4,096 | HumanEval+ | easy | 164 | 86.9% |
| Limit 4,096 | LiveCodeBench | easy | 31 | 79.0% |
| Limit 4,096 | LiveCodeBench | medium | 39 | 32.1% |
| Limit 512 | HumanEval+ | easy | 164 | 84.1% |
| Limit 512 | LiveCodeBench | easy | 31 | 83.9% |
| Limit 512 | LiveCodeBench | medium | 39 | 32.1% |
| LoRA-1 alone (ON) | HumanEval+ | easy | 164 | 85.1% |
| LoRA-1 alone (ON) | LiveCodeBench | easy | 166 | 67.5% |
| LoRA-1 alone (ON) | LiveCodeBench | medium | 134 | 9.0% |
| LoRA-1 + limit 2,048 | HumanEval+ | easy | 164 | 84.1% |
| LoRA-1 + limit 2,048 | LiveCodeBench | easy | 166 | 86.1% |
| LoRA-1 + limit 2,048 | LiveCodeBench | medium | 134 | 38.1% |
| LoRA-1 + OFF | HumanEval+ | easy | 164 | 79.3% |
| LoRA-1 + OFF | LiveCodeBench | easy | 166 | 74.7% |
| LoRA-1 + OFF | LiveCodeBench | medium | 134 | 34.3% |
| Thinking OFF | HumanEval+ | easy | 164 | 78.7% |
| Thinking OFF | LiveCodeBench | easy | 166 | 79.5% |
| Thinking OFF | LiveCodeBench | medium | 134 | 35.4% |
| Thinking ON | HumanEval+ | easy | 164 | 80.5% |
| Thinking ON | LiveCodeBench | easy | 166 | 56.6% |
| Thinking ON | LiveCodeBench | medium | 134 | 4.5% |

[Every benchmark, comparisons and intervals](../CURRENT-RESULTS.md).
Original raw cohort files are unchanged; their earlier summary text is preserved in the dated archive.
