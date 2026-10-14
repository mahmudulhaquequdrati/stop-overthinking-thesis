# RPMR — Colab only

**Parked — 14 October 2026, at the user's request.**
Do not rerun Notebooks 25–28 or start a historical-prefix replay.
Keep the code and reports for recovery and research history.
Compatibility passed; useful recovery remains untested.

Next research candidate: [shared supervision for repeated draft code](../../research/2026-10-14-shared-draft-supervision.md).
No new GPU run is proposed before a Colab CPU data check.
The runtime instructions below are historical, not the current next step.

## The active files

- `25_rpmr_colab_smoke.ipynb`: completed calculation/cache smoke; kept unchanged.
- `26_rpmr_colab_online_smoke.ipynb`: completed short detector/overhead check.
- `27_rpmr_colab_loop_search.ipynb`: completed substring search; no exact loop.
- `28_rpmr_colab_known_loop.ipynb`: completed calibration; both live tries finished without loops.
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

## Notebook 27 completed — 14 October 2026

[Uploaded report](results/20261014T133535Z-da04a204/report.json) saved byte-for-byte.
The response finishes naturally at 1,300 tokens (EOS), closes thinking and gives a final answer.
It does not hit the 2,048-token cap. No exact repeat event; no repairs enabled.
The first 384 token IDs match Notebook 26's substring prefix exactly.
Within thinking, two Python code blocks are byte-identical, separated by reconsideration prose.
That is redundancy, not the three adjacent short repeated blocks targeted by our detector.
It does not establish a sustained loop, correctness, or a benefit from RPMR. No code was executed.
Wall time 148.978 seconds; estimated 0.2802 units at the entered 6.77/hour rate.
Generation 64.21 seconds, about 20.25 tokens/second; peak allocated GPU memory 4.48 GB.
Do not rerun this completed question or lower detection thresholds just to obtain triggers.
Next: use saved training-generation outputs to identify candidate loops before another Colab run.
Actual billing remains unverified; all three supplied reports entered a balance of 50.

## Candidate search in saved training outputs — 14 October 2026

Read-only word-cycle screening found 15 candidate attempts in existing 2B training
generations: 5/800 MBPP attempts and 10/320 LCB attempts. These are attempt counts,
not unique problems, and use word blocks rather than the notebook's token detector.
Sources: results/2026-09-24-thesis-run/train-mbpp.jsonl and train-lcb.jsonl.
Directly inspected Mbpp/568 sample0, Mbpp/623 sample0 and lcb/2866 sample0.
Each repeatedly reproduces the same reconsideration text inside thinking and reaches
its thinking cap without a closing marker (4,096 MBPP tokens or 8,192 LCB tokens).
These are stronger development candidates than the completed substring example.
Older sampling, model provenance and runtime differ; current greedy reproduction is not guaranteed.
Candidate traces are not final evaluation data or evidence that RPMR helps.
Next: select one candidate, verify training/evaluation separation and reproduce/calibrate
its token-cycle detection in Colab before comparing protected versus unprotected recovery.
No extra GPU run or notebook was created for this read-only screening.

## Next: Notebook 28 — one known training-loop candidate

Candidate Mbpp/568 and its exact original question are embedded from saved training files.
The task ID is verified absent from the 464 current evaluation IDs.
First tokenize the archived loop in Colab and calibrate detection against it and the completed
Notebook 27 thinking trace. Historical IDs are reconstructed from saved text.
Detector periods expand to 8–128, with at least three adjacent blocks and 64 repeated tokens.
This calibration is development work, not a new detector novelty claim. If it fails, stop.

Then try one greedy response and, only if no loop appears, one sampled response
(temperature 0.6, top-p 0.95, top-k 20, seed 3407). At most 4,096 total tokens per try.
Stop at the first natural exact thinking-repeat event. No artificial prefix, memory repair,
training, generated-code execution or accuracy claim. Historical batch64 Unsloth generation
is not exactly reproduced by the pinned official-model single-response runtime.

Planning estimate: 4–12 A100 minutes, about 0.45–1.35 units at the recorded 6.77/hour rate.
Three-unit estimated ceiling, preserving 20 units; enter the actual live balance and rate.
Saved report, raw answers and events go to a unique Drive run folder and downloadable ZIP.
Notebook 28 is prepared and syntax-checked, not run in Colab. Return its ZIP before
we design paired protected/unprotected recovery. If no live repeat occurs, report that plainly.
Decision #125.

## Notebook 28 completed — 14 October 2026

[Report](results/20261014T164802Z-05b6d7ea/report.json) and
[answers](results/20261014T164802Z-05b6d7ea/answers.jsonl) extracted byte-for-byte from the user's ZIP.
Archived positive calibration passed at reconstructed token 2,855 with period 81 and three blocks.
The completed substring thinking trace was not flagged. This validates these two calibration
examples only; period81 lies outside the earlier 8/16/32-only detector choices.
Live candidate Mbpp/568 finishes naturally: greedy198 tokens, sampled200 tokens, both EOS
and thinking closed. No live repeat, artificial prefix or memory edit. Code was not executed.
Runtime97.708 seconds; estimated0.1837 units. Actual account charges remain unverified.
Old batch64 Unsloth generation and current official-model serial generation differ.
The mismatch could involve sampling, model/tokenizer revisions, batching or kernels; cause unknown.
No RPMR recovery or accuracy result is established. Stop rerunning this candidate as-is.
Recommended next diagnostic: a clearly labelled controlled continuation from the saved loop prefix.
First check whether an unchanged model continues or escapes that prefix naturally.
Only if the baseline persists should protected/unprotected memory repairs be compared.
This would study a replayed historical context, not prove current natural loop incidence.
No new notebook or GPU run is started by this result audit.
