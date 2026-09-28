# Q&A 33: All three models compared (fill after both new runs)

⬅️ [All Q&A](README.md) · Decision: [#72](../DECISIONS.md) · Join page: [results/ALL-RESULTS.md](../results/ALL-RESULTS.md)

---

## 1. The step in 2 sentences

**Status: waiting on Colab.** When 0.8B and 4B summaries exist, rebuild `results/ALL-RESULTS.md` with `python scripts/make_all_results.py` and answer the questions below from that page.

---

## 2. Questions a teacher may ask

**Q: Does a bigger model need a bigger thinking limit?**
A: _(compare best limit on 0.8B vs 2B vs 4B)_

**Q: Is training worth it on any of the three sizes?**
A: _(LoRA-1 vs best limit per size)_

**Q: Who should use which free option?**
A: Budget code users of small reasoning models: try the best limit for your size first; use OFF when tokens matter most; train only if the model finishes and has short correct answers.

---

## 3. Checked vs. assumed

| Checked | Assumed |
|---|---|
| 2B full results | 0.8B and 4B until Colab finishes |

---

## 5. Where it is written

- [results/ALL-RESULTS.md](../results/ALL-RESULTS.md)
