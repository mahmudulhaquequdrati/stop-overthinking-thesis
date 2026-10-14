# Q&A 20: The first model load ran out of memory

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

⬅️ [All Q&A](README.md) · Hard word? See [GLOSSARY.md](../GLOSSARY.md) · Result: [results/2026-09-19-notebook11-out-of-memory.md](../results/2026-09-19-notebook11-out-of-memory.md)

---

## 1. The step in 2 sentences

We ran notebook 11 on a free Colab T4. Loading Gemma crashed with "out of memory", because one big word table needs two copies on the GPU for a moment.
We found the exact cause in the code and changed the notebook: that table now sits in CPU memory, and the notebook runs on Kaggle.

---

## 2. Questions a teacher may ask

**Q: What went wrong?**
The GPU has 14.56 GiB. The loaded model used 10.22 GiB. Then the loader asked for 5.25 GiB more, and it did not fit.

**Q: What is the 5.25 GiB piece?**
Gemma's *per-layer word table*. It stores a small piece of information for every word (262,144) in every layer (42): 262,144 × 42 × 256 numbers × 2 bytes = 5.25 GiB.
That is exactly the number in the error. We took the numbers from the model's `config.json`.

**Q: Why does it need two copies?**
The T4 cannot compute in bf16, the format the table is stored in. So Unsloth converts it to float16. While converting, the old copy and the new copy both exist.
We found this line in Unsloth's source code. It is the same line as in the error message.

**Q: But the model is "4-bit". Why is this table so big?**
Only part of the model is squeezed to 4-bit. The word tables are kept in 16-bit on purpose, because squeezing them hurts quality. The model's own settings list them as "don't squeeze".

**Q: Didn't Unsloth measure 9.9 GB on a T4?**
Yes, with an older version. The current version (2026.9.7) does this conversion, so the old number does not hold anymore. Lesson: a number from someone else's run is a hint, not a fact, until we measure it ourselves.

**Q: How did you fix it?**
We put that one table in normal computer memory (CPU memory). Everything else stays on the GPU. Each word only needs one row of the table, so this costs little time.
Two small "hooks" move the data: the word ids go to the CPU, and the table's rows come back to the GPU.

**Q: Why Kaggle and not Colab?**
Now the conversion happens in CPU memory, and it needs about 10.5 GB or more. Free Colab has about 12.7 GB, which is too tight. Kaggle has about 29 GB (not checked yet). Kaggle is also our main GPU already (DECISIONS #31).

**Q: The first fix also failed on Kaggle. Why?**
We passed the "CPU part allowed" flag in our code. But our model file is **already** 4-bit, and for such a model transformers reads that flag only from the model's own settings file (`config.json`). So our flag was ignored.
Now the notebook makes a copy of the model folder out of shortcuts (no new download) and changes only `config.json`. Lesson: read the code path, don't trust that a setting "gets passed through".

**Q: What else could you have done?**
(1) Use Kaggle's two GPUs and split the model: this is our backup setting. (2) Use float16 directly: Unsloth warns that this doesn't work for Gemma 4. (3) Switch to Qwen3.5-4B: this is the plan's rule only if the memory check really fails. We are not there yet.

---

## 3. Hard questions

**Q: Isn't this a failed memory check? Why not switch to Qwen now?**
The memory check (PLAN §7) asks: "can this model be used on our free GPU?". The model itself fits: after loading it is 10.22 GiB, below the 14 GB rule. Only one loading step needed extra room for a moment.
We switch only if both fixes fail. Switching too early would throw away a lot of planning for a tool problem.

**Q: Does moving the table to the CPU change the model's answers?**
It should not. The table is the same numbers; only the place where it is stored changes. The conversion to float16 happens in every setup on a T4, so it is not new.
We will still check the answers look normal in the same run.

**Q: Does it make the model slower?**
A little, maybe. For every token, one small row (42 × 256 numbers) moves from the CPU to the GPU. Notebook 11 measures the speed, so we will know.

**Q: How do you know the second crash was not just leftover memory from the first run?**
Before the second run we restarted the session. `nvidia-smi` showed 0 MiB used on the GPU. Then the same error came back with the same numbers.

---

## 4. Checked vs. assumed

| We checked | We assume (until the Kaggle run) |
|---|---|
| The error, twice, the second time from a clean GPU (0 MiB) | That `table_on_cpu` loads and answers end to end |
| 5.25 GiB = the per-layer word table (config + file names on Hugging Face) | Kaggle's CPU memory is about 29 GB |
| The conversion line in Unsloth's source code | The speed with the table on the CPU |
| transformers needs `llm_int8_enable_fp32_cpu_offload=True` for a CPU part | That training in week 3 also fits with this setup |

---

## 5. Where it is written

- [results/2026-09-19-notebook11-out-of-memory.md](../results/2026-09-19-notebook11-out-of-memory.md)
- [notebooks/11_first_model_call.ipynb](../notebooks/11_first_model_call.ipynb): sections 3 (`LOAD_MODE`) and 5
- [DECISIONS.md](../DECISIONS.md) rows #43 (the fix), #44 (why we download the model in every Colab session) and #45 (the config.json fix)
- [lessons/07-gpu-memory.md](../lessons/07-gpu-memory.md) §4.6
