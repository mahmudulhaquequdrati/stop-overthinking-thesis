# PLAN: "Stop Overthinking, Keep Passing the Tests"

> **What is this file?** The research design: what exactly we will do.
> New here? Read [ROADMAP.md](ROADMAP.md) first.
> Every choice has its reason in [DECISIONS.md](DECISIONS.md).
> Teacher questions and answers are in [qa/](qa/).
> Hard word? See [GLOSSARY.md](GLOSSARY.md).
> The proposal that matches this plan is in [proposal/](proposal/).
>
> Status: **planned, nothing run yet** (2026-09-13).
> Cut to **one research question** on 2026-09-13 (DECISIONS #25).

---

## 1. The whole thesis on one screen

```text
PROBLEM     Small AI models "think" a lot on code, even easy code.
            That wastes time and computer power.
GAP         Nobody has tested this on ONE small model with a thinking ON/OFF switch:
            is TRAINING it to think shorter better than the free options?
            (free options = switch thinking OFF, set a thinking limit, or say "think briefly")
QUESTION    Does training on the model's shortest correct answers give
            a better balance of accuracy and length than the free options?
EXPERIMENT  Same model, same test problems, 5 ways of answering
RESULTS     Accuracy vs. thinking length (in tokens), with error bars
CONCLUSION  Is training worth it for code, on a small model?
```

A *token* is a small piece of text, about ¾ of a word.

**Everyday example.** A student writes 5 pages for every exam question, even
"2 + 2". We want to teach them to write short answers when short is enough,
without getting more questions wrong. We also check whether simply telling them
"don't think, just answer" works as well.

---

## 2. Why only one question

We want **one** study done well, with the best chance of a positive result, so it can
become a conference paper.

- **Savings are likely.** The same method (keep the shortest correct answer, train on it)
  already cut tokens on math (Munkhbat et al. 2025) and on code with a 7B model (SEER).
- **Clearest gap.** Our search found this gap (G-A, below) most clearly open.
- **Fits free GPUs.** It needs only **one** training run, so the free GPU time goes into doing it properly.
- **No need to beat thinking ON on accuracy.** We need a **better balance**:
  much shorter, almost as accurate, and more accurate than the free options.

**Honest:** nobody can promise a positive result. The room-to-shorten check in week 3 (§7)
warns us early.

---

## 3. Scope: easy + medium code problems only

We leave out hard problems, and we write this down as a limitation. Four reasons:

| # | Reason | In simple words |
|---|---|---|
| 1 | **Memory** | Thinking on hard problems is often 10,000–15,000 tokens. Training on a free T4 GPU fits about 3,500. |
| 2 | **Nothing to learn from** | A 4B model solves few hard problems, so there are few correct answers to train on. |
| 3 | **Time** | Long answers × 4 tries × thousands of problems is too slow on free GPUs. |
| 4 | **Nothing to measure** | If the base model scores about 0% on hard problems, we can't ask "did accuracy drop?" |

**Fair testing:** the 3,500-token limit is **only for training examples**.
At test time, every way of answering gets the **same** thinking limit (for example 8,000 tokens).
We record how often each one hits that limit.

**Risk: "always stop early".** A model that only sees short answers may learn to stop too early
on medium problems. Two protections:
1. LoRA adds a small add-on, so the base model stays unchanged.
2. Our selection rule skips answers shorter than half the median correct length.

---

## 4. The gap (from the 2026-09-13 paper search)

Full reading list: [PAPERS.md](PAPERS.md). Full search notes: [research/gaps.md](research/gaps.md).

| # | Gap | Verdict | What we do |
|---|---|---|---|
| **G-A** | On one small model with a thinking switch, nobody compares for code: thinking OFF · thinking budget · "think briefly" prompt · thinking ON · thinking ON + LoRA trained on shortest correct answers | OPEN | **The whole thesis** |

**Future work (dropped on 2026-09-13, DECISIONS #25):**
- how much training data is needed (a learning curve)
- does training on code also shorten math thinking (code → math transfer)
- LoRA size 8 vs 32
- fresh problems vs. problems the model may have seen
- GRPO (training with rewards)
- hard problems

**We do NOT claim to be:**
- the first to shorten code reasoning (SEER and ASAP did),
- the first on cheap GPUs (TokenSkip did),
- the first to show math → code transfer (HAPO and LC-R1 did).

---

## 5. The 9 research questions

| Question | Answer |
|---|---|
| **What am I testing?** | Does LoRA training on shortest correct answers give a better balance of accuracy and length on code than the built-in switch and simple prompts? |
| **Hypothesis** | Compared with thinking ON, the trained model: **(1)** uses ≥25% fewer thinking tokens, **(2)** loses ≤3 points of first-try pass rate (on the same problems), **(3)** is more accurate than thinking OFF, the thinking budget and the "think briefly" prompt. |
| **What I change** (independent variable) | The way of answering: thinking OFF · thinking budget (stop at k tokens) · "think briefly" prompt · thinking ON · thinking ON + our LoRA |
| **What I measure** (dependent variables) | First-try pass rate, called *pass@1* (averaged over 4 tries) · thinking tokens · % of answers that hit the thinking limit |
| **What we compare against** (baselines) | Thinking ON (the normal way), thinking OFF, thinking budget, "think briefly" prompt |
| **Data** | §6 |
| **How we judge** (metric) | Error bars (95%) made by comparing the same problems before and after, re-sampled many times (*paired bootstrap, grouped by problem*) · fixed seeds · a chart of accuracy vs. tokens |
| **Supports it** | All 3 parts are true on the code test set |
| **Proves it wrong** | A free option is as accurate as the trained model, or accuracy drops by more than 3 points |

---

## 6. Data

⚠️ Dataset ids come from the 2026-09-13 search. Re-check each one in the first data notebook.

| Role | Dataset (Hugging Face id) | Size | Notes |
|---|---|---|---|
| **Train (code)** | `agentica-org/DeepCoder-Preview-Dataset` (primeintellect + taco parts, MIT) · `codeparrot/apps` introductory (MIT) | Thousands | Has tests. **Drop DeepCoder's `lcbv5` part** (it overlaps with our test set). Keep examples ≤3,500 tokens. |
| **Test (code)** | HumanEval+ (164) + MBPP+ (378) + `livecodebench/code_generation_lite` easy + medium | ~1,000+ (LiveCodeBench counts still to check) | Never used for training. The base model and the trained model see the same problems, so the comparison stays fair. |

**How we load LiveCodeBench** (checked 2026-09-17): it uses a Python loading script that Hugging Face
refuses to run, so we download its `.jsonl` files directly. Each problem has a date (`contest_date`)
and a difficulty.

**How many problems are fresh** (counted 2026-09-17): from February 2025 on there are 131 problems:
**31 easy + 39 medium** + 61 hard. So only **70 fresh easy/medium problems**. That is too few to carry the
main result, so the fresh set is a side note; the main comparison uses the full paired test set (DECISIONS #41).

**Overlap check** (before any training): remove every training problem that matches
a test problem, exactly or nearly.

**How big must the test set be?**
- A 2–3 point accuracy change is small, so it is hard to see.
- Comparing the **same** problems before and after (a *paired* comparison) needs
  about **1,000–2,000 problems** to see it clearly.
- A big token change (−25%) shows with only a few hundred problems.

Details: [research/data-size-and-test-size.md](research/data-size-and-test-size.md).

---

## 7. Model, memory, and the checks

### The model

- **Main: `google/gemma-4-E4B-it`.** Released March 2026. Has a thinking ON/OFF switch. Apache-2.0 licence.
  Published cutoff: January 2025 (✅ checked on the model card 2026-09-17: it is the cutoff of the **pre-training** data; later training stages have no published date).
- **Backup: `Qwen/Qwen3.5-4B`.** February 2026. Thinking switch. Apache-2.0.

### How a 16 GB model fits in a 15 GB GPU

```text
A model = a huge list of numbers. Gemma-4-E4B has 8.0 billion of them.

16-bit  (2 bytes each)                → 16.0 GB   ✗ bigger than the GPU     (checked on HF)
4-bit   (only part of it squeezed)    → 11.0 GB   ✓ the file we load        (checked on HF)
On the GPU while training (short examples) → 10.7 GB peak  (measured by Unsloth on a T4)
```

Only 3.5 of the 8 billion numbers get squeezed to 4-bit. The word lookup tables and
the image and audio parts stay 16-bit. That's why the file is 11 GB, not 4 GB.
*Everyday example:* a big photo saved as a JPEG. A bit less detail, much smaller.

### The two checks (week 3, before spending GPU days)

1. **Memory check.** Train on 50 examples, each up to 3,500 tokens long.
   - Peak memory ≤14 GB → keep Gemma.
   - Otherwise → switch to Qwen3.5-4B (9.6 GB measured on a T4).
2. **Room-to-shorten check.** The base model answers 200 training problems, 4 times each.
   - **Share of problems solved at least once** must be **≥40%**.
   - **Room to shorten** (shortest correct length ÷ average correct length) must be **≤0.75**.
     This means short answers are at least 25% shorter.
   - Fails → **ask each problem 8 times instead of 4** (more chances for a short correct answer), then check again.
3. **Selection rule.** Keep the shortest correct answer, but not shorter than half the median correct length
   (the S3-CoT paper warns that the very shortest answers hurt accuracy).

### Risks we have not checked yet (checked in weeks 1–3)

- A Gemma-4 bug on the T4: a number gets too big in the audio part in 16-bit mode. We use text only.
- Whether vLLM (software that writes answers fast) runs Gemma-4 on a T4. Backup: Unsloth or `transformers` (slower).
- Free GPU limits change. Colab: up to 12 h per session, no published weekly limit. Kaggle: ~30 GPU-hours per week on 2×T4.

---

## 8. The method, step by step

```text
1. The base model answers each training problem 4 times (thinking ON)
          │
2. Grade every answer with the problem's tests (in a sandbox, a safe closed box)
          │
3. For each problem: keep the SHORTEST CORRECT answer (not below ½ the median)
          │
4. Train ONE LoRA add-on on those (problem → short correct answer)
          │
5. Test all 5 ways of answering on the same test problems, same limits, same seeds
```

---

## 9. Timeline (12 weeks, same as the proposal)

| Weeks | Work |
|---|---|
| 1–2 | Learn the tools, set up Colab/Kaggle, check the model and datasets, build the sandbox grader, first call with thinking ON vs. OFF |
| 3 | Memory check + room-to-shorten check |
| 4–5 | Test the 4 free ways of answering |
| 6–7 | Build training data (answer, grade, select), overlap check |
| 8–9 | Train the LoRA add-on, test it |
| 10–12 | Error bars, chart, write the thesis + paper draft |

---

## 10. Rough free-GPU budget (estimates, to be measured in the trial run)

⚠️ Estimates, not measurements. Full calculation and sources:
[research/gpu-time-budget.md](research/gpu-time-budget.md) (2026-09-17).

| Stage | How much text | GPU-hours (T4) |
|---|---|---|
| Making training data: ~4,000 problems × 4 answers × ~2,500 tokens | ~40M tokens written | 15–40 |
| Testing: 5 ways of answering × ~1,000 problems × 4 answers | ~30M tokens written | 10–30 |
| Checks and small trial runs (50 training examples; 200 problems × 4 answers) | ~2M tokens | 2–5 |
| **One LoRA training run** (~2,000 examples × ~1,800 tokens, **1 epoch** = one pass through the data) | 3.6M tokens seen | **3–7 (plan ~4)** |

- **Training is the cheapest part.** One run fits in one free session (Colab ≤12 h,
  Kaggle ~12 h per session and 30 GPU-hours per week). Making and grading answers costs far more.
- **Speed we assume: ~250 training tokens per second** (range 150–350). It comes from a calculation of how much
  math the GPU can do. **Not checked yet.** We measure it during the week-3 memory check, then redo this table.
- **Sort training examples by length, or pack them together.** Padding a 400-token example
  up to 3,500 tokens can make training up to 2× slower.
- In total: many tens of GPU-hours, spread over weeks on Kaggle (2 GPUs = 2 workers) and Colab.
- Save results to Google Drive every ~20 problems. Save a training checkpoint (a save point) every ~30 minutes.
- Calendar time ≈ 3–5× GPU time on a first attempt (crashes, re-runs, disconnects).

---

## 11. Working inside a 12-hour session limit

A free session is short (Colab "at most 12 h", Kaggle ~12 h, and both can end early),
but we need tens of hours. **We never run one long job.** Every job can **stop and continue later**.

*Everyday example:* reading a long book with a bookmark.

```text
start → connect Google Drive → read the "done" list → skip finished items
      → work → add results every ~20 problems → session dies → start again
```

| Stage | Needs one unbroken run? | How it survives a stop |
|---|---|---|
| Making training data (15–40 h) | No, problems are independent | "done" list + a results file we only add to, on Drive |
| Testing the 5 ways of answering (10–30 h) | No | same |
| LoRA training (3–7 h) | Fits one session | save point every ~30 min (the add-on, the training settings and progress, the data order, and the random seed state) |

**Rules:**
- **Only add** to results files. Never change old lines.
- Every result has a fixed name: `problem_id + sample_index + policy` (policy = the way of answering).
  This tells us what is already done.
- After each write, make sure the result is **really saved to disk** (flush + `fsync`).
- Each item has its own fixed seed, so the same item gives the same output in any session.
- Store the model's raw answers exactly as written, so re-grading never needs the GPU.

**Which GPU for what:**
- **Kaggle is the main worker.** Its "Save & Run All" keeps running **with the browser closed**,
  and it has 2 T4s (≈ 2 workers).
- **Colab** needs the browser tab open, so it is the second worker and the place to fix bugs.

⚠️ **Not checked yet (check in week 1):** whether a 2×T4 Kaggle session uses 1 or 2 hours
of the ~30 GPU-hour weekly limit per hour of real time.

**Cut the work before asking for more sessions.** Write many answers at the same time
(vLLM, 32–64 prompts at once). This is **2–5×** faster and changes nothing in the science, so do it first.
Full detail: [research/gpu-time-budget.md](research/gpu-time-budget.md) §8.
