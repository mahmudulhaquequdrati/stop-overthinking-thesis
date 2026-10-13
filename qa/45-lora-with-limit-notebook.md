# 2B LoRA-1 with a 1,024-token thinking limit

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

The earlier zero-answer TorchAO failure is preserved in the failure notes.

## The step in two sentences

We made a separate Colab notebook for the existing 2B LoRA-1 with a thinking limit.
It asks 464 problems once, saves answers, grades them, and compares saved first attempts.

## What are we testing?

Does the existing trained add-on help when both models use the same limit?
The main comparison is original 2B + limit versus LoRA-1 + limit.
A win over unlimited thinking alone does not answer this question.

## Why start with 2B?

The 1,024 limit is already the best observed full-coverage 2B free control.
The saved small-model runtimes do not show that 0.8B is automatically cheaper.
This experiment uses existing weights and needs no new training.

## Which notebook?

[Notebook 21](../notebooks/21_2b_lora1_limit1024.ipynb).
Select an A100, then Runtime → Run all.
Allow Drive access and enter the displayed compute units per hour.
Use a fresh runtime. No code editing or GitHub push is required.

The original LoRA-1 weight file must already be at:

```text
MyDrive/stop-overthinking/results/mini/lora/lora100/adapter_model.safetensors
```

The notebook includes the correct saved adapter configuration.
Use weights from the original lora100 run. Do not substitute LoRA-2 weights.

## How does it load code and problems now?

Notebook 21 follows the readable GitHub/Drive flow of notebooks 18, 19, and 20.
There is no Base64 bundle. The notebook is about 24 KB.
It clones or updates the project from GitHub, then checks scripts and small input files.
The frozen question/ID and reference-score files live in results/lora-limit-inputs/.
Push the latest project changes before running the updated notebook.

Like earlier notebooks, tests load from Hugging Face and saved project data files.
The source revisions and content checks prevent the exam from silently changing.
The complete checked problem set is cached on Drive for resumes.
No separate test ZIP needs uploading.
It stops before model downloading if Drive, an A100, or the original weights are missing.

## Is grading really HumanEval+?

The old local problem file lacked the plus tests.
The notebook loads tests from the official evalplus/humanevalplus dataset at a fixed revision.
Its revision is d32357cf319e50e9c8d8dab5ea876c72b0fd321b.
The 164 HumanEval problems must all have plus tests; easier tests are not a silent fallback.
The complete questions and tests must match the expected file hash before generation starts.
LiveCodeBench retains the saved tests, with at most 20 tests per problem.

## Why did the previous setup fail?

The pasted log showed successful package downloads and installation.
It then attempted to compile causal-conv1d with only about four minutes available.
The budget watchdog stopped the compilation. That was not a model inference failure.
It also showed forced downgrades of Transformers and PEFT, and unrelated API dependencies from EvalPlus.

The revised setup keeps compatible installed Transformers and PEFT versions.
Our saved-test grader does not need the full EvalPlus package installed.
Notebook 21 tries cached or published convolution-library wheels like notebook 20.
The setup removes unused TorchAO and checks PEFT injection on a tiny CPU model before downloading 2B.
For Python 3.13, a published v1.7.0 wheel exists for Torch 2.9, CUDA 12, and ABI TRUE.
If current Torch 2.11/CUDA 13 has no matching wheel, it uses Torch 2.9.1 + CUDA 12.8,
with matching torchvision and torchaudio packages, then installs the ready wheel.
A new Python worker checks the fast libraries before downloading the model.
It does not attempt a source compilation.

## What is the budget?

The user-approved 45-unit total ceiling applies to the revised workflow.
Recorded usage from the failed LoRA-loading attempt counts toward it; the ledger is not reset.
Older initial setup costs remain separately documented.
Finish when the work is done; the ceiling is not a target to spend.
Enter the current resource-panel unit rate and available balance at startup.
The new compute-ledger-v2.json keeps usage across revised-workflow resumes.
It checks both recorded elapsed usage and the balance change since the revised workflow started.
It does not infer disconnected usage from elapsed calendar hours alone.
The old compute-ledger.json is preserved for reference.

Generation leaves three estimated units for grading and reports.
Grading leaves 1.5 units for final work.
The notebook cannot read the live billing balance automatically.
A watchdog stops worker processes when their allotted time ends.
If an earlier cell fails, disconnect and delete the runtime yourself.
On normal completion, the notebook saves a ZIP and releases the GPU automatically.

## Does an interruption lose everything?

Each raw answer and completed grade is flushed to Drive.
Rerunning the same notebook skips completed work.
An incomplete final line is archived before repair; corruption elsewhere stops the run.
The revised ledger persists across sessions. Enter the fresh balance when resuming; it accounts for unobserved usage.
Do not delete the ledger to bypass the cap.
Changing weights or generation code is rejected when resuming existing answers.
A failed attempt with zero answers/grades can archive its old configuration and adopt the corrected worker.
Different A100 memory sizes can change batch size; that fact is recorded.

## Why one attempt?

It reduces generation cost. Saved reference results use their first attempts too.
The reference score is recalculated; it is not automatically the earlier 38.6% combined score.
That earlier score used all available attempts.
LoRA-1 without the limit covers 424 shared problems; the main limit control covers 464.
Missing reference results are not counted as failures.

## What do the first 16 decide?

They check adapter loading, answer markers, output saving, and task types.
They count toward the 464. They are not an accuracy-based selection gate.
The run continues when technical checks pass and budget remains.

## Where are the outputs?

```text
MyDrive/stop-overthinking/results/lora-limit-2b/
  test-lora1-limit1024-he.jsonl
  test-lora1-limit1024-lcb.jsonl
  test-lora1-limit1024-he-graded.csv
  test-lora1-limit1024-lcb-graded.csv
  run-config.json
  environment-*.json
  compute-ledger-v2.json
  SUMMARY.md
  summary.json
```

A ZIP is also saved at results/lora-limit-2b-download.zip.
Partial reports show their actual coverage. They are not called full-set scores.
The comparison uses shared problem IDs and paired uncertainty intervals.

## What supports or contradicts the idea?

Support: more passing answers with a positive gap interval against the same limit alone.
Similar accuracy with fewer total tokens can also be useful.
Contradiction: no useful gain, lower accuracy, or more cost without improved accuracy.
An interval that crosses zero is inconclusive, not proof that the methods are equal.
Saved historical references have package and batch differences; matching seeds does not remove them.
This is a retrospective extension, not a fresh held-out evaluation.

## Local checks and later completed run

Checked locally: notebook cell syntax; embedded file hashes; 464 distinct problem IDs;
training ID separation; all HumanEval+ tests present after loading; source parity; interrupted-file recovery;
duplicate and setting checks; shared-problem calculations; worker budget stopping.
The grader passed 8/8 official HumanEval+ solutions using the frozen tests.
The external data loader reconstructed all 464 questions/tests exactly using cached source fixtures.
A verified Drive cache skipped all dataset downloads in the local check.
The saved-test grader passed 8/8 official solutions with no third-party packages.
Mocked setup tests cover retained working kernels and Torch 2.11/CUDA 13 fallback to a ready wheel.

The local checks did not execute A100 inference. The user's later ZIP contains the completed GPU run.
Its saved logs confirm LoRA weights loaded and all 464 answers were generated and graded.
The checked accuracy is now **41.2% (191/464)**.
Local documentation and result checks spend no Colab units.

## What to do next

Do not rerun the completed Notebook 21.
Prepare only [the missing40 LoRA-alone runs](../results/lora-missing40/PLAN.md) for 2B and 4B.
