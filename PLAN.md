# PLAN — "Think Less, Code Just as Well"

> The research design, in easy English. If you're new, read
> [ROADMAP.md](ROADMAP.md) first. This file is the "what exactly are we going to
> do" reference. Every choice below has its reason in [DECISIONS.md](DECISIONS.md).
> The proposal that matches this plan is in [proposal/](proposal/).
>
> Status: **planned, nothing run yet** (2026-09-13).
> Cut to **one research question** on 2026-09-13 (DECISIONS #25).

---

## 1. The whole thesis on one screen

```text
PROBLEM     Small reasoning models "think" a lot on code, even easy code → wasted time and compute
GAP         Nobody has tested, on ONE small model with a thinking switch:
            is TRAINING shorter thinking better than the free options (switch OFF, limit, "think briefly")?
QUESTION    Does "shortest correct answer" training give a better accuracy-for-tokens deal than the free options?
EXPERIMENT  Same model, same test problems, 5 ways of answering
RESULTS     Accuracy vs thinking tokens, with error bars
CONCLUSION  Is training worth it for code on a small model?
```

**Everyday example.** A student writes 5 pages for every exam question, even
"2 + 2". We want to teach them to write short answers when short is enough,
without getting more questions wrong. We also check whether simply telling them
"don't think, just answer" works as well.

---

## 2. Why only one question

We want **one** study done well, with the best chance of a positive result, so it can
become a conference paper.

- The method (keep the shortest correct answer, train on it) already cut tokens on math
  (Munkhbat et al. 2025) and on code with a 7B model (SEER). So token savings are likely.
- It is the gap our search found most clearly open (G-A below).
- It needs **one** training run, so free-GPU time goes into doing it properly.
- We don't need to beat thinking ON on accuracy. We need a **better balance**:
  much shorter, almost as accurate, and more accurate than the free options.

**Honest:** no one can promise a positive result. The headroom check in week 3 (§7)
warns us early.

---

## 3. Scope: easy + medium code problems only

Hard problems are a written limitation:
1. **Memory.** Hard-problem thinking is often 10,000–15,000 tokens. Training on a free T4 fits ~3,500.
2. **Nothing to learn from.** A 4B model solves few hard problems.
3. **Time.** Long answers × 4 tries × thousands of problems is too slow on free GPUs.
4. **Nothing to measure.** If the base model scores ~0% on hard, "did accuracy drop?" has no answer.

**Fairness at test time:** the 3,500-token cap is only for *training examples*.
Every way of answering gets the **same** test thinking limit (e.g. 8,000 tokens),
and we record how often each one hits it.

**Risk "always stop early":** a model shown only short answers may stop early on medium
problems. Protections: LoRA keeps the base model unchanged, and the selection rule skips
answers shorter than half the median correct length.

---

## 4. The gap (from the 2026-09-13 literature check)

Full reading list: [PAPERS.md](PAPERS.md). Full search notes: [research/gaps.md](research/gaps.md).

| # | Gap | Verdict | What we do |
|---|---|---|---|
| **G-A** | On one small hybrid-thinking model, nobody compares thinking OFF vs thinking budget vs "think briefly" prompt vs thinking ON vs thinking ON + shortest-correct LoRA, on code | OPEN | **The whole thesis** |

**Future work (dropped on 2026-09-13, DECISIONS #25):** how much training data is needed
(learning curve), code → math transfer, LoRA rank 8 vs 32, fresh vs possibly-seen problems,
GRPO, hard problems.

**We do NOT claim:** first to shorten code reasoning (SEER, ASAP), first on cheap
GPUs (TokenSkip), or any math transfer.

---

## 5. The 9 research questions

| Question | Answer |
|---|---|
| **What am I testing?** | Does shortest-correct LoRA training give a better accuracy-for-tokens deal on code than the built-in switch and simple prompts? |
| **Hypothesis** | Compared with thinking ON, the trained model: **(1)** uses ≥25% fewer thinking tokens, **(2)** loses ≤3 points of pass@1 (paired), **(3)** is more accurate than thinking OFF, the thinking budget and the "think briefly" prompt. |
| **Independent variable** (what I change) | The way of answering (the *policy*): thinking OFF · thinking budget (stop at k tokens) · "think briefly" prompt · thinking ON · thinking ON + our LoRA |
| **Dependent variables** (what I measure) | pass@1 (mean over 4 tries), thinking tokens, % of answers hitting the thinking limit |
| **Baselines** | Thinking ON (the normal way), thinking OFF, thinking budget, brief prompt |
| **Data** | §6 |
| **Metric** | Paired bootstrap 95% intervals, clustered by problem; fixed seeds; an accuracy-vs-tokens chart |
| **Supports it** | All 3 parts hold on the code test set |
| **Contradicts it** | A free option is as accurate as the trained model, or accuracy drops more than 3 points |

---

## 6. Data

⚠️ Dataset ids come from the 2026-09-13 search. Re-check each one in the first data notebook.

| Role | Dataset (Hugging Face id) | Size | Notes |
|---|---|---|---|
| **Train (code)** | `agentica-org/DeepCoder-Preview-Dataset` (primeintellect + taco parts, MIT) · `codeparrot/apps` introductory (MIT) | Thousands | Has tests. **Drop DeepCoder's `lcbv5` part** (it overlaps our test). Keep examples ≤3,500 tokens. |
| **Test (code)** | HumanEval+ (164) + MBPP+ (378) + `livecodebench/code_generation_lite` easy + medium | ~1,000+ (LCB counts to verify) | Never used for training. Base and trained model see the same problems, so the comparison stays fair |

**Overlap check** (before any training): remove every training problem that matches
a test problem, exactly or nearly.

**How big must the test set be?** A 2–3 point accuracy change is small. Comparing
the *same* problems before/after (paired) needs roughly **1,000–2,000 problems**
to see it clearly. A big token change (−25%) shows with a few hundred. Details:
[research/data-size-and-test-size.md](research/data-size-and-test-size.md).

---

## 7. Model, memory, and the checks

### The model

- **Main: `google/gemma-4-E4B-it`.** Released March 2026, has a thinking on/off switch, Apache-2.0.
  Training cutoff published as January 2025 (re-check on the model card).
- **Fallback: `Qwen/Qwen3.5-4B`.** Feb 2026, thinking switch, Apache-2.0.

### How a 16 GB model fits in a 15 GB GPU

```text
A model = a huge list of numbers. Gemma-4-E4B has 8.0 billion of them.

16-bit  (2 bytes each)                → 16.0 GB   ✗ bigger than the GPU     (checked on HF)
4-bit   (only part of it squeezed)    → 11.0 GB   ✓ file we load            (checked on HF)
On the GPU while training (short examples) → 10.7 GB peak  (measured by Unsloth on a T4)
```

Only 3.5 of the 8 billion numbers get squeezed to 4-bit. The word lookup tables and
the image and audio parts stay 16-bit. That's why the file is 11 GB, not 4 GB.
*Everyday example:* a RAW photo saved as a JPEG. A bit less detail, much smaller.

### The checks (week 3, before spending GPU days)

1. **Memory check.** Train 50 examples up to 3,500 tokens long.
   - Peak ≤14 GB → keep Gemma.
   - Otherwise → switch to Qwen3.5-4B (9.6 GB measured on a T4).
2. **Headroom check.** The base model answers 200 training problems 4 times each.
   - **Coverage** (share of problems with ≥1 correct answer) must be **≥40%**.
   - **Headroom** (shortest correct ÷ average correct length) must be **≤0.75**, i.e. short answers are at least 25% shorter.
   - Fails → **sample 8 answers per problem instead of 4** (more chances for a short correct one), then check again.
3. **Selection rule.** Shortest correct answer, but not shorter than half the median correct length (S3-CoT warning).

### Unverified risks (checked in weeks 1–3)

- A Gemma-4 bug on T4: a number overflow in the audio part in 16-bit mode. We use text only.
- Whether vLLM (fast generation software) runs Gemma-4 on a T4. Fallback: Unsloth or `transformers` (slower).
- Free GPU limits change: Colab up to 12 h per session, no published weekly quota. Kaggle ~30 GPU-h/week on 2×T4.

---

## 8. The method, step by step

```text
1. Base model answers each training problem 4 times (thinking ON)
          │
2. Grade every answer with the problem's tests (sandbox)
          │
3. Per problem: keep the SHORTEST CORRECT answer (not below ½ median)
          │
4. Train ONE LoRA add-on on those (problem → short correct answer)
          │
5. Test all 5 policies on the same test problems, same limits, same seeds
```

---

## 9. Timeline (12 weeks, same as the proposal)

| Weeks | Work |
|---|---|
| 1–2 | Learn the tools, set up Colab/Kaggle, check model + datasets, sandbox grader, first call ON vs OFF |
| 3 | Memory + headroom checks |
| 4–5 | Test the 4 free policies |
| 6–7 | Build training data (sample, grade, select), overlap check |
| 8–9 | Train the LoRA add-on, test it |
| 10–12 | Confidence intervals, chart, write thesis + paper draft |

---

## 10. Rough free-GPU budget (estimates, to be measured in the pilot)

- Making training data: ~4,000 problems × 4 answers × ~2,500 tokens ≈ 40M tokens.
- Testing: 5 policies × ~1,000 problems × 4 answers.
- One LoRA training run.
- Many tens of GPU-hours in total, spread over weeks on Kaggle (2 GPUs = 2 workers) and Colab.
- Save results to Google Drive every ~20 problems.
