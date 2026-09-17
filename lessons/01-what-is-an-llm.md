# Lesson 01: What an LLM is, and why it exists

⬅️ [Lesson 00](00-what-is-a-thesis.md) · [ROADMAP](../ROADMAP.md) · ➡️ Lesson 02 (Tokens, written when you get there) · Hard word? See [GLOSSARY](../GLOSSARY.md)

---

## 1. In one sentence

**An LLM is a program that read a huge amount of text and learned one skill: guess the next word. It does this again and again, and that one skill writes answers, code and explanations.**

---

## 2. What is it?

**LLM** = **L**arge **L**anguage **M**odel.

| Word | Meaning |
|---|---|
| **Large** | Very big: billions of numbers inside it (our model has 8 billion) |
| **Language** | It works with text: words, sentences, code |
| **Model** | A program that learned from examples instead of being hand-programmed with rules |

**Everyday example: your phone keyboard.**

When you type *"See you"*, your phone suggests *"tomorrow"*.
It guesses the next word from what usually comes next.

```text
Phone keyboard:   "See you"  →  tomorrow        (learned from your messages)
An LLM:           "See you"  →  tomorrow        (learned from a huge part of the internet,
                                                  books, and code)
```

An LLM is that same idea, but **much, much bigger**. So its guesses are good enough to:
- answer questions
- write working code
- explain things
- translate

---

## 3. Why does it exist? And why do we need it?

**Why it exists:** before LLMs, you had to talk to a computer in *its* language
(buttons, menus, programming). An LLM lets you use **your** language:
*"Write a Python function that sorts a list."* → it writes the code.

**Why we need it in our thesis:** our whole thesis is about **one LLM**
(Gemma-4-E4B) and how much it writes *before* its answer. To understand
"overthinking", you first need to see that an LLM writes **one piece at a time**.
(A piece is called a *token*: a small piece of text, about ¾ of a word. Lesson 02 is about tokens.)
Every extra piece costs time.

---

## 4. How does it work?

### Step by step

```text
You type:  "Write a function that adds two numbers"
                         │
                         ▼
          ┌──────────────────────────────┐
          │          THE MODEL           │
          │  "What piece of text most    │
          │   likely comes next?"        │
          └──────────────────────────────┘
                         │
                         ▼
               writes one piece:  "def"
                         │
      ┌──────────────────┘
      │  The new piece is added to the text, and the model is asked again:
      ▼
   "...numbers def"        → next piece:  " add"
   "...numbers def add"    → next piece:  "("
   "...def add("           → next piece:  "a"
      ...  again and again ...
   until it writes a special "I'm done" piece.
```

**The key idea: it's a loop.** The model never writes the whole answer at once.
It writes **one small piece, adds it, and repeats.**

### How did it learn to guess well?

```text
1. Collect a huge amount of text (web pages, books, code)
2. Hide the next word:   "The cat sat on the ___"
3. Model guesses:        "car"     ✗  → adjust its numbers a tiny bit
4. Model guesses:        "mat"     ✓  → adjust a tiny bit the other way
5. Repeat billions of times
```

The "billions of numbers" inside the model are what gets adjusted.
After enough practice, those numbers hold patterns of language, facts, and code.
(Lesson 03 explains learning in more detail.)

### Where "thinking" fits (the link to our thesis)

Some newer LLMs are **reasoning models**. Before the answer, they first write
**thinking**: notes to themselves, like working on scrap paper.
Many new models have a **switch**: thinking ON or thinking OFF.

```text
Question: "Is 91 a prime number?"

THINKING (scrap paper, written piece by piece):
  "Let me check. 91 ÷ 7 = 13. So 91 = 7 × 13. Not prime."

ANSWER:
  "No, 91 = 7 × 13."
```

Thinking is **also written one piece at a time, with the same loop.**
So **more thinking = more loop turns = more time and computer power.**

```text
Easy question, short thinking:    ████               → fast
Easy question, LONG thinking:     ████████████████   → slow, same answer  ← "overthinking"
```

**That's our thesis problem.**

### ⚠️ A common mix-up: "thinking = searching for information"

It is easy to think the model **searches** or **collects** information while it thinks.
**It does not.**

```text
❌ Wrong picture:  a librarian running to the shelves to find facts   (slow because of searching)
✅ Right picture:  a person writing a long draft by hand, word by word (slow because of writing)
```

- Everything the model knows is **already inside its numbers**, from training.
  While answering, it does not look anything up. (Our Gemma model in the notebook has no internet.)
- Its thinking notes often **do** check the answer ("let me test this with 91…").
  But checking is just **more text it writes**.
- So the time comes from **how many pieces it writes**, not from searching.

Some chat websites add a separate web-search tool. That is an extra tool, not the model's thinking.

---

## 5. Try it (free, 5 minutes)

1. Open any free AI chat in your browser (for example gemini.google.com, chatgpt.com or claude.ai).
2. Type: **"Write a Python function that checks if a number is even."**
3. **Watch the answer appear.** Notice it comes in **word by word** (or small chunks), not all at once. That's the loop.
4. Now type: **"Is 97 a prime number? Think step by step."**
5. Notice the answer is much longer. The step-by-step part is like thinking: **more pieces written = more waiting.**

**What you should notice:** asking for step-by-step thinking made the response longer and slower, even though the final answer ("yes, prime") is one word.

---

## 6. ✅ Check yourself

**Q1.** In one sentence, what is the one skill an LLM learned?

<details><summary>Answer</summary>
Guessing the next piece of text, based on everything written so far.
</details>

**Q2.** Why does an answer appear word by word instead of all at once?

<details><summary>Answer</summary>
Because the model works in a loop: it writes one piece, adds it to the text, then
guesses the next piece again. The screen shows each piece as it's made.
</details>

**Q3.** Why does "thinking" cost time, even when the final answer is short?

<details><summary>Answer</summary>
Thinking is written with the same loop, one piece at a time. A long thinking part
means many extra loop turns before the answer, even if the answer itself is one word.
</details>

**Q4 (harder).** Our thesis wants the model to think *shorter*. Why can't we just always switch thinking OFF?

<details><summary>Answer</summary>
On some problems, thinking is what makes the answer correct, like scrap paper for a
hard sum. Switching it OFF may cause wrong answers. We want short thinking where
short is enough. That's exactly what our experiment tests. (Thinking OFF is one
of the things we compare against.)
</details>

---

## 7. You are here

```text
PART 0 ✅  →  PART 1: What AI is  [01 ✅ LLM] → 02 Tokens → 03 Learning → 04 Thinking → 05 Overthinking → 06 Cutoffs
                                      ↑ you just finished this
```

**Research chain:** in this lesson we are before **PROBLEM**. We're learning the words we need
to understand the problem.

**Explain-back test:** tell me in your own words: *what is an LLM, and why does thinking cost time?*
When you can, we write **Lesson 02 — Tokens**.
