# Q&A 38: 2B limit-512 fill-in (notebook 16)

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
