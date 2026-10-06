# Complete thesis A→Z · where to check · what to tell the teacher

> **Read this before a meeting.**  
> Full thesis: [thesis/THESIS.md](thesis/THESIS.md) · PDF: [thesis/Stop-Overthinking-Thesis.pdf](thesis/Stop-Overthinking-Thesis.pdf)  
> **All numbers for the paper:** [results/RESULTS-INDEX.md](results/RESULTS-INDEX.md)  
> Three-size page: [results/SIZE-COMPARISON.md](results/SIZE-COMPARISON.md)

---

## 1. The whole story in 30 seconds (say this out loud)

```text
PROBLEM   Small AI models "think" too long on code and burn time.
GAP       Nobody checked on one small model with an ON/OFF switch:
          is TRAINING to think shorter better than free options?
QUESTION  Train shorter — or just use OFF / a thinking limit?
HYPOTHESIS Training should shorten thinking and keep accuracy.
EXPERIMENT Same 234 code problems · free ways + LoRA · real tests.
RESULT    On 2B: free LIMIT 1024 wins (49.8%). Training does NOT shorten.
WHY       The waste is LOOPS (stuck), not careful long thinking.
SIZE CHECK Same problems on 0.8B / 2B / 4B:
          best free = OFF / limit1024 / limit2048.
          LoRA never beats that free winner.
```

**One sentence for the teacher:**  
*"On small Qwen3.5 code models, a free control beats shortest-correct LoRA; which free control wins depends on size — OFF on 0.8B, limit 1024 on 2B, limit 2048 on 4B — because the main waste is looping, not careful overthinking."*

---

## 2. Thesis A→Z (what to open, in order)

| Step | Open this | What it is | ~time |
|---|---|---|---|
| A | [THESIS.md](thesis/THESIS.md) → **Abstract** | One-page science summary | 3 min |
| B | Same file → **“The thesis in one page”** | Everyday story + bar chart of numbers | 5 min |
| C | Ch **1** Introduction | Problem, gap, question, hypotheses | 10 min |
| D | Ch **2** Background | LLM, tokens, thinking, LoRA (simple) | 15 min |
| E | Ch **3** Method | Six ways, 234 problems, fairness rules | 15 min |
| F | Ch **4** How we measure | Pass rule, points, error bars, loops | 15 min |
| G | Ch **5** Results | **2B tables first**, then **§5.13** size table | 20 min |
| H | Ch **6** Analysis | Why loops; §6.7 size meaning | 15 min |
| I | Ch **7** Conclusion | Advice + §7.5.4 size wrap-up | 10 min |
| J | [SIZE-COMPARISON.md](results/SIZE-COMPARISON.md) | Three-size cheat sheet | 5 min |

**Print / hand-in:** [Stop-Overthinking-Thesis.pdf](thesis/Stop-Overthinking-Thesis.pdf)

**Fill before hand-in:** your name, supervisor, university in [thesis/00-front-matter.md](thesis/00-front-matter.md), then rebuild PDF.

---

## 3. Where to *test* / *check* (so you are not guessing)

Everyday example: before you tell a teacher “49.8%”, open the file and point at the number.

### Main 2B thesis (the big claim)

| What to check | Where |
|---|---|
| Main accuracy table | [results/2026-09-24-thesis-run.md](results/2026-09-24-thesis-run.md) |
| Full charts + every problem | [results/full-results/FULL-RESULTS.md](results/full-results/FULL-RESULTS.md) |
| Limit 49.8% vs ON 42.1% | Thesis Ch 5 · or summary above |
| “Passed” = real tests | Thesis Ch 4 · scripts `grade_*.py` |
| Error bars | Thesis Ch 4 · `scripts/compare_thesis.py` |
| Overlap (no test in train) | Decision #66 · notebook 14 / overlap file |

### Size extension (0.8B + 4B)

| What to check | Where |
|---|---|
| 0.8B table | [results/0.8b/SUMMARY.md](results/0.8b/SUMMARY.md) · story: [0.8b/RUN.md](results/0.8b/RUN.md) |
| 4B table | [results/4b/SUMMARY.md](results/4b/SUMMARY.md) |
| Join 0.8B+2B+4B | [results/ALL-RESULTS.md](results/ALL-RESULTS.md) · [SIZE-COMPARISON.md](results/SIZE-COMPARISON.md) |
| Raw graded CSVs | `results/0.8b/raw/test-*-graded.csv` · `results/4b/raw/` |
| Notebooks used | [15a 0.8B](notebooks/15a_qwen35_0_8b.ipynb) · [15b 4B](notebooks/15b_qwen35_4b.ipynb) |

### Later lists (do not mix into 49.8% or 78.2%)

| What to check | Where |
|---|---|
| Extra 40 | [results/extra/SUMMARY.md](results/extra/SUMMARY.md) · 2B OFF 12.5% · 4B OFF tied limit 2048 at 46.2% |
| The 190 | [results/more/SUMMARY.md](results/more/SUMMARY.md) · 0.8B OFF **9.5%** · 2B limit 1024 **31.1%** · 4B limit 2048 **69.5%** |
| Story of the 190 | [results/more/RUN.md](results/more/RUN.md) · qa/43 |
| **Counts and charts** | [easy-thesis/10-all-counts.md](easy-thesis/10-all-counts.md) · 464 tests · train 100 and 280 |

Say this if asked: a free way still wins. The 190 winner matches the exam. 2B training was skipped. On 4B medium only, OFF was higher (44.4% vs 38.9%).

### Quick “is the number real?” test (do once)

```text
1. Open results/0.8b/SUMMARY.md → OFF 20.5%
2. Open results/4b/SUMMARY.md   → limit2048 78.2%
3. Open SIZE-COMPARISON.md       → same numbers side by side
4. Open thesis §5.13             → same numbers again
```

If all four match, you can trust what you say.

### What we did *not* re-run (say this honestly)

| Honest limit | Why |
|---|---|
| 0.8B = **1 try**; 2B/4B = **2 tries** | Hour budget (DECISIONS #75–76) |
| 0.8B no limit 2048/4096 | Max 1024 (won on 2B); save hours |
| Code only, easy+medium | Scope of the thesis |
| One model family (Qwen3.5) | Fair size compare |

---

## 4. What to tell the teacher (practice answers)

Cover the answers. Say yours out loud. Then check.

### Opening (30 seconds)

**Q: What did you do?**  
*I compared free ways to control thinking (OFF, ON, a length limit) against training a small LoRA on shortest correct answers, on the same 234 code problems, with the benchmarks’ own tests.*

**Q: What is your main finding?**  
*On Qwen3.5-2B, a free thinking limit of 1,024 tokens was best: 49.8% vs 42.1% for normal thinking. Training did not make thinking shorter. The long answers were mostly loops.*

**Q: Why only one model?**  
*The main thesis is 2B. I also ran 0.8B and 4B in the same family on the same problems. Free controls still beat LoRA; the best free way moved with size.*

### Method

**Q: How do you know an answer is correct?**  
*I extract the Python code and run the benchmark’s tests in a sandbox. Every test must pass. I do not grade by eye.*

**Q: What is fair about your comparison?**  
*Same problems, same limits for generation, same seeds, same checker. Only the “way of answering” changes.*

**Q: What is a LoRA?**  
*A small add-on trained on top of the model — cheaper than full training. LoRA-1 = full MBPP+ shortest-correct examples.*

### Results & hard questions

**Q: Why did training fail to shorten thinking?**  
*Finished correct answers were already short. The waste was loops. Training never showed “how to get unstuck,” so the model kept looping.*

**Q: Isn’t a limit just cheating / cutting useful thought?**  
*We checked with more room (16k) for ON. It got better but still lost to the limit. On 4B, longer limits (4096) were not better than 2048.*

**Q: Why is OFF best on 0.8B but not on 2B/4B?**  
*0.8B is too weak: ON hits the wall 78% of the time and only gets 7.3%. Better not to start a long think. Stronger models benefit from a short think with a cut.*

**Q: Did you cherry-pick the 0.8B plan?**  
*No — locked before the run: max limit 1024 (won on 2B), 1 try, no Stage C, to stay under 50 compute hours after 4B used ~100.*

**Q: Can I trust 0.8B with only 1 try?**  
*Ranking ways inside 0.8B is fair (every way has 1 try). Cross-size error bars are a bit wider; I label that in the tables.*

**Q: Who should care?**  
*Students and developers who run small reasoning models for code on one GPU — try OFF and a short limit before paying for training.*

### Closing

**Q: What would you do next?**  
*Try still larger models (e.g. 9B) with a cheap “check first” for loops; try methods that stop repeats while generating; harder tasks / other families.*

---

## 5. Teacher Q&A files (practice by topic)

| Topic | File |
|---|---|
| Whole thesis (2B core) | [qa/30](qa/30-the-complete-thesis.md) |
| Real 2B run | [qa/28](qa/28-thesis-run-results.md) |
| Size plan | [qa/31](qa/31-size-limit-extension.md) |
| 4B run | [qa/32](qa/32-4b-run.md) |
| All three sizes | [qa/33](qa/33-all-models-compared.md) |
| Lean 0.8B plan | [qa/34](qa/34-lean-0.8b-plan.md) |
| 0.8B run | [qa/35](qa/35-0.8b-run.md) |
| Written into thesis | [qa/36](qa/36-size-extension-in-thesis.md) |
| **This A→Z guide** | [qa/37](qa/37-thesis-a-to-z-teacher.md) (copy of the practice core) |

Hard words: [GLOSSARY.md](GLOSSARY.md) · Every choice: [DECISIONS.md](DECISIONS.md)

---

## 6. Research chain (point at the wall)

```text
PROBLEM ✅ → GAP ✅ → QUESTION ✅ → HYPOTHESIS ✅
    → EXPERIMENT ✅ → DATA/CODE ✅ → RESULTS ✅
    → ANALYSIS ✅ → CONCLUSION ✅
```

You are here: **CONCLUSION written**; still fill **name/supervisor**, then defend.

---

## 7. What to do next (one path)

1. Read **Abstract + one-page summary** in THESIS.md (today).  
2. Practice the **Opening** answers out loud (10 minutes).  
3. Open **SIZE-COMPARISON.md** and point at the three best free ways.  
4. Fill your **name** in `thesis/00-front-matter.md` before hand-in.
