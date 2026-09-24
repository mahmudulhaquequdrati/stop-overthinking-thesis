# 3. Method

This chapter says **what** we did and **why**. Chapter 4 explains **how we measured** it.

## 3.1 The design in one picture

```text
                        TRAINING (only for the LoRAs)
 MBPP+ 200 + old LiveCodeBench 80 ──► model answers 4× ──► check with tests ──► keep shortest correct ──► train LoRA-2
 (pilot: MBPP+ 100) ────────────────────────────────────────────────────────────────────────────────────► LoRA-1

                        TESTING (the same for all six ways)
 234 test problems ──► 6 ways × 2 tries = 2,808 answers ──► run the tests ──► accuracy, tokens, loops
```

The design is a **comparison on the same problems**: every way answers exactly the same 234 problems, with the same
settings, so the only thing that changes is the way of answering.

## 3.2 The model

| | |
|---|---|
| Model | **Qwen3.5-2B** (`unsloth/Qwen3.5-2B`), released February 2026, Apache-2.0 licence |
| Size | about 2 billion parameters; 4.6 GB in 16-bit |
| Why this model | Small, has a real thinking switch, free licence, and fast enough to finish in our time (Section 3.10) |
| Settings when answering | temperature 0.6, top-p 0.95, top-k 20 — the model makers' own settings for coding in thinking mode |

*Temperature, top-p and top-k* control how random the model's word choices are. We used the official settings, so
the model is not disadvantaged by our choices.

## 3.3 The six ways of answering

| # | Way | Exactly what we did |
|---|---|---|
| 1 | **Thinking ON** | Switch on. The model thinks as long as it wants (up to the overall token limit). **What we compare against.** |
| 2 | **Thinking OFF** | Switch off. The model answers directly. |
| 3 | **Think briefly** | Switch on, and one sentence added to the question: *"Think briefly: keep your thinking to a few short sentences, then give the answer."* |
| 4 | **Thinking limit** | Switch on. After **1,024** thinking tokens we stop the thinking, add the end-of-thinking marker ourselves, and let the model write its answer. |
| 5 | **LoRA-1** | Switch on, plus the LoRA trained in the pilot study (100 MBPP+ training problems). |
| 6 | **LoRA-2 (main)** | Switch on, plus the LoRA trained for this run (200 MBPP+ + 80 older LiveCodeBench problems). |

**Why 1,024 for the limit?** In the pilot study, the trained model thought for about 1,000 tokens. So the limit
asks a fair question: *is a simple hard cut as good as training?*

**Why LoRA-2 is the main one.** We decided **before** the run that LoRA-2 would be the main result if it was trained.
This stops us from picking whichever LoRA looks best afterwards.

## 3.4 The test problems (234)

| Set | Problems | Level | What the model must do |
|---|---|---|---|
| HumanEval+ | 164 | easy | Complete one Python function |
| LiveCodeBench | 31 | easy | Write a full program: read input, print output (a few are class methods) |
| LiveCodeBench | 39 | medium | The same, harder |
| **Total** | **234** | | |

- The LiveCodeBench problems were released from **February 2025 on**.
- **Hard problems were left out.** A 2-billion-parameter model solves almost none, so they could not show differences.
- The test set was **fixed on 2026-09-20, before any result**.

**The question the model saw** (identical for every way, except "think briefly"):

```text
HumanEval+:     "Complete this Python function. Answer with one Python code block only,
                 containing the complete function."  + the function to complete

LiveCodeBench:  the problem text  + "Write a complete Python program. It reads from standard input and
                 prints the answer to standard output. Answer with one Python code block only."
```

## 3.5 The training data

| Pool | Problems | Why |
|---|---|---|
| MBPP+ | 200 | Easy Python problems with good tests; the pilot showed they work |
| LiveCodeBench, older (release v1, before February 2025) | 80 (40 easy + 40 medium) | The same *type* as the LiveCodeBench test problems, but older, so they can never be test problems |

**Overlap check.** No test problem may appear in the training data. A script compared every training problem with
every test problem and removed any that had the same function name, or shared many 5-word pieces of text (30% or
more). It removed one training problem (`Mbpp/309`).

## 3.6 Making the training examples: "shortest correct"

```text
For each training problem:
  1. Thinking ON answers it 4 times (token limit: 4,096 for MBPP+, 8,192 for LiveCodeBench).
  2. Each answer is checked with the problem's tests.
  3. From the correct answers, keep the SHORTEST one ...
  4. ... but never one shorter than HALF of the middle (median) correct length for that problem.
```

**Why step 4?** The S3-CoT paper warns that training on the very shortest answers can hurt accuracy. A lucky, too-short
answer would teach "always stop early". So we keep the shortest *reasonable* answer.

The kept answer is stored **word for word**, with its thinking and its code, and becomes one training example.

## 3.7 Training the LoRA

| Setting | Value |
|---|---|
| Method | LoRA on the attention and feed-forward layers |
| LoRA size | rank 16, alpha 16 |
| Learning rate | 0.0002, with a short warm-up |
| Epochs (passes over the data) | 3 |
| Batch | 1 example × 4 steps gathered together |
| Seed | 3407 |
| Tool | Unsloth, following its Qwen3.5 guide |

LoRA-2 trained on **157 examples** (133 from MBPP+, 24 from LiveCodeBench) in about **6 minutes**.

**A safety check on the add-on.** In the pilot we found that the saved LoRA could load "empty", with its parts matched to
nothing, so the "trained" model silently behaved like the untrained one. The answering script now **stops** if any LoRA part
is not matched to the model. This check passed for both LoRAs.

## 3.8 The pilot study (the "mini-thesis")

Before the main run, we ran the whole method once, small:

- 100 MBPP+ training problems → shortest-correct examples → LoRA-1.
- Tested on **100 other MBPP+ problems**, 1 try each.

**Pilot result:** LoRA-1 used 41% fewer tokens than thinking ON (x0.59) **and** was more accurate (65% against 50%).
This was a strong sign that the method works, so we went ahead with the main run. The main run then tested whether
this holds on **different** problems (Chapter 5.10).

## 3.9 The fairness rules (fixed before the run)

| Rule | Value | Why |
|---|---|---|
| Same problems for every way | all 234 | a fair, paired comparison |
| Same overall token limit for every way | **4,096** (HumanEval+), **8,192** (LiveCodeBench) | nobody gets more room |
| Same settings and seeds | temperature 0.6, top-p 0.95, top-k 20; a fixed seed per try | only the way of answering changes |
| Same prompt | except the one extra sentence for "think briefly" | |
| Tries per problem | **2** | budget (Section 3.10) |
| Main LoRA | LoRA-2 | fixed in advance |
| Hypotheses and their thresholds | H1–H3 (Section 1.4) | fixed in advance |
| Grading | the benchmarks' own tests, never by eye | Chapter 4 |
| Raw answers | every answer saved word for word | anyone can re-check |

**Why 4,096 and 8,192?** HumanEval+ problems are easy; in the pilot almost every answer that reached 4,096 was a loop.
LiveCodeBench has medium problems, where honest reasoning can be longer. To check that these limits did not unfairly hurt
normal thinking, we re-ran thinking ON's cut-off answers with **16,384** tokens (Section 4.9).

## 3.10 How the run was done

| Stage | What | Colab units (estimated) |
|---|---|---|
| Smoke test | every way on 2 problems per set, to check that everything works | 0.6 |
| A | 5 ways × 234 problems, try 1 | 2.9 on 24 Sept, plus part of the 21 Sept session (that session used about 8.7 units in total, including idle time) |
| B | make LoRA-2's training data, train LoRA-2, test it (try 1) | 9.0 |
| C | try 2 for all 6 ways | 10.3 |
| D | re-run thinking ON's cut-off answers with 16,384 tokens | 4.2 |

- **Computer:** one Google Colab **A100** GPU, bfloat16 numbers, batches of up to 128 answers at a time.
- **Budget rule:** a stage started only if at least 20 units would be left afterwards.
- **Total:** about 38 units, from 2026-09-21 to 2026-09-24 (including set-up time).
- Results were saved to Google Drive after every step, so a disconnect lost nothing.

## 3.11 What changed from the proposal, and why

We report every change honestly. All were made **before** the main results were seen.

| Proposal | What we did | Why |
|---|---|---|
| Model Gemma-4-E4B | **Qwen3.5-2B** | Gemma ran at only about 4.4 tokens per second on a free GPU; far too slow to finish. Qwen3.5-2B is smaller and has the same kind of switch. |
| Free GPUs only ($0) | A small paid Colab package (A100) | A one-week deadline; free GPUs were too slow. |
| About 1,000 test problems incl. MBPP+ | **234** (HumanEval+ + LiveCodeBench) | 1,000 problems × 5 ways × 4 tries would need 13+ GPU hours. |
| 4 tries per problem | **2** | Budget. Cost: wider error bars. |
| Training on DeepCoder and APPS | MBPP+ + older LiveCodeBench | Already loaded and graded by tested code; less risk in one week. |
| Five ways of answering | **Six** (two LoRAs) | LoRA-2 added medium-style training problems; LoRA-1 kept for comparison. |

## 3.12 Ethics and safety

- The model's code was **never run inside our notebook**. It ran in a separate process, in a temporary folder, with a time
  limit, so broken or harmful code could not damage anything.
- No personal data was used. All data sets are public.
