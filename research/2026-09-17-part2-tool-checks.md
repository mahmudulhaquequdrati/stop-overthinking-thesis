# Research note: checks for Part 2 (loading Gemma, the switch, the test data), 2026-09-17

> **What is this?** Facts we checked ourselves before writing lessons 07–11 and the first notebooks.
> Everything here was checked on 2026-09-17 by reading the real web pages and files.
> Hard word? See [GLOSSARY.md](../GLOSSARY.md).

---

## 1. Gemma-4-E4B model page (`huggingface.co/google/gemma-4-E4B-it`)

| Fact | What we found |
|---|---|
| Gated (must ask for access)? | **No** (`gated: False` on the Hugging Face API). No token needed to download. |
| Cutoff | "Our pre-training dataset … with a cutoff date of January 2025." Only for **pre-training** data. |
| Thinking ON | Special token `<\|think\|>` at the start of the system prompt. In code: `enable_thinking=True`. |
| Thinking format | Thinking comes between `<\|channel>thought` and `<channel\|>`, then the final answer. |
| **Thinking default** | **OFF.** The chat template says `enable_thinking` defaults to false. So we must always set it on purpose. |
| Recommended sampling | `temperature=1.0`, `top_p=0.95`, `top_k=64` (model card "Best Practices" and `generation_config.json`). |
| Software | Card: "use all Gemma 4 models with the latest version of Transformers". |

## 2. Unsloth notebook `Gemma4_(E4B)-Text.ipynb` (GitHub `unslothai/notebooks`)

Its saved outputs show a real run on a **free Tesla T4**:
- "Max memory: 14.563 GB", "Bfloat16 = FALSE" (the T4 has no bf16).
- Loaded `unsloth/gemma-4-E4B-it` with `load_in_4bit=True`: **9.891 GB reserved** after loading. *(Update 2026-09-19: did not hold for us with Unsloth 2026.9.7; see `results/2026-09-19-notebook11-out-of-memory.md`.)*
- Short training demo (60 steps, max_seq_length 1024, LoRA r=8): **10.715 GB peak**, 368 seconds.
  "Trainable parameters = 18,350,080 of 8,014,506,528".
- Install cell pins `transformers==5.5.0`.
- It uses `train_on_responses_only`: the error score is counted **only on the answer part**, not on the question.
  (We adopted this for our own training too: DECISIONS #42.)

Repos checked (Hugging Face API): `unsloth/gemma-4-E4B-it` (not gated, one `model.safetensors`),
`unsloth/gemma-4-E4B-it-unsloth-bnb-4bit` (not gated, 3 files, 10.95 GB, the 4-bit version in DECISIONS #8).
Both have `enable_thinking` in their chat template.

⚠️ **Not checked:** whether `enable_thinking` passes through Unsloth's `apply_chat_template` in our notebook.
The lesson 11 notebook checks this itself with an `assert`.

## 3. Test datasets

| Dataset | Rows | Notes |
|---|---|---|
| `evalplus/humanevalplus` | **164** (split `test`) | Not gated. Columns: `task_id`, `prompt`, `canonical_solution`, `entry_point`, `test` |
| `evalplus/mbppplus` | **378** (split `test`) | Not gated |
| `livecodebench/code_generation_lite` | release_v6 = files `test.jsonl` … `test6.jsonl` | Not gated. Uses a **loading script** (`code_generation_lite.py`); the Hugging Face viewer refuses it ("runs arbitrary Python code"). Files are big: 1,252.6 + 713.4 + 623.4 + 1,204.6 + 557.7 + 134.3 MB |

LiveCodeBench fields (checked): `question_title`, `question_content`, `platform`, `question_id`, `contest_id`,
**`contest_date`**, `starter_code`, **`difficulty`**, `public_test_cases`, `private_test_cases`, `metadata`.

⚠️ Because of the loading script, newer versions of the `datasets` library may not load it with `load_dataset`.
Plan: download the `.jsonl` files directly (`hf_hub_download`). Check in the data notebook.

### 3.1 How many LiveCodeBench problems are fresh for Gemma? (counted)

We read every row of `test5.jsonl` and `test6.jsonl` (342 rows) and counted by month and difficulty.
The earlier files end before these months (by the release order in the loading script).

| Month | Rows |
|---|---|
| 2024-09 → 2024-12 | 3 + 51 + 57 + 49 |
| 2025-01 (cutoff month: "maybe seen") | 7 + 44 = 51 |
| **2025-02** | **51** |
| **2025-03** | **68** |
| **2025-04** | **12** |

**From February 2025 on (fresh): 131 problems = 31 easy + 39 medium + 61 hard.**
So only **70 fresh easy + medium problems**.

**What it means:**
- The fresh part of our test set is **small** (70). Too small to show a 2–3 point accuracy change on its own (needs ~1,250+).
- This supports the plan: the main comparison uses the full paired test set (~1,000+), and "fresh vs. seen" stays future work.
- Not counted yet: easy + medium in the older LiveCodeBench files (needs the big files; do it in the data notebook).

## 4. Sources

- https://huggingface.co/google/gemma-4-E4B-it (README, `chat_template.jinja`, `generation_config.json`)
- https://huggingface.co/api/models/unsloth/gemma-4-E4B-it-unsloth-bnb-4bit
- https://github.com/unslothai/notebooks/blob/main/nb/Gemma4_(E4B)-Text.ipynb
- https://huggingface.co/datasets/evalplus/humanevalplus · https://huggingface.co/datasets/evalplus/mbppplus
- https://huggingface.co/datasets/livecodebench/code_generation_lite
