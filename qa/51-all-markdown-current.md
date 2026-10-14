# Updating every thesis-related Markdown file

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

[Every method, benchmark, difficulty, token count and interval](../results/CURRENT-RESULTS.md) · [Full easy thesis](../easy-thesis/FULL-THESIS.md) · [Full formal Markdown thesis](../thesis/THESIS.md).

<!-- CURRENT-STUDY:END -->

The earlier update covered the easy thesis, but left the formal thesis and older summaries stale.
We audited every Markdown file, rebuilt the current theses, and labelled historical notes.

## What changed?

Both full theses now show all saved configurations and benchmark groups.
The main result pages and model summaries use current scores.
Earlier proposals, Q&A, lessons and run notes show a current-study notice and retain their original context.
The original Markdown files are preserved in a dated archive.
Raw answer files, grades, model weights and downloaded reports are unchanged.

## Why keep older numbers anywhere?

A 234-problem result is a real historical result, not an error to replace with a 464-problem score.
Its scope must stay clear. Missing results cannot be invented or treated as failures.
Current first-attempt comparisons must not be mixed with all-attempt averages.

## Are all benchmark settings complete?

The six planned LoRA combinations each cover all 464 problems.
Some older limit sweeps and LoRA-2 remain partial; the current tables show their actual coverage.
No claim is made that every possible setting was tested.

## Checked and not run

Every Markdown path has a disposition in the documentation audit.
The eight downloaded run reports are byte-checked and preserved, with current links from their parent pages.
The project rules file remains an instruction file. The decision log is append-only.
The audit checks notices, current results, local links, raw report hashes and the formal/easy result text.
No model generation, training or paid compute was used. Existing PDF/HTML exports are not refreshed.

[Complete audit](../results/DOCUMENTATION-AUDIT.md) · [Current tables](../results/CURRENT-RESULTS.md) ·
[Full easy thesis](../easy-thesis/FULL-THESIS.md) · [Full formal thesis](../thesis/THESIS.md).
