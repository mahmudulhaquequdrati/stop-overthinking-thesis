# Lesson 06: Cutoff dates ("Has the model already seen the test?")

⬅️ [Lesson 05](05-overthinking.md) · [ROADMAP](../ROADMAP.md) · ➡️ Lesson 07 (GPU memory, written when you get there) · Hard word? See [GLOSSARY](../GLOSSARY.md)

---

## 1. In one sentence

**A model's cutoff date is the day its training text ends; if a test problem was on the internet before that day, the model may have already seen it, so a good score might be memory instead of skill.**

---

## 2. What is it?

### 2.1 Everyday example: the leaked exam

```text
Student A: studied, then solved the exam            → score shows SKILL
Student B: saw the exact exam questions last night  → score shows MEMORY
```

Both get 90%. Only one score tells you how good the student really is.

### 2.2 The cutoff date

A model learns from a huge pile of text collected up to a certain day. That day is the **cutoff date**.

```text
                cutoff date
                     │
 ────────────────────┼──────────────────────▶ time
  text before it:    │   text after it:
  the model MAY      │   the model has NOT
  have read it       │   read it ("fresh")
```

### 2.3 Contamination

When test problems were inside the training text, we call it **contamination**
(the test is "polluted" with things the model already saw).

---

## 3. Why do we need it? (in our thesis)

Three reasons:

1. **We chose our model partly because of it.** Gemma-4-E4B has a **published** cutoff: **January 2025**.
   Our backup, Qwen3.5-4B, has **no** published cutoff. That is a written downside of the backup (DECISIONS #9).
2. **It decides which test problems are "fresh".** LiveCodeBench problems from **Feb–Apr 2025** came out after Gemma's cutoff.
3. **A teacher will ask:** "How do you know the model didn't just memorize your test?" You need a clear answer.

---

## 4. How does it work?

### 4.1 What Gemma's model page says (✅ checked 2026-09-17)

On the Hugging Face page of `google/gemma-4-E4B-it`, section "Training Dataset":

> "Our pre-training dataset … includes web documents, code, images, audio, with a cutoff date of January 2025."

⚠️ **Read it carefully.** It says the **pre-training** data ends in January 2025 (lesson 03, stage 1).
It does **not** say when the data for the later stages (chat training, reasoning training) ends.
So "January 2025" is strong evidence, **not a 100% proof**. We say this honestly in the thesis.

### 4.2 Which of our test problems are fresh?

| Test set | When were the problems published? | Fresh for Gemma? |
|---|---|---|
| **LiveCodeBench**, Feb–Apr 2025 part | after Jan 2025 (LiveCodeBench stores a date for each problem) | ✅ fresh |
| LiveCodeBench, older part (from May 2023) | before Jan 2025 | ⚠️ may be seen |
| **HumanEval+** (164) | built on HumanEval, an older, very famous set | ⚠️ may be seen |
| **MBPP+** (378) | built on MBPP, an older, very famous set | ⚠️ may be seen |

(LiveCodeBench `release_v6`: 1,055 problems, May 2023 – Apr 2025, checked on Hugging Face.
How many are easy + medium **and** from Feb–Apr 2025: **not counted yet**.)

So: **most** of our test set may have been seen. Only a small part is surely fresh.

### 4.3 Then why is our experiment still fair?

Because of **how** we compare.

```text
The SAME model, on the SAME problems, 5 ways of answering:

   problem seen before?   thinking OFF  budget  "briefly"  ON   ON+LoRA
   yes (maybe)                 ↓          ↓        ↓        ↓      ↓
                         all 5 have the same "memory advantage"
```

- Our question is **not** "how good is Gemma at code?".
- Our question **is** "which way of answering gives the best balance of accuracy and length?".
- Memory helps **all 5 ways equally**, because it is the same model underneath.
  So the **comparison** stays fair, even if the absolute scores are a bit too high.

*Everyday example:* if all runners get the same tailwind, you can still see who is fastest.
You just can't claim a world record.

**Honest limit:** maybe memory affects *thinking length* differently (a remembered problem might need less thinking).
Testing "fresh vs. seen" separately is **future work** (DECISIONS #25).

### 4.4 Two different kinds of "seen before" — don't mix them up

| | Kind 1: seen in Google's training | Kind 2: seen in OUR training |
|---|---|---|
| What | Test problems were in Gemma's original training text | Test problems are in **our** fine-tuning data |
| Can we control it? | No, we can only pick fresh problems and compare fairly | **Yes** |
| What we do | Use the cutoff date; same problems for all 5 ways | **Overlap check** before training; drop DeepCoder's `lcbv5` part (it overlaps LiveCodeBench) |
| How bad if it happens | Scores a bit too high for all 5 ways | **Very bad**: only our trained model gets the advantage → unfair |

Kind 2 would make our trained model look better than it is. That's why the overlap check is a hard rule.

---

## 5. Try it (free, 10 minutes)

### Part A: check a fact yourself (like a researcher)

1. Open https://huggingface.co/google/gemma-4-E4B-it
2. Press **Ctrl+F** (Mac: **Cmd+F**) and search for `cutoff`.
3. Write down: which date? For which data (pre-training or all training)?

This is exactly how we turn "we assume" into "we checked".

### Part B: fresh or maybe seen? (paper and pen)

Gemma's cutoff is **January 2025**. For each problem, write **fresh** or **maybe seen**:

| Problem | Published |
|---|---|
| P1 | March 2025 |
| P2 | June 2023 |
| P3 | January 2025 |
| P4 | April 2025 |

<details><summary>Answers</summary>

- P1 (March 2025): **fresh**
- P2 (June 2023): **maybe seen**
- P3 (January 2025): **maybe seen**: it is in the cutoff month itself, so to be safe we count it as possibly seen.
  That's why our docs say "Feb–Apr 2025" for fresh problems, not "Jan–Apr".
- P4 (April 2025): **fresh**
</details>

---

## 6. ✅ Check yourself

**Q1.** What is a cutoff date?

<details><summary>Answer</summary>
The day the model's training text ends. The model has not read anything published after it.
</details>

**Q2.** Why is a test problem from before the cutoff a problem?

<details><summary>Answer</summary>
The model may have seen it (and its solution) during training, so a good score might be memory, not skill. This is called contamination.
</details>

**Q3.** Most of our test problems may have been seen by Gemma. Why is our comparison still fair?

<details><summary>Answer</summary>
All 5 ways of answering use the same model on the same problems, so any memory advantage is the same for all of them. We compare the ways of answering with each other, not Gemma with other models.
</details>

**Q4.** What is the difference between the cutoff problem and the overlap check?

<details><summary>Answer</summary>
The cutoff is about Google's original training (we can't control it). The overlap check is about our own fine-tuning data (we can control it). A test problem in our training data would help only our trained model, which would make the comparison unfair.
</details>

**Q5.** Gemma's page says "January 2025". Why is that not a 100% proof?

<details><summary>Answer</summary>
The date is for the pre-training data only. The page does not say when the data for later training stages ends.
</details>

---

## 7. You are here

```text
PART 1: What AI is → 01 ✅ → 02 ✅ → 03 ✅ → 04 ✅ → 05 ✅ → [06 ✅ Cutoffs]   PART 1 DONE ✅
                                                                  ↑ you just finished this
Next: PART 2: The tools → 07 GPU memory → 08 Python → 09 Colab/Kaggle → 10 Hugging Face → 11 First model call
```

**Research chain:** you now know the words for **PROBLEM → GAP → QUESTION → HYPOTHESIS**, and why our **EXPERIMENT** is fair.

---

## 8. Part 1 final check: explain it back

Part 1 is finished. Before Part 2 (where we start using real tools), explain these in your own words.
**One or two sentences each is enough.**

1. **Tokens (02):** What is a token, and why do more tokens take more time?
2. **Learning (03):** How does a model learn, and what is fine-tuning?
3. **Thinking (04):** What is "thinking", and what are our 5 ways of answering?
4. **Overthinking (05):** What is overthinking, and how can we see it with numbers?
5. **Cutoffs (06):** Why does the cutoff date matter, and why is our comparison still fair?

When you can explain all five, we start **Part 2, Lesson 07: GPU memory**.
