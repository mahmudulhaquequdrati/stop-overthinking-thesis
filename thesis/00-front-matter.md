# Stop Overthinking, Keep Passing the Tests

## Shortest-Correct LoRA Fine-Tuning versus Free Thinking Controls in a Small Code Model (Qwen3.5-2B)

**Author:** [your name] · **Supervisor:** [supervisor's name] · **[University], [Department]** · September 2026

---

## Abstract

Some AI models "think" before they answer. They write notes to themselves first, then give the answer.
Thinking often makes answers better, but it costs time and computer power. Small models are said to
**overthink**: they think far longer than they need to.

This thesis asks one question: **on a small model with a thinking switch, is it better to *train* the model
to think shorter, or to use a free option?** The free options are: switch thinking off, stop thinking at a
fixed length, or ask the model in words to "think briefly".

We used the model **Qwen3.5-2B** and **234 code problems** from two well-known test sets (HumanEval+ and
LiveCodeBench). We trained a small add-on (a **LoRA**) on the model's own shortest correct answers. Then we
compared six ways of answering on the same problems, two tries each. Every answer was checked by running the
test sets' own tests.

**Main results.**

- **The free thinking limit was the most accurate way.** Stopping thinking at 1,024 tokens solved **49.8%**
  of answers, against **42.1%** for normal thinking. That is +7.7 percentage points, and the 95% error bar
  [+4.3, +11.3] is fully above zero.
- **Training did not shorten thinking.** The trained model thought exactly as long as the normal model
  (x1.00). Its accuracy was 45.1%, a gain of +3.0 points that we cannot prove.
- **Thinking off was the cheapest.** It used 4× fewer tokens (860 against 3,446 per answer) at about the
  same accuracy as normal thinking.
- **Why:** the long answers were mostly **loops**. The model repeated the same lines until it ran out of room.
  Answers that finished were already short. Training on short correct answers cannot teach a model to get out
  of a loop. A thinking limit simply stops it.

**Conclusion.** For a small reasoning model on code, the waste is not long, careful thinking but **getting
stuck**. A free thinking limit handles this better than training. We suggest testing larger models, which may
loop less, as future work.

**Keywords:** reasoning models, overthinking, thinking budget, LoRA, code generation, efficient inference.

---

## The thesis in one page (for everyone)

### The problem, with an everyday example

Imagine a student who writes five pages for every exam question, even "what is 2 + 2?". That is slow, and
it doesn't make the answers better. New AI models do something similar. Before they answer, they "think" by
writing notes to themselves. On easy code problems, these notes are often much longer than needed.

### What we tried

```text
                           ┌─ 1. Thinking OFF        (switch it off)
                           ├─ 2. Thinking ON         (normal: what we compare against)
Same model, same 234  ─────┼─ 3. "Think briefly"     (ask in words)
code problems              ├─ 4. Thinking limit      (stop thinking at 1,024 tokens)
                           ├─ 5. LoRA-1              (trained on short correct answers, small)
                           └─ 6. LoRA-2              (trained on short correct answers, bigger)
```

Ways 1–4 are **free**: no training is needed. Ways 5–6 need training. We wanted to know: is training worth it?

### What we found

```text
Accuracy on 234 code problems (higher is better)

Thinking limit   ██████████████████████████  49.8%   ← best, and proven
LoRA-1           ███████████████████████     45.5%
LoRA-2 (main)    ███████████████████████     45.1%   (not shorter)
Thinking ON      ██████████████████████      42.1%   (what we compare against)
Thinking OFF     █████████████████████       40.8%   (4× cheaper)
"Think briefly"  ███                          6.6%   (confused the model)
```

### Why it happened

We read the answers that were too long. Most of them were **loops**: the model wrote the same few lines again
and again until it ran out of space. So the model was not "thinking too carefully". It was **stuck**.

- Our training showed the model short, correct answers. That teaches it nothing about how to get unstuck.
- A thinking limit simply stops the loop and makes the model answer. That works.

### What it means

For small AI models that write code, a **free thinking limit** works better than training the model to think
shorter. Before spending money on training, try the free options first.

---

## Key facts at a glance

| | |
|---|---|
| Research question | Is training a small model to think shorter better than the free options? |
| Answer | **No.** A free thinking limit was better. |
| Model | Qwen3.5-2B (2 billion parameters, has a thinking on/off switch) |
| Test problems | 234: HumanEval+ (164) and LiveCodeBench (70: 31 easy, 39 medium) |
| Answers checked | 2,808 test answers (6 ways × 234 problems × 2 tries), plus 96 re-runs with more room |
| How answers were checked | By running each test set's own tests on the code (no checking by eye) |
| Best way | Thinking limit at 1,024 tokens: **49.8%**, +7.7 points over normal thinking [+4.3, +11.3] |
| Cheapest way | Thinking off: 860 tokens per answer (normal thinking: 3,446) |
| Main reason | Long answers were mostly **loops** (69.5% of normal thinking's unfinished answers) |
| Computer used | One Google Colab A100 GPU, about 38 paid units |
