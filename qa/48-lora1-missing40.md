# Notebook 22: fill only the two missing40 LoRA-alone runs

## What will run?

Qwen3.5-2B LoRA-1 alone on 40, then Qwen3.5-4B LoRA-1 alone on the same 40.
One attempt each. No thinking-token limit. No training.
The 8,192-token overall output cap stays the same as the earlier contest runs.
2B repeat stopping is OFF; 4B is ON. Sampling stays at seed 3407,
temperature 0.6, top-p 0.95, and top-k 20.
The existing 2B combination result stays **41.2% (191/464)**.

## Why won't completed problems run again?

The manifest lists the exact 40 IDs and hashes the historical graded sources.
The worker checks each model's existing 424 LoRA-alone IDs before every phase.
Their missing sets must both equal this 40-ID list.
It also checks saved raw answers on Drive and removes them from pending generation.
Grades resume separately, so an ungraded answer does not need regeneration.

The combination used these questions too. It is a different method.
Only the missing model + LoRA-alone results are added here.

## How to run

1. Commit and push the updated project files to GitHub.
   The notebook clones the latest master and checks script hashes against the manifest.
2. Open [Notebook 22](../notebooks/22_lora1_missing40_2b_4b.ipynb) in Colab.
3. Select A100, then Run all. Allow Drive access.
4. Enter the actual units-per-hour rate and available unit balance.
5. Save the downloaded `lora-missing40-download.zip` and send it back.

The original 2B adapter must be at:
`MyDrive/stop-overthinking/results/mini/lora/lora100/adapter_model.safetensors`.
The 4B adapter comes from `results/4b/raw/lora/lora1/` in the project.
Both weight and config hashes must match before installation.
The successful Notebook 21 package/wheel setup is reused.
It removes unused TorchAO and checks CPU adapter injection for both models.
Real tensor mapping and nonzero trained weights are checked during GPU loading.

## Budget and output

Separate ceiling: **20 estimated units total**, including setup and all resumes.
At 6.77 units/hour, the full ceiling corresponds to about 2.95 hours.
Actual work can finish sooner. The resource-rate estimate is not an exact billing receipt.
This is a new ledger; Notebook 21's 45-unit ceiling and recorded cost remain unchanged.

Results live at `MyDrive/stop-overthinking/results/lora-missing40/2b/` and `4b/`.
Each contains raw answers, grades, settings, environment, and a subset report.
An incomplete report shows its actual coverage. Zero answers is not 0% model accuracy.
The final cell saves a ZIP and releases the GPU. If setup stops early, disconnect manually.

## When do the docs change again?

After both 40-problem sets are checked, combine them with each model's existing 424.
Update the 464-problem scores, shared-ID comparisons, intervals, token means, and charts.
Keep first-attempt and all-attempt calculations labelled separately.
Other missing methods remain outside scope.

## Checks completed locally

Eleven new offline tests and thirteen existing Notebook 21 tests pass.
All notebook code cells compile. Both models' exact missing sets equal the extra40.
No training IDs overlap. Original saved results are unchanged.
These checks do not claim a real A100 execution of Notebook 22.
