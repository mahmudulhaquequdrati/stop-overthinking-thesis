# Q&A 41: Extra 40 problems (notebook 18)

⬅️ [All Q&A](README.md) · Decision: [#86](../DECISIONS.md) · Lists: [results/extra/LISTS.md](../results/extra/LISTS.md)

---

## 1. The step in 2 sentences

We listed 40 more LiveCodeBench problems that were not in the old exam and not in training.
Notebook 18 will grade them later. The 234 scores are not changed. This step has **no new accuracy number yet**.

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

**Q: Why not a 500-token limit or a 2000-token limit?**
2B already has limit 512 and limit 2048 on the old 234. The new run copies those settings. It does not invent a new one.

**Q: Why did the fast-path cell say "restart"?**
It installed a speed library that did not match this Colab. The import failed. The message said to restart. A restart ran the same install, so it failed again. The cell now downloads the ready-made file whose name matches this Colab's PyTorch (DECISIONS #87).

**Q: Why did Python say `/content/scripts/build_extra_problems.py` is missing?**
The project is in `/content/thesis`. The fast-path cell had moved the notebook to `/content`. The next cell looked for `scripts/` in the wrong folder. It now walks back to `/content/thesis` first (DECISIONS #88).

---

## 3. Hard questions

**Q: Is 274 now the thesis number?**
Not yet. The thesis number stays 234 until notebook 18 has been run and the extra table is written beside it. We will not replace 49.8% or 78.2% with a mixed number in the main table.

**Q: Does this prove a sharper result?**
No. Forty extra problems make the error bars only a little tighter. The question is whether the same free way still wins.

---

## 4. What we checked, and what we only assume

| ✅ We checked this | ❌ We only assume this |
|---|---|
| 234 old exam ids, same in every model folder | That the add-on weight files are still on Drive |
| 80 training ids, none inside the 234 | How many real hours notebook 18 will take |
| 40 new ids, no overlap, saved in `results/extra/` | The extra scores — not run yet |
| Wheel names on the causal-conv1d release (v1.7.0) match torch 2.6–2.10 and 26.02–26.07 | That this download loads on the A100 — not run yet |

---

## 5. Where this is written down

- **Lists:** [results/extra/LISTS.md](../results/extra/LISTS.md)
- **Notebook:** [notebooks/18_extra_problems.ipynb](../notebooks/18_extra_problems.ipynb)
- **Decision:** [DECISIONS.md](../DECISIONS.md) #86, fast-path fix #87, folder fix #88
