# RPMR — Colab only

Notebooks 25 and 26 are complete; do not rerun them. Open **27_rpmr_colab_loop_search.ipynb**
in Google Colab using **File → Upload notebook**.
Choose a fresh **GPU runtime → Run all**. Allow Drive and enter the current
compute-unit balance and the live units/hour shown in Colab Resources.
No Git push, repository clone, local setup, or training is needed.

## The active files

- `25_rpmr_colab_smoke.ipynb`: completed calculation/cache smoke; kept unchanged.
- `26_rpmr_colab_online_smoke.ipynb`: completed short detector/overhead check.
- `27_rpmr_colab_loop_search.ipynb`: next single-question longer detection-only search.
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

**Colab smoke passed on 14 October 2026.** See the saved report below.

## Undo and preserved work

Existing thesis workers, notebooks, scores and adapters are unchanged.
Verified baseline: `backups/pre-rpmr-2026-10-14-181425/` (795 saved files).
The baseline recovery helper remains inside that ignored backup folder.
Removed local-only tools and duplicate files were archived before deletion:
`backups/rpmr-colab-cleanup-2026-10-14-183358/`.
Local smoke reports remain historical archive evidence; they are not Colab results.
No commit or push was made. Decision #118 records this cleanup.

## First Colab result — 14 October 2026

[Saved report](results/20261014T125828Z-bf30149f/report.json), copied from the user's pasted Colab output.
The original Drive report was not accessed independently.
A100 80GB; 107.826 seconds; estimated 0.2028 units at the entered 6.77/hour rate.
Actual account charges have not been verified. The user confirmed the GPU runtime is disconnected.
Projection checks, real prompt-query capture, cache editing and zero-strength equivalence passed.
Selected readout error: 1.50e-9; next-token score difference: 0.25.
Peak allocated GPU memory: 4.52 GB. Short baseline decode: 18.90 tokens/second over 16 tokens.
This excludes online loop detection and repeated repair; it cannot establish pilot runtime.
Reference PyTorch kernels were used because optional acceleration packages were absent.
No loop recovery, benchmark accuracy, or novelty has been established.
Next: implement the online loop detector and measure its complete overhead in Colab.

## Next: Notebook 26 — online detection and timing

Two hand-written development questions × three methods: ordinary thinking, detection-only,
and conditional RPMR. One greedy answer each; at most 384 total generated tokens per response.
The detector flags three consecutive identical token blocks of length 8, 16 or 32 inside thinking.
At most two protected memory repairs per response, spaced at least 64 tokens apart.
The protected basis comes from actual prompt queries; edit directions come from suspected-loop drift.
No code is executed, no LoRA trained and no benchmark accuracy measured.

**Budget:** at most three estimated units; retain the 20-unit reserve.
At the recorded 6.77 A100 units/hour this allows about 26.6 minutes.
Planning estimate: 4–10 minutes, about 0.45–1.13 historical-rate units.
Assumes similar setup and short-prefix speed to Notebook 25; not a measured guarantee.
The current live rate and balance are requested again, and setup time is counted.

All six answers, trigger/repair events and timing go to Drive in a unique
`stop-overthinking/rpmr-online-smoke/` run folder. A ZIP is offered for download.
Ordinary and detection-only greedy tokens must match exactly. If no eligible natural
repair occurs, the report says loop recovery remains untested. Do not force a loop to claim success.
Short token caps can miss later loops. This stage measures instrumentation, not final usefulness.

Notebook 26 is prepared and syntax-checked, not executed in Colab.
Next action: upload Notebook 26, choose a fresh GPU runtime and Run all.
Afterward, review its report and saved outputs before enlarging the study. Decision #120.

## Notebook 26 report — 14 October 2026

[Uploaded report](results/20261014T131227Z-2ff3a723/report.json) saved byte-for-byte.
Six responses completed; all six hit the 384-token cap.
Detection-only greedy output matched ordinary output on both prompts, as reported by the worker.
No detected episodes and no online repairs. Instrumentation passed; recovery remains untested.
Wall time 203.295 seconds; estimated 0.3823 units at the entered 6.77/hour rate.
Short decoding measured about 20.4–20.9 tokens/second without triggered repairs.
Detection-only wall ratios were 0.991 and 1.009; this tiny sample establishes no speed gain.
Actual charges and raw-output equivalence were not independently checked.
Only report.json was supplied; answers.jsonl and the downloaded ZIP are missing.
Next: inspect the saved raw answers before selecting a longer natural-loop diagnostic.
The two supplied reports both use initial_balance=50; check live balance before another run.

## Notebook 26 raw-output audit — 14 October 2026

[Uploaded raw answers](results/20261014T131227Z-2ff3a723/answers.jsonl) saved byte-for-byte.
Six unique prompt/method pairs and every summary timing/token/event value match report.json.
All three methods have identical token IDs and text for each question.
The even-sum prompt closes thinking and begins its final answer; the cap cuts off that answer.
The substring prompt writes code inside thinking, then begins reconsidering it and hits the cap
without closing thinking. That reconsideration is not proof of a harmful cycle.
No generated code was executed or graded.

## Next: Notebook 27 — one longer natural-loop search

Only the substring question, detection only, at most 2,048 total new tokens.
Same pinned model revision and greedy decoding; no memory repair, training or easy-question rerun.
Stops at the first exact thinking-repeat event or normal end; otherwise stops at the cap.
Planning estimate: 3–8 minutes, about 0.34–0.90 units at the recorded 6.77/hour A100 rate.
Assumes similar setup and roughly 20 tokens/second; long-prefix performance is unmeasured.
Two-unit estimated ceiling (about 17.7 minutes at that rate); retain the 20-unit reserve.
The current live balance and rate are requested.
Prepared and syntax-checked, not run in Colab. This search is not a recovery/accuracy test.
Upload Notebook 27, Run all, and return its report.json. Inspect that result before expanding.
