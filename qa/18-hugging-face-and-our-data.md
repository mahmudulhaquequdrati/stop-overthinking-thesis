# Q&A 18: Hugging Face, and checking our data

⬅️ [All Q&A](README.md) · Hard word? See [GLOSSARY.md](../GLOSSARY.md) · Lesson: [10 Hugging Face](../lessons/10-hugging-face.md)

---

## 1. The step in 2 sentences

We learned where our model and data come from (Hugging Face) and how to read a model or dataset page.
Then we checked our test sets ourselves, with a notebook that needs no GPU.

---

## 2. Questions a teacher may ask

**Q: Where do your model and data come from?**
All from Hugging Face, free: the model `unsloth/gemma-4-E4B-it-unsloth-bnb-4bit`, and the datasets
`evalplus/humanevalplus`, `evalplus/mbppplus` and `livecodebench/code_generation_lite`.

**Q: Did you check the sizes yourself?**
Yes, with [notebook 10](../notebooks/10_look_at_the_data.ipynb), on 2026-09-17:
- HumanEval+: **164** problems ✅ (matches PLAN.md)
- MBPP+: **378** problems ✅
- LiveCodeBench (newest file): 2025-01: 44 · 2025-02: 51 · 2025-03: 68 · 2025-04: 12

**Q: How many test problems are really "fresh" for Gemma?**
From February 2025 on: **131 problems = 31 easy + 39 medium + 61 hard**.
So only **70 fresh easy + medium problems**. We count only easy and medium, so the fresh part of our test set is small.

**Q: Do you need an account or a token?**
No. The Gemma model and all these datasets are not gated (checked). A token is only needed for gated or private files, and it is never written into a notebook or into git.

**Q: Why do you download the same model again in every session?**
The download is cached on the session's computer, and a free session is wiped when it ends.

---

## 3. Hard questions

**Q: Only 70 fresh easy + medium problems. Isn't that too few?**
Too few to show a 2–3 point accuracy change on its own (that needs about 1,250+). So the fresh set is **not** our main test.
Our main comparison uses the full test set and compares the same problems before and after, which stays fair even for problems the model may have seen (lesson 06).
A separate "fresh vs. seen" study is future work.

**Q: LiveCodeBench doesn't load like the others. Why?**
It uses a Python loading script. The Hugging Face viewer refuses to run it, and newer versions of the `datasets` library may refuse too.
We download its `.jsonl` files directly instead. Our notebook does this and it works.

**Q: Those files are big. Is that a problem on a free machine?**
The newest file is 134 MB, but the whole set is about 4.5 GB. We plan to download only the parts we need, and to keep the problems we use in a small file of our own.

**Q: How do you make sure a dataset id still exists?**
PLAN.md says to re-check every id in the first data notebook. That is exactly what notebook 10 does.

---

## 4. Checked vs. assumed

| We checked (2026-09-17) | We assume |
|---|---|
| 164 HumanEval+, 378 MBPP+ (loaded and counted) | How many easy + medium problems are in the **older** LiveCodeBench files (not counted yet) |
| LiveCodeBench fields include `contest_date` and `difficulty` | That the dataset ids stay the same |
| Fresh counts: 31 easy, 39 medium, 61 hard (from 2025-02) | That the earlier files hold no problems after January 2025 (they end before, by release order) |
| Gemma and all three datasets are not gated | |

---

## 5. Where it is written

- [lessons/10-hugging-face.md](../lessons/10-hugging-face.md) · [notebooks/10_look_at_the_data.ipynb](../notebooks/10_look_at_the_data.ipynb)
- [research/2026-09-17-part2-tool-checks.md](../research/2026-09-17-part2-tool-checks.md) §3
- [PLAN.md](../PLAN.md) §6 · [DECISIONS.md](../DECISIONS.md) rows #18, #40
