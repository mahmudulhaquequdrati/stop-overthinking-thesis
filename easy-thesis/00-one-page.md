# The thesis in one page

Small code models often "think" for a long time.
A free stop on that thinking beat training them to think shorter.

## Everyday example

Imagine a student who writes five pages for "what is 2 + 2?".
That is slow.
It does not make the answer better.
Some small AI models do the same thing on easy code problems.
They write notes to themselves before the code.
Those notes are often a stuck loop, not careful work.

## The picture

```text
Same 234 code problems
        │
   ┌────┴────────────┐
   ▼                 ▼
 Free ways           Trained add-on (LoRA)
 OFF · limit ·       shortest correct answers
 "think briefly"
        │
        ▼
 On 2B, stop thinking at 1,024 tokens: 49.8%
 Normal thinking:                         42.1%
 Training did not make thinking shorter.
```

A *token* is a small piece of text, about three quarters of a word.
A *LoRA* is a small add-on we train on top of the model.
We do not retrain the whole model.

## What we found

```text
How often the first answers pass the tests (2B, higher is better)

Limit 1,024     ██████████████████████████  49.8%   best, and proven
LoRA-1          ███████████████████████     45.5%
LoRA-2          ███████████████████████     45.1%   not shorter
Thinking ON     ██████████████████████      42.1%   what we compare against
Thinking OFF    █████████████████████       40.8%   about 4× fewer tokens
"Think briefly" ███                          6.6%   the wording confused it
```

Three sizes, same 234 problems:

| Size | Best free way | Score | Trained add-on |
|---|---|---|---|
| 0.8B (1 try) | Thinking OFF | 20.5% | 17.9% |
| 2B | Limit 1,024 | 49.8% | 45.5% |
| 4B (2 tries) | Limit 2,048 | 78.2% | 69.9% |

The trained add-on never beat the best free way.

## Later check

We also graded 40 newer contest problems.
A free way still wins.
Thinking OFF was best, or it tied the limit.

| Size | On these 40 | Thinking ON |
|---|---|---|
| 0.8B (1 try) | OFF 5.0% (2/40) | 0% |
| 2B (2 tries) | OFF 12.5% (10/80) | 0% |
| 4B (2 tries) | OFF 46.2%, tied with limit 2,048 | 18.8% |

The first exam scores above stay the exam scores.
The full table is in [05-results.md](05-results.md).

## Why

Most very long answers were loops.
The model repeated the same lines until it ran out of room.
A thinking limit cuts the loop and forces an answer.
Training on short finished answers does not teach the model how to get unstuck.

## One line

For these small code models, try thinking OFF or a short thinking limit first.
Train only if those free ways are not enough.
