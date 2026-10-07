# The 190-problem run (notebook 19)

Checked from the Drive zip `more-20261006T224333Z-1-001.zip` on 2026-10-07.
Every graded file has **190** rows. Every raw answer file has **190** lines.
Easy is **118**. Medium is **72**.
The old exam files were not in this zip, and they were not changed.

This list is **not** mixed into 49.8% or 78.2%.
Those stay on the first exam of 234.

## Everyday example

The first exam is already marked.
We wrote 190 more contest questions.
We marked them on their own sheet.
We did not erase the old marks and average them in.

## Where we are

```text
PROBLEM ✅ → GAP ✅ → QUESTION ✅ → HYPOTHESIS ✅ → EXPERIMENT ✅ → DATA ✅ → RESULTS ← this side check
```

## What I am testing

| Question | Answer |
|---|---|
| What am I testing? | Do the free ways still beat training on a bigger contest list? |
| Hypothesis? | A free way still wins. Training does not beat it. |
| What I change? | The way of answering, on the same 190 problems. |
| What I measure? | How often the code passes every test. |
| What we compare against? | Thinking ON, and the trained add-on where it ran. |
| Data? | 190 LiveCodeBench problems. 118 easy. 72 medium. |
| Metric? | Pass rate. One try. Seed 3407. |
| What supports it? | On each size, the best score is a free way. |
| What would reject it? | The trained add-on beating every free way. That did not happen. |

## The clock

The hours file says **7.947** real hours.
The cap for this pass was about **14.8** real hours (100 compute hours).
The run stopped with room left.
File timestamps run from **15:05** to **22:38** on **2026-10-06**.

| Way | Hours |
|---|---|
| 0.8B OFF | 0.601 |
| 0.8B limit 512 | 0.552 |
| 0.8B ON | 0.533 |
| 0.8B LoRA-1 | 0.545 |
| 2B limit 1,024 | 0.491 |
| 2B OFF | 0.482 |
| 2B ON | 0.458 |
| 4B limit 2,048 | 1.211 |
| 4B OFF | 0.785 |
| 4B ON | 1.144 |
| 4B LoRA-1 | 1.145 |

Models in the answer files: `unsloth/Qwen3.5-0.8B`, `unsloth/Qwen3.5-2B`, `unsloth/Qwen3.5-4B`.
Number format: bfloat16. One try each. Seed 3407.

The notebook refuses to start unless the GPU name contains A100 or H100.
The zip does not contain that printed GPU line.
So the chip is an A100 or an H100. We do not have the exact name saved.

## Scores (all 190)

| Way | 0.8B | 2B | 4B |
|---|---|---|---|
| Thinking OFF | **9.5%** (18/190) | 24.7% (47/190) | 66.8% (127/190) |
| Thinking ON | 1.1% (2/190) | 13.7% (26/190) | 38.9% (74/190) |
| Best limit | 4.2% (8/190) at 512 | **31.1%** (59/190) at 1,024 | **69.5%** (132/190) at 2,048 |
| LoRA-1 | 7.9% (15/190) | 27.4% (52/190) | 46.3% (88/190) |

A free way still wins on every size.
The winner matches the first exam:

| Size | Winner here | First exam winner |
|---|---|---|
| 0.8B | OFF 9.5% | OFF 20.5% |
| 2B | limit 1,024 at 31.1% | limit 1,024 at 49.8% |
| 4B | limit 2,048 at 69.5% | limit 2,048 at 78.2% |

The scores are lower than the first exam.
This list is contest problems only.
The first exam also has easy function questions.

## Easy and medium

| Way | 0.8B easy | 0.8B medium | 2B easy | 2B medium | 4B easy | 4B medium |
|---|---|---|---|---|---|---|
| OFF | **15.3%** (18/118) | 0% (0/72) | 38.1% (45/118) | 2.8% (2/72) | 80.5% (95/118) | **44.4%** (32/72) |
| ON | 0.8% (1/118) | 1.4% (1/72) | 19.5% (23/118) | 4.2% (3/72) | 59.3% (70/118) | 5.6% (4/72) |
| Limit | 5.9% (7/118) | 1.4% (1/72) | **44.1%** (52/118) | **9.7%** (7/72) | **88.1%** (104/118) | 38.9% (28/72) |
| LoRA-1 | 11.9% (14/118) | 1.4% (1/72) | 42.4% (50/118) | 2.8% (2/72) | 67.8% (80/118) | 11.1% (8/72) |

On 4B medium, thinking OFF beats the 2,048 limit (32 vs 28).
The limit still wins the full 190, because it wins the easy slice by more (104 vs 95).

## How often the answer hit the wall

"Hit the limit" means the answer used up the token room and stopped.

| Way | Easy hits | Medium hits | All 190 |
|---|---|---|---|
| 0.8B ON | 113 / 118 | 68 / 72 | 181 / 190 |
| 0.8B OFF | 19 / 118 | 30 / 72 | 49 / 190 |
| 2B ON | 85 / 118 | 64 / 72 | 149 / 190 |
| 2B OFF | 11 / 118 | 22 / 72 | 33 / 190 |
| 4B ON | 47 / 118 | 68 / 72 | 115 / 190 |
| 4B OFF | 0 / 118 | 7 / 72 | 7 / 190 |
| 4B limit 2,048 | 20 / 118 | 54 / 72 | 74 / 190 |

Open thinking still dies on the long notes.
That is the same loop story as the first exam.

## What did not run

2B LoRA-1 is now scored: **27.4%** (52/190), in **0.504** hours.
It loses to the 1,024 limit (59/190) and beats OFF (47/190).
0.8B and 4B training also lost to a free way.

LoRA-2 was not in this notebook.
Other limits were not in this notebook.
Every way here is **one try**. The first exam used two tries on 2B and 4B.

## Checked vs assumed

| We checked | We assume |
|---|---|
| 11 graded files, each 190 rows, pass counts match SUMMARY.md | The GPU was an A100. The notebook allows A100 or H100. The printed name was not in the zip. |
| 118 easy and 72 medium on every file | |
| 2B LoRA-1 is 52/190, easy 50/118, medium 2/72 | |
| Hours add up to 8.451, including 2B LoRA-1 at 0.504 | |
| These scores are not written into the 234 tables | |

## What this does not prove

The gaps are small in places.
4B limit leads OFF by **5 answers** out of 190.
0.8B OFF leads LoRA-1 by **3 answers** out of 190.
We did not draw error bars on this list.
Say "the free way scored higher here."
Do not say "proven" the way we say it for the 2B +7.7 points on the 234.
