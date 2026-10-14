# First real speed on the free Colab T4 (notebook 13, step 7) — 2026-09-22

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

[Every method, benchmark, difficulty, token count and interval](CURRENT-RESULTS.md) · [Full easy thesis](../easy-thesis/FULL-THESIS.md) · [Full formal Markdown thesis](../thesis/THESIS.md).

<!-- CURRENT-STUDY:END -->

**GPU:** free Colab T4 · **Model:** unsloth/Qwen3.5-2B · **Run:** 100 MBPP+ train problems × 4 tries,
thinking ON, 4,096-token limit (before the cut to 50 problems, DECISIONS #62).

## What Colab printed

```text
The fast path is not available because one of the required library is not installed.
Falling back to torch implementation. (flash-linear-attention, causal-conv1d)
loaded unsloth/Qwen3.5-2B as torch.float32 | GPU memory used: 3.76 GB
mbpp · thinking_on · 4 tries: 400 of 400 answers still to do
  8/400 | 735s | 26 tokens/s
  16/400 | 737s | 30 tokens/s
```

## What it means

| Number | Meaning |
|---|---|
| **26–30 tokens/s** | About **7× slower** than the ~200 tokens/s we need (rough rule, DECISIONS #59) |
| **735 s per batch of 8** | 400 answers = 50 batches ≈ **10 hours**; 200 answers (50 problems) ≈ 5 hours |
| **float32, batch 8** | Step 6 chose float32, so float16 was judged not safe (step 6 output still to check) |
| **"fast path is not available"** | Qwen3.5's special layers run in slow plain-PyTorch code because 2 libraries are missing |

## Two causes, both measured in this output

1. **The slow fallback path.** Qwen3.5 has special "linear attention" layers. Their fast code needs
   `flash-linear-attention` and `causal-conv1d`. Without them, transformers uses slow plain-PyTorch code.
2. **float32 instead of float16.** On a T4, float32 math is several times slower than float16.

## Step 6 output: the float16 check (10 MBPP+ train problems, thinking ON, 1 try)

```text
float16: passed 3/10 | garbage answers 1 | ~26 tokens/s   (batch 10)
float32: passed 4/10 | garbage answers 0 | ~18 tokens/s   (batch 5)
float16 is NOT safe -> everything below uses float32, 8 at a time.
```

- The rule (DECISIONS #59) worked as written: pass counts were within 1, but float16 had **1 garbage
  answer** and float32 had none, so float32 was chosen.
- **float16 is only ~1.4× faster** than float32 here. So the number format is NOT the main reason
  for the slowness; the missing fast-path libraries are.
- ⚠️ **Only 3–4 of 10 easy problems passed.** That is surprisingly low for easy problems and close to
  the 40% gate. Not explained yet. Possible causes to check: answers cut off at 4,096 tokens (they
  count as failures), answers without a code block, or something in the prompt.
- 10 problems is a very small sample: 1 garbage answer may be overflow, or a normal answer that had
  no code block. To check by reading it.

## Not checked yet

- Whether the two libraries install on Colab's Python 3.13 and work on a T4.
- Why only 3–4 of 10 easy problems passed.
- What the 1 "garbage" float16 answer really looks like.
- The memory line says 3.76 GB, which is smaller than expected for float32 (~9 GB). To check.

Harmless warnings in the same output: the Hugging Face token warning (only a download speed limit)
and the `torchao` library warnings (those files are for newer GPUs; we don't use them).
