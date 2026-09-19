# Q&A 21: The first real numbers (thinking ON vs OFF, and the speed problem)

⬅️ [All Q&A](README.md) · Hard word? See [GLOSSARY.md](../GLOSSARY.md) · Result: [results/2026-09-19-notebook11-first-call.md](../results/2026-09-19-notebook11-first-call.md)

---

## 1. The step in 2 sentences

We ran notebook 11 on Kaggle. Gemma loaded, answered one easy code question 4 times, and the thinking switch worked.
But the model writes only about 4.4 tokens per second, which is far too slow for our plan. So a speed test comes next.

---

## 2. Questions a teacher may ask

**Q: What did you measure?**
For each answer: thinking tokens, all new tokens, seconds, and tokens per second. Two answers with thinking ON, two with thinking OFF, the same question, fixed seeds.

**Q: What came out?**
| Way | Thinking tokens | All tokens | Seconds |
|---|---|---|---|
| ON, try 0 | 307 | 337 | 105.9 |
| ON, try 1 | 0 | 30 | 6.7 |
| OFF, try 0 | 0 | 28 | 6.3 |
| OFF, try 1 | 0 | 28 | 6.5 |

**Q: Did the loading fix work?**
Yes. The per-layer word table sat in CPU memory, the model loaded, and all 4 answers were the same normal solution.

**Q: Did you see overthinking?**
Yes. In one answer the model thought for 307 tokens about a one-line function. It even wrote the whole function inside its thinking, and then wrote it again as the answer. The thinking was about 10 times longer than the answer.

**Q: Why is one thinking-ON answer without any thinking?**
The prompt had the thinking token (the notebook checks this). The model still chose to answer straight away. So with thinking ON, Gemma sometimes skips thinking by itself, maybe because the question is so easy. In the real experiment we report the **average** over all answers, and we count how often it skips thinking.

**Q: Why is 4 tokens per second a problem?**
A thinking answer of 2,000 tokens then takes about 8 minutes. Making our training data needs about 40 million tokens: at this speed that is about 2,500 GPU-hours. We planned 15–40. That is impossible on free GPUs.

**Q: What will you do about it?**
First, ask many questions at once. A GPU is built to do many things in parallel; one answer at a time wastes most of it. We will also check if vLLM (a tool for fast answer writing) runs Gemma-4 on a T4. Then we decide, with real numbers.

---

## 3. Hard questions

**Q: 4 answers on 1 question. Isn't this far too little to conclude anything?**
About accuracy or thinking length: yes, and we claim nothing about them. About **speed**: no. Speed hardly depends on the question, and all 4 answers ran at 3.2–4.5 tokens per second. That is enough to see the plan is 60–170× too slow.

**Q: Maybe the slowness comes from your own fix (the table in CPU memory)?**
Maybe partly. We don't know yet. Other possible causes: one answer at a time, float32 mode on the T4, and unpacking the 4-bit numbers for every token. The speed test will separate them. We won't guess.

**Q: Why not switch to Qwen now?**
Because we don't know yet whether Qwen would be faster on a T4, or whether asking many questions at once already solves it. Switching now would be a decision without data.

**Q: Did the model get the answer right?**
The answers **look** right when we read them. But we did not grade them, because grading means running the model's code, and that is only done in a sandbox (lesson 14).

---

## 4. Checked vs. assumed

| We checked | Not checked yet |
|---|---|
| Loading with the table in CPU memory works on Kaggle | GPU and CPU memory numbers (printed, not saved) |
| The switch changes the prompt | How often thinking ON gives 0 thinking tokens |
| ~4.4 tokens per second, one answer at a time | Why it is so slow |
| One clear overthinking example | Whether asking many questions at once fixes the speed |

---

## 5. Where it is written

- [results/2026-09-19-notebook11-first-call.md](../results/2026-09-19-notebook11-first-call.md) · [CSV](../results/2026-09-19-notebook11-first-call.csv) · [raw answers](../results/2026-09-19-notebook11-raw.jsonl)
- [DECISIONS.md](../DECISIONS.md) row #46 · [PLAN.md](../PLAN.md) §10
