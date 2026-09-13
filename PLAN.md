# PLAN — "Think Less, Code Just as Well"

> The research design, in easy English. If you're new, read
> [ROADMAP.md](ROADMAP.md) first. This file is the "what exactly are we going to
> do" reference. Every choice below has its reason in [DECISIONS.md](DECISIONS.md).
>
> Status: **planned, nothing run yet** (2026-09-13).

---

## 1. The whole thesis on one screen

```text
PROBLEM     Small reasoning models "think" a lot on code, even easy code → wasted time and compute
GAP         Nobody has tested, on ONE small model with a thinking switch:
            is TRAINING shorter thinking better than just switching thinking OFF?
QUESTION    Can "shortest correct answer" training make the model think shorter on code,
            keep its accuracy, beat the switch, and carry over to math?
EXPERIMENT  Same model, same test problems, 5 ways of answering; a learning curve; a math test
RESULTS     Accuracy vs thinking tokens, with error bars
CONCLUSION  When training is worth it, how much data it needs, whether it transfers
```

**Everyday example.** A student writes 5 pages for every exam question, even
"2 + 2". We want to teach them to write short answers when short is enough,
without getting more questions wrong. We also check whether simply telling them
"don't think, just answer" works as well.

---

## 2. Code or math? → Code is the main topic, math is the transfer test

| | Code (main) | Math |
|---|---|---|
| Is it new? | ✅ Only ~3 papers train shorter thinking on code (ASAP, SEER, EvoThink), all on older always-thinking 7B models | ❌ Dozens of papers already |
| Transfer test | ✅ Train on code → test on math: **no paper found** | ❌ Math → code already done (HAPO, LC-R1, One-Domain-to-All, ETR) |
| Unseen test problems | ✅ LiveCodeBench 2025 problems (after the model's cutoff) | ~125 contest problems |
| Grading | ⚠️ Harder: run the code safely with tests | ✅ Easy: compare one answer |
| On a free GPU | ⚠️ Code thinking is long, so training examples are capped at ~3,500 tokens | ✅ Shorter |

**Why code wins:** a thesis is judged on what's new, and the open gaps are on
the code side. Grading code is a skill we learn once.

---

## 3. Scope: easy + medium problems only

**We train and test on easy + medium code problems.** Hard problems are a written limitation.

Why not hard problems:
1. **Memory.** Hard-problem thinking is often 10,000–15,000 tokens. Training on a free T4 fits ~3,500.
2. **Nothing to learn from.** A 4B model solves few hard problems. No correct answer means no training example.
3. **Time.** Long answers × 4 tries × thousands of problems is too slow on free GPUs.
4. **Nothing to measure.** If the base model scores ~0% on hard, "did accuracy drop?" has no answer.

**One pre-set exception:** the first pilot also tries 50 hard problems.
- Base model solves **≥15%** → we add a small hard check at the end (H7).
- Below 15% → hard stays a limitation.

### Will training on short answers break testing?

- **Fairness: no problem.** The 3,500-token cap is only for *training examples*.
  At test time **every** way of answering gets the **same** thinking limit
  (e.g. 8,000 tokens), and we record how often each one hits it.
- **Behaviour: a real risk, and we measure it.** A model shown only short answers
  may learn "always stop early", even on medium problems that need more thinking.
  Protections:
  1. **LoRA** adds only a small piece, so the base model's long-thinking ability stays.
  2. **Selection rule:** shortest correct answer, but **not below half the median**
     correct length, so training shows a range of lengths.
  3. **Adaptivity check (H7'):** the trained model should still think **longer on
     medium than on easy**. If not, and medium accuracy drops, we report that failure.

---

## 4. The gaps we fill (from the 2026-09-13 literature check)

Full reading list: [PAPERS.md](PAPERS.md). Full search notes: [research/gaps.md](research/gaps.md).

| # | Gap | Verdict | What we do |
|---|---|---|---|
| **G-A (main)** | On one small hybrid-thinking model, nobody compares thinking OFF vs thinking budget vs "think briefly" prompt vs thinking ON vs thinking ON + shortest-correct LoRA, on code | OPEN | The main experiment: **is training better than flipping the switch?** |
| **G-B** | No learning curve for how much data shortest-correct training needs | OPEN (not found) | Train on 100 / 250 / 500 / 1k / 2k examples, draw the curve |
| **G-C** | Code → math transfer of shorter thinking | OPEN (not found) | Train on code, test on MATH-500 + AIME 2026 + HMMT Feb 2026 |
| G-D (secondary) | LoRA cost ~7 points vs full fine-tuning in SEER | Partly | LoRA rank 8 vs 32 |
| G-E (secondary) | Fresh vs possibly-memorized problems, for a 2026 model | Thin | Compare savings on pre- vs post-cutoff LiveCodeBench |

**We do NOT claim:** first to shorten code reasoning (SEER, ASAP), first on cheap
GPUs (TokenSkip), or math → code transfer (HAPO, LC-R1).

---

## 5. The 9 research questions

| Question | Answer |
|---|---|
| **What am I testing?** | Does shortest-correct LoRA training give a better accuracy-for-tokens deal on code than the built-in switch and simple prompts? |
| **Hypotheses** | **H1** thinking tokens −25% or more vs base ON. **H2** accuracy within 3 points of base ON (paired). **H3** better accuracy than OFF, budget and brief prompt at equal or fewer tokens. **H4** (exploratory) savings level off by ≤1,000 examples. **H5** on math, tokens fall with ≤3 points accuracy loss. **H6** same direction on post-cutoff problems. **H7'** trained model still thinks longer on medium than easy; medium accuracy within 3 points. *(H7: hard check only if the pilot gate allows it.)* |
| **Independent variable** (what I change) | The way of answering (the *policy*): thinking OFF · thinking budget (stop at k tokens) · "think briefly" prompt · thinking ON · thinking ON + our LoRA (trained on 100–2k examples) · LoRA rank 8 vs 32 |
| **Dependent variables** (what I measure) | pass@1 (mean over 4 tries), thinking tokens, % of answers hitting the thinking limit |
| **Baselines** | Base thinking ON (the normal way), thinking OFF, thinking budget, brief prompt |
| **Data** | §6 |
| **Metric** | Paired bootstrap 95% intervals, clustered by problem; fixed seeds; an accuracy-vs-tokens (Pareto) chart |
| **Supports it** | H1 + H2 + H3 hold on the code test set |
| **Contradicts it** | OFF or the brief prompt does as well as the trained model, or accuracy drops more than 3 points |

---

## 6. Data

⚠️ Dataset ids come from the 2026-09-13 search. Re-check each one in the first data notebook.

| Role | Dataset (Hugging Face id) | Size | Notes |
|---|---|---|---|
| **Train (code)** | `agentica-org/DeepCoder-Preview-Dataset` (primeintellect + taco parts, MIT) · `codeparrot/apps` introductory (MIT) | Thousands | Has tests. **Drop DeepCoder's `lcbv5` part** (it overlaps our test). Keep examples ≤3,500 tokens. |
| **Test (code, standard)** | HumanEval+ (164) + MBPP+ (378) + LiveCodeBench easy + medium before the cutoff | ~1,000+ (LCB counts to verify) | Old, maybe seen by the model, but seen by *both* base and trained, so the comparison stays fair |
| **Test (code, fresh)** | `livecodebench/code_generation_lite`, easy + medium, dated after the model's cutoff | Count to verify | Provably unseen if the cutoff is published |
| **Transfer (math)** | MATH-500 + `MathArena/aime_2026` ✔ + `MathArena/hmmt_feb_2026` ✔ | ~560 | Code → math |

**Overlap check** (before any training): remove every training problem that matches
a test problem, exactly or nearly.

**How big must the test set be?** A 2–3 point accuracy change is small. Comparing
the *same* problems before/after (paired) needs roughly **1,000–2,000 problems**
to see it clearly. A big token change (−25%) shows with a few hundred. Details:
[research/data-size-and-test-size.md](research/data-size-and-test-size.md).

---

## 7. Model, memory, and the gates

### The model

- **Main: `google/gemma-4-E4B-it`.** Released March 2026, has a thinking on/off switch, Apache-2.0.
  Its training cutoff is **published as January 2025** (re-check on the model card).
  That makes every 2025–26 problem provably unseen.
- **Fallback: `Qwen/Qwen3.5-4B`.** Feb 2026, thinking switch, Apache-2.0. No published cutoff.

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

### The gates (checked before spending GPU days)

1. **Memory gate.** Train 50 examples up to 3,500 tokens long.
   - Peak ≤14 GB → keep Gemma.
   - Otherwise → switch to Qwen3.5-4B (9.6 GB measured on a T4). H6 then becomes "likely unseen".
2. **Headroom gate.** The base model answers 200 training problems 4 times each.
   - **Coverage** (share of problems with ≥1 correct answer) must be **≥40%**.
   - **Headroom** (shortest correct ÷ average correct length) must be **≤0.75**, i.e. short answers are at least 25% shorter.
   - Otherwise we change the difficulty or the method **before** scaling up.
   - Same pilot: 50 hard problems. Solves ≥15% → add the H7 hard check.
3. **Selection rule.** Shortest correct answer, but not shorter than half the median correct length (S3-CoT warning).
4. **Stretch (GRPO, reinforcement learning).** Penalise length **only on correct answers** (Acoer warning: penalising wrong answers too made training collapse).

### Unverified risks (checked in the pilot)

- A Gemma-4 bug on T4: a number overflow in the audio part in 16-bit mode. We use text only.
- Whether vLLM (fast generation software) runs Gemma-4 on a T4. Fallback: Unsloth or `transformers` (slower).
- Free GPU limits change: Colab up to 12 h per session, no published weekly quota. Kaggle ~30 GPU-h/week on 2×T4 (P100 no longer works with current PyTorch).

---

## 8. The method, step by step

```text
1. Base model answers each training problem 4 times (thinking ON)
          │
2. Grade every answer with the problem's tests (sandbox)
          │
3. Per problem: keep the SHORTEST CORRECT answer (not below ½ median)
          │
4. Train a LoRA add-on on those (problem → short correct answer)
          │
5. Test all 5 policies on the same held-out problems, same limits
          │
6. Repeat step 4 with 100 / 250 / 500 / 1k / 2k examples → learning curve
          │
7. Test the trained model on math (transfer) and on post-cutoff problems
```

---

## 9. Rough free-GPU budget (estimates, to be measured in the pilot)

- Making training data: ~4,000 problems × 4 answers × ~2,500 tokens ≈ 40M tokens.
- Testing: ~7 policies × ~1,500 problems × 4 answers.
- Many tens of GPU-hours in total, spread over weeks on Kaggle (2 GPUs = 2 workers) and Colab.
- Save results to Google Drive every ~20 problems.
