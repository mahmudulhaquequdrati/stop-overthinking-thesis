# The thesis in one page

Small code models often "think" for a long time.
A free stop on that thinking beat training them to think shorter.

You are in the **CONCLUSION** box.
The lists below are the whole study on one page.

## Everyday example

Imagine three exam papers and two homework piles.
You mark each exam paper on its own.
You do not add the three marks into one score.
The homework is what we used to train the add-on.
The homework is not the exam.

## Every problem, in one count

```text
TEST  (three lists, marked apart)
  234  first exam      easy functions + contest
+  40  extra contest   a small later check
+ 190  more contest    a bigger later check
─────
  464  problems we can name

TRAIN  (the add-on only)
  100  easy functions     →  LoRA-1
  280  easy + old contest →  LoRA-2
       200 + 80
       157 of the 280 had a short correct answer we kept
```

**464 is a count of problems.**
It is not one accuracy.
49.8% and 78.2% stay on the 234.

The pictures and the full stats are in [10-all-counts.md](10-all-counts.md).

A *token* is a small piece of text, about three quarters of a word.
A *LoRA* is a small add-on we train on top of the model.
We do not retrain the whole model.

| Add-on | Training problems | What we kept | Where it was used |
|---|---|---|---|
| LoRA-1 | **100** easy functions | 37 on 0.8B, 73 on 4B | 0.8B, 2B, and 4B |
| LoRA-2 | **280** (200 easy + 80 older contest) | **157** (133 + 24) | 2B main exam only |

## Scores on the 234

```text
How often the answers pass the tests (2B, higher is better)

Limit 1,024     ██████████████████████████  49.8%   best, and proven
LoRA-1 (from 100) ███████████████████████   45.5%
LoRA-2 (from 280) ███████████████████████   45.1%   not shorter
Thinking ON     ██████████████████████      42.1%   what we compare against
Thinking OFF    █████████████████████       40.8%   about 4× fewer tokens
"Think briefly" ███                          6.6%   the wording confused it
```

| Size | Best free way | Score | Trained add-on |
|---|---|---|---|
| 0.8B (1 try) | Thinking OFF | 20.5% | LoRA-1 17.9% |
| 2B | Limit 1,024 | 49.8% | LoRA-1 45.5% · LoRA-2 45.1% |
| 4B (2 tries) | Limit 2,048 | 78.2% | LoRA-1 69.9% |

The trained add-on never beat the best free way on this exam.

## Scores on the extra 40

A free way still wins.
Thinking OFF was best, or it tied the limit.

| Size | On these 40 | Thinking ON | Trained add-on |
|---|---|---|---|
| 0.8B (1 try) | OFF 5.0% (2/40) | 0% | LoRA-1 0% |
| 2B (2 tries) | OFF 12.5% (10/80) | 0% | not run |
| 4B (2 tries) | OFF 46.2%, tied with limit 2,048 | 18.8% | not run |

## Scores on the 190

One try each. A free way still wins.
The winner matches the first exam.

| Size | On these 190 | Trained add-on |
|---|---|---|
| 0.8B | OFF 9.5% (18/190) | LoRA-1 7.9% (from the 100) |
| 2B | Limit 1,024 at 31.1% (59/190) | LoRA-1 **27.4%** (52/190) |
| 4B | Limit 2,048 at 69.5% (132/190) | LoRA-1 46.3% (from the 100) |

The 2B add-on is now scored: **27.4%** (52/190).
It beats thinking OFF (47/190) and thinking ON (26/190).
It loses to the 1,024 limit (59/190).
The lead is 7 answers. We did not draw error bars on this list.

On 4B medium only, OFF is 44.4% and the limit is 38.9%.
The limit still wins all 190, because easy is 88.1% against OFF at 80.5%.

The full tables are in [05-results.md](05-results.md).

## Why

Most very long answers were loops.
The model repeated the same lines until it ran out of room.
A thinking limit cuts the loop and forces an answer.
Training on 100 or on 280 short answers does not teach the model how to get unstuck.

## One line

For these small code models, try thinking OFF or a short thinking limit first.
Train only if those free ways are not enough.
