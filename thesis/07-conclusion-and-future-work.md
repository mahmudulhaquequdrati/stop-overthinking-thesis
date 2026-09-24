# 7. Conclusion and Future Work

## 7.1 The answer

We asked whether training a small reasoning model to think shorter is better than the free options. **On Qwen3.5-2B, for
code, it is not.** Training on the model's own shortest correct answers did not shorten its thinking on new problems. The
most accurate way was a free one: **stop thinking at 1,024 tokens**. It reached **49.8%**, against **42.1%** for normal
thinking (+7.7 points, proven), and it also beat the trained model and thinking off.

The reason is the most important lesson of this thesis:

> **A small reasoning model doesn't mainly waste tokens by thinking too carefully. It wastes them by getting stuck in
> loops.** Training on short, finished answers can't teach it to get unstuck. A thinking limit simply cuts the loop.

## 7.2 Main findings

1. **The thinking limit was the most accurate way:** +7.7 points over normal thinking, +4.7 over the trained model, +9.0
   over thinking off (all proven), with 21% fewer tokens than normal thinking.
2. **Training did not shorten thinking** on the test problems (x1.00). Its accuracy gain (+3.0) could not be proven.
3. **Thinking off was the cheapest:** 4× fewer tokens than normal thinking, at about the same overall accuracy, and better on
   the harder LiveCodeBench problems.
4. **Most long answers were loops:** 69.5% of normal thinking's unfinished answers, and 88.5% of the trained model's.
5. **Training only helped on problems like its training data:** 41% less thinking on MBPP+, but almost none on HumanEval+.
6. **More room did not rescue normal thinking:** with 16,384 tokens it gained 5.5 points on HumanEval+ and 7.1 on
   LiveCodeBench, still below the limit.

## 7.3 Advice for people who use small reasoning models for code

```text
1. Try a THINKING LIMIT first (for example ~1,000 tokens).   → most accurate here, cheaper
2. Try THINKING OFF.                                          → cheapest, often good enough
3. Watch for LOOPS: count answers that never finish.          → they are the real waste
4. Train to think shorter ONLY if your real problems look like your training problems.
```

## 7.4 What the hypothesis taught us

Our hypothesis assumed that the waste was **overthinking**: finished but too-long thinking. That assumption came from
studies of larger models. For our small model it was wrong: the waste was **looping**. A rejected hypothesis with a clear,
measured reason is a useful result. It tells the next study what to measure **first** (Section 7.5.2).

## 7.5 Future work

### 7.5.1 Bigger models: will they loop less, think better, and learn from training?

This is the most promising next step. Three pieces of evidence suggest that a bigger model may behave very differently:

| Evidence | Source | What it suggests |
|---|---|---|
| *"Qwen3.5-2B is more prone to entering thinking loops compared to other Qwen3.5 models"* | Official Qwen3.5-2B model card | The **same family's** larger models loop less |
| *"Larger models tend to loop less"* | Pipis et al. (2025), arXiv:2512.12895 | Looping goes down as model size goes up |
| *"small models (≤3B parameters) do not consistently benefit from long chain-of-thought (CoT) reasoning"* | Li et al. (2025), arXiv:2502.12143 | Larger models learn better from reasoning examples |
| Our own data: finished answers were short; the waste was loops | Chapter 5 | If a model loops less, its waste becomes "long but finished" thinking, which **is** what shortest-correct training can shorten |

**Our expectations for a bigger model** (to be tested, not claimed):

```text
                        Qwen3.5-2B (measured)        Bigger Qwen3.5, e.g. 4B or 9B (expected)
Loops                   many (69.5% of cut-offs)     fewer
Normal thinking         often never finishes         finishes more often, but may run long
Room for training       little (kept ÷ avg 0.83–0.99) more ("long but finished" thinking)
Training effect         none on new problems (x1.00)  may shorten thinking and keep accuracy
Thinking limit          best way                     may lose its advantage if loops are rare
```

**How to test it without wasting money: a "check first" step.** Before training a bigger model, run a small, cheap check on
about 40 problems (4 tries, thinking ON, a large token limit, and stop generation when the text repeats). Measure three
numbers, with rules written down **before** looking:

| Check | What it tells us | Qwen3.5-2B | Go ahead if |
|---|---|---|---|
| Share of answers that loop | Is the waste loops? | 28% of thinking-ON answers (132 of 468) | ≤ 10% |
| Kept length ÷ average correct length | Is there short-but-correct thinking to learn from? | 0.83 (MBPP+), 0.99 (LCB) | ≤ 0.75 |
| Problems with ≥ 2 correct out of 4 | Can it solve the training problems? | 56% (MBPP+), 15% (LCB) | ≥ 50% in every set |

If the bigger model passes, training has a real chance. If it fails, it still tests our main explanation on a second model.

**Practical notes.** The Qwen3.5 family includes 0.8B, 2B, 4B and 9B models and larger ones, with the same thinking switch (for
the 9B model, thinking is on by default). A 9B model should fit on one A100 or H100 GPU for LoRA training, but it writes each token
more slowly, so a full run would cost several times our 38 units. These are estimates, not measurements.

### 7.5.2 Methods that target loops directly

Our results suggest attacking the loop itself:

- **Stop when the text repeats.** Detect a loop while the model is writing and stop it early. The model card itself recommends
  *"further tuning the sampling parameters"* and using streaming *"to enable timely detection and interruption of such anomalous
  generation behaviors."*
- **Change the sampling settings.** The model card says a `presence_penalty` between 0 and 2 can *"reduce endless repetitions"*,
  with some trade-offs. Pipis et al. (2025) found that a higher temperature reduces looping, though answers stay long. We used the
  official coding settings (no penalty), so this is untested here.
- **Train on "unstuck" examples.** Instead of only short finished answers, include answers where a loop was cut and the model then
  answered correctly, like the limit's successful answers. This would teach the model what the limit does by force.
- **Combine the limit with training.** Use the thinking limit on top of a trained model.

### 7.5.3 Other extensions

- **Other "think briefly" wordings** that don't clash with the answer rule.
- **More tries per problem** (4 or 8), for narrower error bars.
- **Full fine-tuning** instead of LoRA, given SEER's reported gap between them.
- **Hard problems and math**, where longer, careful thinking may really be needed.
- **Different limits** (512, 2,048), to find the best limit for each kind of problem.

## 7.6 Closing

We set out to teach a small model to stop overthinking, and found that its real problem was getting stuck. For this model, the
simplest free fix, a limit on thinking, beat training. The trained approach may still work for larger models that loop less;
our "check first" step shows how to find out cheaply before paying for it.
