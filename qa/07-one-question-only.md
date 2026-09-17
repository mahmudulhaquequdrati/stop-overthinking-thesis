# Q&A 07: Cutting the thesis to one question

⬅️ [All Q&A](README.md) · Hard word? See [GLOSSARY.md](../GLOSSARY.md)

---

## 1. The step in 2 sentences

At first the plan had several research questions. On 2026-09-13 we cut it down to **one question**,
the one with the best chance of a positive result.

---

## 2. Questions a teacher may ask

**Q: What is your one research question?**
Is training a small model on its shortest correct answers better than the free options
(thinking OFF, a thinking budget, a "think briefly" prompt), for code?

**Q: What did you remove?**
These are now **future work**:

| Removed idea | In simple words |
|---|---|
| Learning curve (G-B) | How many training examples are needed (100 / 250 / 500 / 1k / 2k) |
| Code → math transfer (G-C) | Does training on code also shorten math thinking? |
| LoRA size test (G-D) | Does a bigger add-on (rank 32 vs 8) help? |
| Fresh vs. seen problems (G-E) | Does it work differently on problems the model may have seen? |
| GRPO | Training with rewards |
| Hard-problem pilot | Trying 50 hard problems |
| H7′ | Checking the model still thinks longer on medium than on easy |

**Q: Why only one question?**
1. **One study done well** is better than five done badly.
2. **Best chance of success:** the same method already cut tokens on math (Munkhbat et al.)
   and on 7B code (SEER). So token savings are likely.
3. **Clearest gap:** G-A is the most clearly open gap.
4. **Fits free GPUs:** it needs only **one** training run.
5. I want to turn it into a **conference paper**. A paper needs one clear message.

---

## 3. Hard questions

**Q: Isn't one question too small for a thesis?**
The question is small, but the experiment is big: 5 ways of answering × about 1,000 test problems
× 4 tries each, with error bars. Doing it properly on free GPUs is a lot of work.

**Q: Can you promise a positive result?**
No. Nobody can. The **room-to-shorten check** in week 3 warns us early.
And a negative result, reported honestly, still answers the question.

**Q: You dropped the "thinks longer on medium" check (H7′). How do you know it doesn't stop too early?**
The selection rule (not shorter than half the median) still protects against it.
And we record how often answers hit the thinking limit for every way of answering.

---

## 4. Checked vs. assumed

| We checked | We assume |
|---|---|
| The papers that already show token savings (from our search) | That one run is enough to show the result |

---

## 5. Where it is written

- [DECISIONS.md](../DECISIONS.md) row #25 (and the struck-out rows #4, #12, #15, #17)
- [PLAN.md](../PLAN.md) §2, §4
