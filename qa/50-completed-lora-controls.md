# Completed LoRA combinations and the full easy thesis

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

We checked the five Notebook 24 runs and added their results to the easy thesis.
Together with Notebook 21, all six planned combinations cover 464 problems each.

## What did we do, and why?

We kept every raw answer and grade, checked the frozen IDs and settings,
and recalculated the scores from saved results. This avoids paid reruns.
The full easy thesis now includes every saved configuration and benchmark group.

## What would a teacher ask?

**What is LoRA alone?** The existing trained add-on with thinking ON and no thinking limit.
**Does OFF help LoRA?** Sometimes relative to LoRA alone, but it does not consistently beat OFF without LoRA.
**Does a limit help LoRA?** The observed scores improve over LoRA alone at each model size.
**Does LoRA beat the free limit?** Not reliably for 2B or 4B in these comparisons.
**Why does 4B limit alone show both 71.1% and 71.9%?** First attempts give 71.1%.
Averaging all attempts within each problem gives 71.9%. Do not mix the two rules.
**What about 2B LoRA alone?** Likewise, 34.9% first attempts versus 34.4% all attempts.
**What about benchmarks?** Results show HumanEval+, LiveCodeBench easy and medium separately.
No hard contest tasks were tested. LiveCodeBench used up to 20 tests per problem.

## Hard questions

These are historical, retrospective comparisons, not a new pre-registered study.
Different environments and batch sizes can affect sampling even with the same seed.
Intervals resample whole problems, not attempts, and are unadjusted for multiple comparisons.
An interval crossing zero means the data do not establish a clear direction for that gap.
We do not claim that two extra 4B passes prove the adapter improves accuracy.
Lower token counts alone do not establish lower GPU time or money.

## Checked versus assumed

Checked: all 2,320 new raw answers and grades, unique IDs, no exact training ID overlap,
reference hashes, settings, adapter hashes, token metadata and recomputed paired intervals.
The graded outcomes were read from saved runs; generated code was not re-executed here.
Exact ID separation does not establish no text similarity or pretraining exposure.
Notebook 24 estimates about 57.0 compute units; actual billing is not independently checked.

## Where it is written

- [Full easy thesis](../easy-thesis/FULL-THESIS.md).
- [All benchmark and comparison tables](../easy-thesis/05-results.md).
- [Completed controls chapter](../easy-thesis/11-completed-lora-controls.md).
- [Archive, settings and calculations](../results/lora-controls/README.md).
- [Decision 112](../DECISIONS.md).

Next: read the full thesis and review the conclusions. No more generation is needed for these runs.
