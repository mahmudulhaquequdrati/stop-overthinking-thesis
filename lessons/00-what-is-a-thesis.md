# Lesson 00: What a thesis is

⬅️ [ROADMAP](../ROADMAP.md) · ➡️ [Lesson 01](01-what-is-an-llm.md) · Hard word? See [GLOSSARY](../GLOSSARY.md)

---

## 1. In one sentence

**A thesis is a question nobody has answered yet. You answer it with evidence you collected. You write it so someone else can check it.**

---

## 2. What is it?

A thesis is **not** "a project where I built something".
A thesis is **a claim you can prove**.

**Everyday example: a cooking contest.**

```text
Project:   "I made a cake."                           → nice, but so what?
Thesis:    "Cakes with less sugar taste just as good.
            I tested 40 people, half got each cake,
            and 19 of 20 couldn't tell the difference." → a claim + proof
```

The cake is the tool. **The claim and the proof are the thesis.**

A good thesis has 3 properties:

| Property | Meaning | In the cake example |
|---|---|---|
| **New** | Nobody answered this exact question before | Nobody tested this recipe |
| **Evidence** | You measured, you didn't just believe | 40 people tasted it |
| **Checkable** | Someone else can repeat it and get the same result | The recipe and the test are written down |

---

## 3. Why do we need it? (in *our* thesis)

We will build something: a trained AI model. But the model alone is not the thesis.

The thesis is the **claim**:
> "Training a small model on its own shortest correct answers makes it think shorter
> on code without losing accuracy, and that works better than just switching thinking OFF."

And the **proof**: numbers from the same test problems, before and after training.

If the claim turns out wrong, **it is still a thesis**, as long as the proof is honest:
> "Switching thinking OFF worked just as well, so training was not worth it."

---

## 4. How does it work? The research chain

Every thesis follows the same chain. Each box answers one question.

```text
┌───────────┐   ┌─────┐   ┌──────────┐   ┌────────────┐   ┌────────────┐
│ PROBLEM   │ → │ GAP │ → │ QUESTION │ → │ HYPOTHESIS │ → │ EXPERIMENT │
│ what's    │   │what │   │ what     │   │ what I     │   │ how I test │
│ wrong?    │   │ is  │   │ exactly  │   │ expect     │   │ it fairly  │
│           │   │miss-│   │ do I ask?│   │ (a guess   │   │            │
│           │   │ ing?│   │          │   │ that can   │   │            │
│           │   │     │   │          │   │ be wrong)  │   │            │
└───────────┘   └─────┘   └──────────┘   └────────────┘   └────────────┘
                                                                 ↓
                ┌────────────┐   ┌──────────┐   ┌─────────┐   ┌──────┐
                │ CONCLUSION │ ← │ ANALYSIS │ ← │ RESULTS │ ← │ DATA │
                │ the answer │   │ why did  │   │ the     │   │ /CODE│
                │ + limits   │   │ it happen│   │ numbers │   │      │
                └────────────┘   └──────────┘   └─────────┘   └──────┘
```

**Our thesis, filled in:**

| Box | Our answer (short) |
|---|---|
| Problem | Small AI models think too long on code, even easy code |
| Gap | Nobody compared "train it to think shorter" with "switch thinking OFF" on one small model, for code |
| Question | Can training make it think shorter, keep its accuracy, and beat the OFF switch? |
| Hypothesis | At least 25% less thinking, accuracy drops by 3 points or less, better than OFF |
| Experiment | Same model, same test problems, 5 ways of answering |
| Data/Code | Code problems from Hugging Face, free GPU notebooks |
| Results | (not yet: we haven't run anything) |
| Analysis | (later) |
| Conclusion | (later) |

Two words you will hear a lot:
- **Hypothesis:** a guess you write down *before* testing, which the data can prove wrong.
- **Baseline:** the normal way, which you compare your idea against. Without it, "better" means nothing.

---

## 5. Try it (free, 5 minutes)

Take any claim you've heard, e.g. "coffee helps you study".
Fill in the chain on paper:

1. Problem: ?
2. Question: ?
3. Hypothesis: ?
4. Baseline (compare against what?): ?
5. What result would prove the hypothesis **wrong**?

If you can answer #5, you understand what makes a hypothesis scientific.

---

## 6. ✅ Check yourself

**Q1.** "I built an app that uses AI." Is that a thesis? Why or why not?

<details><summary>Answer</summary>
Not yet. It's a project. It becomes a thesis when there's a claim ("the app does X
better than Y") and evidence (a fair measurement against a baseline).
</details>

**Q2.** Our training fails and the model gets worse. Is the thesis ruined?

<details><summary>Answer</summary>
No. An honest bad result is still an answer to the question. You explain *why*
it failed. Hiding bad results ruins a thesis. Having them does not.
</details>

**Q3.** What is the baseline in our thesis?

<details><summary>Answer</summary>
The same model without our training: thinking ON (the normal way). Plus the free
options: thinking OFF, a thinking limit (budget), and a "think briefly" prompt.
</details>

---

## 7. You are here

```text
PART 0 ✅ The map  →  PART 1: What AI is  →  Tools  →  Research skills  →  Measure  →  Improve  →  Write
   ↑ you just finished this
```

**Next:** [Lesson 01: What an LLM is, and why](01-what-is-an-llm.md)

**Teacher questions about our thesis steps:** [qa/](../qa/README.md)
