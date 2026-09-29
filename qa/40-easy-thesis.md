# Q&A 40: the easy-language thesis folder

⬅️ [All Q&A](README.md) · Decision: [#85](../DECISIONS.md) · Read it: [easy-thesis/FULL-THESIS.md](../easy-thesis/FULL-THESIS.md)

---

## 1. The step in 2 sentences

We wrote the whole study again in short sentences, in a new folder.
One file, [FULL-THESIS.md](../easy-thesis/FULL-THESIS.md), joins every chapter.

## 2. Questions a teacher may ask

**Q: Is this a second thesis with new numbers?**
A: No. The numbers are copied from the checked results. The official chapters stay in `thesis/`.

**Q: Why a new folder?**
A: So a reader can follow who it helps, why a limit wins, and what the datasets are, without the long science file.

**Q: Did you prove the small model is more secure?**
A: No. We say a local model can keep code on your machine. We did not test attacks.

## 3. Hard questions

**Q: Why mention giant models if you never ran one?**
A: The user asked why not use a big model for a private setup, a small GPU, and easy problems. We separate that advice from the scores we actually measured (0.8B, 2B, 4B on 234 problems).

**Q: Where is the LiveCodeBench question text?**
A: Not in git. We show the id `lcb/3705` and the HumanEval/0 text from the saved answer file.

## 4. Checked vs. assumed

| Checked | Assumed |
|---|---|
| Chapter numbers match SIZE-COMPARISON and FULL-RESULTS | A local model is safer in practice. Not measured. |
| HumanEval/0 text copied from `test-off-he.jsonl` | |
| Overlap ids copied from the results files | |

## 5. Where it is written

[easy-thesis/](../easy-thesis/) · DECISIONS #85 · [ROADMAP.md](../ROADMAP.md)
