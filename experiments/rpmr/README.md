# RPMR — Colab only

Open **25_rpmr_colab_smoke.ipynb** in Google Colab using **File → Upload notebook**.
Choose a fresh **GPU runtime → Run all**. Allow Drive and enter the current
compute-unit balance and the live units/hour shown in Colab Resources.
No Git push, repository clone, local setup, or training is needed.

## The three files

- `25_rpmr_colab_smoke.ipynb`: self-contained GPU calculation and Qwen 2B cache check.
- `proposal.md`: invention candidate, derivation, and closest papers.
- `README.md`: these instructions and resource limits.

## Time and cost before running

About **50 Colab units** remain. Keep **20 units** for later work.
The smoke session has a **five-unit estimated ceiling**, including setup after cell 1 starts.
At the historical A100 rate of 6.77 units/hour this allows about **44 minutes**.
Planning estimate: **10–30 minutes**, about **1.1–3.4 units at that historical rate**.
Actual rate, download time and GPU speed are unknown until Colab runs it.
The earlier eight-problem pilot and full novelty study are not run by this notebook.

## What it checks

GPU projection calculations on 128 × 128 matrices; prompt-query capture; a real
DeltaNet cache edit; zero-strength equivalence; finite continuation; and short decode timing.
One hand-written question, 16 greedy prefix tokens and three single-token continuations.
The edit is deliberately forced, not triggered by a detected loop. This is compatibility
checking, not proof of loop recovery, novelty, code correctness or accuracy improvement.
Timing excludes an online detector and repeated repair. It cannot price the full pilot directly.

## What you receive

A `report.json` on Drive at `MyDrive/stop-overthinking/rpmr-smoke/<unique-run>/`.
The report includes the exact model revision, GPU, package versions, checks and timing.
The notebook also attempts a download and runtime disconnection on success or failure.
A wall-time watchdog uses the entered rate; it does not read live account billing.
If it cannot disconnect, choose **Runtime → Disconnect and delete runtime** yourself.

**Prepared and syntax-checked. Not run in Colab yet.** No new paid session started here.

## Undo and preserved work

Existing thesis workers, notebooks, scores and adapters are unchanged.
Verified baseline: `backups/pre-rpmr-2026-10-14-181425/` (795 saved files).
The baseline recovery helper remains inside that ignored backup folder.
Removed local-only tools and duplicate files were archived before deletion:
`backups/rpmr-colab-cleanup-2026-10-14-183358/`.
Local smoke reports remain historical archive evidence; they are not Colab results.
No commit or push was made. Decision #118 records this cleanup.
