# Research note: models that fit a free GPU (2026-09-13)

> Hard word? See [GLOSSARY.md](../GLOSSARY.md).

> **How this note was made**
> - A web search helper read Hugging Face model pages
>   (`https://huggingface.co/api/models/<id>`). *Hugging Face* is a free website
>   where people share models and datasets.
> - It also read the Unsloth docs and notebooks, the vLLM docs, and the Colab and
>   Kaggle pages.
> - Careful: the date a repo was created ≠ the date the model was published.
> - Parameter counts come from the safetensors totals. *Parameters* ("params") are
>   the numbers a model learned. *Safetensors* are the files that store them.
>   "B" means billion.
>
> **After that, the main session checked the file sizes again on the HF API (we checked this):**
> - `google/gemma-4-E4B-it`: 7,996,156,490 params. Safetensors files: **15.99 GB**.
> - `unsloth/gemma-4-E4B-it-unsloth-bnb-4bit`: **10.95 GB**. In this file, 4.60B params
>   stay in BF16 (normal 16-bit numbers). The other 3.50B params are squeezed to 4-bit.
> - `Qwen/Qwen3.5-4B`: 4,659,865,088 params, **9.32 GB**.
>
> Decisions that came from this note: [DECISIONS.md](../DECISIONS.md) #6–#10.

---

## Bottom line (from the search)

A few words first:
- A *GPU* is a chip that does model arithmetic very fast.
- The *T4* is the free NVIDIA GPU you get on Colab and Kaggle.
- *Fine-tuning* means training an existing model a bit more on our own examples.
- *LoRA* is a cheap way to fine-tune. We train a few small extra pieces, not the whole model.
- *QLoRA* is LoRA on a model squeezed to 4-bit, so it takes less memory.
- *Unsloth* is a free tool that makes fine-tuning faster and uses less memory.
- A *notebook* is a page of code you run step by step in the browser.

What the search found:
1. Best fit: **Qwen/Qwen3.5-4B** with plain LoRA. Unsloth says: don't use 4-bit QLoRA on Qwen3.5.
2. Or **google/gemma-4-E4B-it** with QLoRA.
3. Gemma-4-E4B is the only new reasoning model with an official Unsloth notebook
   that really ran on a free T4 and printed its memory use.
4. Qwen3.5-9B and Gemma 4 12B run on a T4. But fine-tuning them there is a stretch.

*Main session's choice:* Gemma-4-E4B is the main model, because its cutoff is published.
Qwen3.5-4B is the backup. See DECISIONS #8–#9.

---

## 1. Candidate models (1B–14B)

### 1.1 What the columns mean

- **Params:** model size. B = billion.
- **Date:** when it came out, or when the repo or card was made (as marked).
- **Thinking switch:** can we turn thinking ON and OFF?
- **License:** the rules for using the model.
- **Context:** how many tokens the model can read at once. A *token* is a small
  piece of text, about ¾ of a word. K = thousand.
- **Stated cutoff:** the *training cutoff* the makers published. It is the last date
  of text the model learned from.

### 1.2 The table

| Repo id | Params | Date | Thinking switch | License | Context | Stated cutoff |
|---|---|---|---|---|---|---|
| `Qwen/Qwen3.5-4B` | 4.66B (counts the image part too) | 2026-02-27 | Yes, `enable_thinking`. ON by default in the official template | Apache-2.0 | 262K (up to ~1M) | Not published |
| `Qwen/Qwen3.5-9B` | 9.65B (counts the image part too) | 2026-02-27 | Yes, ON by default | Apache-2.0 | 262K | Not published |
| `Qwen/Qwen3.5-2B`, `Qwen/Qwen3.5-0.8B` | 2.27B / 0.87B | 2026-02-28 | Yes, OFF by default | Apache-2.0 | 262K | Not published |
| `google/gemma-4-E4B-it` | 4.5B "effective" (8B with embeddings) | Repo 2026-03-02 | Yes, `enable_thinking=True/False` | Apache-2.0 | 128K | **Jan 2025** |
| `google/gemma-4-E2B-it` | 2.3B effective (5.1B total) | Repo 2026-03-02 | Yes | Apache-2.0 | 128K | Jan 2025 |
| `google/gemma-4-12B-it` | 11.95B | Announced 2026-06-03 | Yes | Apache-2.0 | 256K | Jan 2025 |
| `ibm-granite/granite-4.2-8b` | 8.79B, dense | Card 2026-08-25 | Yes, `enable_thinking` + `low_effort`. ON by default | Apache-2.0 | 128K (→512K) | Not found |
| `ibm-granite/granite-4.2-3b` | 3.66B | 2026-08 | Yes | Apache-2.0 | — | Not found |
| `nvidia/NVIDIA-Nemotron-3-Nano-4B-BF16` | 3.97B, a mix of Mamba2 and attention layers | 2026-03-16 | Yes, ON by default | NVIDIA Open Model License | 262K | Sept 2024 (pretraining) |
| `mistralai/Ministral-3-8B-Reasoning-2512` | 8.92B | 2025-10-31 | Separate reasoning model* | Apache-2.0 | — | — |
| `microsoft/Phi-4-mini-flash-reasoning` | 3.85B | 2025-06-19 | Reasoning only* | MIT | — | — |
| `HuggingFaceTB/SmolLM3-3B` | 3.08B | 2025-07-08 | `/think` and `/no_think`* | Apache-2.0 | — | — |
| `allenai/Olmo-3-7B-Think` | 7.30B | 2025-11-18 | Reasoning only* | Apache-2.0 | — | — |

\* We did not check this switch again against the model card.

Small notes on the table:
- A *template* is the chat format file that wraps our question before the model sees it.
- *Embeddings* are the model's word lookup table. Gemma counts 4.5B without it, 8B with it.
- *Dense* means the whole model is used for every token.
- *Mamba2* and *attention* are two kinds of model layers. A *layer* is one step of
  the model's work. Many layers are stacked.

### 1.3 Not found

- Small Qwen3.6 models. Only 27B and 35B-A3B exist.
- Small Qwen3.8 models. Only 27B, 125B MoE and 2.4T exist.
  (*MoE*, "mixture of experts", is a big model where only some parts run per token.
  T = trillion.)
- New Meta models on HF since April 2025.
- Small DeepSeek 2026 distills (small models trained to copy a bigger one).
- Phi-4-reasoning-vision-15B (Jan 2026) is just above our 14B limit.

### 1.4 Watch out

- **Qwen3.5 reads images too** (it is *multimodal*). Most of its layers use
  *linear attention*, a cheaper kind of attention: 24 Gated DeltaNet layers + 8
  full-attention layers.
- **The thinking default does not agree.** Unsloth docs say thinking is OFF by default
  for 0.8B/2B/4B/9B. The official Qwen templates turn it ON for 4B and 9B.
  Check this in the first notebook.
- The Granite 4.2 model card (its info page) still has placeholder text.
- Nemotron 4B's hardware list does not mention the T4.

Sources: [Qwen3.5-9B](https://huggingface.co/Qwen/Qwen3.5-9B) · [Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B) · [Gemma 4 12B card](https://huggingface.co/google/gemma-4-12B-it) · [Gemma 4 12B blog](https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemma-4-12b/) · [gemma-4-E4B-it](https://huggingface.co/google/gemma-4-E4B-it) · [granite-4.2-8b](https://huggingface.co/ibm-granite/granite-4.2-8b) · [Nemotron-3-Nano-4B](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-4B-BF16) · [Qwen3.8-Flash-Next](https://huggingface.co/Qwen/Qwen3.8-Flash-Next)

---

## 2. Unsloth support

### 2.1 Unsloth repos that exist

- `unsloth/Qwen3.5-4B`
- `unsloth/Qwen3.5-9B`
- `unsloth/gemma-4-E4B-it`
- `unsloth/gemma-4-E4B-it-unsloth-bnb-4bit`
- `unsloth/gemma-4-12b-it` (no bnb-4bit version found)
- `unsloth/NVIDIA-Nemotron-3-Nano-4B`
- `unsloth/Ministral-3-8B-Reasoning-2512-unsloth-bnb-4bit`

**No Granite 4.2.** Unsloth only has Granite 4.0.

### 2.2 General memory table

*VRAM* is the memory on the GPU. This table is from the
[Unsloth requirements](https://unsloth.ai/docs/get-started/fine-tuning-for-beginners/unsloth-requirements) page.

| Model size | QLoRA | 16-bit LoRA |
|---|---|---|
| 3B | 3.5 GB | 8 GB |
| 8B | 6 GB | 22 GB |
| 9B | 6.5 GB | 24 GB |
| 11B | 7.5 GB | 29 GB |
| 14B | 8.5 GB | 33 GB |

Unsloth needs *compute capability* 7.0 or more. (Compute capability is a version
number that says how new an NVIDIA GPU is.) → The T4 is supported.

### 2.3 Qwen3.5 on Unsloth

Source: [fine-tune guide](https://unsloth.ai/docs/models/qwen3.5/fine-tune).
- The guide says: *"It is not recommended to do QLoRA (4-bit) training on the Qwen3.5 models."*
- Memory for 16-bit LoRA: 0.8B 3 GB · 2B 5 GB · **4B 10 GB · 9B 22 GB**.
- On a T4, building ("compiling") the small GPU programs (*kernels*) is slow.
- It needs transformers v5. (*transformers* is Hugging Face's Python library for models.)
- Keep ≥75% of the training data in reasoning style. This keeps the model's reasoning.
- Free T4 notebook `Qwen3_5_(4B)_Vision.ipynb` (16-bit LoRA): **9.645 GB peak** on a
  Tesla T4. *Peak* is the highest memory use during the run.
- There are no text-only Qwen3.5 notebooks.

### 2.4 Gemma 4 on Unsloth

Source: [training guide](https://unsloth.ai/docs/models/gemma-4/train).
- QLoRA memory: E2B 8 GB, E4B 10 GB.
- Templates: `gemma-4-thinking` / `gemma-4`.
- **Known T4 bug:** in the audio part, a mask value of −1e9 is too big for fp16
  (16-bit numbers), so it overflows.
- `Gemma4_(E4B)-Text.ipynb` (4-bit, seq len 1024): **9.89 GB after loading,
  10.715 GB peak** on a T4. *Seq len* (sequence length) is how many tokens are in one
  training example.
- The 12B notebooks are made for an A100, a much bigger GPU (16-bit LoRA, 24.85 GB peak).
- There is no official 12B notebook for the T4.

### 2.5 Kaggle with 2×T4

- Notebook: `Kaggle-Qwen3.8_(27B)-Conversational.ipynb`. 4-bit, seq 1024.
- Memory: 23.71 GiB peak reserved. (GiB is a memory unit a little bigger than GB.)
- Careful: this was measured on a bigger card limited to two T4s' memory. It was not run on real T4s.

Sources: [notebook list](https://unsloth.ai/docs/get-started/unsloth-notebooks) · [GitHub notebooks](https://github.com/unslothai/notebooks)

---

## 3. Memory math on a T4 (14.56 GiB usable)

### 3.1 The idea

Think of GPU memory as a desk.
- The model itself takes a fixed part of the desk.
- Each new token the model writes needs a little more space.
- Training needs much more space than just writing answers.

```
T4 memory (14.56 GiB)
┌───────────────────────────────────────────────┐
│ model weights │ memory per token (grows) │ free │
└───────────────────────────────────────────────┘
```

**What we computed vs what we guessed:**
- The KV-cache and state numbers were computed from each model's `config.json` file, at fp16.
- Everything else in this section is an estimate.

The *KV cache* is the model's notes about earlier tokens, so it does not reread them.
It grows with every token. KiB and MiB are smaller memory units than GiB.

### 3.2 Memory per generated token (KV cache)

- **Qwen3.5-4B/9B:** only 8 layers keep a cache → ~32 KiB/token → **~256 MiB at 8k**.
  The linear-attention state stays fixed at ~25 MiB.
- **Gemma 4 12B:** 40 sliding-window layers (each keeps at most 1,024 tokens; together ~320 MiB)
  + 8 global layers (they look at all tokens) at ~8–16 KiB/token → **~0.4–0.5 GB at 8k**.
- **Granite 4.2 8B:** 160 KiB/token → ~1.25 GB at 8k.
- **A typical dense 14B:** ~1.25 GB at 8k.

### 3.3 Case (a): writing answers in 4-bit, outputs of ~8k tokens

- Everything up to ~14B fits.
- Qwen3.5-9B: ~7–8 GB. Its ~2B embedding/output params usually stay 16-bit.
- Gemma 4 12B: ~8–9 GB. Granite 8B: ~6.5 GB.
- Qwen3.5-4B fits even without squeezing, in fp16 (~9.5 GB).
- **Speed is the real limit (unverified):** ~10–20 tokens/s at 8–9B 4-bit on a T4.
  So one 8k *trace* (one full answer with its thinking) ≈ 7–15 min.

### 3.4 Case (b): training (estimates)

Setup:
- Training examples of 4k–8k tokens (seq 4k–8k).
- Batch 1: one example at a time.
- Unsloth *offloaded gradient checkpointing*: a memory-saving trick. It keeps fewer
  in-between results on the GPU and moves some to normal computer memory.

| Model and method | 4k | 8k |
|---|---|---|
| Qwen3.5-4B, 16-bit LoRA | Likely fits (~11–13 GB) | Tight |
| Gemma 4 E4B, QLoRA | Likely fits (~12–13 GB) | Risky |
| Qwen3.5-9B, 16-bit LoRA (22 GB) | No | No |
| Qwen3.5-9B, QLoRA | Memory fits, but Unsloth says don't | Same |
| Gemma 4 12B / Granite 4.2 8B, QLoRA | Maybe (plausible) | Tight |

"Tight" means it may just barely fit.

### 3.5 Why the "chunked loss" matters

- All 4k–8k numbers above assume Unsloth's *chunked loss*. It computes the training
  score in small pieces.
- Without it, the full *logits* for 8k tokens × a 248k *vocabulary* would need ~8 GB alone.
- *Logits* are the model's scores for every possible next token.
  The *vocabulary* is the list of all tokens the model knows.

---

## 4. Free GPU facts

### 4.1 Colab

*Colab* is Google's free notebook website with a GPU. Source: [FAQ](https://research.google.com/colaboratory/faq.html).
- Free sessions last "at most 12 hours".
- Limits are "dynamic" (they change).
- GPU types "vary over time".
- There is no published weekly limit. Claims of "15–30 h/week" are unverified.
- The T4 shows 14.563 GB usable.

### 4.2 Kaggle

*Kaggle* is another free notebook website with GPUs.
- 30 GPU-hours per week. You get one P100 (16 GB) or two T4s.
  Source: [Ultralytics docs](https://docs.ultralytics.com/integrations/kaggle) + forum posts.
- Sessions last ~12 h. This comes from second-hand sources.
- We could not read Kaggle's own docs (the pages need JavaScript).
- **The P100 is practically unusable now.** Current PyTorch needs compute capability
  ≥7.0. The P100 is only 6.0
  ([docker-python #1546](https://github.com/Kaggle/docker-python/issues/1546)).
  vLLM needs 7.5.
- **So: use 2×T4.**

---

## 5. vLLM on the T4

*vLLM* is a free tool that makes a model write answers fast.

### 5.1 Is the T4 still supported?

- **Yes.** vLLM 0.29.0 (2026-09-09).
- The [install docs](https://docs.vllm.ai/en/latest/getting_started/installation/gpu.html)
  say compute capability ≥7.5, for example the T4.

### 5.2 Settings for the T4

- Use `--dtype half` (16-bit numbers). bf16 is not available.
- No FlashAttention, a fast attention method. It needs 8.0.
- So vLLM uses the Triton/Flex backends instead
  ([attention backends](https://docs.vllm.ai/en/latest/design/attention_backends.html)).

### 5.3 Squeezed-model formats on the T4 chip family ("Turing")

*Quantization* means squeezing the model's numbers so it takes less memory.
The names below are different squeezing formats.
Source: [table](https://docs.vllm.ai/en/latest/features/quantization/index.html).
- **Works:** AWQ, GPTQ, Marlin (not MXFP4), bitsandbytes, GGUF, INT8 W8A8.
- **Does not work:** FP8 W8A8, W4A8. So the official `-FP8` repos won't run.

### 5.4 Open T4 bugs

- GGUF crash since v0.22 ([#45293](https://github.com/vllm-project/vllm/issues/45293)).
- FlashInfer FP8 KV cache gone on Turing since v0.24 ([#47549](https://github.com/vllm-project/vllm/issues/47549)).
- TurboQuant crash ([#43576](https://github.com/vllm-project/vllm/issues/43576)).

### 5.5 Unverified

- Do Qwen3.5's linear-attention kernels work in vLLM on a T4? Not checked.
- Do Nemotron's Mamba kernels work in vLLM on a T4? Not checked.

---

## Recommendation from the search

1. **Qwen3.5-4B:** 16-bit LoRA. Training examples ≤4k tokens (seq ≤4k).
   ≥75% reasoning data. It has an official free T4 notebook.
2. **Gemma 4 E4B-it:** 4-bit QLoRA. It has an official T4 notebook with measured memory.
3. **A stretch, not verified on T4:** Gemma 4 12B or Granite 4.2 8B with QLoRA.
4. **Qwen3.5-9B:** only for writing answers, not for training.
