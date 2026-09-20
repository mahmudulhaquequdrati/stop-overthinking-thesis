# Q&A 22: The pilot on the Mac — 30 real problems

⬅️ [All Q&A](README.md) · Hard word? See [GLOSSARY.md](../GLOSSARY.md) · Result: [results/2026-09-20-pilot-e2b-humaneval.md](../results/2026-09-20-pilot-e2b-humaneval.md)

---

## 1. The step in 2 sentences

We asked Gemma-4-E2B the first 30 HumanEval problems on the user's own Mac, with thinking ON and OFF, and graded the answers with the benchmark's own tests.
It solved 93% with thinking OFF and 83% with thinking ON, and thinking ON used 5.5× more tokens.

---

## 2. Questions a teacher may ask

**Q: Why run a pilot at all?**
To check, before spending days, that the model solves enough problems. If it solves almost nothing, there are no correct answers to make shorter, and the whole method has nothing to work with. Our rule (PLAN §7) is at least 40%. We got 93%.

**Q: What exactly did you measure?**
For every answer: did it pass the benchmark's tests, how many thinking tokens, how many tokens in total, and whether the answer was cut off by our token limit.

**Q: How did you grade?**
Each answer runs in its **own** short-lived process, in a temporary folder, with a 15-second limit, against HumanEval's own test code. We never run model-written code inside our own program.

**Q: How do you know the grading is right?**
A control test: we graded the benchmark's **official** solutions. They score 30/30 = 100%. Before the fix, evalplus's own runner gave them **0%**, which is how we found that its Linux-style memory limit does not work on macOS.

**Q: Thinking ON scored lower. Doesn't that kill your thesis?**
No, and the reason matters. 4 of the 5 ON failures were **cut off** by our 2,048-token limit, so the code was broken in the middle. Among answers that were not cut off, ON scored 96% and OFF 93%. A limit that cuts long answers punishes exactly the way of answering that writes more, so it was unfair. We raised the limit to 4,096 for **all** ways of answering and we report how often it is hit.

**Q: What does 5.5× more tokens mean for the thesis?**
It is the waste we want to remove. Thinking ON writes about 1,110 tokens where OFF writes 202, for problems where both are usually right. That is a lot of room to shorten.

**Q: Why did you say HumanEval is "too easy"?**
Because thinking OFF already solves 93%. There is almost no space left to be better. To show when thinking is worth its cost, we need harder (medium) problems too.

---

## 3. Hard questions

**Q: 30 problems, one answer each. Isn't that far too little?**
Yes, for a final result. This is a pilot: its job is to answer "does the setup work, and is the model strong enough?" The final numbers come from the full test set with error bars.

**Q: You changed the token limit after seeing results. Is that allowed?**
Yes, and it must be written down, which we did (DECISIONS #50). We changed a **setup mistake** found in a **pilot**, before touching the main test set, and the new limit is the same for every way of answering. What is not allowed is changing the hypothesis, or picking test problems, after seeing the main results. We did not do that.

**Q: You are using HumanEval's original tests, not the harder HumanEval+ ones. Why?**
Because the tool that runs the extra tests does not work on macOS. It is an honest limit, written in the results file, and we will run the harder tests on Linux (Colab or Kaggle) before the final numbers.

**Q: The model is small. Is a 93% score believable?**
For HumanEval, yes: it is a well-known, fairly easy benchmark, and modern small models score high. Two other facts support it: our grader passes its control test, and the failures have sensible reasons (a cut-off answer, a timeout, two wrong answers).

---

## 4. Checked vs. assumed

| We checked | Not checked yet |
|---|---|
| 93% (OFF) and 83% (ON) on 30 problems | The other 134 HumanEval problems, and MBPP+ |
| The grader is right (official solutions 30/30) | The harder HumanEval+ tests (need Linux) |
| ON writes 5.5× more tokens than OFF | Medium problems, where thinking should pay off |
| 4 ON answers failed because they were cut off | What a fair 4,096-token limit changes |

---

## 5. Where it is written

- [results/2026-09-20-pilot-e2b-humaneval.md](../results/2026-09-20-pilot-e2b-humaneval.md) · [graded CSV](../results/2026-09-20-pilot-e2b-humanevalplus-graded.csv)
- [DECISIONS.md](../DECISIONS.md) rows #50 (the pilot and the two fixes) and #51 (our own grader)
- Code: `scripts/mac_pilot_generate.py` *(deleted 2026-09-20 when we moved to Colab, DECISIONS #52 — still in git history)* · [scripts/grade_humaneval.py](../scripts/grade_humaneval.py)
