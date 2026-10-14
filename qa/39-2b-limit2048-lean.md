# Q&A 39: 2B limit-2048 lean fill-in (notebook 17)

<!-- CURRENT-STUDY:START -->

**Historical record below.** Its earlier scores, model choices and plans describe that stage only.
Use the current results linked here for the completed study.

**Current study — 14 October 2026:** **464 unique test problems**.
Benchmarks: **164 HumanEval+**, **166 LiveCodeBench easy**, **134 LiveCodeBench medium**.
All six planned LoRA combinations are complete, one attempt per problem:

- **0.8B:** LoRA + OFF **14.0% (65/464)**; LoRA + limit 512 **14.4% (67/464)**.
- **2B:** LoRA + OFF **35.6% (165/464)**; LoRA + limit 1,024 **41.2% (191/464)**.
- **4B:** LoRA + OFF **64.7% (300/464)**; LoRA + limit 2,048 **71.6% (332/464)**.

LoRA alone means thinking ON without a thinking-token limit.
Older methods' all-attempt averages and first-attempt comparisons are labelled separately.
LoRA + OFF does not consistently improve on free OFF; the 2B/4B gains over free limits remain uncertain.

[Every method, benchmark, difficulty, token count and interval](../results/CURRENT-RESULTS.md) · [Full easy thesis](../easy-thesis/FULL-THESIS.md) · [Full formal Markdown thesis](../thesis/THESIS.md).

<!-- CURRENT-STUDY:END -->

⬅️ [All Q&A](README.md) · Decision: [#83](../DECISIONS.md)–[#84](../DECISIONS.md) · Numbers: [results/2b-limit2048/SUMMARY.md](../results/2b-limit2048/SUMMARY.md)

---

## 1. The step in 2 sentences

We ran lean 2B × limit **2048**: **46.6%** (1 try, 234 problems).
That is **below** limit 1024 (49.8%), so on 2B the limit curve **peaks at 1024**.

---

## 2. Questions a teacher may ask

**Q: Did 2048 keep going up on 2B?**
A: **No.** 512 = 45.1% → 1024 = **49.8%** → 2048 = 46.6%. Peak at 1024.

**Q: Why 1 try?**
A: To save Colab hours. Direction vs 1024 is still clear.

**Q: Why does 4B like 2048 but 2B does not?**
A: Bigger models can use a longer useful budget. Same family, different sweet spot.

---

## 3. Checked vs. assumed

| Checked | Assumed |
|---|---|
| Graded 234 answers (1 try) | Exact Colab compute hours for this fill-in |

---

## 5. Where it is written

[SIZE-COMPARISON.md](../results/SIZE-COMPARISON.md) · thesis §5.13 · DECISIONS #84
