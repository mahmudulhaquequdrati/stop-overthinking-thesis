# Lesson 03: How a model learns (training and fine-tuning)

⬅️ [Lesson 02](02-tokens.md) · [ROADMAP](../ROADMAP.md) · ➡️ [Lesson 04: Reasoning models and "thinking"](04-reasoning-models-and-thinking.md) · Hard word? See [GLOSSARY](../GLOSSARY.md)

---

## 1. In one sentence

**A model learns by guessing the next token, seeing the right token, and nudging its numbers a tiny bit toward the right one. Fine-tuning is doing a little more of this on our own examples, to teach it a new habit.**

---

## 2. What is it?

### 2.1 Everyday example: learning to throw darts

```text
1. Throw a dart.
2. Look: it landed a bit too far left.
3. Next time, aim a tiny bit more to the right.
4. Repeat 1,000 times → you get good.
```

A model learns in the same way:

| Darts | Model |
|---|---|
| Throw | Guess the next token |
| See where it landed | Compare with the real next token |
| How far off | An **error score** (big = very wrong, small = almost right) |
| Aim a tiny bit differently | **Nudge** its numbers a tiny bit |
| Repeat 1,000 times | Repeat billions of times |

### 2.2 What are "its numbers"?

In lesson 01 we said the model is a huge list of numbers. Gemma-4-E4B has **8.0 billion** of them.
These numbers are called **parameters** (or *weights*).

- The numbers decide which next token the model likes most.
- **Learning = changing these numbers.** Nothing else changes.
- After training, all the "knowledge" and "habits" are stored in these numbers.

*Everyday example:* a huge mixing desk with 8 billion small knobs.
Training turns each knob a tiny bit, again and again, until the music sounds right.

---

## 3. Why do we need it? (in our thesis)

**Our whole method is one fine-tuning run.**

```text
Normal Gemma  →  fine-tune on its own SHORT correct answers  →  Gemma that thinks shorter (we hope)
```

To understand our thesis you must understand:
1. **What the model learns from our examples:** a **habit** (think shorter), not new facts.
2. **Why it can go wrong:** it may learn "always stop early" (so we have the selection rule, lesson 19).
3. **Why training is harder for the GPU than answering:** so training examples have a lower limit
   (3,500 tokens) than the test thinking limit (e.g. 8,000 tokens).
4. **Why we use LoRA** (a small add-on) instead of changing all 8 billion numbers (lesson 18).

---

## 4. How does it work?

### 4.1 One training step, with a tiny example

Training example: `def add(a, b): return a + b`

The model sees the start and must guess the next token:

```text
Model sees:   "def add(a, b): return a +"
Model guesses (made-up numbers, just for the idea):
      " b"  → 60%
      " a"  → 30%
      " 1"  → 10%
Right answer:  " b"
Error score:   small, but not zero (it was only 60% sure)
Nudge:         change the numbers a tiny bit, so " b" gets more likely next time (e.g. 61%)
```

This happens for **every token** in the example, then for the next example, and so on.

### 4.2 The learning loop

```text
        ┌───────────────────────────────────────────────┐
        ▼                                               │
  take an example → guess each next token → compare with the real tokens
                                                        │
                                           error score (how wrong?)
                                                        │
                                      nudge all numbers a tiny bit
                                                        │
                                       next example ────┘
```

Two words you will see later:
- **Learning rate:** **how big** each nudge is. Too big → the model jumps around and breaks. Too small → it learns very slowly.
- **Epoch:** one full pass through all the training examples. Our plan: **1 epoch** (the closest paper, Munkhbat et al. 2025, also used 1).

### 4.3 Three stages of training (a typical recipe)

A model like Gemma is not trained just once. A **typical** recipe has stages.
(⚠️ This is the general idea. We did not check Gemma-4's exact recipe.)

```text
STAGE 1: Pre-training           STAGE 2: Chat training           STAGE 3: Reasoning training
huge amounts of text            questions + good answers         problems + thinking + answer
learns: language, facts, code   learns: to answer questions      learns: to think before answering
cost: giant (big companies)     cost: large                      cost: large
        │                              │                                 │
        └──────────────────────────────┴─────────────────────────────────┘
                                       │
                          Gemma-4-E4B (what we download)
                                       │
                         STAGE 4 (OURS): fine-tuning
                         our short correct answers
                         learns: a habit, think shorter
                         cost: ~4 GPU-hours (estimate)
```

All stages use the **same loop** from 4.2. Only the examples change.

### 4.4 What is fine-tuning?

**Fine-tuning = take a model that is already trained, and train it a little more on your own examples.**

*Everyday example:* a trained cook (already knows cooking) takes a short course
"cook faster, same taste". The cook doesn't relearn cooking. They learn a new habit.

| | Training from zero | Fine-tuning (ours) |
|---|---|---|
| Starts from | random numbers | an already-trained model |
| Examples needed | billions of tokens | thousands of examples (our plan: ~2,000) |
| Cost | huge | small (our estimate: ~4 GPU-hours on a free T4) |
| Learns | everything | one new habit |

The kind of fine-tuning we do is called **SFT** (supervised fine-tuning):
we show the model **example answers** and it learns to write like them.

### 4.5 How does "think shorter" get learned?

Nobody tells the model "be shorter". It learns it **from the examples**.

```text
Our training examples all look like:
   problem  →  SHORT thinking  →  correct code

After ~2,000 of them, the nudges add up:
   "stop thinking and write the code" becomes more likely earlier.
```

*Everyday example:* a student who reads 2,000 short, correct model solutions
starts to write shorter solutions too, without anyone saying "be short".

### 4.6 Why training needs more GPU memory than answering

| Answering | Training |
|---|---|
| Keep the model's numbers | Keep the model's numbers |
| Write tokens | **Also** keep many in-between results, to work out how to nudge each number |
| | **Also** keep extra notes for the nudging |

So the same GPU can **answer** with long text (8,000 tokens) but can only **train** on shorter examples (~3,500 tokens).
That is why the memory check (lesson 17) comes before training.

### 4.7 Two dangers

| Danger | What happens | Our protection |
|---|---|---|
| **Learning the wrong habit** | Model learns "always stop early", fails harder problems | Selection rule: skip answers shorter than half the median |
| **Forgetting** | Changing all numbers can damage old skills | LoRA: the original numbers stay unchanged; we only train a small add-on (lesson 18) |

---

## 5. Try it (free, 5 minutes)

Watch a tiny model learn in your browser. No code, no account.

1. Open the **TensorFlow Playground**: https://playground.tensorflow.org/
2. Press the big **▶ play** button (top left).
3. Watch the number **"Training loss"** (top right). *Loss* = the error score.
4. Watch the picture on the right change as the model learns.
5. Press reset, change **"Learning rate"** (top) to a big value like 3 or 10, and press ▶ again.

**What you should notice:**
- The error score goes **down** step by step. That is learning.
- With a very big learning rate, the error jumps around or doesn't go down. The nudges are too big.
- This tiny model has only a few numbers. Gemma has 8 billion, but the loop is the same.

---

## 6. ✅ Check yourself

**Q1.** In one sentence: how does a model learn?

<details><summary>Answer</summary>
It guesses the next token, compares with the right token, and nudges its numbers a tiny bit toward the right one, again and again.
</details>

**Q2.** What actually changes inside the model when it learns?

<details><summary>Answer</summary>
Only its numbers (parameters / weights). All knowledge and habits are stored in these numbers.
</details>

**Q3.** What is the difference between training from zero and fine-tuning?

<details><summary>Answer</summary>
Training from zero starts from random numbers and needs a huge amount of text. Fine-tuning starts from an already-trained model and needs only a small set of examples to teach a new habit.
</details>

**Q4.** In our thesis, nobody tells the model "think shorter". How does it learn it?

<details><summary>Answer</summary>
From the examples: every training example has short thinking and correct code. After many examples, the small nudges add up, and short thinking becomes the more likely habit.
</details>

**Q5.** Why is our training-example limit (3,500 tokens) lower than our test thinking limit (e.g. 8,000)?

<details><summary>Answer</summary>
Training needs much more GPU memory than answering, because it must keep in-between results to work out the nudges. So the same GPU can answer long texts but only train on shorter ones.
</details>

**Q6.** What is the learning rate, and what happens if it is too big?

<details><summary>Answer</summary>
How big each nudge is. If it is too big, the model jumps around and can break instead of learning.
</details>

---

## 7. You are here

```text
PART 1: What AI is → 01 ✅ LLM → 02 ✅ Tokens → [03 ✅ Learning] → 04 Thinking → 05 Overthinking → 06 Cutoffs
                                                     ↑ you just finished this
```

**Research chain:** still learning the words for **PROBLEM** and **EXPERIMENT**.
Now you can read "train one LoRA add-on, 1 epoch, ~2,000 examples" in our plan.

**Explain-back test.** Tell me in your own words. (Lesson 02's questions are here too, because we moved on before you answered them.)

From lesson 02:
1. What is a token?
2. Why does writing more tokens take more time?

From lesson 03:
3. How does a model learn? (Use the darts example if it helps.)
4. What is fine-tuning, and how will our model learn to think shorter?

When you can, we write **Lesson 04: Reasoning models and "thinking"**.
