# Q&A 38: 2B limit-512 fill-in (notebook 16)

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

⬅️ [All Q&A](README.md) · Decision: [#81](../DECISIONS.md)–[#82](../DECISIONS.md) · Numbers: [results/2b-limit512/SUMMARY.md](../results/2b-limit512/SUMMARY.md)

---

## 1. The step in 2 sentences

We filled the empty **2B × Limit 512** cell: **45.1%** on the same 234 problems (2 tries).
It beats thinking ON (42.1%) but still loses to **limit 1024 (49.8%)**, so the main 2B answer does not change.

---

## 2. Questions a teacher may ask

**Q: What was 2B at limit 512?**
A: **45.1%** (thinking ~492 tokens, 28% cut off).

**Q: Why only 512, not 2048?**
A: 2B’s best free way is already limit **1024**. 4B already showed 2048 can win on a bigger model. 512 was the empty chart cell.

**Q: Does this change the main 2B thesis?**
A: No. Limit 1024 stays best. 512 just shows a shorter budget already helps a bit.

---

## 3. Checked vs. assumed

| Checked | Assumed |
|---|---|
| Graded HE+LCB, 468 answers (234×2) | Exact Colab compute hours for this fill-in |

---

## 5. Where it is written

- [results/2b-limit512/](../results/2b-limit512/) · [SIZE-COMPARISON.md](../results/SIZE-COMPARISON.md)
- Thesis §5.13 · DECISIONS #82
