# 53 — Research pivot

We parked RPMR because useful recovery was still untested.
We screened a new training-loss idea using saved training examples and papers.

## What did we observe?

Duplicate parsed thinking-code structures occur in 60/133 selected MBPP traces.
They also occur in 15/24 selected LiveCodeBench traces.
Parsing reads code structure without executing code.
This does not prove repetition harms learning.

## What might we change?

Give repeated draft-code groups a shared learning weight.
Keep distinct revisions and the final answer supervised.
This changes LoRA's training calculation, not inference memory.

## Is it novel?

General loss weighting and structural repetition methods already exist.
The specific combination needs a stronger search and useful comparisons.
It is a candidate, not a claimed invention.

## Why not continue RPMR?

Its numerical checks passed, but the live candidate did not loop.
More smoke tests would not establish a useful effect.
Its notebooks and results remain available for undo or later study.

## What is checked and what is assumed?

Checked: duplicate AST counts and the closest papers described in the note.
Not checked: duplicate-token share, current adapter training provenance, or training improvement.
No new GPU test, model training, commit, or push occurred.

## What next?

A tokenizer-only data audit in Colab CPU. Forecast cost before any GPU test.
Read [the research note](../research/2026-10-14-shared-draft-supervision.md).
Decision #127 records the change.
