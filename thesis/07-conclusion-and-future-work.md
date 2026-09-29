# 7. Conclusion and Future Work

## 7.1 The answer

We asked whether training a small reasoning model to think shorter is better than the free options. **On Qwen3.5-2B, for
code, it is not.** Training on the model's own shortest correct answers did not shorten its thinking on new problems. The
most accurate way was a free one: **stop thinking at 1,024 tokens**. It reached **49.8%**, against **42.1%** for normal
thinking (+7.7 points, proven), and it also beat the trained model and thinking off.

We then checked **two more sizes** in the same family (0.8B and 4B) on the **same 234 problems**. The free winner
changed with size, but **LoRA-1 never beat the best free way** on any of the three.

The reason is the most important lesson of this thesis:

> **A small reasoning model doesn't mainly waste tokens by thinking too carefully. It wastes them by getting stuck in
> loops.** Training on short, finished answers can't teach it to get unstuck. A thinking limit simply cuts the loop.
> On a *very* small model, even a limit is not enough — switching thinking **OFF** can be best.

## 7.2 Main findings

1. **The thinking limit was the most accurate way on 2B:** +7.7 points over normal thinking, +4.7 over the trained model, +9.0
   over thinking off (all proven), with 21% fewer tokens than normal thinking.
2. **Training did not shorten thinking** on the 2B test problems (x1.00). Its accuracy gain (+3.0) could not be proven.
3. **Thinking off was the cheapest on 2B:** 4× fewer tokens than normal thinking, at about the same overall accuracy, and better on
   the harder LiveCodeBench problems.
4. **Most long answers were loops:** 69.5% of normal thinking's unfinished answers, and 88.5% of the trained model's.
5. **Training only helped on problems like its training data:** 41% less thinking on MBPP+, but almost none on HumanEval+.
6. **More room did not rescue normal thinking:** with 16,384 tokens it gained 5.5 points on HumanEval+ and 7.1 on
   LiveCodeBench, still below the limit.
7. **Size extension (checked):** best free way = **OFF 20.5%** on 0.8B · **limit 1,024 → 49.8%** on 2B · **limit 2,048 → 78.2%** on 4B.
   On 2B, **limit 512 = 45.1%** (fill-in): better than ON, worse than 1024. LoRA-1 lost to that free winner on every size.
   ON cut-off fell as size grew (78% → ~41% → 28%).

## 7.3 Advice for people who use small reasoning models for code

```text
1. Try THINKING OFF and a THINKING LIMIT first.   → free; winner depends on size
2. Pick the limit near your size: ~1k (2B) or ~2k (4B). Tiny models: prefer OFF.
3. Watch for LOOPS: count answers that never finish. → they are the real waste
4. Train to think shorter ONLY if free ways are not enough —
   and only if your real problems look like your training problems.
```

## 7.4 What the hypothesis taught us

Our hypothesis assumed that the waste was **overthinking**: finished but too-long thinking. That assumption came from
studies of larger models. For our small model it was wrong: the waste was **looping**. A rejected hypothesis with a clear,
measured reason is a useful result. It tells the next study what to measure **first** (Section 7.5.2).

## 7.5 Future work

### 7.5.1 Bigger models: will they loop less, think better, and learn from training?

We already ran **0.8B and 4B** (Section 7.5.4). That answers part of the size question. What is still open:

| Still open | Why |
|---|---|
| **9B or larger** in the same family | May loop even less; may finally give “long but finished” thinking that LoRA can shorten |
| **Other families** (not only Qwen3.5) | One family can share quirks |
| **Harder problems / math** | Where careful long thinking may really help |

Earlier evidence that larger models may differ:

| Evidence | Source | What it suggests |
|---|---|---|
| *"Qwen3.5-2B is more prone to entering thinking loops compared to other Qwen3.5 models"* | Official Qwen3.5-2B model card | The **same family's** larger models loop less |
| *"Larger models tend to loop less"* | Pipis et al. (2025), arXiv:2512.12895 | Looping goes down as model size goes up |
| *"small models (≤3B parameters) do not consistently benefit from long chain-of-thought (CoT) reasoning"* | Li et al. (2025), arXiv:2502.12143 | Larger models learn better from reasoning examples |
| Our own data: finished answers were short; the waste was loops | Chapter 5 | If a model loops less, its waste becomes "long but finished" thinking, which **is** what shortest-correct training can shorten |
| **Our 0.8B / 4B runs** | Chapter 5.13 | ON cut-off dropped with size (78% → 28%). Best free way moved from OFF → limit 1k → limit 2k. LoRA-1 still lost. |

**What we expected vs what we saw on 4B:**

```text
Expectation                         What 4B showed (checked)
Fewer cut-offs than 2B              Yes: ON cut-off 28% (vs ~41% on 2B)
Limit may lose if loops are rare    No: limit 2048 still won (78.2%)
Training may finally win            No: LoRA-1 69.9% < every limit and < OFF
```

So “bigger → less looping” helped accuracy, but **not** enough for shortest-correct LoRA to beat a free limit on 4B.

**How to test a still-bigger model without wasting money.** Before full training, run a small check on about 40 problems
(4 tries, thinking ON, a large token limit, stop when text repeats). Measure three numbers with rules written **before** looking:

| Check | What it tells us | Qwen3.5-2B | Go ahead if |
|---|---|---|---|
| Share of answers that loop | Is the waste loops? | 28% of thinking-ON answers (132 of 468) | ≤ 10% |
| Kept length ÷ average correct length | Is there short-but-correct thinking to learn from? | 0.83 (MBPP+), 0.99 (LCB) | ≤ 0.75 |
| Problems with ≥ 2 correct out of 4 | Can it solve the training problems? | 56% (MBPP+), 15% (LCB) | ≥ 50% in every set |

### 7.5.2 Methods that target loops directly

Our results suggest attacking the loop itself:

- **Stop when the text repeats.** Detect a loop while the model is writing and stop it early. The model card itself recommends
  *"further tuning the sampling parameters"* and using streaming *"to enable timely detection and interruption of such anomalous
  generation behaviors."* Our size notebooks already use `--stop-on-repeat` for generation.
- **Change the sampling settings.** The model card says a `presence_penalty` between 0 and 2 can *"reduce endless repetitions"*,
  with some trade-offs. Pipis et al. (2025) found that a higher temperature reduces looping, though answers stay long. We used the
  official coding settings (no penalty), so this is untested here.
- **Train on "unstuck" examples.** Instead of only short finished answers, include answers where a loop was cut and the model then
  answered correctly, like the limit's successful answers. This would teach the model what the limit does by force.
- **Combine the limit with training.** Use the thinking limit on top of a trained model.

### 7.5.3 Other extensions

- **Other "think briefly" wordings** that don't clash with the answer rule.
- **More tries per problem** on 0.8B (we used 1 try to save hours).
- **Full fine-tuning** instead of LoRA, given SEER's reported gap between them.
- **Hard problems and math**, where longer, careful thinking may really be needed.
- **Limits we skipped on 0.8B** (2,048 / 4,096), if more GPU hours appear.

## 7.5.4 Size × limit extension — results (DECISIONS #72–#77)

**Status: done.** Same 234 problems; notebooks `15a` (0.8B) and `15b` (4B); folders `results/0.8b/` and `results/4b/`.

| Size | Best free way | Score | LoRA-1 | Beats LoRA? |
|---|---|---|---|---|
| 0.8B (1 try) | **Thinking OFF** | 20.5% | 17.9% | yes |
| 2B (2 tries) | **Limit 1,024** | 49.8% | 45.5% | yes |
| 2B limit512 fill-in | Limit 512 | **45.1%** | (same LoRA-1) | limit1024 still wins |
| 4B (2 tries) | **Limit 2,048** | 78.2% | 69.9% | yes |

```text
Same problems ──► three sizes
                      │
         ┌────────────┼────────────┐
         ▼            ▼            ▼
       0.8B          2B           4B
      OFF wins   limit1024    limit2048
       20.5%       49.8%        78.2%
```

**Takeaway for users:** try **OFF** and a **short thinking limit** before any training.  
Pick a larger limit as the model grows (about 1k → 2k in this family). On a tiny model, prefer OFF.

Full tables: `results/SIZE-COMPARISON.md` · `results/ALL-RESULTS.md`.

## 7.6 Closing

We set out to teach a small model to stop overthinking, and found that its real problem was getting stuck. For Qwen3.5-2B,
the simplest free fix — a limit on thinking — beat training. Across **0.8B, 2B, and 4B**, a free control always beat
LoRA-1; only *which* free control won changed with size. Methods that attack loops directly, and tests on still-larger
models that finish thinking more often, are the natural next steps.
