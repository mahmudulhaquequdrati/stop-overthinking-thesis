# Q&A 43: The 190 problems, scored

⬅️ [All Q&A](README.md) · Decision: [#93](../DECISIONS.md) · Scores: [results/more/SUMMARY.md](../results/more/SUMMARY.md) · Story: [results/more/RUN.md](../results/more/RUN.md)

---

## 1. The step in 2 sentences

Notebook 19 graded 190 new contest problems on 0.8B, 2B, and 4B.
A free way still wins on every size. These scores stay off the first exam.

---

## 2. Questions a teacher may ask

**Q: What am I testing?**
Whether the free ways still beat training on a bigger contest list.

**Q: What did you expect?**
A free way still wins. Training does not beat it.

**Q: What did you change?**
Only the way of answering. Same 190 problems for every way.

**Q: What did you measure?**
How often the code passes every test. One try. Seed 3407.

**Q: What we compare against?**
Thinking ON, and the trained add-on where it ran.

**Q: What result supports it?**
0.8B OFF is 9.5%. 2B limit 1,024 is 31.1%. 4B limit 2,048 is 69.5%.
Each of those beats the trained add-on that ran.

**Q: What result would reject it?**
The trained add-on beating every free way. That did not happen.

**Q: How many problems in total?**
234 + 40 + 190 = **464**. That is a count. It is not one score.
Training is separate: LoRA-1 used a pool of **100**. LoRA-2 used a pool of **280**, and kept **157**.
The one page is [easy-thesis/00-one-page.md](../easy-thesis/00-one-page.md).

**Q: Did this change 49.8% or 78.2%?**
No. Those stay on the 234. This table is only the 190.

**Q: Why are the scores lower than the exam?**
This list is contest problems only. The exam also has easy function questions.

**Q: Who won?**

| Size | Winner on the 190 | Trained add-on |
|---|---|---|
| 0.8B | OFF **9.5%** (18/190) | 7.9% (15/190) |
| 2B | limit 1,024 **31.1%** (59/190) | not run |
| 4B | limit 2,048 **69.5%** (132/190) | 46.3% (88/190) |

That is the same winner as the first exam, on each size.

**Q: What about easy and medium?**
118 easy. 72 medium.
On 4B easy, the limit is 88.1% and OFF is 80.5%.
On 4B medium, OFF is 44.4% and the limit is 38.9%.
The limit still wins the full list, because the easy lead is bigger.

**Q: Why is 2B training missing?**
Colab printed `lora1 SKIP — no weights at /content/thesis/results/mini/lora/lora100`.
The same step said GO, with about 11 hours left. Time was not the reason.
Git stores the 0.8B and 4B weight files. It does not store this 2B file.
0.8B and 4B training did run. Colab printed "LoRA loaded" for both. Both lost to a free way.

---

## 3. Hard questions

**Q: The extra 40 said OFF wins or ties. Why is that different here?**
The 40 were a small pile. OFF led 2B by 3 answers out of 80.
This list has 190 problems. The 1,024 limit leads 2B by 12 answers (59 vs 47).
The 2,048 limit leads 4B by 5 answers (132 vs 127).
We did not draw error bars. Say the free exam-winner scored higher here.
Do not say this gap is proven the way the +7.7 points on the 234 are proven.

**Q: Did thinking ON get stuck again?**
Yes. It hit the token wall on 181 of 190 answers at 0.8B, 149 at 2B, and 115 at 4B.
OFF hit it on 49, 33, and 7.

**Q: How long did it take?**
7.947 real hours. The cap was about 14.8. The run finished with room left.
File times run from 15:05 to 22:38 on 2026-10-06.

**Q: Which GPU?**
The notebook will not start unless the name contains A100 or H100.
The zip does not include that printed line.
We checked the hours and the model names. We did not check a saved GPU name.

---

## 4. Checked vs. assumed

| We checked | We assume |
|---|---|
| 11 files, 190 rows each, pass counts match the summary | The GPU was an A100. H100 was also allowed. The name was not saved. |
| 118 easy, 72 medium, on every file | |
| Colab printed `SKIP — no weights at .../mini/lora/lora100` while the clock said GO | |
| Hours add to 7.947 | |
| Old exam files were not in the zip | |

---

## 5. Where it is written

- [DECISIONS.md](../DECISIONS.md) row #93
- [results/more/SUMMARY.md](../results/more/SUMMARY.md)
- [results/more/RUN.md](../results/more/RUN.md)
- [easy-thesis/10-all-counts.md](../easy-thesis/10-all-counts.md) — counts, charts, and stats
- [results/RESULTS-INDEX.md](../results/RESULTS-INDEX.md)
- [easy-thesis/09-extra-problems.md](../easy-thesis/09-extra-problems.md)
