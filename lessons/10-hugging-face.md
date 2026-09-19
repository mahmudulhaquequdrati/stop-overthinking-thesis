# Lesson 10: Hugging Face (the free library of models and data)

⬅️ [Lesson 09](09-colab-and-kaggle.md) · [ROADMAP](../ROADMAP.md) · ➡️ [Lesson 11: First model call](11-first-model-call.md) · Hard word? See [GLOSSARY](../GLOSSARY.md)

---

## 1. In one sentence

**Hugging Face is a free website where people share models and datasets; one line of Python downloads what we need, and its pages tell us the facts we must check (size, licence, cutoff date).**

---

## 2. What is it?

*Everyday example:* a **public library**.
- Shelves of models (Gemma, Qwen) and datasets (code problems with tests).
- Every item has an **id** like an ISBN: `google/gemma-4-E4B-it` = owner / name.
- Borrowing is free. Some items need you to sign a form first (**gated**).

```text
huggingface.co
   ├── Models     → google/gemma-4-E4B-it, unsloth/gemma-4-E4B-it-unsloth-bnb-4bit
   ├── Datasets   → evalplus/humanevalplus, livecodebench/code_generation_lite
   └── Spaces     → small free web apps (e.g. the Tokenizer Playground from lesson 02)
```

---

## 3. Why do we need it? (in our thesis)

- **Everything we use comes from there:** the model, the training problems, the test problems. All free.
- **It is our evidence.** When we say "the 4-bit file is 10.95 GB" or "the cutoff is January 2025",
  the Hugging Face page is the proof. A teacher can open the same page.
- **It is where we check ids.** PLAN.md §6 says: re-check every dataset id in the first data notebook.

---

## 4. How does it work?

### 4.1 A model page, part by part

Open https://huggingface.co/google/gemma-4-E4B-it:

| Part | What you learn | Our example |
|---|---|---|
| **Model card** (main text) | What it is, how to use it, training data | "cutoff date of January 2025" |
| **Files** tab | The real files and their sizes | `model.safetensors` ≈ 16 GB |
| **Licence** | What you may do with it | Apache-2.0 (free to use) |
| **Gated?** | Whether you must ask for access | Gemma-4-E4B: **no** (checked 2026-09-17) |
| Downloads / likes | How much others use it | — |

`safetensors` is just the file format that stores the model's numbers.

### 4.2 The same model, in different sizes

```text
google/gemma-4-E4B-it                          16.0 GB   16-bit, the original     ✗ too big for a T4
unsloth/gemma-4-E4B-it-unsloth-bnb-4bit        10.95 GB  4-bit, made by Unsloth   ✓ what we load
```

Same model, different packaging (lesson 07). We use the Unsloth 4-bit one (DECISIONS #8).

### 4.3 A dataset page

Open https://huggingface.co/datasets/evalplus/humanevalplus:
- **Dataset viewer:** a table where you can read the problems in the browser.
- **Files:** the raw data.
- **Splits:** parts of a dataset, like `train` and `test`. HumanEval+ has one split: `test` (164 problems).

⚠️ **Not every dataset has a viewer.** `livecodebench/code_generation_lite` uses a small Python loading script,
and Hugging Face refuses to run it ("runs arbitrary Python code", checked 2026-09-17).
So for LiveCodeBench we download its `.jsonl` files directly. Our notebook shows how.

### 4.4 Downloading in one line

```python
from datasets import load_dataset
humaneval = load_dataset("evalplus/humanevalplus", split="test")   # 164 problems
```

```python
from huggingface_hub import hf_hub_download
path = hf_hub_download("livecodebench/code_generation_lite", "test6.jsonl", repo_type="dataset")
```

For models, the loader takes the id too (lesson 11):

```python
model, tokenizer = FastModel.from_pretrained(model_name="unsloth/gemma-4-E4B-it-unsloth-bnb-4bit", load_in_4bit=True)
```

**Cache:** the download is kept on the session's disk. Running the cell again is fast.
But when the free session ends, the cache is wiped and the next session downloads again.

### 4.5 Accounts and tokens

- Reading public models and datasets: **no account needed**.
- A free account gives you a **token** (a password for programs). You need it only for
  gated models, private files, or uploading your own results.
- **Our rule:** a token is a secret. It never goes into a notebook or into git (CLAUDE.md §4).

---

## 5. Try it (free, 20 minutes)

### Part A: read the pages (5 minutes)
1. Open https://huggingface.co/google/gemma-4-E4B-it → **Files** tab. Find `model.safetensors` and its size.
2. Open https://huggingface.co/unsloth/gemma-4-E4B-it-unsloth-bnb-4bit → **Files**. Add up the model files. Is it about 10.95 GB?
3. Open https://huggingface.co/datasets/evalplus/humanevalplus → read 2 problems in the viewer.

### Part B: run the data notebook (15 minutes, no GPU)
1. Open Colab and upload [`notebooks/10_look_at_the_data.ipynb`](../notebooks/10_look_at_the_data.ipynb).
2. Run it from top to bottom.
3. Check you get: **164** HumanEval+ problems, **378** MBPP+ problems, and for LiveCodeBench from February 2025:
   **31 easy, 39 medium, 61 hard**.

**What you should notice:** these are the same numbers written in PLAN.md and in our research note.
You just checked our claims yourself. That is what "checkable" in lesson 00 means.

(We ran this notebook on 2026-09-17 and got exactly these numbers, on a normal computer without a GPU.)

---

## 6. ✅ Check yourself

**Q1.** What is a Hugging Face model id, and what are its two parts?

<details><summary>Answer</summary>
The name used to download a model, like `google/gemma-4-E4B-it`: the owner (google) and the model name.
</details>

**Q2.** Why do we download the Unsloth 4-bit version instead of Google's original?

<details><summary>Answer</summary>
The original is 16 GB in 16-bit and doesn't fit on a free 15 GB T4. The 4-bit version is 10.95 GB and fits.
</details>

**Q3.** Why can't we use `load_dataset` in the normal way for LiveCodeBench?

<details><summary>Answer</summary>
It uses a Python loading script. Hugging Face's viewer refuses to run it, and newer library versions may refuse too. We download its .jsonl files directly instead.
</details>

**Q4.** Why does the model download again in a new Colab session?

<details><summary>Answer</summary>
The cache lives on the session's computer. When the session ends, everything on it is wiped.
</details>

---

## 7. You are here

```text
PART 2: The tools → 07 ✅ → 08 ✅ → 09 ✅ → [10 ✅ Hugging Face] → 11 First model call
                                                 ↑ you just finished this
```

**Research chain:** **DATA/CODE**: you can now get the real data.

**Next:** [Lesson 11: First model call](11-first-model-call.md), where we finally run Gemma.
