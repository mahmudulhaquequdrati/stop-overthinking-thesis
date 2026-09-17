# Q&A 08: The two checks before the big runs

⬅️ [All Q&A](README.md) · Hard word? See [GLOSSARY.md](../GLOSSARY.md)

---

## 1. The step in 2 sentences

Before spending many GPU days, we run **two small checks** in week 3.
We wrote the pass/fail rules **in advance**, so the data decides, not our wishes.

---

## 2. Questions a teacher may ask

**Q: Why do checks before the real work?**
*Everyday example:* before a long car trip, you check the fuel and the tyres.
Nobody can promise the training will work. But we can check cheaply **before** the expensive part.

**Q: What is check 1 (the memory check)?**
Train on **50 examples**, each up to 3,500 tokens long. Watch the GPU memory.

```text
Peak memory ≤ 14 GB   →  keep Gemma-4-E4B
Peak memory > 14 GB   →  switch to Qwen3.5-4B (measured 9.6 GB on a T4)
```

**Q: What is check 2 (the room-to-shorten check)?**
The base model answers **200 training problems, 4 times each**. Then we measure two things:

| Measure | Meaning | Must be |
|---|---|---|
| **Share of problems solved at least once** | Of the 200 problems, how many got at least 1 correct answer out of 4? | **≥ 40%** |
| **Room to shorten** | Shortest correct answer ÷ average correct answer length | **≤ 0.75** (shortest is at least 25% shorter) |

**Q: Why these two measures?**
- If the model solves too few problems, we have too few correct answers to train on.
- If the shortest correct answer is about as long as the average one, there is nothing
  short to learn from. Training would change nothing.

**Q: What if check 2 fails?**
We set the fix in advance: **ask each problem 8 times instead of 4**, then check again.
More tries give more chances to find a short correct answer.

---

## 3. Hard questions

**Q: Why 40% and 0.75? Where do they come from?**
We chose them before the experiment, as clear pass/fail lines.
0.75 matches our hypothesis: we want at least 25% fewer tokens, so the training answers must be
at least 25% shorter. 40% makes sure enough problems give usable examples.

**Q: Isn't changing from 4 to 8 tries "cheating" if the check fails?**
No. The fix was written down **before** we saw any data (DECISIONS #27).
Changing the plan *after* seeing results would be a problem. This is the opposite.

**Q: What happens if both fixes fail?**
Then we report it honestly: on this model, there was not enough room to shorten.
That is still a real finding.

---

## 4. Checked vs. assumed

| We checked | We assume |
|---|---|
| Unsloth measured 10.7 GB for Gemma training (short examples, 1,024 tokens) | That 3,500-token examples stay under 14 GB |
| Unsloth measured 9.6 GB for Qwen3.5-4B | That the model passes the 40% and 0.75 lines |

Nothing in this step has been run yet. Both checks happen in **week 3**.

---

## 5. Where it is written

- [DECISIONS.md](../DECISIONS.md) rows #16, #27
- [PLAN.md](../PLAN.md) §7
- [research/data-size-and-test-size.md](../research/data-size-and-test-size.md) §2
