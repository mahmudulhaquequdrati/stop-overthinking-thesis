# Q&A 38: 2B limit-512 fill-in (notebook 16)

⬅️ [All Q&A](README.md) · Decision: [#81](../DECISIONS.md) · Run: [results/2b-limit512/RUN.md](../results/2b-limit512/RUN.md)

---

## 1. The step in 2 sentences

The size table had no **2B × Limit 512** number. Notebook **16** runs only that way on the same 234 problems (2 tries). We skip 2048 on 2B for now.

---

## 2. Questions a teacher may ask

**Q: Why only 512, not 2048?**
A: 2B’s best free way is already limit **1024**. 4B already showed 2048 can win on a bigger model. 512 is the empty cell next to 0.8B and 4B.

**Q: Does this change the main 2B thesis?**
A: No. It adds one comparable number. The main result (limit 1024 wins on 2B) stays.

---

## 3. Checked vs. assumed

| Checked | Assumed |
|---|---|
| Notebook 16 built; folder stub ready | Accuracy after Colab Run all |

---

## 5. Where it is written

- [notebooks/16_qwen35_2b_limit512.ipynb](../notebooks/16_qwen35_2b_limit512.ipynb)
- [results/2b-limit512/](../results/2b-limit512/)
- DECISIONS #81
