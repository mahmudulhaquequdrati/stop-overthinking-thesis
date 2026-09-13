# Research note — models that fit a free GPU (2026-09-13)

> **How this was made:** a web search agent checked Hugging Face model pages
> (`https://huggingface.co/api/models/<id>`), Unsloth docs and notebooks, vLLM docs
> and Colab/Kaggle pages. Repo creation dates ≠ publish dates. Parameter counts
> come from safetensors totals.
>
> **Afterwards, the main session re-checked the file sizes on the HF API:**
> `google/gemma-4-E4B-it` 7,996,156,490 params, safetensors **15.99 GB** ·
> `unsloth/gemma-4-E4B-it-unsloth-bnb-4bit` **10.95 GB** (4.60B params kept BF16,
> 3.50B quantized to 4-bit) · `Qwen/Qwen3.5-4B` 4,659,865,088 params, **9.32 GB**.
>
> Decisions drawn from this: [DECISIONS.md](../DECISIONS.md) #6–#10.

---

## Bottom line (from the search)

Best fit: **Qwen/Qwen3.5-4B** (plain LoRA; Unsloth says don't use 4-bit QLoRA on
Qwen3.5), or **google/gemma-4-E4B-it** (QLoRA). Gemma-4-E4B is the only new reasoning
model with an official Unsloth notebook that actually ran on a free T4 and printed its
memory use. Qwen3.5-9B and Gemma 4 12B run on a T4 but are a stretch to fine-tune there.

*Main session's choice:* Gemma-4-E4B as main (published cutoff), Qwen3.5-4B as
fallback. See DECISIONS #8–#9.

---

## 1. Candidate models (1B–14B)

| Repo id | Params | Date | Thinking switch | License | Context | Stated cutoff |
|---|---|---|---|---|---|---|
| `Qwen/Qwen3.5-4B` | 4.66B (includes vision encoder) | 2026-02-27 | Yes, `enable_thinking`; on by default in the official template | Apache-2.0 | 262K (up to ~1M) | Not published |
| `Qwen/Qwen3.5-9B` | 9.65B (includes vision) | 2026-02-27 | Yes, on by default | Apache-2.0 | 262K | Not published |
| `Qwen/Qwen3.5-2B`, `Qwen/Qwen3.5-0.8B` | 2.27B / 0.87B | 2026-02-28 | Yes, off by default | Apache-2.0 | 262K | Not published |
| `google/gemma-4-E4B-it` | 4.5B "effective" (8B with embeddings) | Repo 2026-03-02 | Yes, `enable_thinking=True/False` | Apache-2.0 | 128K | **Jan 2025** |
| `google/gemma-4-E2B-it` | 2.3B effective (5.1B total) | Repo 2026-03-02 | Yes | Apache-2.0 | 128K | Jan 2025 |
| `google/gemma-4-12B-it` | 11.95B | Announced 2026-06-03 | Yes | Apache-2.0 | 256K | Jan 2025 |
| `ibm-granite/granite-4.2-8b` | 8.79B dense | Card 2026-08-25 | Yes, `enable_thinking` + `low_effort`; on by default | Apache-2.0 | 128K (→512K) | Not found |
| `ibm-granite/granite-4.2-3b` | 3.66B | 2026-08 | Yes | Apache-2.0 | — | Not found |
| `nvidia/NVIDIA-Nemotron-3-Nano-4B-BF16` | 3.97B, Mamba2 + attention hybrid | 2026-03-16 | Yes, on by default | NVIDIA Open Model License | 262K | Sept 2024 (pretraining) |
| `mistralai/Ministral-3-8B-Reasoning-2512` | 8.92B | 2025-10-31 | Separate reasoning model* | Apache-2.0 | — | — |
| `microsoft/Phi-4-mini-flash-reasoning` | 3.85B | 2025-06-19 | Reasoning only* | MIT | — | — |
| `HuggingFaceTB/SmolLM3-3B` | 3.08B | 2025-07-08 | `/think` and `/no_think`* | Apache-2.0 | — | — |
| `allenai/Olmo-3-7B-Think` | 7.30B | 2025-11-18 | Reasoning only* | Apache-2.0 | — | — |

\* Switch not re-checked against the model card.

**Not found:** small Qwen3.6 (only 27B, 35B-A3B); small Qwen3.8 (27B, 125B MoE, 2.4T);
new Meta models on HF since April 2025; small DeepSeek 2026 distills.
Phi-4-reasoning-vision-15B (Jan 2026) is just above 14B.

**Watch out:**
- Qwen3.5 is multimodal and mostly uses linear attention (24 Gated DeltaNet + 8 full-attention layers).
- **Thinking default conflict:** Unsloth docs say reasoning is off by default for 0.8B/2B/4B/9B; the official Qwen templates turn it on for 4B and 9B. Check in the first notebook.
- The Granite 4.2 card still has placeholder text.
- Nemotron 4B's hardware list doesn't mention the T4.

Sources: [Qwen3.5-9B](https://huggingface.co/Qwen/Qwen3.5-9B) · [Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B) · [Gemma 4 12B card](https://huggingface.co/google/gemma-4-12B-it) · [Gemma 4 12B blog](https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemma-4-12b/) · [gemma-4-E4B-it](https://huggingface.co/google/gemma-4-E4B-it) · [granite-4.2-8b](https://huggingface.co/ibm-granite/granite-4.2-8b) · [Nemotron-3-Nano-4B](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-4B-BF16) · [Qwen3.8-Flash-Next](https://huggingface.co/Qwen/Qwen3.8-Flash-Next)

---

## 2. Unsloth support

**Repos that exist:** `unsloth/Qwen3.5-4B`, `unsloth/Qwen3.5-9B`, `unsloth/gemma-4-E4B-it`,
`unsloth/gemma-4-E4B-it-unsloth-bnb-4bit`, `unsloth/gemma-4-12b-it` (no bnb-4bit found),
`unsloth/NVIDIA-Nemotron-3-Nano-4B`, `unsloth/Ministral-3-8B-Reasoning-2512-unsloth-bnb-4bit`.
**No Granite 4.2** (only Granite 4.0).

**General VRAM table** ([Unsloth requirements](https://unsloth.ai/docs/get-started/fine-tuning-for-beginners/unsloth-requirements)), QLoRA / 16-bit LoRA:
3B 3.5 / 8 GB · 8B 6 / 22 GB · 9B 6.5 / 24 GB · 11B 7.5 / 29 GB · 14B 8.5 / 33 GB.
Minimum compute capability 7.0 → T4 supported.

**Qwen3.5** ([fine-tune guide](https://unsloth.ai/docs/models/qwen3.5/fine-tune)):
- *"It is not recommended to do QLoRA (4-bit) training on the Qwen3.5 models."*
- 16-bit LoRA: 0.8B 3 GB · 2B 5 GB · **4B 10 GB · 9B 22 GB**.
- Kernel compile slow on T4. Needs transformers v5.
- Keep ≥75% of training data reasoning-style to preserve reasoning.
- Free T4 notebook `Qwen3_5_(4B)_Vision.ipynb` (16-bit LoRA): **9.645 GB peak** on a Tesla T4. No text-only Qwen3.5 notebooks.

**Gemma 4** ([training guide](https://unsloth.ai/docs/models/gemma-4/train)):
- QLoRA: E2B 8 GB, E4B 10 GB. Templates `gemma-4-thinking` / `gemma-4`.
- **Known T4 bug:** audio attention −1e9 mask overflows in fp16.
- `Gemma4_(E4B)-Text.ipynb` (4-bit, seq len 1024): **9.89 GB after loading, 10.715 GB peak** on a T4.
- 12B notebooks target an A100 (16-bit LoRA, 24.85 GB peak). No official 12B T4 notebook.

**Kaggle 2×T4:** `Kaggle-Qwen3.8_(27B)-Conversational.ipynb`, 4-bit, seq 1024, 23.71 GiB
peak reserved. Measured on a bigger card capped to two T4s' memory, not real T4s.

Sources: [notebook list](https://unsloth.ai/docs/get-started/unsloth-notebooks) · [GitHub notebooks](https://github.com/unslothai/notebooks)

---

## 3. Memory math on a T4 (14.56 GiB usable)

KV-cache/state numbers computed from config.json at fp16; the rest are estimates.

**Memory per generated token (KV cache):**
- Qwen3.5-4B/9B: only 8 layers cache → ~32 KiB/token → **~256 MiB at 8k**; linear-attention state fixed ~25 MiB.
- Gemma 4 12B: 40 sliding-window layers capped at 1,024 tokens (~320 MiB) + 8 global layers ~8–16 KiB/token → **~0.4–0.5 GB at 8k**.
- Granite 4.2 8B: 160 KiB/token → ~1.25 GB at 8k.
- Typical dense 14B: ~1.25 GB at 8k.

**(a) 4-bit inference with ~8k outputs:** everything up to ~14B fits.
- Qwen3.5-9B ~7–8 GB (its ~2B embedding/output params usually stay 16-bit).
- Gemma 4 12B ~8–9 GB. Granite 8B ~6.5 GB. Qwen3.5-4B fits even in fp16 (~9.5 GB).
- **Speed is the real limit (unverified):** ~10–20 tokens/s at 8–9B 4-bit on a T4. One 8k trace ≈ 7–15 min.

**(b) Training at seq 4k–8k, batch 1, Unsloth offloaded gradient checkpointing (estimates):**

| Model and method | 4k | 8k |
|---|---|---|
| Qwen3.5-4B, 16-bit LoRA | Likely fits (~11–13 GB) | Tight |
| Gemma 4 E4B, QLoRA | Likely fits (~12–13 GB) | Risky |
| Qwen3.5-9B, 16-bit LoRA (22 GB) | No | No |
| Qwen3.5-9B, QLoRA | Memory fits, Unsloth advises against | Same |
| Gemma 4 12B / Granite 4.2 8B, QLoRA | Plausible | Tight |

All 4k–8k figures assume Unsloth's chunked loss. Full logits for 8k tokens × 248k
vocabulary would need ~8 GB alone.

---

## 4. Free GPU facts

**Colab** ([FAQ](https://research.google.com/colaboratory/faq.html)):
- Free sessions "at most 12 hours"; limits "dynamic"; GPU types "vary over time".
- No published weekly quota ("15–30 h/week" claims unverified).
- T4 shows 14.563 GB usable.

**Kaggle:**
- 30 GPU-hours/week; one P100 (16 GB) or two T4s ([Ultralytics docs](https://docs.ultralytics.com/integrations/kaggle) + forum posts).
- Sessions ~12 h (secondary sources). Kaggle's own docs weren't readable (JavaScript).
- **P100 effectively unusable now:** current PyTorch needs compute ≥7.0, the P100 is 6.0 ([docker-python #1546](https://github.com/Kaggle/docker-python/issues/1546)). vLLM needs 7.5. **Use 2×T4.**

---

## 5. vLLM on the T4

- **Still supported:** vLLM 0.29.0 (2026-09-09); [install docs](https://docs.vllm.ai/en/latest/getting_started/installation/gpu.html) say compute ≥7.5, e.g. T4.
- Use `--dtype half` (no bf16). No FlashAttention (needs 8.0), so the Triton/Flex backends are used ([attention backends](https://docs.vllm.ai/en/latest/design/attention_backends.html)).
- **Quantization on Turing** ([table](https://docs.vllm.ai/en/latest/features/quantization/index.html)):
  - Works: AWQ, GPTQ, Marlin (not MXFP4), bitsandbytes, GGUF, INT8 W8A8.
  - Doesn't work: FP8 W8A8, W4A8, so official `-FP8` repos won't run.
- **Open T4 bugs:** GGUF crash since v0.22 ([#45293](https://github.com/vllm-project/vllm/issues/45293)); FlashInfer FP8 KV cache gone on Turing since v0.24 ([#47549](https://github.com/vllm-project/vllm/issues/47549)); TurboQuant crash ([#43576](https://github.com/vllm-project/vllm/issues/43576)).
- **Unverified:** whether Qwen3.5's linear-attention kernels and Nemotron's Mamba kernels work in vLLM on a T4.

---

## Recommendation from the search

1. Qwen3.5-4B: 16-bit LoRA, seq ≤4k, ≥75% reasoning data, official free T4 notebook.
2. Gemma 4 E4B-it: 4-bit QLoRA, official T4 notebook with measured memory.
3. Stretch, not verified on T4: Gemma 4 12B or Granite 4.2 8B with QLoRA.
4. Qwen3.5-9B: inference only.
