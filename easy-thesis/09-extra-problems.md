# The extra 40 problems

The first exam stays **234** problems.
These 40 are a second test, and their scores are now in the results chapter.

## Everyday example

The exam is already marked.
We wrote 40 more questions.
They are contest problems only.
There are no easy function questions in the pile.
The scores are lower, and that is expected.

## The lists

| List | How many |
|---|---|
| Old exam | 234 |
| Old training problems we must not reuse | 80 |
| New problems | 40 |
| Old exam plus new problems | 274 |

The 40 are easy and medium LiveCodeBench problems from 30 November 2024 to 4 January 2025.
17 are easy. 23 are medium.
None of them are in the old exam. None of them are in training.

The full id list is in [../results/extra/LISTS.md](../results/extra/LISTS.md).
The scores are in [../results/extra/SUMMARY.md](../results/extra/SUMMARY.md).

## What they scored

The run took **3.7 hours** on an A100.

| Way | 0.8B (1 try) | 2B | 4B (2 tries) |
|---|---|---|---|
| Thinking OFF | **5.0%** (2/40) | **12.5%** (10/80) | **46.2%** (37/80) |
| Thinking ON | 0% | 0% | 18.8% (15/80) |
| Limit 1,024 | 0% | 8.8% (7/80) | not run |
| Limit 2,048 | — | 7.5% (3/40, 1 try) | **46.2%** (37/80) |
| LoRA-1 | 0% | not run | not run |

A free way still wins.
Thinking OFF wins on 0.8B and 2B.
On 4B it ties the 2,048 limit.
The same table, with every way, is in [05-results.md](05-results.md).

## What did not run

2B training did not run. The weight files were missing.
4B training did not run. The clock stopped after thinking ON.
The other 4B limits did not run, for the same reason.

Where we are: `RESULTS → extra check`. The extra scores are in the main results chapter.
