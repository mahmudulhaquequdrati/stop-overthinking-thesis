# Q&A 13: Reasoning models, thinking, and the ON/OFF switch

⬅️ [All Q&A](README.md) · Hard word? See [GLOSSARY.md](../GLOSSARY.md) · Lesson: [04 Reasoning models and "thinking"](../lessons/04-reasoning-models-and-thinking.md)

---

## 1. The step in 2 sentences

We learned that a reasoning model writes thinking (notes to itself) before the answer, and that Gemma-4-E4B has a switch to turn it ON or OFF.
Our experiment compares 5 ways of using that thinking on the same model.

---

## 2. Questions a teacher may ask

**Q: What is a reasoning model?**
An LLM trained to write thinking before its final answer. The thinking is ordinary tokens,
between special markers for "thinking starts" and "thinking ends".

**Q: Why does thinking help?**
Each new token is guessed from all the tokens before it. When the model writes in-between steps,
later guesses can build on them. Like doing a hard sum on paper instead of in your head.

**Q: What is the thinking switch?**
A setting that lets the same model answer with thinking (ON) or directly (OFF).
For Gemma it is `enable_thinking=True/False` in code. Underneath, thinking is ON when the special token `<|think|>` is at the start of the system prompt (Gemma model page, checked 2026-09-17). We test it in lesson 11.

**Q: Why did you choose a model with a switch?**
Because our question needs it. Thinking OFF is the free way to be short.
Only with a switch can we fairly compare "train it shorter" with "just turn thinking OFF" on the **same** model.

**Q: What are your 5 ways of answering?**
1. Thinking OFF: answer directly.
2. Thinking budget: think, but stop at a set number of tokens, then answer.
3. "Think briefly" prompt: thinking ON, but we ask in words to keep it short.
4. Thinking ON: the normal way.
5. Thinking ON + our LoRA: normal thinking after our training.

**Q: Why include the "think briefly" prompt?**
It is the cheapest idea anyone would try first: just ask. If asking works, training is not needed.

---

## 3. Hard questions

**Q: Isn't thinking OFF an easy rival to beat?**
No. The NoThinking paper (2504.09858) found that skipping thinking can beat thinking with a small budget
(under ~3,000 tokens), including on coding. So OFF is a strong rival. That makes our comparison honest.

**Q: How exactly do you do the thinking budget on Gemma?**
Plan: count thinking tokens, stop at the limit, close the thinking area ourselves, then let the model answer.
⚠️ The exact way for Gemma is not checked yet. We set it up in the testing notebooks (Part 4).

**Q: Which budget value (k) will you use?**
Not decided yet. It is set before testing, and the same for all problems.

**Q: In chat apps thinking is often hidden. Do you measure the hidden part?**
Yes. In our notebooks we see all thinking tokens and save them word for word. We count exactly those.

---

## 4. Checked vs. assumed

| We checked | We assume |
|---|---|
| Gemma-4-E4B has an `enable_thinking` switch (Hugging Face page, 2026-09-13) | That the switch works cleanly in our notebook (test in lesson 11) |
| NoThinking paper page opened (✔ in PAPERS.md) | How to do the thinking budget on Gemma |
| Qwen Chat page opens (2026-09-17) | That the switch behaves as the page says in our own notebook (lesson 11) |
| Gemma model page: thinking ON via `<\|think\|>`; thinking appears between `<\|channel>thought` and `<channel\|>` (2026-09-17) | |

---

## 5. Where it is written

- [lessons/04-reasoning-models-and-thinking.md](../lessons/04-reasoning-models-and-thinking.md)
- [PLAN.md](../PLAN.md) §5 (the 5 ways of answering)
- [DECISIONS.md](../DECISIONS.md) rows #8 (model with a switch), #19 (what we compare against)
- [research/models-and-gpu.md](../research/models-and-gpu.md) (the switch on candidate models)
- [Q&A 02](02-finding-the-gap.md) (why the switch makes our gap)
