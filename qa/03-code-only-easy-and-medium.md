# Q&A 03: Code only, easy + medium problems only

⬅️ [All Q&A](README.md) · Hard word? See [GLOSSARY.md](../GLOSSARY.md)

---

## 1. The step in 2 sentences

We work on **code problems only**, not math.
We use only **easy and medium** problems. Hard problems are a written limitation.

---

## 2. Questions a teacher may ask

**Q: Why code and not math?**
Math is crowded: there are dozens of papers on shorter math reasoning.
Code has only about 3 training papers, and all of them use older 7B models
that always think (no ON/OFF switch). So code has more open space.

**Q: Did you plan math at first?**
Yes. First the plan was math first, then code. Then "code main, math as a transfer test".
After the gap search we cut math out completely. It is now future work.

**Q: Why no hard problems?**
Four reasons:

| # | Reason | In simple words |
|---|---|---|
| 1 | **Memory** | Thinking on hard problems is often 10,000–15,000 tokens. Training on a free T4 GPU fits only about 3,500. |
| 2 | **Nothing to learn from** | A 4B model solves few hard problems. No correct answers means no short correct answers to train on. |
| 3 | **Time** | Long answers × 4 tries × thousands of problems is too slow on free GPUs. |
| 4 | **Nothing to measure** | If the model scores about 0% on hard, we can't see "did accuracy drop?" |

**Q: Whose idea was "easy + medium only"?**
Mine (the student's). It is recorded in DECISIONS #11.

---

## 3. Hard questions

**Q: If training examples are cut at 3,500 tokens, isn't the test unfair?**
No. The 3,500 limit is **only for training examples**, because of GPU memory.
At test time, **every** way of answering gets the **same** thinking limit (for example 8,000 tokens).
We also record how often each one hits the limit.

**Q: A model trained only on short answers may learn "always stop early". Then it fails medium problems. What protects you?**
Two things:
1. **LoRA** adds a small add-on. The base model itself stays unchanged.
2. **Our selection rule:** we skip answers shorter than **half the median** correct length.
   So we don't train on the extreme shortest answers.

**Q: Isn't dropping hard problems hiding a weakness?**
No, we write it down openly as a limitation, with the 4 reasons above.
Paper 2511.05874 found that cutting reasoning steps hurts hard tasks. So we say clearly:
our result is about easy and medium code.

---

## 4. Checked vs. assumed

| We checked | We assume |
|---|---|
| About 3 code training papers found; math has dozens | That the thinking on hard problems is 10–15k tokens *for our model* (from other models) |
| Unsloth measured Gemma-4-E4B training memory on a T4 (short examples) | That 3,500-token examples fit in memory (checked in week 3) |

---

## 5. Where it is written

- [DECISIONS.md](../DECISIONS.md) rows #4, #5, #11, #12, #13, #25
- [PLAN.md](../PLAN.md) §3
- [research/gaps.md](../research/gaps.md) ("code or math?")
