# Q&A 01: Choosing the topic

⬅️ [All Q&A](README.md) · Hard word? See [GLOSSARY.md](../GLOSSARY.md)

---

## 1. The step in 2 sentences

We chose the topic "stop overthinking". We want to teach a small AI model to think
shorter on code problems, without getting more answers wrong.

---

## 2. Questions a teacher may ask

**Q: What is your thesis about, in one sentence?**
Small AI models think too long before answering code questions, even easy ones.
We train one to think shorter, and check if that is better than just switching its thinking OFF.

**Q: What does "overthinking" mean?**
The model writes long thinking where short thinking gives the same answer.
It is like a student who writes 5 pages for "2 + 2".

**Q: Why is overthinking a problem?**
The model writes text one small piece (a *token*) at a time.
Every extra token costs time and computer power.
So long thinking makes answers slow and expensive.

**Q: What other topics did you consider?**
Four free ideas:
1. Stop overthinking (chosen)
2. Self-repair (the model fixes its own wrong code)
3. Early-failure alarm (predict early that an answer will fail)
4. Prompt shrinker (make the input text shorter)

**Q: Why did you pick "stop overthinking"?**
Three reasons:
1. It has a clear before/after number: how long the thinking is, and how many answers are correct.
2. It produces a real trained model, not only a measurement.
3. Many researchers are working on it right now, so it matters.

**Q: Why is this a new project, not part of your earlier project (CARR)?**
In CARR, the main idea (a "router") added **+0.0 points**. It did not help.
This time I wanted to **build an improvement**, not only measure.
I also wanted to learn from zero in a clean project. CARR stays unchanged in its own folder.

**Q: Why do you only use free tools ($0)?**
It was my own requirement. Everything runs on free Colab and Kaggle GPUs,
with free models and datasets from Hugging Face.
This also means anyone can repeat the thesis without money.

---

## 3. Hard questions

**Q: Isn't shortening AI reasoning already done by many papers?**
Yes, especially for **math**. We don't claim to be the first to shorten reasoning.
Our new part is a fair comparison on **one small new model with a thinking switch**:
is training better than just switching thinking OFF? (See [Q&A 02](02-finding-the-gap.md).)

**Q: What if your training doesn't work?**
Then the answer is "switching thinking OFF is enough, training is not worth it".
That is still an honest answer to the question, so it is still a thesis.

---

## 4. Checked vs. assumed

| We checked | We assume (not checked yet) |
|---|---|
| CARR's router added +0.0 points (from the CARR project) | That training will make thinking shorter on *our* model |
| The topic is an active research area (many 2025–2026 papers found) | |

---

## 5. Where it is written

- [DECISIONS.md](../DECISIONS.md) rows #1, #2, #3
- [ROADMAP.md](../ROADMAP.md) §1
