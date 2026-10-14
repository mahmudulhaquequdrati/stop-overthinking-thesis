# Q&A 33: All three models compared

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

⬅️ [All Q&A](README.md) · Decision: [#72](../DECISIONS.md)–[#77](../DECISIONS.md) · Join: [results/SIZE-COMPARISON.md](../results/SIZE-COMPARISON.md)

---

## 1. The step in 2 sentences

We ran the same 234 code problems on Qwen3.5 **0.8B**, **2B**, and **4B**.
A free control always beat LoRA-1; the *best* free control changes with size (OFF on 0.8B, limit 1024 on 2B, limit 2048 on 4B).

---

## 2. Questions a teacher may ask

**Q: Does a bigger model need a bigger thinking limit?**
A: Where limits help, yes: best was **1024 on 2B** and **2048 on 4B**. On **0.8B**, OFF won (20.5%) — the tiny model is too weak for long thinking.

**Q: Is training worth it on any of the three sizes?**
A: **Not against the best free way.** LoRA-1: 17.9% (0.8B), 45.5% (2B), 69.9% (4B) — each loses to that size’s best free option.

**Q: Who should use which free option?**
A: Start with **OFF** and a **short limit**. On very small models, prefer OFF. On mid/large small models, try limits around 1k–2k. Train only if free ways are not enough.

**Q: Why is ON so bad on 0.8B?**
A: ON got **7.3%** with **78% cut off** — it loops / hits the wall. Switching OFF avoids that waste.

---

## 3. Hard questions

**Q: Is comparing 1-try 0.8B to 2-try 2B/4B unfair?**
A: Ranking ways on 0.8B is still fair (same 1 try for every way). Cross-size % gaps have slightly wider uncertainty on 0.8B. We label tries in every table (DECISIONS #76).

**Q: Did you cherry-pick which limits to run on 0.8B?**
A: No — plan locked before the run: max 1024 because that won on 2B; drop 2048/4096 to stay under 50 compute hours (#75).

---

## 4. Checked vs. assumed

| Checked | Assumed |
|---|---|
| All three graded summaries | Exact Colab compute hours for 0.8B (zip had no hours file; wall ~3h estimated) |
| Same 234 problems | 0.8B would look like 2B if we had run 2048 (we did not) |

---

## 5. Where it is written

- [results/SIZE-COMPARISON.md](../results/SIZE-COMPARISON.md)
- [results/ALL-RESULTS.md](../results/ALL-RESULTS.md)
- [results/0.8b/SUMMARY.md](../results/0.8b/SUMMARY.md) · [results/4b/SUMMARY.md](../results/4b/SUMMARY.md)
