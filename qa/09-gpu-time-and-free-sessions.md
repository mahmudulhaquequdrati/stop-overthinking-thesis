# Q&A 09: GPU time, and working with free 12-hour sessions

⬅️ [All Q&A](README.md) · Hard word? See [GLOSSARY.md](../GLOSSARY.md)

---

## 1. The step in 2 sentences

We estimated how long each part takes on a free GPU. Training takes about **4 hours**,
but making data and testing take tens of hours, so every job must be able to **stop and continue later**.

---

## 2. Questions a teacher may ask

**Q: How long does training take?**
About **4 GPU-hours** (range 3–7), on one free T4 GPU. It fits in one free session.

```text
time = (number of examples × tokens per example) ÷ speed

     = (2,000 × 1,800 tokens) ÷ 250 tokens per second
     = 3.6 million tokens ÷ 250
     ≈ 4 hours
```

**Q: Where do these numbers come from?**

| Number | Where from | Checked? |
|---|---|---|
| ~2,000 examples | ~4,000 training problems × at least 40% solved | assumed |
| ~1,800 tokens each | question ~300 + kept short answer ~1,500 | assumed |
| ~250 tokens/second | calculated from how much math the GPU can do | **not checked** |
| 1 epoch (one pass through the data) | the closest paper (Munkhbat et al. 2025) did 1 | from the paper |

**Q: What takes the most time?**
Not training. Making the data and testing.

| Stage | GPU-hours (estimates) |
|---|---|
| Making training data (~4,000 problems × 4 answers) | 15–40 |
| Testing the 5 ways of answering | 10–30 |
| The two checks and small trial runs | 2–5 |
| **Training (one LoRA run)** | **3–7 (plan ~4)** |

**Q: A free session is only about 12 hours. How do you do 40 hours of work?**
We never run one long job. Every job **saves as it goes** and can **continue later**.
*Everyday example:* reading a long book with a bookmark. You stop, and next time you start at the bookmark.

```text
start → connect Google Drive → read the list of finished problems → skip them
      → work → save results every ~20 problems → session dies → start again
```

Each problem is independent, so the work splits easily.
Training is saved every ~30 minutes (a *checkpoint*), so it can continue too.

**Q: Which free GPUs do you use?**
- **Kaggle is the main one.** About 30 GPU-hours per week, 2 T4 GPUs.
  It keeps running even when the browser is closed.
- **Colab is the second worker**, and the place to fix bugs. It needs the browser tab open.

---

## 3. Hard questions

**Q: If the session dies in the middle, don't you get different results when you re-run?**
No. Each item has its own fixed seed. The same problem gives the same output in any session.
We also save the model's raw answers exactly as written. Re-grading them never needs the GPU again.

**Q: Your speed number is not measured. What if it's wrong?**
It is an estimate, and we say so. In week 3, the memory check already trains 50 examples.
We will measure the real speed there, which costs about 20 minutes, then redo the table.

**Q: What can make training slower?**
- **Padding:** mixing short and long examples wastes time (up to 2× slower).
  Fix: sort examples by length, or pack them together.
- **2 epochs instead of 1:** 2× slower. We start with 1.

**Q: How do you cut the 40 hours?**
First, write many answers **at the same time** with vLLM (32–64 prompts at once).
This is **2–5× faster** and changes nothing in the science. We do this before asking for more hours.

---

## 4. Checked vs. assumed

| We checked | We assume (not checked yet) |
|---|---|
| Colab free sessions are "at most 12 hours" (Colab FAQ) | The speed: ~250 tokens per second |
| Kaggle gives ~30 GPU-hours per week (secondary sources) | Whether 2 T4s on Kaggle use 1 or 2 hours of quota per hour: check in week 1 |
| | Calendar time is about 3–5× GPU time on a first try |

---

## 5. Where it is written

- [DECISIONS.md](../DECISIONS.md) rows #30, #31
- [PLAN.md](../PLAN.md) §10, §11
- [research/gpu-time-budget.md](../research/gpu-time-budget.md) (full calculation)
