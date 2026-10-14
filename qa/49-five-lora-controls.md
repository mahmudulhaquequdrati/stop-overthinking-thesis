# Five new LoRA controls in one session

<!-- CURRENT-STUDY:START -->

**Historical record below.** Its earlier scores, model choices and plans describe that stage only.
Use the current results linked here for the completed study.

**Current study — 14 October 2026:** **464 unique test problems**.
Benchmarks: **164 HumanEval+**, **166 LiveCodeBench easy**, **134 LiveCodeBench medium**.
All six planned LoRA combinations are complete, one attempt per problem:

- **0.8B:** LoRA + OFF **14.0% (65/464)**; LoRA + limit 512 **14.4% (67/464)**.
- **2B:** LoRA + OFF **35.6% (165/464)**; LoRA + limit 1,024 **41.2% (191/464)**.
- **4B:** LoRA + OFF **64.7% (300/464)**; LoRA + limit 2,048 **71.6% (332/464)**.

LoRA alone means thinking ON without a thinking-token limit.
Older methods' all-attempt averages and first-attempt comparisons are labelled separately.
LoRA + OFF does not consistently improve on free OFF; the 2B/4B gains over free limits remain uncertain.

[Every method, benchmark, difficulty, token count and interval](../results/CURRENT-RESULTS.md) · [Full easy thesis](../easy-thesis/FULL-THESIS.md) · [Full formal Markdown thesis](../thesis/THESIS.md).

<!-- CURRENT-STUDY:END -->

**Completed:** all five runs now checked. See [results](../results/lora-controls/README.md).
No rerun is needed. The instructions below describe the original run.

Use [Notebook24](../notebooks/24_lora1_off_and_limits.ipynb), following Notebook21.
It replaces the unfinished two-limit Notebook23 plan; do not run both.

The existing adapter stays fixed. Only its thinking setting changes:

- 0.8B: LoRA-1 + thinking OFF; LoRA-1 + limit512.
- 2B: LoRA-1 + thinking OFF.
- 4B: LoRA-1 + limit2048; LoRA-1 + thinking OFF.

Each uses the same464 frozen problems, one attempt each:2,320 new answers.
No training or rerun of the completed2B LoRA + limit1024 is included.
Earlier LoRA-alone scores mean thinking ON without a thinking-token limit.
A positive LoRA-alone score does not guarantee a gain under OFF or a limit.
These five tests check that question directly. No further configurations are needed now.

## Run it

Push the notebook, new scripts, and `results/lora-controls-inputs/` first.
Select A100, then Run all. Allow Drive access.
Enter the current unit balance, hourly rate, and total unit ceiling for all five runs.
Compute units are not GPU hours. At6.77 units/hour,40 units corresponds to about5.9 hours.
Choose your actual ceiling at startup; the notebook never uses more than the entered available balance.
Its estimated budget includes setup and resumes, with a reserve for grading and reports.
The estimate cannot enforce exact Colab billing. Stops preserve completed work.

The original2B weight file must be on Drive at:
`MyDrive/stop-overthinking/results/mini/lora/lora100/adapter_model.safetensors`.
Adapter configs come from the checked project files;0.8B/4B weights also come from the project.
All hashes and CPU adapter-injection checks pass before generation can start.

The same verified464-question loader and Drive cache are reused from Notebook21.
Each configuration runs in its own worker process, releasing model memory when it exits.
Answers save individually and are skipped on resume. Grades resume separately.
Every variant has a separate output folder under `results/lora-controls/` on Drive.
First16 technical checks count toward464. There is no accuracy gate.
The final ZIP is `lora-controls-download.zip`. The last cell releases the GPU.
If an early setup cell fails, disconnect manually.

## Reports and thesis updates

OFF is compared primarily with OFF without LoRA.
Each limited adapter is compared primarily with the same limit without LoRA.
Reports also include LoRA alone and other saved controls, using first attempts on shared IDs.
Historical package versions and batch layouts can affect sampling.
Missing grades are not failures, and a partial run is never labelled a464-problem score.

After the ZIP arrives, check IDs, attempts, hashes, grades, and coverage.
Then add all five measured scores to the full464 tables and recalculate uncertainty and tokens.
Keep first-attempt and all-attempt results labelled separately.
All five scores are now measured: 0.8B OFF 14.0%, limit 512 14.4%;
2B OFF 35.6%; 4B limit 2,048 71.6%, OFF 64.7%. Each covers 464/464.

Nine new offline checks pass: all five configurations, generator dispatch, thinking counts,
method isolation, frozen464 IDs/training separation, complete references, scheduling, failure reports,
and notebook syntax. The user completed the real GPU run in Colab; the saved ZIP was audited locally.
