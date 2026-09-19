# Q&A 14: Overthinking (our problem)

⬅️ [All Q&A](README.md) · Hard word? See [GLOSSARY.md](../GLOSSARY.md) · Lesson: [05 Overthinking](../lessons/05-overthinking.md)

---

## 1. The step in 2 sentences

We learned what overthinking is: long thinking where much shorter thinking gives the same correct answer.
We also learned how to see it with numbers: ask the same problem several times and compare the shortest correct answer with the average correct answer.

---

## 2. Questions a teacher may ask

**Q: What is overthinking?**
Long thinking where shorter thinking would give the same correct answer.
Signs: checking the same thing again and again, "wait, let me reconsider" after the answer is already right, trying other solutions when one already works.

**Q: Why is it a problem?**
Every thinking token costs time and GPU power. Companies pay per token.
On easy problems, the extra tokens give nothing back.

**Q: Why do models overthink?**
The usual explanation in papers: in reasoning training, models are rewarded for correct answers.
Long thinking often helps on hard problems, and nothing punishes length. So "think long" becomes a habit everywhere.
We did not test this explanation ourselves.

**Q: How do you measure overthinking?**
We ask each problem 4 times and look only at the correct answers.
**Room to shorten** = shortest correct length ÷ average correct length.
Example: correct answers of 2,400, 1,200 and 1,800 tokens → 1,200 ÷ 1,800 = 0.67.
The model already *can* solve it with 33% fewer tokens, but doesn't every time.

**Q: What is your rule for "enough room to shorten"?**
Averaged over 200 training problems, the ratio must be **≤ 0.75** (short answers at least 25% shorter).
If not, we ask 8 times instead of 4 and check again. (PLAN.md §7, DECISIONS #16, #27.)

**Q: Is all long thinking bad?**
No. On hard problems, long thinking is often needed. That's why we don't simply switch thinking OFF,
and why accuracy may not drop more than 3 points in our hypothesis.

---

## 3. Hard questions

**Q: If a very short correct answer exists, why not always train on it?**
It may be a lucky answer. The S3-CoT paper (2602.01982) warns that training only on the very shortest answers hurts accuracy.
So we skip answers shorter than half the median correct length.

**Q: Your 25% target: is that realistic?**
Earlier work suggests yes: SEER got about 40% shorter on code with a 7B model;
Munkhbat et al. got about 12% shorter on math without special prompts.
But no one did it on Gemma-4-E4B, so we check the room to shorten **before** training.

**Q: What if the model doesn't overthink at all on easy code?**
Then the room-to-shorten check fails, even with 8 tries. We report that honestly:
"this model has little overthinking on easy/medium code", which is also a finding.

**Q: Can't you just remove "wait" words from the thinking?**
That changes the text by hand and may break the reasoning. Some papers prune thinking like that (e.g. TokenSkip, ASAP).
We chose the model's **own complete, correct** answers instead, so every training example really passed the tests.

---

## 4. Checked vs. assumed

| We checked | We assume |
|---|---|
| Munkhbat et al., SEER and 2511.05874 papers opened (✔ in PAPERS.md) | The "why models overthink" explanation |
| | That Gemma overthinks enough on easy/medium code (checked in week 3) |
| | The numbers in the lesson examples are made up, for teaching only |

---

## 5. Where it is written

- [lessons/05-overthinking.md](../lessons/05-overthinking.md)
- [PLAN.md](../PLAN.md) §7 (the checks), §8 (the method)
- [DECISIONS.md](../DECISIONS.md) rows #14, #16, #27
- [Q&A 08](08-safety-checks-before-training.md) (the checks before the big runs)
