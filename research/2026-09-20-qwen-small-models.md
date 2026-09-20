# Which small model, and where to run it? (2026-09-20)

**The question.** The Mac is too slow for medium problems. Which model should the thesis use,
and on which machine, so that everything finishes inside a free Google Colab account in one week?

**Short answer.** Qwen3.5-2B, on a free Colab T4, with plain `transformers`. Provisional until
the pilot in [notebooks/12_qwen_colab.ipynb](../notebooks/12_qwen_colab.ipynb) reports the gates.

---

## 1. First: how slow was it really, and why?

Measured from our own result files, not guessed.

| Where | Speed | Source |
|---|---|---|
| 30 easy HumanEval problems, 8 at a time, thinking ON | **52 tokens/s** | `results/2026-09-20-pilot-e2b-humanevalplus.jsonl` |
| 1 medium LiveCodeBench problem, one at a time, thinking ON | **21 tokens/s** = 250 s for ONE problem | `results/.live-progress.json` |

So there were **three** causes, not one:

```
1. Medium problems are simply long   5,340 tokens vs ~1,180 on easy   -> 4.5x more work
2. The live run answered ONE at a time   21 tok/s instead of 52       -> 2.5x slower
3. The model was big                 4.55 GB on an 8 GB Mac           -> ~1.5-2x slower
```

Worth saying plainly: **changing the model only fixes cause 3.** Moving to a GPU fixes all three,
because a T4 answers 16 problems at once and has room for a whole model.

---

## 2. Which small Qwen models exist? (checked on the Hugging Face API)

The user pointed at Unsloth's model list sorted by smallest. Unsloth's own Apple-format (MLX)
builds only exist for big models (27B, 35B), so for a small Qwen we use the plain repos:

| Repo | Size | Note |
|---|---|---|
| `unsloth/Qwen3.5-0.8B` | 0.65 GB squeezed | fastest, but very weak at code — real risk of failing the 40% gate |
| **`unsloth/Qwen3.5-2B`** | **4.58 GB in 16-bit** | **chosen** |
| `unsloth/Qwen3.5-4B` | 3.06 GB squeezed | the fallback if 2B is too weak |
| `unsloth/gemma-4-E2B-it-UD-MLX-4bit` | 4.55 GB | the old Mac model, for comparison |

---

## 3. Does Qwen3.5-2B really have a thinking switch? (the load-bearing question)

The whole thesis compares thinking ON with thinking OFF. A model without a real switch is useless
to us. So we did not trust the marketing page — we downloaded the model's own chat template:

```
mlx-community/Qwen3.5-2B-MLX-4bit/raw/main/chat_template.jinja   (153 lines)

line 149:  {%- if enable_thinking is defined and enable_thinking is true %}
line 150:      {{- '<think>\n' }}
line 152:      {{- '<think>\n\n</think>\n\n' }}       <- what it writes when the switch is OFF
lines 94-96:   the model's own thinking is wrapped in <think> ... </think>
```

**Checked:**
- the switch is real, and it is a proper setting (`enable_thinking`), not a polite request in the prompt
- thinking is **OFF by default**
- the markers are `<think>` and `</think>`

**And one thing we nearly missed.** When the switch is ON, the template writes `<think>` at the
**end of the question**. So the model never writes an opening `<think>` into its answer — it only
writes the closing `</think>`. Our old counter hunted for the opening marker in the answer. With
Qwen it would have found nothing and reported **0 thinking tokens on every answer, with no error**.
See DECISIONS #56 and `scripts/test_prompts.py`.

---

## 4. Other facts checked on the model card

| Fact | Value |
|---|---|
| Released | February 2026 |
| Licence | Apache-2.0 |
| Context length | 262,144 tokens |
| Settings for thinking + code | temperature 0.6, top_p 0.95, top_k 20 |
| Training cutoff date | **not published** ❌ |
| LiveCodeBench / HumanEval score for the 2B | **not published** ❌ |

The missing cutoff date is the real cost of this change (DECISIONS #54). The missing code score is
why the pilot exists: nobody can tell us how good it is, so we have to measure it.

---

## 5. Why it fits on a free Colab T4, and Gemma did not

```
free Colab T4:            ~15 GB of GPU memory

Qwen3.5-2B, 16-bit        ~4.5 GB   -> fits completely, ~10 GB left for answers   ✅
Gemma-4-E4B, 4-bit        ~10.2 GB  + a 5.25 GB word table that must be copied
                                    = more than 14.56 GB                          ❌
```

Gemma's fix was to keep that table in slow computer memory instead. That worked, and it is exactly
why it wrote at **4.4 tokens per second** (DECISIONS #43, #46). With Qwen the trick is not needed,
so the slowness it caused is gone rather than worked around.

---

## 6. Why NOT vLLM, even though it is the fastest

vLLM would answer faster than `transformers`. We are not using it:

- vLLM issue **#20259**: Triton float16 compile error when serving a model **with a LoRA adapter on a T4**
- a reported Qwen3.5 LoRA key-layout mismatch, where the adapter loads but **does nothing**

Our fifth way of answering *is* a LoRA. An adapter that silently does nothing would look like
"training didn't help" — a completely wrong conclusion, with no error message to warn us. A 2B
model on a T4 is fast enough without vLLM. (DECISIONS #57.)

---

## 7. What is decided, and what the pilot must still decide

| ✅ Decided on checked facts | ⬜ The pilot decides |
|---|---|
| Move everything to Colab (#52) | Is Qwen3.5-2B fast enough? |
| Use Qwen3.5-2B (#53, provisional) | Does it solve ≥40% at least once? |
| Give up the cutoff-date proof (#54) | Is there ≥25% room to shorten? |
| Use Qwen's own sampling settings (#55) | Does the full run fit in free Colab? |
| Do not use vLLM (#57) | |
| Cut the test set to 234 problems (#58) | |

**Sources:** Hugging Face API and model cards for `Qwen/Qwen3.5-2B`, `unsloth/Qwen3.5-2B`,
`mlx-community/Qwen3.5-2B-MLX-4bit` (all read 2026-09-20) · the model's own `chat_template.jinja` ·
vLLM issue #20259 and the vLLM LoRA docs · our own result files in `results/`.
