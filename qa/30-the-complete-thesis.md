# Q&A 30: The complete thesis, from top to bottom

⬅️ [All Q&A](README.md) · Hard word? See [GLOSSARY.md](../GLOSSARY.md) · Decision: [#70](../DECISIONS.md) · The thesis: [thesis/THESIS.md](../thesis/THESIS.md)

---

## 1. The step in 2 sentences

We wrote the whole thesis, from the abstract to the appendices, in simple English, as one file per chapter joined into
[thesis/THESIS.md](../thesis/THESIS.md). It puts the **thinking limit** first, explains exactly how every piece of evidence
is computed (Chapter 4), and uses checked sources to argue that bigger models may loop less (Chapter 7).

**Where we are:** `... → RESULTS ✅ → ANALYSIS ✅ → CONCLUSION ✅ (draft)`

---

## 2. Questions a teacher may ask

**Q: What is your main result, in one sentence?**
A free thinking limit (stop thinking at 1,024 tokens) was the most accurate way: 49.8% against 42.1% for normal thinking,
+7.7 points with an error bar of [+4.3, +11.3], while training the model to think shorter did not shorten its thinking at all.

**Q: How do you decide that an answer "passed"?**
We take the last Python code block from the answer and run the benchmark's own tests on it, in a separate process with a
time limit. It passes only if **every** test passes. A crash, a wrong output, a timeout or a missing answer is a fail.

**Q: What is a "point"?**
A percentage point: the plain difference between two percentages. 49.8% − 42.1% = 7.7 points. (In relative terms, that's 18% better.)

**Q: How do you know +7.7 is not luck?**
The bootstrap: we re-drew the 234 problems at random 2,000 times and recomputed the difference each time. The middle 95% of
those results ran from +4.3 to +11.3. That range doesn't include 0, so the difference is real for this test set.

**Q: Why do you think a bigger model would behave differently?**
Three sources: the Qwen3.5-2B model card says this model loops more than other Qwen3.5 models; Pipis et al. (2025) found that
larger models loop less; Li et al. (2025) found that models of 3B or less don't learn well from long reasoning. Our own data
shows loops were the main waste. So a bigger model probably has less looping and more "long but finished" thinking, which is
what training can shorten.

---

## 3. Hard questions

**Q: You changed the model, the test set and the number of tries after the proposal. Isn't that a problem?**
Every change was made **before** the main results were seen, for time and budget reasons, and is logged with its reason
(Chapter 3.11, DECISIONS.md). The main LoRA and the hypotheses were fixed before the run.

**Q: Isn't the limit's win just because your token limit was too small for normal thinking?**
Partly, on HumanEval+. We measured it: with 16,384 tokens, normal thinking went from 53.7% to 59.1%, close to the limit's
60.4%. But it needed 16 times more thinking room to get there, and on LiveCodeBench it stayed far behind (17.1% against 25.7%).

**Q: If the model card already says the model loops, what is new?**
The card says it loops more than its siblings. We measured **how much** looping costs on code (69.5% of normal thinking's
unfinished answers), showed that shortest-correct training does **not** fix it, and showed that a simple limit does.

---

## 4. Checked vs. assumed

| Checked | Assumed / not checked |
|---|---|
| Every number matches FULL-RESULTS.md, built from the raw files | That bigger models will loop less **for our problems** (future work) |
| The model card, Pipis et al. and Li et al. quotes, opened and matched word for word | The s1 and Qwen3-report descriptions (found by a helper search) |
| Every link and figure in the thesis points to a real file | NeurIPS 2023 as the EvalPlus venue (as in the proposal) |
| The grader passed the official solutions before grading | Cost of a bigger-model run (estimate only) |

---

## 5. Where it is written

- The whole thesis: [thesis/THESIS.md](../thesis/THESIS.md), chapters in [thesis/](../thesis/README.md)
- Built by: `node scripts/build_thesis.js`
- Evidence for bigger models: [research/2026-09-25-bigger-models-and-loops-evidence.md](../research/2026-09-25-bigger-models-and-loops-evidence.md)
- Decision: [DECISIONS #70](../DECISIONS.md)
