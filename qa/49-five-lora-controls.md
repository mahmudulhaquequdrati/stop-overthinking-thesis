# Five new LoRA controls in one session

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
For now all five new scores are **not measured**.

Nine new offline checks pass: all five configurations, generator dispatch, thinking counts,
method isolation, frozen464 IDs/training separation, complete references, scheduling, failure reports,
and notebook syntax. RealGPU execution of this notebook has not been performed locally.
