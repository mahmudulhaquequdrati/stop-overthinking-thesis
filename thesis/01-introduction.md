# 1. Introduction

## 1.1 The problem

AI models that write text, called **large language models** (LLMs), are now used every day to write computer
code. A newer kind, the **reasoning model**, does something extra. Before it answers, it writes a **thinking**
part: notes to itself, like a student's rough work on scrap paper. Then it writes the answer.

Thinking often helps. But it has a price. Every word the model writes costs time, electricity and money.
Researchers have noticed that reasoning models often **overthink**. They write long thinking even for easy
questions, where a short answer would be just as correct (Sui et al., 2025).

> **Everyday example.** A student writes five pages for every exam question, even "what is 2 + 2?". The
> answers are not better, but the exam takes much longer.

This matters most for **small** models. Small models are cheap and can run on one ordinary graphics card
(GPU). That is why people use them. If they waste most of their time on unneeded thinking, that advantage
is lost.

## 1.2 Two ways to fix it

There are two kinds of fixes.

**The free fixes** need no training:

| Free fix | How it works |
|---|---|
| Thinking OFF | Many 2026 models have a switch that turns thinking off. The model answers directly. |
| Thinking limit | Let the model think, but stop it after a fixed number of words and make it answer. |
| "Think briefly" | Ask the model in the question to keep its thinking short. |

**The trained fix** teaches the model to think shorter by itself. A simple way is: let the model answer each
practice problem several times, keep its **shortest answer that is still correct**, and train the model on those
short answers (Munkhbat et al., 2025). Earlier work did this on math, and on code with larger models of 7–8 billion
parameters, and reported 23–40% shorter thinking (SEER, 2025; ASAP, 2025).

## 1.3 The gap

The trained fix costs work and computer time. The free fixes cost nothing. So the key question is:
**is training worth it compared with the free fixes, on the same model?**

We found no study that answers this for a small model that has a thinking switch, on code. Earlier training
studies used models without a switch, so they could not compare with "thinking off". Studies of the switch
(for example HRBench, 2026) compared ways of using the switch, but not a model trained to think shorter.

## 1.4 The research question

> **On a small model with a thinking switch, does training on its own shortest correct code answers give a
> better balance of accuracy and thinking length than the free options?**

We expected yes. Our hypothesis had three parts. Compared with normal thinking, the trained model would:

1. **H1:** use at least **25% less** thinking;
2. **H2:** lose **no more than 3 points** of accuracy;
3. **H3:** be **more accurate** than thinking off, the thinking limit, and "think briefly".

All three rules were written down **before** we saw any result (Chapter 3). This matters: it stops us from
choosing the rules later to fit the results.

## 1.5 What we did, in short

```text
PROBLEM → GAP → QUESTION → HYPOTHESIS → EXPERIMENT → DATA → RESULTS → ANALYSIS → CONCLUSION
 1.1       1.3    1.4        1.4          Ch. 3        Ch. 3   Ch. 5     Ch. 6      Ch. 7
```

- **Model:** Qwen3.5-2B, a small 2026 reasoning model with a thinking switch.
- **Test:** 234 code problems from HumanEval+ and LiveCodeBench.
- **Six ways of answering:** thinking ON, thinking OFF, "think briefly", a thinking limit, and two trained versions.
- **Checking:** every answer's code was run against the test sets' own tests. Chapter 4 explains exactly how we
  count a pass, compute accuracy, and decide whether a difference is real.

## 1.6 What we found, in short

The answer was **no**. Training did not make the model think shorter on the test problems. The free thinking
limit was the most accurate way of all. The reason surprised us: the long answers were mostly **loops**, not
careful thinking. Chapters 5 and 6 show the evidence.

## 1.7 Contributions

1. **A fair, same-model comparison** of a trained "think shorter" model against all three free options, on code,
   with rules fixed in advance.
2. **Evidence that the main waste in a small reasoning model is looping**, not long careful thinking, and that
   training on short correct answers does not remove it.
3. **Evidence that a simple thinking limit is a strong, free fix**, including a check that our token limit did
   not unfairly hurt normal thinking.
4. **Everything is open:** every raw answer, every grade, the scripts and the trained add-ons, so anyone can
   check or repeat the work.

## 1.8 How this thesis is organised

| Chapter | What it covers |
|---|---|
| 2. Background | What LLMs, tokens, thinking, LoRA and code test sets are; earlier work |
| 3. Method | The six ways of answering, the data, the training, the fairness rules |
| 4. How we measure | How a pass is decided, how accuracy, points, error bars and loops are computed |
| 5. Results | All numbers, tables and charts |
| 6. Analysis | Why it happened, how it fits earlier work, and what could be wrong |
| 7. Conclusion and future work | The answer, advice, and what to test next (including bigger models) |
