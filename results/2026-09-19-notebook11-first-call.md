# Result: the first real model call (notebook 11, Kaggle, 2026-09-19)

> **In one sentence:** Gemma loaded and answered, and the thinking switch works.
> But it writes only about **4 tokens per second**, which is far too slow for our plan.
>
> Research chain: `EXPERIMENT` → first test of the setup (a "smoke test"). No accuracy is measured here.

Files:
- The raw answers, word for word: [2026-09-19-notebook11-raw.jsonl](2026-09-19-notebook11-raw.jsonl)
- One row per answer: [2026-09-19-notebook11-first-call.csv](2026-09-19-notebook11-first-call.csv)

---

## 1. The numbers

Question: "write `is_palindrome(s)`, ignoring upper and lower case". Kaggle T4, `LOAD_MODE = "table_on_cpu"` (the default; the user ran the notebook without changing it).

| Way of answering | Try | Thinking tokens | All new tokens | Seconds | Tokens per second |
|---|---|---|---|---|---|
| thinking ON | 0 | **307** | 337 | 105.9 | 3.2 |
| thinking ON | 1 | **0** | 30 | 6.7 | 4.5 |
| thinking OFF | 0 | 0 | 28 | 6.3 | 4.4 |
| thinking OFF | 1 | 0 | 28 | 6.5 | 4.3 |

No answer hit the 4,096-token limit.
**Not in the file:** the memory numbers from sections 5 and 11. They were only printed on screen.

---

## 2. What we learned

### 2.1 The fix for loading works ✅ (checked)
With the per-layer word table in CPU memory, the model loaded and answered 4 times.
All 4 answers are the same, normal one-line solution. So moving the table did not visibly break the model.
(We only **read** the answers. Grading means running the code in a sandbox, and that comes later, in lesson 14.)

### 2.2 The switch works, but ON does not always mean "think" ⚠️ (checked, 2 tries only)
- Thinking ON, try 0: **307 thinking tokens** for a one-line function. That is 91% of all tokens it wrote.
- Thinking ON, try 1: **0 thinking tokens.** The prompt had the `<|think|>` token (the notebook checks it), but the model answered straight away.
- So with thinking ON, Gemma sometimes **decides by itself** to skip thinking.

What it means for the thesis: "thinking ON" has to be reported as an **average**, including the answers with no thinking at all.
We should also count **how often** it skips thinking. Two tries are far too few to say how often that is.

### 2.3 Overthinking, seen with our own eyes ✅
In try 0, the thinking part lists 8 steps, writes the full function **inside the thinking**, and then writes it **again** as the answer.
The final answer is 30 tokens. The thinking before it was 307 tokens: about **10 times** longer than the answer.
This is exactly the problem of lesson 05, on the easiest possible question.

### 2.4 Writing speed: ~4 tokens per second ❌ (checked; the biggest finding)

```text
Measured:  about 4.4 tokens per second (one answer at a time; the first answer was slower, at 3.2)
One thinking answer of 2,000 tokens  →  about 8 minutes
Our plan: ~40 million tokens to make training data  →  about 2,500 GPU-hours at this speed
Our budget said: 15–40 GPU-hours
```

**At this speed, the plan is impossible.** It is about 60–170 times too slow.
We need a much faster way to write answers **before** Part 4.

Possible causes (**not checked yet**, only ideas to test):
1. **One answer at a time.** A GPU is built to do many things at once. Asking 32–64 questions together usually multiplies the total speed a lot. This was already our plan (DECISIONS #31: vLLM).
2. **The number format on the T4.** Unsloth said "float16 won't work for gemma4 → float32". A T4 is much slower in float32 than in float16.
3. **The 4-bit squeeze.** For every token, the 4-bit numbers are unpacked again. That costs time when writing one token at a time.
4. **The table in CPU memory.** For every token, a small row moves from CPU to GPU. This is probably small, but we don't know yet.
5. **The first call is slower** (setup work happens once). That is why try 0 ran at 3.2 and the others at about 4.4.

---

## 3. Checked vs. assumed

| We checked | Not checked yet |
|---|---|
| The model loads and answers with `table_on_cpu` on Kaggle | GPU and CPU memory numbers (printed on screen, not saved) |
| The switch changes the prompt (the notebook's check passed) | How often thinking ON gives 0 thinking tokens (2 tries is too few) |
| Writing speed ≈ 4.4 tokens per second, one answer at a time | Which of the 5 causes makes it slow |
| One clear overthinking example (307 thinking tokens vs. a 30-token answer) | Whether answering many questions at once (vLLM or batching) fixes the speed |

---

## 4. What it means for the plan

- The **GPU-hour table in PLAN §10 is not valid** until we have a faster way to write answers.
- New step before Part 4: **a speed test.** Measure tokens per second when asking many questions at once (batching), and check if vLLM runs Gemma-4 on a T4.
- If no way gets close to the budget, we must cut the work: fewer problems, fewer tries, or shorter limits. Or we switch to the backup model (Qwen3.5-4B) if it is much faster. That decision comes **after** the speed test, based on the numbers.
