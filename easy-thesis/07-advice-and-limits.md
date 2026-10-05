# What to do, and what we did not prove

Try the free settings first.
Train only if they are not enough, and only if your real problems look like the training problems.

## The answer

On Qwen3.5-2B, for these code tests, training to think shorter was **not** better than the free options.
The best way was free: **stop thinking at 1,024 tokens (49.8%)**.

On the same 234 problems:

| Size | Do this first | Score | Trained add-on |
|---|---|---|---|
| 0.8B | Thinking OFF | 20.5% | 17.9% |
| 2B | Limit about 1,024 | 49.8% | 45.5% (LoRA-1) |
| 4B | Limit about 2,048 | 78.2% | 69.9% |

> A small reasoning model does not mainly waste tokens by thinking carefully.
> It wastes them by getting stuck.
> A limit cuts the loop.
> On a very small model, even a limit is weak, and thinking OFF can be best.

## Advice you can use

```text
1. Try thinking OFF and a thinking limit before any training.
2. Match the limit to the size.
      tiny model  →  OFF
      about 2B    →  about 1,024 thinking tokens
      about 4B    →  about 2,048 thinking tokens
3. Count answers that never finish. Those loops are the waste.
4. Train only if the free ways are not enough,
   and only if new problems look like the training problems.
```

## The later 40 contest problems

The size rule above is for the first exam.
That exam is mostly easy functions.

On 40 newer contest problems, start with thinking OFF on every size we tested.
On 4B, also try a 2,048 limit.
It tied OFF at **46.2%**.
On the medium ones it was a bit higher: **30.4%** against OFF at **26.1%**.

Training was not retested on 2B or 4B for these 40.
On 0.8B it scored **0 out of 40**.

## Who should not expect a miracle

- **Medium and hard contest problems.** On the first exam's medium slice, every 2B way was near zero. OFF reached 9.0%. The limit reached 0%. On the 40 newer problems, 2B medium was still near the floor: OFF 6.5%, limit 1,024 at 4.3%.
- **A giant model.** We stopped at 4B. A 9B model might loop less and might finally have long finished thinking that training can shorten. That is still open.
- **A privacy proof.** Running locally can keep code on your machine. We did not test attacks or leaks.
- **Another "be brief" sentence.** We tested one wording. It clashed with "one code block only".

## What could still be wrong

| Limit of this study | Why it matters |
|---|---|
| One model family | Qwen3.5 may share quirks. Another family might differ. |
| 0.8B and the 2B limit-2048 cell use 1 try | The direction is clear. The exact percent is less firm than the 2-try cells. |
| Error bars are wide on the small LiveCodeBench groups | 31 and 39 problems cannot support a tiny gap. |
| The token room cut some honest thinking | With 16,384 tokens, normal thinking gained 5.5 points on HumanEval+. The limit still led. |
| LoRA is not full retraining | A full retrain might differ. We did not run one. |
| No hard problems and no math | Careful long thinking may matter there. |

## What to measure next

Before spending money on a bigger model, run a small check on about 40 problems with thinking ON.
Go ahead with shortest-correct training only if loops are rare (about 10% or less of answers) and there are short correct answers to learn from.
On our 2B model, **28%** of thinking-ON answers looped (132 of 468).
That failed the "loops are rare" bar.

Other ideas that target the loop itself:

- Stop when the text starts repeating.
- Change the sampling penalty that discourages repeats. We used the official coding settings, with no penalty.
- Train on examples where a loop was cut and the model then answered correctly.
- Put the thinking limit on top of a trained add-on.

## One recommendation

If you run a small Qwen3.5 code model on one GPU, start with **thinking OFF** on the tiniest size and a **short thinking limit** on 2B or 4B.
Do not pay for shortest-correct training until those free ways fail on your own problems.
