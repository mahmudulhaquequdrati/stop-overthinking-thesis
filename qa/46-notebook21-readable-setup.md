# Notebook 21: readable setup after the Colab timeout

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

## What happened?

Packages installed, but the convolution library started compiling with about four minutes left.
The watchdog stopped it before model generation. The log also showed avoidable package downgrades.

## What changed?

Notebook 21 now follows notebooks 18, 19, and 20: Drive, GitHub, package setup,
fast-library check, problem loading, generation, and grading.
There is no Base64 string. The notebook is about 24 KB.
Small frozen input files are ordinary project JSON files under results/lora-limit-inputs/.

## Why not copy every old package install?

This experiment runs inference and saved test programs; it does not train a model.
Installing the full EvalPlus package pulled unrelated API packages and resolver work.
Its import was moved inside the original grader's command-line entry point.
The saved-test grader can now reuse the same code extractor without that package.
The original grader still imports EvalPlus when its old command is used.

## How is the compile problem handled?

Keep current fast libraries if they work. Otherwise look for a matching saved/released wheel.
If current Torch 2.11/CUDA 13 has no ready wheel, use the officially published
Torch 2.9.1 + CUDA 12.8 stack with matching torchvision/torchaudio.
The released causal-conv1d v1.7.0 wheel supports Torch 2.9, Python 3.13, CUDA 12, and ABI TRUE.
No source build is attempted. A fresh-process import check must pass before inference.

## How is budget tracking different?

The revised workflow has its own 15-unit estimated cap and ledger.
Earlier failed setup costs are separate and remain in the old ledger.
Enter the current unit rate and balance. Resume checks the change in actual reported balance,
as well as its recorded elapsed estimate. It no longer guesses disconnected calendar hours.
No paid run was performed while editing the notebook locally.

## What is checked?

All cells compile; input hashes match; 464 IDs are distinct and separated from training IDs.
Nine local tests pass. Mocked setup checks exercise both existing kernels and the ready-wheel fallback.
Eight official solutions pass the saved HumanEval+ grader with no third-party packages.
A real Colab package install and A100 inference remain untested here.

## What to do next

Push the revised notebook, scripts, and results/lora-limit-inputs/.
Disconnect the failed runtime, reopen the updated Notebook 21, choose A100, and Run all.
