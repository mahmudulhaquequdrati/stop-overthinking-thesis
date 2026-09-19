# Result: notebook 11 ran out of GPU memory on a free Colab T4 (2026-09-19)

> **In one sentence:** loading Gemma-4-E4B crashed. For a short moment during loading,
> one big word table needs two copies on the GPU, and the T4 has no room for both.
>
> Research chain: `EXPERIMENT` → the **memory check** (PLAN.md §7), first try.

---

## 1. What happened

We ran [notebook 11](../notebooks/11_first_model_call.ipynb) on a free Colab T4. It crashed twice in cell 5 (load the model).
The second run started clean: `nvidia-smi` showed **0 MiB** used. So running the cell twice was **not** the cause.

The error:

```text
OutOfMemoryError: CUDA out of memory. Tried to allocate 5.25 GiB.
GPU 0 has a total capacity of 14.56 GiB of which 4.10 GiB is free.
... 10.22 GiB is allocated by PyTorch
```

The setup, as printed by the run:

| Thing | Value |
|---|---|
| GPU | Tesla T4, 15,360 MiB (14.563 GB usable) |
| Unsloth | 2026.9.7 |
| transformers | 5.5.0 |
| Torch | 2.11.0+cu128 |
| bf16 on the GPU | **No** |
| Unsloth message | "Using float16 precision for gemma4 won't work! Using float32." |

---

## 2. Why it happened (checked)

**Everyday example:** you want to redraw a big poster in a new colour. You need space for the new poster
before you can throw the old one away. The desk has no room for both.

```text
Step 1  the model loads onto the GPU                               10.22 GiB used ✅
Step 2  the T4 has no bf16 → Unsloth turns on "forced float32" mode
Step 3  it converts every module named "embed_tokens..." to float16, ON the GPU
        → the per-layer word table needs a 2nd copy               + 5.25 GiB
        10.22 + 5.25 = 15.47 GiB  >  14.56 GiB                      → crash ❌
```

**What is the 5.25 GiB piece?** Gemma's *per-layer word table* (`model.language_model.embed_tokens_per_layer`).
It holds a small piece of information for every word, in every layer:

```text
262,144 words × 42 layers × 256 numbers × 2 bytes = 5,637,144,576 bytes = 5.25 GiB
```

That is exactly the number in the error.

How we checked it:
- The numbers (262,144 · 42 · 256) come from the model's `config.json` on Hugging Face.
- The table's name comes from `model.safetensors.index.json`.
- The model's own settings keep word tables in 16-bit on purpose (`llm_int8_skip_modules` lists `embed_tokens`), so they are **not** squeezed to 4-bit.
- The conversion is in Unsloth's source code: `unsloth_zoo/patching_utils.py`, `patch_model_and_tokenizer`.
  In forced float32 mode it runs `module.to(float16)` on every module whose name contains `embed_tokens`.
  That is the line in the error's traceback.

**Why Unsloth's own "9.891 GB after loading" didn't hold:** that number was measured with an older Unsloth.
It is not true for Unsloth 2026.9.7 on a T4. (We don't know which older version they used.)

---

## 3. The fix we are trying (DECISIONS #43)

```text
GPU (T4):        the model's main parts, in 4-bit
CPU memory:      the per-layer word table (5.25 GiB), converted there instead
```

Each word needs only **one row** of that table, so reading it from CPU memory is cheap.
Gemma's small "E" models were designed with this table in mind.

- Notebook setting: `LOAD_MODE = "table_on_cpu"`.
- **Run on Kaggle, not Colab.** The conversion now happens in CPU memory: about 5.25 GiB × 2 at the peak, maybe more.
  Free Colab has about 12.7 GB of CPU memory, which is too tight. Kaggle has about 29 GB (**not checked yet**).
- **Backup:** `LOAD_MODE = "two_gpus"` splits the model over Kaggle's two T4s.
- **If both fail,** the memory check has failed. Then PLAN §7 says: switch to Qwen3.5-4B.

Things we checked in the source code before writing the fix:
- transformers 5.5.0 refuses a CPU part in a 4-bit model unless `llm_int8_enable_fp32_cpu_offload=True`.
- ~~Unsloth passes our own `quantization_config` through, so passing the flag in code is enough.~~
  **Wrong (Kaggle run, 2026-09-20):** we got the same "Some modules are dispatched on the CPU" error.
  For a model that is **already** 4-bit, transformers uses the model's own `config.json` and ignores the
  4-bit settings passed in code (`merge_quantization_configs`, checked in its source code).
  **Fix (DECISIONS #45):** the notebook makes a folder of shortcuts to the downloaded files, with one
  changed `config.json` where the flag is on, and loads from that folder.
- Gemma's code adds the table's rows to numbers that are on the GPU (`project_per_layer_inputs`).
  So the notebook adds two small hooks: word ids go to the CPU table, and its rows come back to the GPU.

---

## 4. Checked vs. assumed

| We checked | Not checked yet |
|---|---|
| The error, twice, from a clean start | Whether `table_on_cpu` loads and answers end to end |
| 5.25 GiB = the per-layer word table (config + file names) | Kaggle's CPU memory (~29 GB) |
| The conversion line in Unsloth's code | The writing speed with the table on the CPU |
| transformers needs the CPU-offload flag | Whether training (week 3) also fits with this setup |

---

## 5. What it means for the thesis

- This is **not** a failure of the memory check yet. The loading tool needs one extra setting.
- The memory check must now report **GPU memory and CPU memory**. It must also name the load mode.
- A good side effect: with the table on the CPU, the GPU has about 5 GB **more** free space.
  That helps the week-3 training check (examples up to 3,500 tokens).
- One new risk: on a T4, Unsloth runs Gemma 4 in a float32/float16 mix instead of bf16.
  This may change speed. It is measured in the same run.
