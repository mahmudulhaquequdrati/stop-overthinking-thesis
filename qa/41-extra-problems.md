# Q&A 41: Extra 40 problems (notebook 18)

⬅️ [All Q&A](README.md) · Decision: [#86](../DECISIONS.md), scores [#89](../DECISIONS.md) · Scores: [results/extra/SUMMARY.md](../results/extra/SUMMARY.md)

---

## 1. The step in 2 sentences

We graded 40 more LiveCodeBench problems that were not in the old exam and not in training.
A free way still wins. The 234 scores stay the first exam. On these 40, thinking OFF was best or tied the limit.

---

## 2. Questions a teacher may ask

**Q: Why more problems?**
The exam was 234 problems, fixed before the scores. A later check asks whether the same winner still wins on more questions.

**Q: Why not rerun notebooks 14 to 17?**
Those notebooks train and redo the old 234. That does not fit the remaining A100 hours. The new notebook only answers the 40 new problems.

**Q: Where did the 40 come from?**
LiveCodeBench has no newer file than the one we already used. HumanEval+ is already all 164 problems. We took easy and medium problems from April 2024 to January 2025 that we had never used. There were 300 of those. We kept the latest 40. Dates: 30 November 2024 to 4 January 2025. Mix: 17 easy, 23 medium.

**Q: Could one of the 40 be a training problem?**
No. We checked the ids. Overlap with the 234 exam ids: 0. Overlap with the 80 training ids: 0. Overlap of the question text with saved training questions: 0.

**Q: What did they score?**
0.8B thinking OFF **5.0%** (2/40). Every other 0.8B way, including training, scored 0. 2B thinking OFF **12.5%** (10/80). The 1,024 limit scored 8.8% (7/80). Thinking ON scored 0. 4B thinking OFF and the 2,048 limit both scored **46.2%** (37/80). Thinking ON scored 18.8% (15/80).

**Q: Did the winner change?**
On the first exam, no. 49.8% and 78.2% stay. On these 40, thinking OFF won or tied. The 2B gap is 3 answers out of 80. We have no error bars, so we do not call that a new proven winner.

**Q: Why not replace 49.8% with one blended number?**
The 40 are contest problems only. The old exam is mostly easy functions. A blend would be pulled by the old 234, and the new result would disappear. 2B and 4B training also did not run on these 40, so a full new headline table would have holes.

**Q: Why is training missing on 2B and 4B?**
2B training was skipped. The run continued to later free ways, and the score file has no 2B training rows, so the weight files were not used. 4B stopped after thinking ON. The clock file shows 3.7 hours used of a 4.5 hour cap, with half an hour kept spare.

**Q: Why not a 500-token limit or a 2000-token limit?**
2B already has limit 512 and limit 2048 on the old 234. The new run copies those settings. It does not invent a new one. 2B's 2,048 cell is still 1 try (3/40 = 7.5%).

---

## 3. Hard questions

**Q: Is 274 now the thesis number?**
No. The thesis exam stays 234. The 40 are a second table in the easy thesis results chapter.

**Q: Does this prove a sharper result?**
No. Forty problems do not tighten the old error bars. The new fact is that a free way still wins when the questions are newer contest problems, and thinking ON is weaker there.

---

## 4. What we checked, and what we only assume

| ✅ We checked this | ❌ We only assume this |
|---|---|
| Graded files match the summary: 40 problems, 17 easy, 23 medium | Error bars on these 40 — not computed |
| Try counts: 0.8B is 1 try, most 2B and all 4B rows are 2 tries, 2B limit 2048 is 1 try | The Colab screen itself — we read the saved zip |
| 2B and 4B training rows are absent from the score file | That a missing 2B weight file is the only reason those rows are absent |
| Hours file: 3.657 hours used, cap 4.5 | |

---

## 5. Where this is written down

- **Scores:** [results/extra/SUMMARY.md](../results/extra/SUMMARY.md)
- **Easy thesis:** [easy-thesis/05-results.md](../easy-thesis/05-results.md) and [easy-thesis/FULL-THESIS.md](../easy-thesis/FULL-THESIS.md)
- **Decision:** [DECISIONS.md](../DECISIONS.md) #86, #87, #88, #89
