# Q&A 32: 4B Colab run (done)

⬅️ [All Q&A](README.md) · Decision: [#72](../DECISIONS.md) · [#73](../DECISIONS.md) · Numbers: [results/4b/SUMMARY.md](../results/4b/SUMMARY.md)

---

## 1. The step in 2 sentences

We ran Qwen3.5-**4B** on the same 234 problems: OFF, ON, limits 512/1024/2048/4096, and LoRA-1.
The best way was a free **thinking limit of 2,048** (78.2%). LoRA-1 did not beat the limits.

---

## 2. Questions a teacher may ask

**Q: On the 4B model, which way was most accurate?**
A: **limit 2048 → 78.2%**. Then limit4096 76.7%, limit1024 76.5%, limit512 75.4%. ON was only 64.3%.

**Q: Did 4B loop less / finish more than 2B?**
A: Cut-off for ON was **28%** on 4B vs **41%** on 2B — fewer unfinished answers. Accuracy is much higher overall (ON 64% vs 42%).

**Q: Did LoRA-1 shorten thinking on 4B?**
A: Thinking 2,565 vs ON 2,938 (~12% less), accuracy 69.9% — better than ON, but **worse than every limit**. So training still does not beat a free cut.

**Q: Does a bigger model need a bigger thinking limit?**
A: On 2B the best limit was 1,024 (49.8%). On 4B the best was **2,048** (78.2%). So yes, the best limit moved up with size (on this family).

---

## 3. Hard questions

**Q: Why is OFF better than ON on 4B?**
A: OFF 69.7% vs ON 64.3%, with far fewer tokens (720 vs 3,096). ON still hits the wall often (28% cut off). A hard limit fixes that better than leaving thinking open.

**Q: Is this the same as the 2B story?**
A: Same shape: **free limit wins over LoRA-1**. Different best limit size (2048 vs 1024).

---

## 4. Checked vs. assumed

| Checked | Assumed |
|---|---|
| SUMMARY from graded CSVs in `results/4b/raw/` | Exact loop % (not re-counted here) |
| Wall hours ~8.5 on the shared ledger | Colab UI “100 hours left” (user report) |

---

## 5. Where it is written

- [results/4b/SUMMARY.md](../results/4b/SUMMARY.md) · [results/ALL-RESULTS.md](../results/ALL-RESULTS.md) · [shared/hours_budget.json](../results/shared/hours_budget.json)
