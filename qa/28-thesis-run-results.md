# Q&A 28: The real thesis run: the results, and what they mean

⬅️ [All Q&A](README.md) · Hard word? See [GLOSSARY.md](../GLOSSARY.md) · Decision: [#67](../DECISIONS.md) · Numbers: [results/2026-09-24-thesis-run.md](../results/2026-09-24-thesis-run.md)

---

## 1. The step in 2 sentences

We ran all 6 ways of answering on the 234 test problems, 2 tries each, on a Colab A100. Our
trained model (LoRA-2) did **not** think shorter, and a simple thinking limit gave the best accuracy.

```text
ON 42.1% ── LoRA-2 45.1% (not shorter, gain not proven) ── limit 49.8% (best, proven +7.7)
                         why?  most long answers are LOOPS, not careful thinking
```

**Where we are:** `EXPERIMENT ✅ → DATA ✅ → RESULTS ✅ → ANALYSIS ⬅ HERE → CONCLUSION`

---

## 2. Questions a teacher may ask

**Q: What was your main result?**
Training the model on its own shortest correct answers did not make it think shorter on the test
problems (x1.00 of normal thinking). Accuracy went up 3 points, but the error bar includes 0.

**Q: Which way was best?**
The thinking limit: let the model think, but stop at 1,024 thinking tokens. It scored 49.8%
against 42.1% for normal thinking. The error bar [+4.3, +11.3] is fully above 0, so this is proven.

**Q: Why did the limit win?**
Most answers that ran too long were **loops**: the model repeated the same lines until the limit
(66–90% of cut-off answers). When normal thinking *finishes*, it is already short (middle 672 tokens
on HumanEval+). So there was little careful thinking to cut, and a lot of looping to stop.

**Q: Why didn't your training work here when it worked in the mini-thesis?**
Two reasons, both checked. (1) The mini-thesis tested on MBPP+, the same kind of problems it trained
on; HumanEval+ and LiveCodeBench are different. (2) LoRA-2's LiveCodeBench training examples were
few (24) and long (middle 4,709 tokens), because the model almost never solved medium problems (1 of 160).
So it learned to think *long* on those.

**Q: Why is "think briefly" so bad (6.6%)?**
The sentence clashed with our other rule, "answer with one code block only". The model argued with
itself about the two rules until it ran out of tokens. We checked this by reading the answers. This is
a result for this one wording, not for asking to be brief in general.

---

## 3. Hard questions

**Q: Wasn't your 4,096 token limit unfair to normal thinking?**
A little, on HumanEval+. We measured it (stage D): with 16,384 tokens, normal thinking goes from
53.7% to 59.1% on try 1. That's almost the limit way's 60.4%. On LiveCodeBench it only goes from
10.0% to 17.1%, still below the limit (25.7%) and OFF (28.6%), because loops don't end with more room.

**Q: Isn't this a failed thesis?**
No. The question was "is training better than the free options?". The answer, measured with error
bars, is "not on this model; a free limit is better, because the waste is loops". A clear negative
answer with a reason is a real result.

**Q: Did you choose LoRA-2 because it looked good?**
No. LoRA-2 was named the main model **before** the run (DECISIONS #66). LoRA-1 did slightly better
(45.5%, x0.87 thinking), but we report LoRA-2 as the main result, as fixed in advance.

---

**Q: Why is thinking OFF not 4× faster on the GPU, if it writes 4× fewer tokens?**
We answer in batches of up to 128, and a batch waits for its slowest answer. A few OFF answers
on LiveCodeBench still ran to 8,192 tokens, so its batches took long (29 vs 38 minutes). One answer
at a time, time follows tokens. So we use **tokens** as the cost measure (DECISIONS #68).

**Q: How many of the 234 problems could the model solve at all?**
168 were solved by at least one way in at least one try. 66 were solved by no way.

---

## 4. Checked vs. assumed

| Checked | Assumed / not checked |
|---|---|
| Every table number matches the raw graded files | The loop test is rough; the true loop share is probably higher |
| Loops: counted in the raw answers | That the same happens on bigger models |
| "Brief" failure: read in the raw answers | That another "brief" wording would do better (not tested) |
| Stage D, training-set sizes, try-1 numbers | Colab's real units left (the ledger's ~30 is an estimate) |

---

## 5. Where it is written

- **Everything, with 10 charts and every problem:** [results/full-results/FULL-RESULTS.md](../results/full-results/FULL-RESULTS.md)
- Numbers and meaning (short): [results/2026-09-24-thesis-run.md](../results/2026-09-24-thesis-run.md)
- Raw files: [results/2026-09-24-thesis-run/](../results/2026-09-24-thesis-run/)
- Checker: [scripts/check_thesis_run.js](../scripts/check_thesis_run.js)
- Decision: [DECISIONS #67](../DECISIONS.md)
