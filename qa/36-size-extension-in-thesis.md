# Q&A 36: Size extension written into the thesis

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
