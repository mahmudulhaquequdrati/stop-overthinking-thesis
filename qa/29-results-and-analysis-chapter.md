# Q&A 29: The results and analysis chapter (first draft)

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

⬅️ [All Q&A](README.md) · Hard word? See [GLOSSARY.md](../GLOSSARY.md) · Decision: [#69](../DECISIONS.md) · The chapter: [thesis/05-results.md](../thesis/05-results.md) and [thesis/06-analysis.md](../thesis/06-analysis.md) (was one draft file; split on 2026-09-25, DECISIONS #70)

---

## 1. The step in 2 sentences

We wrote the first draft of the thesis chapters "Results" (what we measured) and "Analysis" (what it means
and why). Every number comes from the full results page, which a script builds from the raw answers.

```text
raw answers (Drive) → make_full_results.js → FULL-RESULTS.md → thesis/05-results.md + 06-analysis.md
                                             (all numbers)      (the story, for the examiner)
```

**Where we are:** `RESULTS ✅ → ANALYSIS ✅ (draft) → CONCLUSION ⬅ next`

---

## 2. Questions a teacher may ask

**Q: What is the difference between "Results" and "Analysis"?**
Results says *what* happened, with tables and charts, and no opinions. Analysis says *why* it happened and
what it means, and compares it with other papers.

**Q: What is the main story of the chapter?**
Training did not make the model think shorter. A free thinking limit worked better. The reason: the model's
waste is **loops** (getting stuck), not long careful thinking, and training on short correct answers teaches
nothing about loops.

**Q: Why did you add comparisons that were not in your plan (limit vs OFF)?**
The analysis compares our result with the NoThinking paper, which is about OFF vs a thinking budget. So we
needed that number. We used the same method as the plan (2,000 resamples, seed 3407). The chapter shows them
as **extra** comparisons, separate from the hypotheses fixed in advance.

**Q: What does "threats to validity" mean?**
The honest list of reasons our result could be wrong or might not hold elsewhere. For example: one model
only, one "brief" wording, only 2 tries per problem.

---

## 3. Hard questions

**Q: If the limit is so good, why train at all?**
On problems like the training data, training did help (pilot study: 41% fewer tokens, +15 points). It just
did not carry over to new kinds of problems. So training is worth it only if your real problems look like
your training problems.

**Q: Does your result disagree with NoThinking?**
Not directly. NoThinking found that OFF can beat a small thinking budget. We found that the 1,024 limit beat
OFF overall (+9.0, proven), but OFF beat the limit on medium problems. The models and budgets differ.

**Q: Could full fine-tuning have worked where LoRA failed?**
Possibly. SEER reports that LoRA was about 7 points less accurate than full fine-tuning. We did not test this.
It is listed as future work.

---

## 4. Checked vs. assumed

| Checked | Assumed / not checked |
|---|---|
| Every chapter number matches FULL-RESULTS.md | That bigger models loop less (future work) |
| The extra comparisons reproduce the notebook's interval for LoRA-2 − limit exactly | That full fine-tuning would do better |
| All charts were rendered and looked at | The paper claims (SEER, ASAP, NoThinking) are as summarised in PAPERS.md |

---

## 5. Where it is written

- The chapter: [thesis/05-results.md](../thesis/05-results.md) and [thesis/06-analysis.md](../thesis/06-analysis.md) (was one draft file; split on 2026-09-25, DECISIONS #70)
- All numbers, charts and problem lists: [results/full-results/FULL-RESULTS.md](../results/full-results/FULL-RESULTS.md)
- The script: [scripts/make_full_results.js](../scripts/make_full_results.js)
- Decision: [DECISIONS #69](../DECISIONS.md)
