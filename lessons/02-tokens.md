# Lesson 02: Tokens

⬅️ [Lesson 01](01-what-is-an-llm.md) · [ROADMAP](../ROADMAP.md) · ➡️ [Lesson 03: How a model learns](03-how-a-model-learns.md) · Hard word? See [GLOSSARY](../GLOSSARY.md)

---

## 1. In one sentence

**A token is a small piece of text, about ¾ of a word. The model reads and writes text one token at a time, so tokens are how we measure the length of its thinking.**

---

## 2. What is it?

In lesson 01 we said the model writes "one piece at a time". **That piece is called a token.**

A token is **not always a whole word**. It can be:

| Kind of token | Example |
|---|---|
| A whole common word | `the`, `cat`, `def` |
| Part of a long or rare word | `over` + `thinking` |
| A space or symbol | `(`, `:`, `    ` (spaces in code) |
| A number or part of a number | `20` + `26` |

⚠️ These splits are **examples only**. Every model cuts text in its own way.
We will count Gemma's real tokens in lesson 11.

**Everyday example: LEGO bricks.**
A LEGO house is not built from one big piece. It is built from many small bricks.
Common shapes are one brick. Strange shapes need several small bricks.

```text
Text:     "Stop overthinking!"
Tokens:   [Stop] [ over] [thinking] [!]      ← 4 bricks (example split)
```

**Rule of thumb (for English text):** 100 tokens ≈ 75 words.
Code often needs **more** tokens, because of symbols and spaces.

---

## 3. Why do we need it? (in our thesis)

**Almost every number in our thesis is counted in tokens.**

| Where in our thesis | The token number |
|---|---|
| Our hypothesis | The trained model uses **at least 25% fewer thinking tokens** |
| Training example limit | At most **3,500 tokens** (GPU memory limit) |
| Test thinking limit | The same for every way of answering, e.g. **8,000 tokens** |
| Thinking budget (one way of answering) | "Stop thinking after k tokens" |
| Thinking on hard problems | Often **10,000–15,000 tokens** (why we skip them) |
| GPU time | Training ≈ **3.6 million tokens** ≈ 4 hours (estimate) |

So if you understand tokens, you can read our plan.

---

## 4. How does it work?

### 4.1 Text becomes tokens, tokens become numbers

A computer can't read letters. It only works with numbers.
So a tool called a **tokenizer** does two jobs:

```text
"def add(a, b):"
       │  tokenizer cuts the text
       ▼
[def] [ add] [(] [a] [,] [ b] [):]
       │  each token has an ID number in the model's "dictionary"
       ▼
[ 822, 1147, 7, 64, 11, 275, 2599 ]      ← made-up ID numbers, just to show the idea
       │
       ▼
   THE MODEL  (works with numbers)
       │
       ▼
next token's ID  →  turned back into text  →  " return"
```

### 4.2 One token = one turn of the loop

Remember the loop from lesson 01. **Each turn writes exactly one token.**

```text
turn 1 → "def"
turn 2 → " add"
turn 3 → "("
...
```

So:

```text
more tokens  =  more turns of the loop  =  more time
```

### 4.3 Let's feel the time (made-up speed, just for the idea)

Imagine the model writes **20 tokens per second**. (This is an example, not a measured speed.)

| What the model writes | Tokens | Time at 20 tokens/second |
|---|---|---|
| A short answer, thinking OFF | 100 | 5 seconds |
| Short thinking + answer | 500 | 25 seconds |
| Long thinking + answer | 2,500 | about 2 minutes |
| Very long thinking (hard problem) | 10,000 | about 8 minutes |

Now multiply by **1,000 test problems × 4 tries × 5 ways of answering**.
That's why overthinking is expensive, and why we count tokens.

### 4.4 Why count tokens and not seconds?

Seconds change with the computer: a fast GPU gives fewer seconds, a slow GPU more.
**The token count stays the same on any computer.** So tokens make a fair comparison.

```text
Same answer on a slow GPU:  2,500 tokens, 4 minutes
Same answer on a fast GPU:  2,500 tokens, 30 seconds
                            ─────────────
                            the token count doesn't change
```

---

## 5. Try it (free, 5 minutes)

1. Open the free **Tokenizer Playground**: https://huggingface.co/spaces/Xenova/the-tokenizer-playground
   (It is a Hugging Face page. It may take a moment to load.)
2. Pick any model from its list. (Gemma may not be in the list. That's fine: the idea is the same.)
3. Type: `The cat sat on the mat.` → count the tokens.
4. Type: `Stop overthinking, keep passing the tests.` → which words are split into pieces?
5. Paste this code:
   ```python
   def is_even(n):
       return n % 2 == 0
   ```
   → count the tokens. Are there more tokens than words?

**What you should notice:** common words are one token; long or rare words get cut into pieces;
code has many small tokens for symbols and spaces.

---

## 6. ✅ Check yourself

**Q1.** What is a token, in one sentence?

<details><summary>Answer</summary>
A small piece of text (about ¾ of a word) that the model reads or writes in one step.
</details>

**Q2.** A model writes 2,000 tokens of thinking on one problem. Another way of answering writes 1,000. Which one takes more time, and why?

<details><summary>Answer</summary>
The 2,000-token one. Each token is one turn of the loop, so twice the tokens is about twice the writing time.
</details>

**Q3.** Why does our thesis measure thinking in tokens, not in seconds?

<details><summary>Answer</summary>
Seconds depend on the computer (fast or slow GPU). The number of tokens stays the same on any computer, so it is a fair way to compare.
</details>

**Q4.** Our hypothesis says "at least 25% fewer thinking tokens". Thinking ON uses 2,000 tokens on average. What is the most the trained model may use?

<details><summary>Answer</summary>
1,500 tokens. 25% of 2,000 is 500, and 2,000 − 500 = 1,500.
</details>

**Q5 (the mix-up from lesson 01).** Does the model take longer when thinking because it is searching for information?

<details><summary>Answer</summary>
No. It knows everything from training already; it doesn't search. It takes longer because it writes more tokens, one at a time.
</details>

---

## 7. You are here

```text
PART 1: What AI is  →  01 ✅ LLM  →  [02 ✅ Tokens]  →  03 Learning  →  04 Thinking  →  05 Overthinking  →  06 Cutoffs
                                          ↑ you just finished this
```

**Research chain:** still learning the words for **PROBLEM**. Now you can read "25% fewer thinking tokens" in our hypothesis.

**Explain-back test:** tell me in your own words:
1. What is a token?
2. Why does writing more tokens take more time?
3. Why do we count tokens instead of seconds?

When you can, we write **Lesson 03: How a model learns**.

➡️ Lesson 03 is written: [How a model learns](03-how-a-model-learns.md). Its explain-back test also includes the questions from this lesson.
