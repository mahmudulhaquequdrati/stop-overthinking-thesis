# Notebook 14: the real thesis run — results (checked)

> **Status: CHECKED against the raw files** (2026-09-25).
> Raw data: [2026-09-24-thesis-run/](2026-09-24-thesis-run/) (the Drive `thesis/` folder) ·
> Last-cell output: [2026-09-24-thesis-run-step12-output.txt](2026-09-24-thesis-run-step12-output.txt) ·
> Extra checks: [2026-09-24-thesis-run-checks.txt](2026-09-24-thesis-run-checks.txt), made by
> `node scripts/check_thesis_run.js results/2026-09-24-thesis-run`.

A *token* is a small piece of text, about ¾ of a word. *Cut off* means the answer hit the token
limit before it finished, so it counts as wrong.

## 1. The run

- **Where:** Google Colab, **A100** GPU, bfloat16, batch 128. Model: `unsloth/Qwen3.5-2B`.
- **When:** started 2026-09-21 (smoke test), main run 2026-09-24, finished about 20:05.
- **What ran:** every stage. Smoke test · A (5 ways, try 1) · B (LoRA-2 made and tested) ·
  C (try 2 for all 6 ways) · D (cut-off thinking-ON answers re-run with 16,384 tokens).
- **Units left:** about 30 (the ledger's estimate; Colab's own number not given yet).

## 2. The main table (all 234 problems, 2 tries each)

| Way | Accuracy | Thinking tokens | All tokens | Cut off | Accuracy vs ON (95% error bar) |
|---|---|---|---|---|---|
| ON (what we compare against) | 42.1% | 3,262 | 3,446 | 41% | — |
| OFF | 40.8% | 0 | 860 | 7% | −1.3 [−6.6, +4.3] |
| brief | 6.6% | 5,064 | 5,080 | 92% | −35.5 [−41.2, −29.3] |
| limit (1,024) | **49.8%** | 843 | 2,722 | 26% | **+7.7 [+4.3, +11.3]** |
| LoRA-1 (mini-thesis) | 45.5% | 2,838 | 3,158 | 36% | +3.4 [−0.4, +7.7] |
| LoRA-2 (main, fixed in advance) | 45.1% | 3,252 | 3,392 | 41% | +3.0 [−1.1, +7.3] |

By group (accuracy): HumanEval+ ON 55.2 · OFF 47.3 · limit **60.4** · LoRA-2 56.4.
LCB easy ON 24.2 · OFF 46.8 · limit **56.5** · LoRA-2 38.7. LCB medium: every way 0–9%.

## 3. The hypotheses (for LoRA-2)

| | Test | Result |
|---|---|---|
| H1 | Thinking ≤ 0.75× ON | **NO.** x1.00 [0.94, 1.06] |
| H2 | Accuracy ≥ ON − 3 points | YES. +3.0 [−1.3, +7.3] |
| H3 | Better than OFF | Not proven. +4.3 [−0.6, +9.2] |
| H3 | Better than limit | **NO.** −4.7 [−9.0, −0.2] |
| H3 | Better than brief | Yes (+38.5), but brief failed for its own reason (see 4.3) |

## 4. What the raw files show (checked)

### 4.1 Most cut-offs are loops

A *loop* is when the model repeats the same lines again and again until the limit.

| Way | HumanEval+ cut off | of those, loops | LCB cut off | of those, loops |
|---|---|---|---|---|
| ON | 73 / 328 | 66% | 117 / 140 | 72% |
| limit | 25 / 328 | 72% | 96 / 140 | 78% |
| LoRA-1 | 68 / 328 | 79% | 100 / 140 | 87% |
| LoRA-2 | 82 / 328 | 90% | 110 / 140 | 87% |

The loop test is rough and misses loops with small changes, so the true share is likely higher.

### 4.2 When ON finishes, it is already short

Middle (median) thinking of answers that **finished**, HumanEval+: ON 672 · LoRA-1 711 ·
LoRA-2 695 · limit 800. They are all about the same. So on easy problems the extra length is
**not** long careful thinking. It is loops. Our training copies short correct answers, but it
does not stop loops. The limit stops loops by force, and that is why it wins.

### 4.3 "Think briefly" is not a code bug: the instruction clashes with our prompt

The prompt already says "Answer with one Python code block only". "Think briefly … then give the
answer" adds a second rule. The model argues with itself about the two rules ("Wait, if I output
thinking text, is it one Python code block only?") until the limit. Only 15 of 328 HumanEval+
answers finished. 230 of 328 answers talk about the instruction itself. This is a real result for
**this wording**, not for "asking to be brief" in general.

### 4.4 Stage D: more tokens help ON a little, but not enough

Only try 1, thinking ON, the cut-off answers re-run with 16,384 tokens:

| | ON, normal limit | ON, cut-offs get 16k | limit way (try 1) | OFF (try 1) |
|---|---|---|---|---|
| HumanEval+ | 88/164 = 53.7% | 97/164 = **59.1%** | 99/164 = 60.4% | 79/164 = 48.2% |
| LCB (70) | 7/70 = 10.0% | 12/70 = **17.1%** | 18/70 = 25.7% | 20/70 = 28.6% |

- HumanEval+: 23 of 36 finished, 9 correct. With 16k, ON almost catches the limit way (59.1 vs 60.4).
  So part of the limit's win on HumanEval+ comes from our 4,096 limit. **Say this in the thesis.**
- LCB: only 10 of 60 finished; 48 of the 50 still cut off were loops. More room does not fix loops.

### 4.5 Why LoRA-2 did not learn to be shorter

| Training pool | Problems | ≥ 1 correct | ≥ 2 correct (a real choice) | Kept | Middle thinking of kept |
|---|---|---|---|---|---|
| MBPP+ | 200 | 134 | 111 | 133 | 515 |
| LiveCodeBench (older) | 80 | 24 | 12 | 24 | **4,709** |

- The model solved only **1 of 160** medium training tries. So "learning from medium problems" had nothing to learn from.
- The 24 LiveCodeBench examples are **long** (middle 4,709 tokens). The shortest correct answer was
  still long (target 0.987 = almost no shortening). They taught LoRA-2 to think long on
  LiveCodeBench-style problems: its middle thinking there is 3,974, against LoRA-1's 1,066.
- LoRA-2 trained on 157 examples in total (`lora/lora2/loss.json`).

## 5. What it means (careful)

1. On this small model, **shortest-correct training did not shorten thinking** on the test problems (H1 NO).
   It gave a small accuracy gain that is not proven (+3.0, error bar includes 0).
2. The real waste is **loops**, not long careful thinking. A plain **thinking limit** stops loops and
   gave the best accuracy overall (+7.7 vs ON, proven), with about 21% fewer tokens in total.
3. On LiveCodeBench, thinking **OFF** is as good as or better than every thinking way, at a
   fraction of the tokens.
4. The mini-thesis win (#64) came on easy MBPP+ problems that look like its training data. It did
   **not** carry over to HumanEval+ or LiveCodeBench.

## 6. Honest limits

- 1–2 tries per problem, 234 problems, one model (Qwen3.5-2B), one wording for "brief".
- The loop test is rough (it probably under-counts).
- The token limits (4,096 / 8,192) cut off some honest thinking on HumanEval+ (stage D shows +5.5 points for ON).
- LCB medium is at the floor (0–9%) and can't separate the ways.
