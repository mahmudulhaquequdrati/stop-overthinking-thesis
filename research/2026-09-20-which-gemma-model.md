# Which Gemma model is best for us? (2026-09-20)

> The user asked: look at Unsloth's Gemma models on Hugging Face, and choose the best and fastest one that is still good enough for the thesis.
> Source: Hugging Face API (`author=unsloth`, search "gemma", 161 models), and Gemma 4's model card (copied in `unsloth/gemma-4-12b-it` README). All checked on 2026-09-20.

---

## 1. First filter: it must have a thinking ON/OFF switch

Our whole question compares thinking ON with thinking OFF. **Only Gemma 4 has the switch** ("All models in the family are designed as highly capable reasoners, with configurable thinking modes", model card).
Gemma 1, 2, 3 and 3n have no thinking mode, so they are out. That leaves **5 sizes**, which come in many file formats.

## 2. Second filter: it must fit a free T4 (about 15 GB), for answering AND training

| Size | What it is | Code skill: LiveCodeBench v6 | 4-bit size | Fits a T4? |
|---|---|---|---|---|
| **E2B** | small, with a per-layer word table | 44.0% | 8.13 GB (bnb) · GGUF smaller | ✅ |
| **E4B** (ours) | small, with a per-layer word table | 52.0% | 10.95 GB (bnb) · **4.98 GB (GGUF Q4_K_M)** | ✅ (bnb needs the CPU-table trick) |
| **12B** | medium, normal ("dense") | 72.0% | 7.12 GB (GGUF Q4_K_M) | Answering ✅. Training with 3,500-token examples: ❓ probably too tight |
| **26B A4B** | mixture of experts: 25.2B numbers, 3.8B used per token | 77.1% | ~14+ GB | ❌ with room for thinking; training ❌ |
| **31B** | big, dense | 80.0% | ~17+ GB | ❌ |

(Model card numbers are Google's own. The 12B was released 2026-05-29.)

## 3. What the file formats mean

| Format in the name | Runs on | Good for us? |
|---|---|---|
| `unsloth-bnb-4bit` | NVIDIA GPU, with Unsloth or transformers | ✅ for **training** (what we use now). Slow for writing answers (we measured 4.4 tokens/s). |
| `GGUF` | **llama.cpp**, a fast answer-writing program; runs on NVIDIA GPUs too | ✅ likely the **fastest way to write answers on a T4**; the per-layer word table is squeezed too (E4B: 4.98 GB instead of 10.95 GB) |
| `MTP/…gguf` (inside the GGUF folders) | a small "draft" helper for llama.cpp (guesses a few tokens ahead) | Maybe extra speed. Not needed at first. |
| `qat-w4a16` | vLLM | ❓ Its fast 4-bit code usually needs newer GPUs than the T4 (not checked) |
| `NVFP4` | only the newest NVIDIA GPUs | ❌ not on a T4 |
| `MLX` | only Apple Macs | ❌ not on Kaggle or Colab (see `2026-09-20-e2b-mlx-option.md`) |
| no suffix (e.g. `gemma-4-E4B-it`) | full 16-bit | ❌ too big for a T4 |

## 4. The choice

```text
Model:  keep Gemma-4-E4B            (fits, has the switch, 52% on hard code tests; easy+medium is our scope)
Engine: write answers with llama.cpp + GGUF Q4_K_M   ← the real speed fix, to be tested
Train:  keep Unsloth + the bnb-4bit file             (training needs this format)
```

**Why not E2B?** It is faster, but clearly weaker (44% vs 52%). Its bnb file also keeps the big 16-bit word table, so it has the same loading problem. The model is not our speed problem; writing one answer at a time is.

**Why not 12B?** It is much stronger (72%), but it does about 3× more math per token (≈12B vs ≈4.5B numbers used), so it is slower. Training it on a T4 with 3,500-token examples is probably too tight. It is a good option **for future work**.

**Why not 26B A4B or 31B?** They don't fit a free T4 with room for long thinking, and training them is impossible for free.

## 5. How the thesis stays fair with two engines

- **All 5 ways of answering** (OFF, limit, "think briefly", ON, ON + LoRA) are written by the **same engine, with the same GGUF squeeze**.
- The LoRA add-on is trained with Unsloth, then merged into the model and saved as GGUF in the same way (Unsloth can save GGUF files). The base model's GGUF uses the same squeeze.
- Thinking tokens are still counted with Gemma's own tokenizer, so the numbers stay comparable.

## 6. Checked vs. not checked

| Checked | Not checked yet |
|---|---|
| Only Gemma 4 has the thinking switch | llama.cpp's real speed with Gemma-4-E4B on a T4 |
| Sizes, file sizes and code scores above | That llama.cpp runs Gemma 4 with the thinking switch (`enable_thinking`) |
| GGUF E4B Q4_K_M = 4.98 GB | That the merged LoRA → GGUF path works for Gemma 4 |
| 12B has no per-layer word table (no CPU trick needed) | Whether 12B training fits a T4 |
