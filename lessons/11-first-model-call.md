# Lesson 11: First model call (thinking ON vs OFF)

⬅️ [Lesson 10](10-hugging-face.md) · [ROADMAP](../ROADMAP.md) · ➡️ Lesson 12 (Reading a paper, written when you get there) · Hard word? See [GLOSSARY](../GLOSSARY.md)

Notebook: [`notebooks/11_first_model_call.ipynb`](../notebooks/11_first_model_call.ipynb)

---

## 1. In one sentence

**We load Gemma on a free GPU, ask it one easy code question with thinking ON and with thinking OFF, count the thinking tokens, and save every raw answer: the first real measurement of the thesis.**

---

## 2. What is it?

This is the moment Part 2 was for. Everything you learned is used once:

| Lesson | Used here |
|---|---|
| 02 Tokens | We count thinking tokens |
| 03 Learning | We only **use** the model; no training yet |
| 04 Thinking | We flip the switch ON and OFF |
| 07 GPU memory | We load the 4-bit model and print the memory |
| 08 Python | You can read every cell |
| 09 Colab | We run it on a free T4 and save to Drive |
| 10 Hugging Face | The model comes from there |

---

## 3. Why do we need it? (in our thesis)

Small run, four big answers:

1. **Does our setup work at all?** (model loads, fits in memory, writes an answer)
2. **Does the thinking switch really work?** Our whole comparison depends on it.
3. **Can we count thinking tokens correctly?** Every later number is built on this.
4. **How fast is the free GPU really?** PLAN.md §10 says our speed number is a guess. Here we get a real one.

This is also the **shape** of every later experiment: ask → count → save the raw answer.

---

## 4. How does it work?

### 4.1 The plan of the notebook

```text
1. nvidia-smi          → which GPU did we get?
2. install libraries   → Unsloth + transformers (copied from Unsloth's own T4 notebook)
3. settings            → model id, seed, limits, the question   (one cell, nothing hidden)
4. where to save       → Google Drive, append-only file
5. load the model      → 4-bit, prints memory used
6. CHECK THE SWITCH    → print both prompts, stop if they are the same
7. ask() function      → one answer + counts
8. run 4 answers       → 2 with thinking ON, 2 with OFF, saved one by one
9. table               → thinking tokens, total tokens, seconds, tokens/second
10. read one thinking part with your own eyes
11. peak memory and speed
```

### 4.2 The settings we chose, and why

| Setting | Value | Why |
|---|---|---|
| Model | `unsloth/gemma-4-E4B-it-unsloth-bnb-4bit` | The 4-bit version fits a free T4 (lesson 07) |
| Seed | 3407, plus the try number | Fixed seeds, so anyone can repeat the run |
| Sampling | `temperature=1.0, top_p=0.95, top_k=64` | Gemma's model card recommends exactly these |
| Same settings for ON and OFF | yes | Only **one** thing may differ: the thinking switch |
| Limit | 4,096 new tokens, same for both | A fair limit, and we record if an answer hits it |
| Question | our own easy question, **not** a test-set problem | So we never tune our prompts on the test set |

**Why sampling (not always the same answer)?** Our thesis asks each problem 4 times and averages.
Random answers are the point: they show how much the length varies (lesson 05).

### 4.3 The safety check inside the notebook

```python
assert "<|think|>" in on_text, "Thinking ON did not add the <|think|> token."
```

`assert` means: "if this is not true, stop with an error".
Gemma's card says thinking is ON when the special token `<|think|>` is in the prompt.
If our switch silently did nothing, every later number would be wrong. Better to crash than to lie.

⚠️ Note: Gemma's thinking is **OFF by default**. So we always set the switch on purpose, both ways.

### 4.4 How we count thinking tokens

Gemma writes the thinking between two markers: `<|channel>thought` … `<channel|>`.

```text
output tokens:  [<|channel>] [thought] [ … thinking … ] [<channel|>] [ … the answer … ]
                              └──────── we count these ────────┘
```

The notebook counts the tokens **between the two markers**, using the model's own output ids.
That is exact. If the markers are missing, it falls back to counting the text again and says so.

### 4.5 What we save (and why it matters)

Every answer is written as one line in a file on Google Drive, with the **raw text kept word for word**:

```json
{"problem_id": "lesson11_is_palindrome", "policy": "thinking_on", "sample_index": 0, "seed": 3407,
 "thinking_tokens": 812, "total_new_tokens": 1024, "seconds": 61.2, "hit_limit": false,
 "raw_output": "…the complete answer…"}
```

(Example only; the real numbers come from your run.)

Why raw text: re-counting or re-grading later is then **free**. Re-generating would cost GPU hours again (CLAUDE.md §4).

### 4.6 What this notebook does NOT do

- It does **not** run the code the model writes. That needs a sandbox (lesson 14).
- It does **not** grade the answer. So "correct or not" is **not** measured here.
- It does **not** train anything.

---

## 5. Try it (free, 20–40 minutes, needs a GPU)

⚠️ **Update 2026-09-19: use Kaggle, not Colab.** On a free Colab T4, loading ran out of memory. The fix needs more CPU memory than free Colab has ([qa/20](../qa/20-first-model-load-out-of-memory.md)).

1. Open Kaggle → **New Notebook → File → Import Notebook** → [`notebooks/11_first_model_call.ipynb`](../notebooks/11_first_model_call.ipynb).
2. In **Settings**: **Accelerator → GPU T4 x2**, **Internet → On** (Kaggle checks your phone number once).
   If "GPU T4 x2" is **grey**, your phone is not verified yet: profile picture → **Settings** → **Phone verification**, then reload the notebook.
3. Run the cells from top to bottom, **once each**. The model download (about 11 GB) is the slow part.
4. Write down these numbers:

| What | Your number |
|---|---|
| GPU name | |
| GPU memory after loading (Unsloth's older 9.891 GB did not hold, see qa/20) | |
| CPU memory after loading | |
| Average thinking tokens, thinking ON | |
| Average thinking tokens, thinking OFF | |
| Writing speed (tokens per second) | |
| Did any answer hit the 4,096 limit? | |

5. Read the thinking part in step 10. **Do you see overthinking** (lesson 05)? Which sentences were not needed?

⚠️ **We have not run this notebook yet.** It is written from the Gemma model card and Unsloth's official T4 notebook.
If a cell fails, that is not your mistake: copy the error to me, and we fix the notebook together. A failure is a finding, and it goes into DECISIONS.md.

---

## 6. ✅ Check yourself

**Q1.** Why does the notebook stop with an error if `<|think|>` is missing from the ON prompt?

<details><summary>Answer</summary>
Because then the thinking switch did nothing, and every later number would be wrong. It is better to stop than to save wrong results.
</details>

**Q2.** Why do we use the same seed and the same sampling settings for thinking ON and OFF?

<details><summary>Answer</summary>
So that only one thing differs: the thinking switch. That is what makes the comparison fair.
</details>

**Q3.** Why do we save the raw answer text and not only the token counts?

<details><summary>Answer</summary>
Because re-counting or re-grading raw text costs nothing, while generating the answers again costs GPU hours.
</details>

**Q4.** Why don't we run the model's code in this notebook?

<details><summary>Answer</summary>
Model-written code must only run in a sandbox (a safe closed box). That comes in lesson 14.
</details>

**Q5.** The question in the notebook is our own, not from HumanEval+. Why?

<details><summary>Answer</summary>
So we don't tune our prompts or settings while looking at the test problems. The test set stays untouched until the real experiment.
</details>

---

## 7. You are here

```text
PART 2: The tools → 07 ✅ → 08 ✅ → 09 ✅ → 10 ✅ → [11 ✅ First model call]    PART 2 DONE ✅
Next: PART 3: Research skills → 12 Reading a paper → 13 Finding a gap
```

**Research chain:** you have reached **DATA/CODE**. The next numbers you see will be your own.

**Explain-back test (Part 2).** In one or two sentences each:
1. Why doesn't the 16-bit Gemma fit on a free T4, and what do we load instead?
2. Why must results be saved to Drive while the notebook runs?
3. Where do the model and the datasets come from, and why is that our evidence?
4. What are the four things this first run is meant to tell us?

When you can, we start **Part 3: Reading papers**.
