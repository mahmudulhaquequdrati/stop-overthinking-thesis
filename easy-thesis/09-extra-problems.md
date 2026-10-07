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

## A later list of 190, now scored

Notebook 19 graded a second list.
It is not mixed into these 40, and it is not mixed into 49.8% or 78.2%.

| List | How many |
|---|---|
| Old exam | 234 |
| Extra 40 | 40 |
| New list | 190 (118 easy, 72 medium) |
| Total | 464 |

The total is a count of problems. It is not a blended accuracy.

The run took **7.9 hours**. The cap was about 14.8 hours.
One try each. Seed 3407.

| Way | 0.8B | 2B | 4B |
|---|---|---|---|
| Thinking OFF | **9.5%** (18/190) | 24.7% (47/190) | 66.8% (127/190) |
| Thinking ON | 1.1% (2/190) | 13.7% (26/190) | 38.9% (74/190) |
| Best limit | 4.2% at 512 (8/190) | **31.1%** at 1,024 (59/190) | **69.5%** at 2,048 (132/190) |
| LoRA-1 | 7.9% (15/190) | **27.4%** (52/190) | 46.3% (88/190) |

A free way still wins.
This time the winner matches the first exam on every size.
OFF on 0.8B. Limit 1,024 on 2B. Limit 2,048 on 4B.

On 4B medium only, OFF wins: **44.4%** (32/72) against the limit at **38.9%** (28/72).
The limit still wins all 190, because easy is **88.1%** against OFF at **80.5%**.

2B LoRA-1 scored **27.4%** (52/190). The 1,024 limit still leads, 59 to 52.
0.8B and 4B training also lost to a free way.

The charts for all three lists are in [10-all-counts.md](10-all-counts.md).

The ids are in [../results/more/LISTS.md](../results/more/LISTS.md).
The scores are in [../results/more/SUMMARY.md](../results/more/SUMMARY.md).
