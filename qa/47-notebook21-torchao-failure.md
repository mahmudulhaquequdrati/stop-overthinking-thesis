# Why Notebook 21 produced zero answers

## Completed result and next step — 14 October 2026

**Qwen3.5-2B + LoRA-1 + thinking limit 1,024: 41.2% (191/464).**
All 464 problems were generated and graded, one attempt each.
Limit alone: 38.6% on the same 464 first attempts.
Gap: +2.6 points; 95% interval −1.5 to +6.7. The gain remains inconclusive.
On 424 shared first attempts: combination 43.9%, LoRA-1 alone 38.0%.
Earlier all-attempt LoRA-1 accuracy is 37.4%; keep the weighting labels.
The v2 ledger records 20.51 estimated units under the 45-unit ceiling.

Next planned work: **2B LoRA-1 alone on the missing 40, then 4B LoRA-1 alone on the same 40**.
No training or rerun of their existing 424 answers. Other missing methods are outside scope.
Results are not available yet; new combined scores will be added after grading.
[Completed evidence](../results/lora-limit-2b/README.md) · [Exact missing IDs and plan](../results/lora-missing40/PLAN.md).


## The step in two sentences

The base model loaded, but PEFT could not attach LoRA because of an old optional TorchAO package.
We fixed the setup and failure reporting; the run still has no accuracy result.

## What exactly failed?

PEFT's adapter-injection path found TorchAO 0.10.0.
That PEFT version requires TorchAO >=0.16.0 when the optional backend is present.
The exception occurred before any answers were generated.
The HF authentication warning was not the cause.

## Why remove TorchAO instead of upgrade it?

This run loads a 16-bit model; it does not use TorchAO quantization.
The optional backend is unnecessary for this workflow.
Removing it avoids another binary dependency and its compatibility constraints.
This only changes packages in the Colab inference runtime, not trained model weights.

## Why did the notebook reach the ZIP cell?

The generation exception was caught so saved partial work could be graded.
With zero answers, the grading step had nothing to do.
The last cell saved available logs/report files and released the GPU.
That looked like a completed run, but no accuracy existed.
The fixed notebook skips grading when there are no answers and reports FAILED with its cause.

## What check was added?

A tiny CPU model exercises the same PEFT injection path using the adapter configuration.
It checks the weight file's LoRA tensor headers without downloading the full 2B model.
The real saved tensor matching/merging remains checked when the 2B model loads.
A CPU compatibility check is not proof of successful real-model inference.

## Will the saved configuration prevent recovery?

The failed attempt created a run-config.json but saved zero answers and grades.
The fixed worker archives that obsolete configuration before applying the corrected revision.
It does not delete logs or reset a budget ledger.
If any answers or grades exist, changing the revision is rejected to prevent mixed results.

## How much budget is left?

The report estimated 11.31/15 units used. That leaves 3.69 under the current cap.
Generation had only 6.9 minutes available after setup.
Do not assume the full 464-problem run will fit after fixing the package.
The user then reported 120 units available and approved a 45-unit total ceiling to complete the full set.
The revised notebook retains recorded usage and ends when work is done.

## Checked versus pending

Checked: 13 local regression tests, including zero-answer FAILED reporting,
skipping grading after a failure, empty-run configuration recovery, and protection of existing answers.
The generated notebook cells compile and input/script hashes match.
The optional TorchAO rule is confirmed in PEFT's official import utilities.
Pending: the actual CPU compatibility check with Colab's installed PEFT/Torch,
real LoRA tensor loading on A100, and all generation/accuracy results.
No Colab units were spent while making this fix locally.

## Where is it written?

[Failure record](../results/lora-limit-2b/2026-10-14-failure.md),
[Notebook 21](../notebooks/21_2b_lora1_limit1024.ipynb), and Decision 105.

## What to do next

Push the fixed files, reopen the updated Notebook 21 in a fresh A100 runtime, and Run all.
The CPU compatibility check must pass before model loading. The 45-unit ceiling retains earlier recorded usage.
