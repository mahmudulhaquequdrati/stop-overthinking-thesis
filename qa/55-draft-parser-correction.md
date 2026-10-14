# 55 — Draft parser correction

The first 4B CPU audit passed source checks, but its repetition count was incomplete.
We fixed indentation handling before applying the preset data screen.

## What was the mistake?

The parser allowed at most three spaces before a code fence.
Many thinking drafts use four or eight spaces. They were silently skipped.
The report therefore counted 12 duplicate traces and 1.59% affected thinking supervision.
These are incomplete counts, not evidence that the candidate fails the screen.

## What changed?

The parser accepts spaces and tabs, requiring matched opening/closing indentation.
It still parses only Python or unlabelled draft blocks without executing code.
Distinct code revisions and final-answer protection remain unchanged.
The earlier notebook version is backed up. Original report bytes are preserved.

## What is checked?

Four-space, eight-space, and tab fixtures pass.
The new nonempty parsed structures match the initial broad audit across all 73 traces.
It finds 238 nonempty parseable blocks and 27 duplicate traces with character fixtures.
The older 239 count included one empty parsed block. One block is invalid.
Character fixtures cannot provide corrected tokenizer shares.

## What remains untested?

The corrected Colab token percentage and the method's training effect.
Run revised Notebook 29 on CPU only. Keep the 5% screen unchanged.
No GPU training, new generation, commit, or push occurred.
[Preserved result](../experiments/shared-draft-supervision/results/20261014T173308Z-c83f4503/README.md).
Decision #132.
