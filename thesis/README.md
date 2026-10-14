# The updated thesis

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

[Every method, benchmark, difficulty, token count and interval](../results/CURRENT-RESULTS.md) · [Full easy thesis](../easy-thesis/FULL-THESIS.md) · [Full formal Markdown thesis](THESIS.md).

<!-- CURRENT-STUDY:END -->

Read [THESIS.md](THESIS.md) for the full formal Markdown thesis.
The [easy thesis](../easy-thesis/FULL-THESIS.md) uses the same checked results.
Both include all six completed LoRA combinations and every saved benchmark/configuration.

[All result tables](../results/CURRENT-RESULTS.md) · [Documentation audit](../results/DOCUMENTATION-AUDIT.md).

The chapters contain the motivation, background, method, datasets, measurement,
all results, interpretation, limitations, references, and all 464 test IDs.
First-attempt results and all-attempt problem averages are labelled separately.
Partial sweeps, the pilot, LoRA-2 and loop findings keep their actual coverage.

## Rebuild

Run `python3 scripts/sync_thesis_markdown.py` after rebuilding the easy thesis.
The full command sequence is in the appendices. It uses no GPU calls.
Edit generators or source chapters rather than the joined THESIS.md file.

## Export status

The existing PDF and HTML files are older exports. They have not been refreshed.
Use current Markdown for this completed 464-problem study.
The dated archive preserves all earlier Markdown, including the original thesis.
