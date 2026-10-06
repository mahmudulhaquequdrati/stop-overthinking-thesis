# Q&A 42: A growing list, one notebook (not run yet)

⬅️ [All Q&A](README.md) · Decision: [#90](../DECISIONS.md) · List: [results/more/LISTS.md](../results/more/LISTS.md)

---

## 1. The step in 2 sentences

We built one Colab notebook that can grade 0.8B, 2B, and 4B on a new problem list.
The list has 190 problems and can grow later. It has not been run on the GPU yet.

---

## 2. Questions a teacher may ask

**Q: Why one file for three models?**
The settings stay in one config cell. You remove a model name to skip it. You do not keep three notebooks in step.

**Q: How many problems can you show?**
Old exam 234, plus the extra 40, plus this new list of 190. Total **464**. That number is a count. It is not a new accuracy.

**Q: Why 190 and not 200?**
The clean pool had 260 easy and medium problems that were not in the exam, the extra 40, or training. 70 of them had tests longer than 2.7 MB. One was about 150 MB. The extra 40 already graded nothing bigger than 2.6 MB. After that cut, 190 problems were left. We kept all of them: 118 easy and 72 medium.

**Q: Can you add more later?**
Yes. Raise `N_NEW` in the config cell and run again. New ids are added at the end. Old ids are not deleted or reordered. Problems that already have a grade are skipped.

**Q: Why is LoRA-2 not in this notebook?**
On the locked 234, LoRA-2 scored 45.1% and the 1,024 limit scored 49.8%. It did not think shorter. This run uses LoRA-1 only, one try, on all three models.

**Q: Will this change 49.8% or 78.2%?**
No. Those stay on the 234. The new scores, when they exist, go in `results/more/SUMMARY.md`, with an easy row and a medium row.

---

## 3. Hard questions

**Q: The run is on a new Google account. Does the old Drive have to be there?**
No. The new Drive starts empty. The 190 problems, and the 0.8B and 4B add-ons, come from GitHub. Scores are saved on the new Drive. The old account is not opened.
The 2B add-on is the one file that is only on the old Drive. If you do not copy `results/mini/lora/lora100` onto the new Drive, that one way is skipped. The free ways still run.

**Q: Notebook 18 failed more than once. What is different here?**
Two failures are blocked. After the speed-library cell, every later cell goes back to `/content/thesis` before it looks for `scripts/`. That was the folder error in notebook 18. And this notebook will not download LiveCodeBench during the GPU run. The 190 problems are already in `results/more/more-lcb.json`. If that file is missing from GitHub, the notebook stops before it spends hours.

**Q: Why leave 100 compute hours unused?**
The cap on this pass is 100 compute hours, about 15 real A100 hours. The other 100 are for a dead session or a redo. A list that spends the whole pot on the first try cannot be finished if the 4B fails.

**Q: Why one try?**
The locked exam already used two tries. This side list uses one, so more problems fit in the cap.

---

## 4. Checked vs. assumed

| We checked | We assume |
|---|---|
| 190 ids, 0 overlap with the 234, the extra 40, and the 80 train ids | That Colab will finish inside 100 compute hours |
| 118 easy, 72 medium, dates 2023-08-26 to 2024-11-23 | That the LoRA-1 weight files will be on Drive |
| Lowering the target does not delete ids (tried target 50, list stayed 190) | |
| The score writer refuses to write into the extra-40 summary | |

---

## 5. Where it is written

- [DECISIONS.md](../DECISIONS.md) row #90
- [results/more/LISTS.md](../results/more/LISTS.md)
- [notebooks/19_more_problems.ipynb](../notebooks/19_more_problems.ipynb)
