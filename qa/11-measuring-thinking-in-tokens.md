# Q&A 11: Measuring thinking length in tokens

⬅️ [All Q&A](README.md) · Hard word? See [GLOSSARY.md](../GLOSSARY.md) · Lesson: [02 Tokens](../lessons/02-tokens.md)

---

## 1. The step in 2 sentences

We learned what a token is: a small piece of text, about ¾ of a word.
We measure the length of the model's thinking in **tokens**, not in seconds or words.

---

## 2. Questions a teacher may ask

**Q: What is a token?**
A small piece of text that the model reads or writes in one step.
It can be a whole word (`cat`), part of a word (`over` + `thinking`), or a symbol (`(`).
About 100 tokens ≈ 75 English words.

**Q: Why does more thinking take more time?**
The model writes one token per turn of its loop.
More tokens = more turns = more time and computer power.
It is **not** because the model searches for information. It already knows everything from training.

**Q: Why do you measure thinking in tokens and not in seconds?**
Seconds depend on the computer. The same answer is fast on a big GPU and slow on a free T4.
The token count is the same on any computer. So tokens give a fair comparison,
and other researchers can compare with our numbers.

**Q: Why not count words?**
Models don't work in words; they work in tokens.
Limits (like our 3,500-token training limit and the 8,000-token test limit) and GPU memory
are all set in tokens. Code also has many symbols that are not really "words".

**Q: Where do tokens appear in your thesis?**
- Hypothesis: **at least 25% fewer** thinking tokens than thinking ON.
- Training examples: at most **3,500** tokens.
- Test thinking limit: the same for every way of answering (e.g. **8,000** tokens).
- Thinking budget: stop thinking after a set number of tokens.
- GPU time: the training run sees about **3.6 million** tokens.

---

## 3. Hard questions

**Q: Different models cut text into tokens differently. Doesn't that make your numbers unfair?**
Not inside our thesis. All 5 ways of answering use **the same model**, so they use the same tokenizer.
The comparison is fair. But you can't directly compare our token numbers with a paper that used
a different model. We will say that in the limitations.

**Q: Does fewer tokens always mean faster in real life?**
Mostly yes, because each token is one turn of the loop.
But real time also depends on the GPU, the software, and how many answers run together.
That's exactly why we report tokens as the main number.

**Q: Do you count the answer tokens too, or only the thinking?**
Our main number is **thinking tokens** (PLAN.md §5). The answer part (the code) is short
and similar across ways of answering.

---

## 4. Checked vs. assumed

| We checked | We assume |
|---|---|
| The free Tokenizer Playground page opens (2026-09-17) | "100 tokens ≈ 75 words" is a rule of thumb for English, not exact for Gemma |
| | The real Gemma token counts: we count them in lesson 11 (first model call) |

---

## 5. Where it is written

- [lessons/02-tokens.md](../lessons/02-tokens.md)
- [PLAN.md](../PLAN.md) §5 (what we measure)
- [DECISIONS.md](../DECISIONS.md) row #35
