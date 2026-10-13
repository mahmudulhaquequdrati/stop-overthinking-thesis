# Notebook 21 implementation check — 14 October 2026

## Full 464 update — 14 October 2026

**2B LoRA-1 alone: 34.4%;4B LoRA-1 alone: 56.8%. Both now cover 464/464.**
The exact missing40 runs passed 1/40 (2B) and 12/40 (4B), with one attempt each.
No existing 424 LoRA-alone IDs were repeated.
The scores above average attempts within problems, then weight problems equally.

For 2B on the same 464 first attempts:
**LoRA + limit1024: 41.2% (191/464); LoRA alone: 34.9% (162/464); OFF: 32.5% (151/464).**
The combination's gain over LoRA alone is 6.2 points, interval +2.4 to +10.1.
Its gain over OFF is 8.6 points, interval +4.5 to +12.9.
LoRA alone's smaller lead over OFF remains inconclusive.
Limit alone is 38.6%; the combination's gain over it remains inconclusive.

Missing40 work is complete. Do not rerun Notebook 22 or the existing 424 answers.
Other incomplete methods remain outside scope.
[Updated results and both weighting rules](../results/lora-missing40/README.md).


The notebook reuses the model, prompt, adapter-name remapping, generation, and grader functions from earlier notebooks.
The worker loads and merges LoRA-1 once, then uses the existing two-stage thinking-limit generator.
It uses seed 3407, one attempt, 1,024 thinking tokens, and overall caps of 4,096 (HumanEval+) and 8,192 (LiveCodeBench).
It does not add repeat stopping to the 2B conditions.

Reference scores are saved first attempts, with 464 limit/OFF/ON IDs and 424 LoRA-1 IDs.
The first 16 answers span function, easy contest, and medium contest tasks, and count toward the full run.
This is a retrospective comparison against historical samples; batches and package versions may differ.

The local data/problems.json lacked HumanEval+ test programs.
The builder reads the cached official HF Arrow dataset at revision d32357cf319e50e9c8d8dab5ea876c72b0fd321b.
The slim notebook loads that fixed dataset revision when it runs, without changing original problem files.
Eight official solutions passed the frozen plus-test grader locally.

The notebook fixes Transformers at 5.15.0 and requests PEFT >=0.20.0,<0.21 to read the saved adapter configuration.
It checks optional causal_conv1d and flash-linear-attention imports before model loading.
It reuses compatible Drive wheels, attempts a matching released wheel, then limits source building to ten minutes.
This follows the earlier wheel repair approach and checks it in fresh Python processes.
A successful import is a prerequisite, not evidence of measured inference speed.

Official Transformers documentation describes the hybrid Qwen3.5 architecture and optional fast kernels:
[Qwen3.5 documentation](https://huggingface.co/docs/transformers/v5.15.0/model_doc/qwen3_5).

Scripts, frozen questions/IDs, and reference grades are embedded with hashes.
Tests are external, matching the earlier notebooks' approach.
Original LiveCodeBench tests come from revision 0fe84c3912ea0c4d4a78037083943e8f0c4dd505, test6.jsonl.
The two saved contest files come from project commit 5ff583e6ed2b950636342d2b3583f7420fb9ed4b.
Their downloaded bytes are checked before combining. The combined file must match the expected SHA-256.
A checked combined file is cached on Drive so resumes do not download data again.
The LoRA weight file is not embedded; it must be the user's original lora100 weights on Drive.
The notebook was initially 36.3 MB; this design was replaced at the user's request.
The notebook is now about 0.3 MB, without test data embedded.
Offline reconstruction using the cached official source and saved project files matched the exact expected hash.
A second preparation reused the checked cache without downloading.

Budget enforcement is based on entered units/hour and elapsed runtime, not actual Colab billing APIs.
The 15-unit cap is an estimate; setup, waiting, and failure idle time can affect billing.
The worker watchdog kills the process group, preserving completed answers and grades.
Normal completion saves a ZIP and releases the runtime. Setup failures require manual disconnection.
Actual Colab/A100 behavior remains untested locally.

## Superseding setup revision: Decision 104

The user supplied the Colab install/compile log and requested the structure of notebooks 18–20.
The final notebook is about 24 KB, with readable cells and project input JSON files.
No code or data is Base64-encoded. GitHub must contain the latest files before running.

The log showed Python 3.13, Torch 2.11.0+cu130, and forced downgrades of installed Transformers/PEFT.
The source build was stopped with only about four minutes remaining. Installing EvalPlus also pulled unrelated API packages.
The saved-test path now avoids importing/installing EvalPlus; eight official solutions still pass without third-party packages.

The official release API confirms a v1.7.0 causal_conv1d ready wheel for cu12/torch2.9/ABI TRUE/cp313/linux_x86_64.
[Convolution library release](https://github.com/Dao-AILab/causal-conv1d/releases/tag/v1.7.0).
PyTorch publishes the matching 2.9.1/0.24.1/2.9.1 stack on its cu128 index.
[Official PyTorch installation commands](https://pytorch.org/get-started/previous-versions/).

The revised setup keeps working current kernels first and otherwise selects this published stack.
Mocked tests confirm both paths. Actual Colab installation and inference still require a real run.
The revised-workflow budget uses a new v2 ledger and entered current balance rather than charging unobserved calendar hours.
The previous attempt ledger is preserved; previous paid setup costs are not erased or included in the revised 15-unit allowance.

## First actual generation failure: Decision 105

The user's log confirms bfloat16 model loading succeeded, then PEFT adapter injection failed
because TorchAO 0.10.0 was installed. PEFT's optional-backend check requires >=0.16.0 when present.
[Official PEFT check](https://raw.githubusercontent.com/huggingface/peft/main/src/peft/import_utils.py).
This unquantized 16-bit inference run does not use that backend, so the setup uninstalls it.
A tiny CPU adapter-injection check now runs before the 2B download and again before generation.

The notebook previously caught the exception and proceeded through empty grading/reporting/ZIP saving.
Now it skips grading with zero answers and reports FAILED with the cause. There is no 0% accuracy claim.
The reported estimated cost was 11.31/15 units; generation had only 6.9 minutes allowed after setup.
The cap is not raised or reset. Corrected full generation may need a separate budget decision.
Thirteen offline tests check the new zero-answer recovery and failure-reporting behavior.
Actual corrected PEFT injection and A100 inference remain to be tested in Colab.

## Budget approved after the failure

The user reports 120 units available and explicitly approves a 45-unit total ceiling to finish all 464 problems.
The revised-workflow ledger retains prior recorded usage; the original failed attempt is not erased.
The 45-unit figure is a ceiling, not a target. No other models, new training, or extra samples are added.
