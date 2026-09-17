# Research note — how long does the LoRA training run take? (2026-09-17)

> Hard word? See [GLOSSARY.md](../GLOSSARY.md).
>
> **Why this note exists:** the user asked "how much time to train our model with
> LoRA?". (*LoRA* is a cheap way to train: we train a small add-on, not the whole model.)
>
> ⚠️ **Nothing has been run yet.** Every number here is **math done on estimates**,
> not a measurement. The pilot in week 3 turns them into real numbers.
>
> Decisions drawn from this: [DECISIONS.md](../DECISIONS.md) #30 and #31.

---

## 0. The answer in one line

**One LoRA run ≈ 3–7 GPU-hours on one free T4** (best guess **~4 h**, one epoch).

- A *GPU* is the chip that does the heavy math for AI. A *GPU-hour* is one GPU busy for one hour.
- A *T4* is the older, smaller GPU that Colab and Kaggle give for free.
- An *epoch* is one pass through all the training examples.

What this means:

- It fits inside a single free session.
- It is the **cheapest** part of the thesis.
- Making the training data (~15–40 h) costs far more.
- Testing 5 ways of answering (~10–30 h) also costs far more.

---

## 1. What "training time" depends on

**Everyday example:** how long it takes to read a pile of books depends on
how many pages there are, and how fast you read. Nothing else.

```text
time  =  (number of examples × tokens per example)  ÷  training speed (tokens/second)
            └──────── how much text ────────┘            └── how fast the GPU eats it ──┘
```

(A *token* is a small piece of text, about ¾ of a word.)

- Nothing else matters much.
- LoRA rank, learning rate and batch size change the *result*, not the *clock*.
  (These are training settings: add-on size, step size, and how many examples go in at once.)

## 2. The three inputs, with their sources

| Input | Value used | Where it comes from | Checked? |
|---|---|---|---|
| Training examples | **~2,000** | ~4,000 training problems ([PLAN.md](../PLAN.md) §10) × share of problems solved at least once ≥40% (gate, PLAN §7), minus problems dropped by the overlap check | assumed |
| Tokens per example | **~1,800** (prompt ~300 + kept answer ~1,500) | An average written answer ≈2,500 tokens (PLAN §10). We keep the *shortest correct* one. The room-to-shorten gate demands ≤0.75 of the average | assumed |
| Training speed | **~250 tokens/s** (range 150–350) | Computer-arithmetic math, §3 | **unverified** |
| Epochs | **1** | Munkhbat et al. 2025 trained on shortest-correct answers for 1 epoch ([data-size note](data-size-and-test-size.md)) | from paper |

(A *gate* is a check we set in advance. If it fails, we stop and rethink.)

Tokens per epoch = 2,000 × 1,800 ≈ **3.6M tokens**.

## 3. Where 250 tokens/second comes from

### 3a. The idea

**Everyday example:** to know how fast a worker is, divide how much work they can do
per second by how much work one item needs.

- Work one token needs = amount of computer arithmetic per token.
- Work the T4 can do = amount of computer arithmetic per second.
- Speed = the second one ÷ the first one.

### 3b. Work for one token

Training one token costs about `8 × (active parameters)` small math steps.
(*Parameters* are the model's numbers. "Active" = the ones used for each token.)
The amount of computer arithmetic is counted in *FLOPs* (one FLOP = one small math step).

Why 8:

- **2** for the forward pass (the model reads the text and makes a guess).
- **4** for the backward pass (the model works out how to fix its numbers).
- **2** more for *gradient checkpointing*. This saves memory by not storing
  in-between results. So it must run the forward pass a second time.

### 3c. The math

```text
Gemma-4-E4B active params ≈ 4e9
cost per token ≈ 8 × 4e9        = 3.2e10 FLOPs
T4 peak (fp16)                   = 65 TFLOPS  →  realistic 6–12 TFLOPS with
                                   4-bit dequantisation + checkpointing (10–18%)
speed = 1.0e13 / 3.2e10          ≈ 310 tokens/s at 10 TFLOPS
                                 ≈ 190 tokens/s at 6 TFLOPS
```

How to read it:

- `4e9` means 4 × 10⁹ = 4 billion. `3.2e10` = 32 billion.
- *TFLOPS* = trillions of FLOPs per second. So 10 TFLOPS = `1.0e13` per second.
- *fp16* = numbers stored in a normal half-size format. This is the T4's best case: 65 TFLOPS.
- We squeeze the model's numbers to *4-bit* so it takes less memory.
  But then the GPU must unsqueeze them ("dequantisation") during work.
  That, plus checkpointing, means the T4 really uses only 10–18% of its peak.
  So we expect 6–12 TFLOPS.
- 10 TFLOPS gives ≈ 310 tokens/s. 6 TFLOPS gives ≈ 190 tokens/s.

### 3d. A second way to check

- An A100 (a big paid GPU) is ~5× a T4 on fp16.
- *QLoRA* (LoRA on a squeezed 4-bit model) of an 8B model on an A100 is
  commonly ~1,500 tokens/s.
- 1,500 ÷ 5 → ~300 on a T4.

The two ways agree, so 150–350 is a fair range.
⚠️ **Still unverified** — measure it.

## 4. The result

| Speed | Time for 3.6M tokens (1 epoch) |
|---|---|
| 150 tokens/s | 6.7 h |
| **250 tokens/s** | **4.0 h** |
| 350 tokens/s | 2.9 h |

**Plan for ~4 h. Budget 7 h.**

Free session limits:

- Colab ≤12 h.
- Kaggle ~12 h per session, and 30 GPU-h per week
  ([models-and-gpu note](models-and-gpu.md) §4).

So one run fits in one session, with room to spare.

### Things that would make it slower

| Risk | Effect | Fix |
|---|---|---|
| **Padding.** Examples in one batch must be the same length. So a 400-token example next to a 3,500-token one gets filled with empty tokens up to the long length | up to **2× slower** | Pack sequences (join short examples into one row), or sort examples by length before making batches |
| 2 epochs instead of 1 | 2× | Start with 1 epoch. That is what the closest paper did |
| More data (4,000 kept examples, or writing 8 answers per problem gives more solved problems) | up to 2× | Still ≤14 h. Split across two sessions with a saved checkpoint |
| Session dies at hour 3 | lose the run | Save a checkpoint to Google Drive every ~30 minutes |

(A *checkpoint* is a saved copy of the training so far, like a save point in a video game.)

## 5. Honest context: training is the small cost

| Stage | Tokens moved | Rough GPU-hours | Note |
|---|---|---|---|
| Making training data (4,000 problems × 4 answers × ~2,500 tokens) | ~40M written | **15–40 h** | Writing answers works well in batches, but it is 11× more text than training |
| Testing 5 ways of answering (~1,000 problems × 4 answers) | ~30M written | **10–30 h** | Can be split across Kaggle's 2 T4s |
| **LoRA training** | 3.6M seen | **3–7 h** | One session |
| Gates + pilots (50 examples, 200 problems × 4) | ~2M | 2–5 h | Week 3 |

So "training the model" is about **one afternoon**.
The thesis spends its GPU time on *writing answers* and *grading* them, not on training.

## 6. Calendar time vs GPU time

- [PLAN.md](../PLAN.md) §9 gives weeks 8–9 to "train the LoRA add-on, test it".
- That is right. It is only ~4 h of GPU.
- But first runs crash, settings get changed, and free sessions disconnect.
- Rule of thumb: **calendar time ≈ 3–5× GPU time** for a first try.

## 7. How to replace these guesses with facts (week 3, costs ~20 minutes)

The memory gate already trains 50 examples at 3,500 tokens. Add two lines to it:

1. Record `tokens_seen / seconds` → the real speed.
2. Multiply: `time = 3.6M ÷ measured speed`.

Then this whole note becomes a measured number instead of an estimate.

---

## 8. "We need 40 hours but a session is 12 hours" — how we survive (2026-09-17)

**Everyday example:** you don't read a 40-hour book in one sitting.
You use a bookmark, stop, and continue tomorrow.

- **We never need a 40-hour run without a break.**
- We need 40 hours of *work* in total. That is a different thing.
- The fix: make every job **a job that can stop and continue later**.
  It can be killed at any second, and it continues from where it stopped.

### 8.1 What each stage needs

| Stage | Needs one run with no break? | Why |
|---|---|---|
| Making training data (15–40 h) | **No** | Each problem is separate. Do 200, save, stop, continue. |
| Testing 5 ways of answering (10–30 h) | **No** | Same — separate problems. |
| LoRA training (3–7 h) | **Fits one session** | And it can still continue from a checkpoint if it dies. |

So the only question is good record-keeping, not GPU power.

### 8.2 The "stop and continue" pattern (used by every notebook we write)

```text
start → mount Google Drive
      → read done.jsonl  (which problem ids are finished?)
      → skip those, work on the rest
      → after EVERY ~20 problems: append results to Drive, flush
      → session dies at any moment → next session repeats from the top
```

How to read it:

- "Mount Google Drive" = connect the notebook to your Google Drive folder.
- `done.jsonl` = a results file. *JSONL* means one line of data per result.
- "Append" = add to the end. "Flush" = make sure the result is really saved to disk.

Rules that make it safe:

- **Only add, never change.** A results file where we only add new lines, never change
  old ones (append-only JSONL). One line per (problem id, sample index). Never rewrite a file.
- **A fixed name for each item.** `problem_id + sample_index + policy` decides "already done".
  (`policy` = the way of answering.)
- **Flush and `os.fsync`** after each write. Both make sure the result is really saved to disk.
  Without them, a dead session loses what was still waiting in memory.
- **A fixed seed for each item**, e.g. `seed = base_seed + hash(problem_id)*8 + sample_index`.
  (A *seed* is the number that fixes the random choices.)
  So a re-run of the same item gives the same output, in whichever session it lands.
- **Store raw outputs exactly as written** (CLAUDE.md §4).
  Then grading again never needs the GPU again.

### 8.3 Training checkpoints (for the 3–7 h run)

Save every ~30 minutes, to Drive. Save these six things:

1. LoRA add-on weights (the trained numbers).
2. Optimizer state (the helper that decides each update keeps its own memory).
3. LR-scheduler state (where we are in the plan for changing the learning rate).
4. Step number.
5. The data order (the shuffled list of example numbers).
6. RNG state (the state of the random number maker).

- To continue = load all six.
- Without the data order and RNG state, the continued run can't be repeated exactly.
- Being able to repeat a run is a thesis requirement (fixed seeds).

### 8.4 Where the hours come from

| Source | Session length | Weekly limit | Runs with nobody watching? |
|---|---|---|---|
| Colab free | "at most 12 h", usually less; limits change | none published | **No** — an idle browser tab disconnects (~90 min) |
| Kaggle | ~12 h | ~30 GPU-h/week | **Yes** — "Save & Run All" runs the notebook without the browser |

⚠️ **Unverified, and it matters:**

- A Kaggle session with 2 T4s: does it use the weekly limit at 1 h or 2 h per real-clock hour?
- If 1 h, two workers running side by side give free speed.
- Check in week 1: run a short session, and read the limit meter before and after.

**Plan:**

- Kaggle does most of the work (runs with nobody watching, two GPUs).
- Colab is the second worker, and the place to find and fix bugs by hand.

### 8.5 The 40 hours as a calendar

```text
40 GPU-h of generation
  ÷ 2 workers (Kaggle 2×T4, or Kaggle + Colab)   = 20 h wall-clock
  ÷ ~8 usable hours per day                      ≈ 3 days
  + re-runs and crashes (×1.5)                   ≈ 4–5 days
```

("Generation" = the model writing answers. "Wall-clock" = real time on a clock.)

That fits weeks 6–7 of [PLAN.md](../PLAN.md) §9.

### 8.6 Cheaper before longer — cut the 40 h first

| Lever | Saving | Cost to the thesis |
|---|---|---|
| **Batch generation** (vLLM, 32–64 prompts at once instead of 1) | **2–5×** | None. Biggest single win. |
| Cap answers at the test limit (8k tokens) and stop at the stop-token | ~10–20% | None |
| 4 answers per problem, not 8 | 2× | Only if the room-to-shorten gate passes at 4 (PLAN §7) |
| 3,000 training problems instead of 4,000 | 25% | Slightly less training data |

(*vLLM* is a free tool that makes a model write answers fast, many at once.
The *stop-token* is the token that means "I am done".)

- Do the batching first.
- Buying more sessions to run slow code is the wrong order.
