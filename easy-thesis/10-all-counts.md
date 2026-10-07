# All the problems, then the scores

This page is the whole pile in one place.
The pictures come first. The tables sit under them.

You are in the **RESULTS** box.
Each test list keeps its own score.
464 is a count. It is not one accuracy.

## Everyday example

Three exam papers sit in one folder.
Two homework piles sit next to them.
You can count every sheet.
You still mark each exam on its own.

## The count

![How many problems](figures/counts.svg)

| Pile | How many | What it is |
|---|---|---|
| First exam | **234** | Easy functions plus contest problems |
| Extra contest | **40** | Later check |
| More contest | **190** | Bigger later check. 118 easy, 72 medium |
| **Tests in total** | **464** | 234 + 40 + 190. A count, not a blended score |
| LoRA-1 pool | **100** | Easy functions used to train the small add-on |
| LoRA-2 pool | **280** | 200 easy functions + 80 older contest problems |
| LoRA-2 kept | **157** | Short correct answers actually used. 133 + 24 |

49.8% and 78.2% stay on the 234.

## Best free score on each list

![Best free score](figures/best-free.svg)

| List | 0.8B | 2B | 4B |
|---|---|---|---|
| Exam 234 | OFF **20.5%** | Limit 1,024 **49.8%** | Limit 2,048 **78.2%** |
| Extra 40 | OFF **5.0%** (2/40) | OFF **12.5%** (10/80) | OFF **46.2%**, tied with limit 2,048 |
| More 190 | OFF **9.5%** (18/190) | Limit 1,024 **31.1%** (59/190) | Limit 2,048 **69.5%** (132/190) |

A free way wins on every list.
The winner on the 190 matches the first exam.

## The 190, way by way

![The 190 by way](figures/more-190-ways.svg)

| Way | 0.8B | 2B | 4B |
|---|---|---|---|
| Thinking OFF | 9.5% (18/190) | 24.7% (47/190) | 66.8% (127/190) |
| Thinking ON | 1.1% (2/190) | 13.7% (26/190) | 38.9% (74/190) |
| Best limit | 4.2% at 512 | **31.1%** at 1,024 | **69.5%** at 2,048 |
| LoRA-1 | 7.9% (15/190) | **27.4%** (52/190) | 46.3% (88/190) |

On 2B, LoRA-1 is **27.4%**.
The 1,024 limit is still higher, at 31.1% (59 vs 52).
LoRA-1 does beat thinking OFF (47) and thinking ON (26).
On the easy 118, LoRA-1 is 42.4% (50/118), just under the limit at 44.1%.
On the medium 72, LoRA-1 is 2.8% (2/72), the same as OFF. The limit is 9.7%.

On 4B medium only, OFF is 44.4% (32/72) and the limit is 38.9% (28/72).
The limit still wins all 190, because easy is 88.1% (104/118) against OFF at 80.5% (95/118).

The first pass took **7.9 hours**. The 2B add-on added **0.5 hours**.
The hours file now says **8.5 hours**. One try. Seed 3407.

## What this does not say

The three lists are not one exam.
Do not average 49.8%, 12.5%, and 31.1% into a new 2B score.
The 4B lead on the 190 is 5 answers (132 vs 127).
We did not draw error bars on the 40 or the 190.
