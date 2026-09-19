# Lesson 07: GPU memory

⬅️ [Lesson 06](06-cutoff-dates.md) · [ROADMAP](../ROADMAP.md) · ➡️ [Lesson 08: Python basics](08-python-basics.md) · Hard word? See [GLOSSARY](../GLOSSARY.md)

---

## 1. In one sentence

**A GPU has a fixed amount of memory (a free T4 has about 15 GB); the model's numbers, the text it is working on, and (when training) extra training notes must all fit inside, or the program crashes.**

---

## 2. What is it?

### 2.1 What is a GPU?

A **GPU** is a computer chip that does many small math steps **at the same time**.
A normal chip (CPU) is like 8 very smart workers. A GPU is like 2,000 simple workers.
A model needs billions of simple multiplications, so the GPU is much faster.

### 2.2 What is GPU memory?

The GPU has its **own** memory (also called **VRAM**). Everything the GPU works on must be **inside** it.

*Everyday example: a desk.*

```text
┌──────────────────── the desk (GPU memory, ~15 GB) ────────────────────┐
│  [ the model's numbers ]  [ notes about the text so far ]  [ free ]   │
└────────────────────────────────────────────────────────────────────────┘
If you put more on the desk than fits → things fall off → the program crashes ("out of memory").
```

### 2.3 Our desk: a free T4

- Colab and Kaggle give a free **NVIDIA T4** GPU.
- It is a 16 GB card. The software shows **14.563 GB** usable (Unsloth's notebook on a T4, checked).
- In our docs we round this to "a 15 GB GPU".

---

## 3. Why do we need it? (in our thesis)

Memory decides three big things in our plan:

| Decision | Because of memory |
|---|---|
| Model: Gemma-4-E4B, **4-bit version** | The normal version (16 GB) doesn't fit on a 15 GB desk |
| Not a 9B model | Training it would need ~22 GB |
| Training examples ≤ **3,500 tokens** | Training needs extra memory for each token |
| **Memory check** in week 3 (≤ 14 GB) | If it doesn't fit, we switch to the backup model |

---

## 4. How does it work?

### 4.1 Memory for the model's numbers

A model is a list of numbers (parameters). Each number takes some space:

| Format | Space per number | Detail |
|---|---|---|
| 16-bit | **2 bytes** | normal |
| 4-bit | **0.5 byte** | squeezed (a bit less exact) |

**Simple rule:** memory = number of parameters × bytes per number.
1 billion numbers × 1 byte = 1 GB.

### 4.2 Gemma-4-E4B, worked out

Gemma-4-E4B has **8.0 billion** numbers (7,996,156,490, checked on Hugging Face).

```text
All 16-bit:   8.0 billion × 2 bytes = 16.0 GB     ✗ bigger than our 15 GB desk
```

The Unsloth 4-bit version doesn't squeeze everything. Some parts stay 16-bit (the word lookup table, image and audio parts):

```text
Squeezed to 4-bit:   3.50 billion × 0.5 byte = 1.75 GB
Kept at 16-bit:      4.60 billion × 2 bytes  = 9.20 GB
                                               ────────
Total                                          10.95 GB   ✓ fits
```

And the real file on Hugging Face is **10.95 GB** (checked). Our simple math matches exactly.

*Everyday example:* a photo album where only some photos are saved as small JPEGs; the rest stay full size.

### 4.3 Memory that grows while the model writes

When the model writes, it keeps **notes about every earlier token**, so it doesn't redo work each step.
These notes are called the **KV cache**.

```text
after 100 tokens:    [model] [■]
after 2,000 tokens:  [model] [■■■■■■]
after 8,000 tokens:  [model] [■■■■■■■■■■■■■■■■]
```

- Longer thinking → more notes → more memory.
- Answering **many problems at the same time** (to be faster) → notes for all of them → even more memory.
- How much Gemma-4-E4B needs per token: **not measured yet** (lesson 11 and week 3).

### 4.4 Training needs even more (lesson 03)

```text
Answering:  [model numbers] [notes about the text]
Training:   [model numbers] [notes about the text] [in-between results for the nudges] [LoRA add-on + its training notes]
```

That's why training examples have a lower limit (3,500 tokens) than answering (e.g. 8,000 tokens).

**Measured by Unsloth on a free T4** (checked in their notebook):

| Moment | Memory |
|---|---|
| After loading Gemma-4-E4B 4-bit | **9.891 GB** |
| Peak during a short LoRA training (examples up to 1,024 tokens) | **10.715 GB** |

Our examples are longer (up to 3,500 tokens), so our peak will be higher. **How much higher is the memory check** (week 3, rule: ≤ 14 GB).

⚠️ **Update 2026-09-19:** the 9.891 GB came from an older Unsloth. With Unsloth 2026.9.7, loading crashed on our T4. See §4.6.

### 4.6 What really happened on our T4 (2026-09-19)

Two lessons from our first real run:

1. **A "4-bit model" still has big 16-bit parts.** Gemma's *per-layer word table* stays 16-bit:
   262,144 words × 42 layers × 256 numbers × 2 bytes = **5.25 GB**.
2. **Changing a number's format needs double space for a moment.** The T4 can't compute in bf16, so the loader converts that table to float16. While it converts, the old and the new copy both exist:

```text
10.22 GB (model) + 5.25 GB (new copy of the table) = 15.47 GB  >  14.56 GB  → crash
```

**The fix:** keep that one table in normal computer memory (CPU memory), and everything else on the GPU.
Full story: [results/2026-09-19-notebook11-out-of-memory.md](../results/2026-09-19-notebook11-out-of-memory.md) · [qa/20](../qa/20-first-model-load-out-of-memory.md).

### 4.5 A small warning about "GB"

Computers count memory in two slightly different ways (1,000 × 1,000 × 1,000 bytes, or 1,024 × 1,024 × 1,024 bytes).
The difference is about 7%. File sizes on Hugging Face use the first; GPU tools often use the second.
For this lesson we ignore it. When we compare with the 14 GB rule, we use the number the GPU tool prints.

---

## 5. Try it (free, 10 minutes, pen and paper)

Use: memory = parameters × bytes per number (16-bit = 2 bytes, 4-bit = 0.5 byte).

1. **Qwen3.5-4B** (our backup) has **4.66 billion** numbers. How big is it in 16-bit?
2. Does it fit on our ~15 GB desk (just the numbers)?
3. **Qwen3.5-9B** has **9.65 billion** numbers. How big in 16-bit? Does it fit?
4. If Qwen3.5-9B were fully squeezed to 4-bit, how big would it be?
5. Why did we still say "not a 9B model"? (Hint: lesson 03 and §4.4.)

<details><summary>Answers</summary>

1. 4.66 × 2 = **9.32 GB**. (The real file on Hugging Face is 9.32 GB, checked.)
2. **Yes**, with ~5 GB left for notes and training.
3. 9.65 × 2 = **19.3 GB** → **no**, too big.
4. 9.65 × 0.5 ≈ **4.8 GB** (in real life a bit more, because some parts stay 16-bit).
5. **Training** needs much more than the numbers: 16-bit LoRA training of Qwen3.5-9B needs ~22 GB, and Unsloth advises against 4-bit training for Qwen3.5 (DECISIONS #7).
</details>

---

## 6. ✅ Check yourself

**Q1.** What happens if the model and its work don't fit in GPU memory?

<details><summary>Answer</summary>
The program crashes with an "out of memory" error.
</details>

**Q2.** Why does Gemma-4-E4B take 16 GB in 16-bit but only 10.95 GB in the Unsloth 4-bit version?

<details><summary>Answer</summary>
In 16-bit each number takes 2 bytes: 8.0 billion × 2 = 16 GB. In the 4-bit version, 3.50 billion numbers are squeezed to 0.5 byte (1.75 GB) and 4.60 billion stay at 2 bytes (9.20 GB), total 10.95 GB.
</details>

**Q3.** Why does memory grow when the model writes long thinking?

<details><summary>Answer</summary>
It keeps notes (the KV cache) about every earlier token. More tokens → more notes → more memory.
</details>

**Q4.** Why is the training example limit (3,500) lower than the answer limit (8,000)?

<details><summary>Answer</summary>
Training needs extra memory for in-between results and the LoRA training notes, on top of what answering needs.
</details>

---

## 7. You are here

```text
PART 1 ✅  →  PART 2: The tools → [07 ✅ GPU memory] → 08 Python → 09 Colab/Kaggle → 10 Hugging Face → 11 First model call
                                        ↑ you just finished this
```

**Research chain:** you now understand the **memory check** and why we chose the 4-bit Gemma.

**Next:** [Lesson 08: Python basics](08-python-basics.md).
