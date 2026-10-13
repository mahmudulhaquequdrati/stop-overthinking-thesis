# Notebook 21 implementation check — 14 October 2026

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
