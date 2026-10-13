# 2B LoRA-1 with a 1,024-token thinking limit

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

## How does it avoid the earlier file problems?

The small notebook carries scripts, frozen questions/IDs, and reference grades.
Like earlier notebooks, it loads tests from Hugging Face and saved project data files.
The source revisions and content checks prevent the exam from silently changing.
The complete checked problem set is cached on Drive for resumes.
Its embedded files are checked with hashes, which identify file contents.
It stops before installing packages if Drive, an A100, or the weights are missing.
It uses absolute paths and its own working folder.
It does not depend on an updated GitHub branch or a Drive code mirror.
Saved contest data is downloaded from an already-published, fixed project commit.
The notebook is about 0.3 MB. No separate test ZIP needs uploading.

## Is grading really HumanEval+?

The old local problem file lacked the plus tests.
The notebook loads tests from the official evalplus/humanevalplus dataset at a fixed revision.
Its revision is d32357cf319e50e9c8d8dab5ea876c72b0fd321b.
The 164 HumanEval problems must all have plus tests; easier tests are not a silent fallback.
The complete questions and tests must match the expected file hash before generation starts.
LiveCodeBench retains the saved tests, with at most 20 tests per problem.

## What is the budget?

A 15-unit estimated cap includes setup and worker time.
Generation leaves three estimated units for grading and reports.
Grading leaves 1.5 units for final work.
The notebook uses the rate entered from Colab; it cannot read actual billing balance.
A watchdog stops worker processes when their allotted time ends.
Idle time before the first cell or after a failure is not completely controlled.
If setup fails, disconnect and delete the runtime yourself.
On normal completion, the notebook saves a ZIP and releases the GPU automatically.

## Does an interruption lose everything?

Each raw answer and completed grade is flushed to Drive.
Rerunning the same notebook skips completed work.
An incomplete final line is archived before repair; corruption elsewhere stops the run.
The budget ledger persists across sessions. Unobserved time after a disconnect is charged conservatively.
Do not delete the ledger to bypass the cap.
Changing weights or generation code is rejected when resuming existing answers.
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
  compute-ledger.json
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

## Checked versus not run

Checked locally: notebook cell syntax; embedded file hashes; 464 distinct problem IDs;
training ID separation; all HumanEval+ tests present after loading; source parity; interrupted-file recovery;
duplicate and setting checks; shared-problem calculations; worker budget stopping.
The grader passed 8/8 official HumanEval+ solutions using the frozen tests.
The slim notebook reconstructed all 464 questions/tests exactly using cached source fixtures.
A verified Drive cache skipped all dataset downloads in the local check.

Not run here: actual A100 inference, LoRA tensor loading, Colab package installation,
current wheel/data downloads, Drive permissions, or Colab runtime release.
No new accuracy score is claimed. No Colab units were spent while building it.

## What to do next

Run Notebook 21 on an A100 with your original LoRA-1 weights in Drive.
