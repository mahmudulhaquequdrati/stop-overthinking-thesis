# Q&A 36: Size extension written into the thesis

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

⬅️ [All Q&A](README.md) · Numbers: [SIZE-COMPARISON.md](../results/SIZE-COMPARISON.md) · Thesis: [THESIS.md](../thesis/THESIS.md)

---

## 1. The step in 2 sentences

We wrote the 0.8B / 2B / 4B comparison into the thesis: Results §5.13, Analysis §6.7, Conclusion §7.5.4, plus the abstract.
The story: a free way always beats LoRA-1; which free way wins depends on size (OFF → limit1024 → limit2048).

---

## 2. Questions a teacher may ask

**Q: Where are the 0.8B and 4B numbers in the thesis?**
A: Chapter **5.13** (tables), **6.7** (what they mean), **7.5.4** (short wrap-up). Abstract and “one page” summary mention them too.

**Q: Does this change the main 2B answer?**
A: No. On 2B, limit 1,024 is still best. The size runs **support** “try free options first” across three sizes.

**Q: What is still future work?**
A: 9B+ models, other families, harder tasks, loop-stopping methods, more tries on 0.8B.

---

## 3. Checked vs. assumed

| Checked | Assumed |
|---|---|
| Graded summaries for all three sizes | Exact Colab unit cost for the whole size extension |

---

## 5. Where it is written

- `thesis/05-results.md` · `06-analysis.md` · `07-conclusion-and-future-work.md` · `00-front-matter.md`
- Rebuild: `node scripts/build_thesis.js`
