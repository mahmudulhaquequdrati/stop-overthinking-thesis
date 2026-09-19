# Result: Gemma-4-E2B (MLX 4-bit) really runs on this Mac — and it is 8–13× faster (2026-09-20)

> **In one sentence:** the small model runs on the user's own Mac at 34 tokens per second alone,
> and 59 tokens per second when answering 8 questions at once, using under 4 GB of memory.
> The free Kaggle T4 gave 4.4 tokens per second.
>
> Research chain: `EXPERIMENT` → the speed test, done early because of the one-week deadline.

Files: [raw answers](2026-09-20-e2b-mlx-mac-raw.jsonl) · [CSV](2026-09-20-e2b-mlx-mac.csv)

---

## 1. What we ran

| Thing | Value |
|---|---|
| Computer | The user's Mac: Apple M2, 8 GB memory |
| Model | `unsloth/gemma-4-E2B-it-UD-MLX-4bit` (4.55 GB) |
| Software | `mlx-lm` 0.31.3 (free, from Apple's MLX project) |
| Question | The same one as notebook 11 (`is_palindrome`) |
| Settings | The same as notebook 11: temperature 1.0, top_p 0.95, top_k 64, seeds 3407/3408 |

## 2. The numbers

| Setting | Thinking tokens | All tokens | Tokens per second | Memory used |
|---|---|---|---|---|
| ON, try 0 | 620 | 710 | 33.6 | 3.62 GB |
| ON, try 1 | 726 | 843 | 34.5 | 3.64 GB |
| OFF, try 0 | 0 | 520 | 22.6 | 3.64 GB |
| OFF, try 1 | 0 | 244 | 35.0 | 3.64 GB |
| 4 questions at once | – | 1,981 | **46.4** | 3.74 GB |
| 8 questions at once | – | 3,307 | **59.0** | 3.84 GB |

Loading the model took 15 seconds. Downloading it took 8.5 minutes, once.

```text
Kaggle T4 + E4B (2026-09-19):   4.4 tokens/s
Mac M2 + E2B, one question:    ~34 tokens/s   →  ~8× faster
Mac M2 + E2B, 8 questions:      59 tokens/s   → ~13× faster
```

## 3. What else we learned

- **The thinking switch works here too.** ON gave 620 and 726 thinking tokens; OFF gave none.
- **E2B thinks much more than E4B on the same question** (620–726 vs. 307 tokens). So there is a lot of room to shorten. This is good news for our method, but it is only one question.
- **With thinking OFF, the model writes long chatty answers** (520 and 244 tokens, with docstrings and comments). So "OFF" is not automatically short. This must be measured, not assumed.
- **Memory is not a problem:** under 4 GB, in an 8 GB Mac.
- **The Mac has no session limit.** It can run all night. Kaggle and Colab cannot.

## 4. Three problems in the tools, and how we solved them (all checked)

| Problem | Fix |
|---|---|
| Loading failed: "140 parameters not in model" | In this model the last 20 of 35 layers **share** the memory of earlier layers, so their own copies are unused. Load with `strict=False`. |
| `batch_generate` crashed on text prompts | It wants token numbers, not text: use `tokenize=True`. |
| `batch_generate` crashed with "division by zero" | A bug in mlx-lm 0.31.3's speed counter. We patch it in memory, not on disk. |

## 5. Checked vs. not checked

| Checked | Not checked yet |
|---|---|
| Speed, memory and the thinking switch, on this Mac | Speed with 16 or 32 questions at once |
| Batches of 4 and 8 work | Whether LoRA training runs on this Mac (MLX's LoRA is generic, so it probably does) |
| Under 4 GB of memory | Whether E2B is accurate enough on our test sets (Google's number: 44% on LiveCodeBench v6, vs. 52% for E4B) |
| The three tool problems above | How the MLX 4-bit squeeze compares with the GPU 4-bit squeeze |

## 6. What it means for the one-week plan

- The Mac becomes a **free worker that never times out**, next to the paid Colab GPU (DECISIONS #48).
- With ~60 tokens per second, the smallest useful experiment (~1.6M tokens for the test runs) takes about **8 hours** of Mac time, which can run overnight.
- Open choice: **E2B everywhere** (one model, all on the Mac, simplest) or **E4B on the paid GPU** (stronger at code).
  Decide on Day 1 after a short accuracy pilot, because a model that can't solve the problems gives us nothing to shorten.
