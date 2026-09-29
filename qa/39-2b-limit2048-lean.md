# Q&A 39: 2B limit-2048 lean fill-in (notebook 17)

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
