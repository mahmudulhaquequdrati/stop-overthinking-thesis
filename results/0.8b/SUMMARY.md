# 0.8B: all saved configurations

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
| Limit 1,024 | 11.3% | 274/464 | 274 | 975 | 4,794 |
| Limit 512 | 10.6% | 464/464 | 464 | 510 | 5,920 |
| LoRA-1 alone (ON) | 12.3% | 464/464 | 464 | 5,150 | 5,256 |
| LoRA-1 + limit 512 | 14.4% | 464/464 | 464 | 503 | 4,979 |
| LoRA-1 + OFF | 14.0% | 464/464 | 464 | 0 | 1,278 |
| Thinking OFF | 14.7% | 464/464 | 464 | 0 | 1,781 |
| Thinking ON | 4.1% | 464/464 | 464 | 6,147 | 6,206 |

| Way | Benchmark | Difficulty | Coverage | Accuracy |
|---|---|---|---|---|
| Limit 1,024 | HumanEval+ | easy | 164 | 17.1% |
| Limit 1,024 | LiveCodeBench | easy | 48 | 6.2% |
| Limit 1,024 | LiveCodeBench | medium | 62 | 0.0% |
| Limit 512 | HumanEval+ | easy | 164 | 22.6% |
| Limit 512 | LiveCodeBench | easy | 166 | 6.6% |
| Limit 512 | LiveCodeBench | medium | 134 | 0.7% |
| LoRA-1 alone (ON) | HumanEval+ | easy | 164 | 22.0% |
| LoRA-1 alone (ON) | LiveCodeBench | easy | 166 | 12.0% |
| LoRA-1 alone (ON) | LiveCodeBench | medium | 134 | 0.7% |
| LoRA-1 + limit 512 | HumanEval+ | easy | 164 | 26.8% |
| LoRA-1 + limit 512 | LiveCodeBench | easy | 166 | 12.7% |
| LoRA-1 + limit 512 | LiveCodeBench | medium | 134 | 1.5% |
| LoRA-1 + OFF | HumanEval+ | easy | 164 | 25.0% |
| LoRA-1 + OFF | LiveCodeBench | easy | 166 | 13.9% |
| LoRA-1 + OFF | LiveCodeBench | medium | 134 | 0.7% |
| Thinking OFF | HumanEval+ | easy | 164 | 25.6% |
| Thinking OFF | LiveCodeBench | easy | 166 | 15.7% |
| Thinking OFF | LiveCodeBench | medium | 134 | 0.0% |
| Thinking ON | HumanEval+ | easy | 164 | 10.4% |
| Thinking ON | LiveCodeBench | easy | 166 | 0.6% |
| Thinking ON | LiveCodeBench | medium | 134 | 0.7% |

[Every benchmark, comparisons and intervals](../CURRENT-RESULTS.md).
Original raw cohort files are unchanged; their earlier summary text is preserved in the dated archive.
