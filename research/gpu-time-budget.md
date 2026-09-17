# Research note — how long does the LoRA training run take? (2026-09-17)

> **Why this note exists:** the user asked "how much time to train our model with
> LoRA?". Nothing has been run yet, so every number here is **arithmetic on
> estimates**, not a measurement. The pilot in week 3 turns them into real numbers.
>
> Decisions drawn from this: [DECISIONS.md](../DECISIONS.md) #28.

---

## 0. The answer in one line

**One LoRA run ≈ 3–7 GPU-hours on one free T4** (best guess **~4 h**, one epoch).
It fits inside a single free session. It is the **cheapest** part of the thesis;
making the training data (~15–40 h) and testing 5 policies (~10–30 h) cost far more.

---

## 1. What "training time" depends on

```text
time  =  (number of examples × tokens per example)  ÷  training speed (tokens/second)
            └──────── how much text ────────┘            └── how fast the GPU eats it ──┘
```

Nothing else matters much. LoRA rank, learning rate and batch size change the
*result*, not the *clock*.

## 2. The three inputs, with their sources

| Input | Value used | Where it comes from | Checked? |
|---|---|---|---|
| Training examples | **~2,000** | ~4,000 training problems ([PLAN.md](../PLAN.md) §10) × coverage ≥40% (gate, PLAN §7), minus overlap-check drops | assumed |
| Tokens per example | **~1,800** (prompt ~300 + kept answer ~1,500) | Average sampled answer ≈2,500 tokens (PLAN §10); we keep the *shortest correct* one, and the headroom gate demands ≤0.75 of the average | assumed |
| Training speed | **~250 tokens/s** (range 150–350) | FLOP arithmetic, §3 | **unverified** |
| Epochs | **1** | Munkhbat et al. 2025 trained shortest-correct SFT for 1 epoch ([data-size note](data-size-and-test-size.md)) | from paper |

Tokens per epoch = 2,000 × 1,800 ≈ **3.6M tokens**.

## 3. Where 250 tokens/second comes from

Training one token costs roughly `8 × (active parameters)` floating-point
operations: 2 for the forward pass, 4 for the backward pass, 2 more because
gradient checkpointing recomputes the forward pass to save memory.

```text
Gemma-4-E4B active params ≈ 4e9
cost per token ≈ 8 × 4e9        = 3.2e10 FLOPs
T4 peak (fp16)                   = 65 TFLOPS  →  realistic 6–12 TFLOPS with
                                   4-bit dequantisation + checkpointing (10–18%)
speed = 1.0e13 / 3.2e10          ≈ 310 tokens/s at 10 TFLOPS
                                 ≈ 190 tokens/s at 6 TFLOPS
```

Sanity check: an A100 is ~5× a T4 on fp16, and QLoRA of an 8B model on an A100 is
commonly ~1,500 tokens/s → ~300 on a T4. The two routes agree, so 150–350 is a
fair band. **Still unverified** — measure it.

## 4. The result

| Speed | Time for 3.6M tokens (1 epoch) |
|---|---|
| 150 tokens/s | 6.7 h |
| **250 tokens/s** | **4.0 h** |
| 350 tokens/s | 2.9 h |

**Plan for ~4 h, budget 7 h.** Free session limits: Colab ≤12 h, Kaggle ~12 h per
session and 30 GPU-h per week ([models-and-gpu note](models-and-gpu.md) §4), so one
run fits in one session with room to spare.

### Things that would make it slower

| Risk | Effect | Fix |
|---|---|---|
| **Padding.** Mixing a 400-token example with a 3,500-token one in the same batch pads the short one to the long one | up to **2× slower** | Pack sequences, or sort examples by length before batching |
| 2 epochs instead of 1 | 2× | Start with 1 epoch; that is what the closest paper did |
| More data (4,000 kept examples, or sampling 8 per problem raises coverage) | up to 2× | Still ≤14 h; split across two sessions with a saved checkpoint |
| Session dies at hour 3 | lose the run | Save a checkpoint to Google Drive every ~30 minutes |

## 5. Honest context: training is the small cost

| Stage | Tokens moved | Rough GPU-hours | Note |
|---|---|---|---|
| Making training data (4,000 problems × 4 answers × ~2,500 tokens) | ~40M generated | **15–40 h** | Generation batches well, but it is 11× more text than training |
| Testing 5 policies (~1,000 problems × 4 answers) | ~30M generated | **10–30 h** | Can be split across Kaggle's 2 T4s |
| **LoRA training** | 3.6M seen | **3–7 h** | One session |
| Gates + pilots (50 examples, 200 problems × 4) | ~2M | 2–5 h | Week 3 |

So "training the model" is about **one afternoon**. The thesis spends its GPU time
on *generating* and *grading*, not on training.

## 6. Calendar time vs GPU time

[PLAN.md](../PLAN.md) §9 gives weeks 8–9 to "train the LoRA add-on, test it".
That is right: ~4 h of GPU, but first runs crash, hyperparameters get changed, and
free sessions disconnect. Rule of thumb: **calendar time ≈ 3–5× GPU time** for a
first attempt.

## 7. How to replace these guesses with facts (week 3, costs ~20 minutes)

The memory gate already trains 50 examples at 3,500 tokens. Add two lines to it:

1. Record `tokens_seen / seconds` → the real speed.
2. Multiply: `time = 3.6M ÷ measured speed`.

Then this whole note becomes a measured number instead of an estimate.

---

## 8. "We need 40 hours but a session is 12 hours" — how we survive (2026-09-17)

**We never need a 40-hour unbroken run.** We need 40 hours of *work*, which is a
different thing. The fix is to make every job **resumable**: it can be killed at any
second and continue from where it stopped.

### 8.1 What each stage needs

| Stage | Unbroken run needed? | Why |
|---|---|---|
| Making training data (15–40 h) | **No** | Each problem is independent. Do 200, save, stop, continue. |
| Testing 5 policies (10–30 h) | **No** | Same — independent problems. |
| LoRA training (3–7 h) | **Fits one session** | And it can still be resumed from a checkpoint if it dies. |

So the only question is bookkeeping, not GPU power.

### 8.2 The resume pattern (used by every notebook we write)

```text
start → mount Google Drive
      → read done.jsonl  (which problem ids are finished?)
      → skip those, work on the rest
      → after EVERY ~20 problems: append results to Drive, flush
      → session dies at any moment → next session repeats from the top
```

Rules that make it safe:
- **Append-only JSONL**, one line per (problem id, sample index). Never rewrite a file.
- **A stable key.** `problem_id + sample_index + policy` decides "already done".
- **Flush and `os.fsync`** after each write, or a dead session loses the buffer.
- **Fixed seed per item**, e.g. `seed = base_seed + hash(problem_id)*8 + sample_index`,
  so a re-run of the same item gives the same output whichever session it lands in.
- **Store raw outputs verbatim** (CLAUDE.md §4), so re-grading never needs the GPU again.

### 8.3 Training checkpoints (for the 3–7 h run)

Save every ~30 minutes, to Drive: LoRA adapter weights · optimizer state · LR-scheduler
state · step number · the data order (shuffled index list) · RNG state.
Resume = load all six. Without the data order and RNG state the resumed run is not
reproducible, and reproducibility is a thesis requirement (fixed seeds).

### 8.4 Where the hours come from

| Source | Session length | Quota | Unattended? |
|---|---|---|---|
| Colab free | "at most 12 h", usually less; dynamic limits | none published | **No** — idle tab disconnects (~90 min) |
| Kaggle | ~12 h | ~30 GPU-h/week | **Yes** — "Save & Run All" commits run without the browser |

⚠️ **Unverified, and it matters:** whether a 2×T4 Kaggle session burns quota at 1 h or
2 h per wall-clock hour. If 1 h, two parallel workers are free speed. Check in week 1
by running a short session and reading the quota meter before and after.

**Plan:** Kaggle is the workhorse (unattended commits, two GPUs). Colab is the
second worker and the place for interactive debugging.

### 8.5 The 40 hours as a calendar

```text
40 GPU-h of generation
  ÷ 2 workers (Kaggle 2×T4, or Kaggle + Colab)   = 20 h wall-clock
  ÷ ~8 usable hours per day                      ≈ 3 days
  + re-runs and crashes (×1.5)                   ≈ 4–5 days
```
That fits weeks 6–7 of [PLAN.md](../PLAN.md) §9.

### 8.6 Cheaper before longer — cut the 40 h first

| Lever | Saving | Cost to the thesis |
|---|---|---|
| **Batch generation** (vLLM, 32–64 prompts at once instead of 1) | **2–5×** | None. Biggest single win. |
| Cap generation at the test limit (8k) and stop on the stop-token | ~10–20% | None |
| 4 samples per problem, not 8 | 2× | Only if the headroom gate passes at 4 (PLAN §7) |
| 3,000 training problems instead of 4,000 | 25% | Slightly less training data |

Do the batching first. Buying more sessions to run slow code is the wrong order.
