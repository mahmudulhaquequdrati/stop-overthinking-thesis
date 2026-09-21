# Q&A 26: The mini-thesis results: training worked on easy problems

⬅️ [All Q&A](README.md) · Hard word? See [GLOSSARY.md](../GLOSSARY.md) · Decision: [DECISIONS #63, #64](../DECISIONS.md) · Numbers: [results](../results/2026-09-22-mini-thesis-first-results.md)

---

## 1. The step in 2 sentences

We ran the whole method once, small, on 100 easy MBPP+ test problems on a Colab A100. The trained
LoRA solved **65%** of the problems against **50%** for normal thinking, while using **41% fewer tokens**.

```text
thinking ON     50%   ████████████████████ 1,936 tokens   27 never finished
LoRA (ours)     65%   ████████████ 1,145 tokens            15 never finished
thinking OFF    56%   █ 100 tokens
think briefly    3%   ██████████████████████████████████████████ 4,056 tokens
```

---

## 2. Questions a teacher may ask

**Q: What is the main result?**
On easy code problems, training the model on its own shortest correct answers made it think 41%
shorter **and** get 15 more problems right out of 100. The error bars (+6 to +25 points) do not
include zero, so the gain is unlikely to be luck.

**Q: How can thinking less make it MORE accurate?**
Because many normal answers never finished. 27 of 100 thinking-ON answers thought until the
4,096-token limit and never wrote code, so they failed. After training, only 15 did. The model
learned to stop and answer. *Everyday example:* a student who used to run out of time now hands
in their work.

**Q: Why did "think briefly" score only 3%?**
We read the answers. The model treats "think briefly" as one more rule, then keeps checking
whether it follows the rule ("Wait, I need to make sure…") until the limit. Asking it to be brief
made it overthink more. That is why training is needed: the free, ask-nicely option failed.

**Q: Is the LoRA better than just switching thinking OFF?**
It is more accurate (65% vs 56%). But OFF is about 11 times cheaper (100 tokens vs 1,145). So it
is a trade-off, not a clear win. We have not yet computed error bars for LoRA vs OFF directly.

**Q: Would more training data help?**
Probably not much. LoRAs trained on 25%, 50% and 100% of the examples all scored about the same
(65%, 68%, 65%) with about the same length. The curve is already flat.

---

## 3. Hard questions

**Q: Isn't this too easy a test? Train on MBPP+, test on MBPP+?**
Yes, and we say so. The test problems were different from the training problems, but of the same
kind. The real thesis run tests on HumanEval+ and on medium LiveCodeBench problems, which the
training never saw. This result shows the method *can* work; it does not yet show it generalises.

**Q: Your rule R5 said "make shorter examples". Why don't you follow it?**
Because we found the rule compared two different things. The target was measured only among
finished, correct answers; the LoRA's ratio was measured against all answers, including 27 that
ran to the limit. Reading R5 as written would be wrong, so we don't act on it, and we explain why.

**Q: Why did you switch to a paid GPU?**
The free T4 wrote about 26–30 tokens per second. The whole mini-thesis would have taken many hours.
On the A100 (bought Colab units, allowed by DECISIONS #48) a batch of 64 answers took ~4 minutes.

**Q: What almost went wrong?**
The trained LoRAs first loaded **empty**, because Unsloth saved them under longer names. Our
safety check stopped the run. Without it, the "trained" model would have been the untrained one,
and we would have reported "training does nothing". It is now fixed and checked.

---

## 4. What we checked, and what we only assume

| ✅ We checked this | ❌ We only assume this |
|---|---|
| LoRA: 65% vs ON 50%, error bars [+6, +25] | That it also works on HumanEval+ and medium problems |
| Tokens x0.59 of ON, error bars [0.46, 0.75] | That LoRA beats OFF by more than chance (no paired test yet) |
| "Think briefly" loops (read in the raw answers) | That another "brief" wording would also fail |
| The LoRAs are really trained (non-zero weights, falling loss) | That 1 try per problem gives the same picture as 4 |

---

## 5. Where this is written down

- **Numbers:** [results/2026-09-22-mini-thesis-first-results.md](../results/2026-09-22-mini-thesis-first-results.md)
- **Decisions:** [DECISIONS.md](../DECISIONS.md) #63 (A100, LoRA fix), #64 (the result)
- **Roadmap:** [ROADMAP.md](../ROADMAP.md) "You are here"
