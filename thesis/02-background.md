# 2. Background

This chapter explains the ideas the thesis builds on, from the ground up. If you already know how language
models work, you can skip to Section 2.7.

## 2.1 What is a large language model?

A **large language model** (LLM) is a computer program that writes text. It works by guessing the next piece
of text again and again.

> **Everyday example.** Your phone's keyboard suggests the next word as you type. An LLM is the same idea,
> but much bigger and much better. It can continue a question with a whole correct answer.

The model learned to guess by reading a huge amount of text. What it learned is stored in billions of numbers
called **parameters**. Our model, Qwen3.5-2B, has about **2 billion** parameters. That is small for 2026. It
fits on one graphics card.

## 2.2 What is a token?

The model doesn't read or write whole words. It uses **tokens**: small pieces of text, about ¾ of a word on
average. "Overthinking" might be split into "Over" + "think" + "ing".

Tokens are how we measure **cost**. The model writes one token at a time, so:

```text
more tokens  →  more time  →  more electricity  →  more money
```

In this thesis, "the model wrote 3,446 tokens" means it wrote about 2,600 words.

## 2.3 What is a reasoning model, and what is "thinking"?

A **reasoning model** writes two parts:

```text
Question → [ THINKING: notes to itself ... ] → [ ANSWER: the final code ]
```

The thinking part is like a student's rough work on scrap paper. It often makes the final answer more correct.
In our model, the thinking ends with a special marker, `</think>`. Everything before the marker is thinking.
Everything after it is the answer.

## 2.4 The thinking switch

Many 2026 models, including the Qwen3.5 family, have a **thinking switch**. With the switch ON, the model thinks
before answering. With it OFF, the model answers directly. Qwen3.5-2B is OFF by default; we turned thinking on
where needed with the setting `enable_thinking=True`.

## 2.5 Overthinking, and a second problem: loops

**Overthinking** means thinking much longer than needed, for example checking an easy answer again and again
(Sui et al., 2025).

A related but different problem is the **loop** (also called *repetition*). The model starts repeating the same
lines, and never reaches the end marker:

```text
"...I'll track opening and closing parentheses... The implementation requires careful tracking...
 ...I'll track opening and closing parentheses... The implementation requires careful tracking...
 ...I'll track opening and closing parentheses..."          ← until it runs out of space
```

This difference turns out to be the key to our results. Overthinking still ends with an answer. A loop never
ends by itself. The makers of our model warn about exactly this. The official Qwen3.5-2B model card says:
*"Qwen3.5-2B is more prone to entering thinking loops compared to other Qwen3.5 models, which may prevent it from
terminating generation properly."*

## 2.6 What is training, and what is LoRA?

**Training** (or **fine-tuning**) means showing the model examples and nudging its parameters so it becomes more
likely to write text like those examples.

Changing all 2 billion parameters is expensive. **LoRA** (Low-Rank Adaptation; Hu et al., 2022) is a cheaper way.
It leaves the model unchanged and trains a **small add-on** that sits on top of it.

> **Everyday example.** Instead of rewriting a whole textbook, you add sticky notes to some pages. The book stays
> the same; the notes change how you read it.

Our LoRA add-ons are about 44 MB, against 4.6 GB for the model.

## 2.7 Training a model to think shorter: "shortest correct"

The idea we test comes from Munkhbat et al. (2025):

```text
1. The model answers each practice problem several times (here: 4 times).
2. Check each answer with the problem's tests.
3. Keep the SHORTEST answer that is still CORRECT.
4. Train the model on these short, correct answers.
```

The hope is that the model learns the habit: "stop thinking once you have enough".

**What earlier work found:**

| Work | Setting | Result |
|---|---|---|
| Munkhbat et al., 2025 | Math, models of 1.5–8B | About 12% fewer tokens with a plain prompt, accuracy about the same |
| SEER, 2025 | Code, a 7B model | About 40% shorter thinking; LoRA about 7 points less accurate than full training |
| ASAP, 2025 | Code, 7–8B models | 23.5% fewer tokens on LiveCodeBench |
| S3-CoT, 2026 | — | Warns that training on the *very* shortest answers hurts accuracy |

None of these models had a thinking switch, so none could compare training with simply turning thinking off.

## 2.8 The free options in earlier work

- **Thinking OFF.** NoThinking (2025) showed that skipping thinking can beat thinking with a small budget, also on
  code. So "thinking off" is a serious option that any trained method must beat.
- **Thinking limit** (also called a *thinking budget* or *budget forcing*). Stop the thinking after a fixed number of
  tokens and make the model answer. The s1 paper (2025) describes budget forcing as *"forcefully terminating the
  model's thinking process"*. The Qwen3 report (2025) also describes a *"thinking budget mechanism"*.
- **Ask to be brief.** Put an instruction like "think briefly" in the question.
- **HRBench (2026)** compared many ways to use the thinking switch, on models from Qwen3.5-2B upwards, and found no
  single winner. It did not include a model trained to think shorter.

## 2.9 Why small models may be different

Two recent findings matter for a 2-billion-parameter model:

- **Small models learn less from long reasoning.** Li et al. (2025): *"small models (≤3B parameters) do not
  consistently benefit from long chain-of-thought (CoT) reasoning or distillation from larger models."*
- **Smaller models loop more.** Pipis et al. (2025): *"Larger models tend to loop less, and distilled students loop
  significantly even when their teachers rarely do."*

We did not know these when we planned the study. They help explain our results (Chapter 6).

## 2.10 How code answers are checked: test sets

A **benchmark** is a fixed set of problems with a fair way to check answers. For code, the check is to **run the
code against tests**. A **test case** is one input with the expected output:

```text
Problem:   write add(a, b)
Test 1:    add(2, 3)   should give 5
Test 2:    add(-1, 1)  should give 0
Answer passes only if it passes ALL tests.
```

We used two benchmarks:

| Benchmark | What the problems are like | Tests |
|---|---|---|
| **HumanEval+** (Liu et al., 2023) | 164 easy problems: complete one Python function | The original HumanEval tests extended *"by 80x"* with extra, harder tests |
| **LiveCodeBench** (Jain et al., 2024) | Programming-contest problems: read input, print output | Hidden tests from the contest site; new problems are added over time |

LiveCodeBench keeps adding new problems. We used problems released from **February 2025 on**, to lower the chance
that the model saw them while it was being built. We also used **MBPP+** (Liu et al., 2023), a set of easy
Python problems, but only for training and for our pilot study, never as test problems in the main run.

## 2.11 Summary

```text
Reasoning models think before answering → thinking costs tokens → small models may overthink
                                                                  → or get stuck in LOOPS
Fixes: FREE (off / limit / "brief")  vs  TRAINED (shortest-correct LoRA)
Nobody had compared them on one small model with a switch, on code  → this thesis
```
