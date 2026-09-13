# ROADMAP — start here

> This is the front door. It shows the whole thesis, where you are, and the next step.
> Other files: [PLAN.md](PLAN.md) (the research design) · [DECISIONS.md](DECISIONS.md)
> (every choice and why) · [PAPERS.md](PAPERS.md) (related work) · [research/](research/) (search notes).

---

## 1. The thesis in one picture

Working title: **"Think Less, Code Just as Well"**

```text
PROBLEM     Small AI models "think" a lot before answering code questions, even easy ones.
            Thinking costs time and computer power.
   ↓
GAP         Nobody has checked, on one small model that has a thinking ON/OFF switch:
            is TRAINING it to think shorter better than just switching thinking OFF?
   ↓
QUESTION    Can we train the model to think shorter, keep its accuracy,
            beat the OFF switch, and still do well on math?
   ↓
EXPERIMENT  Same model, same test problems, 5 ways of answering:
            OFF · budget · "think briefly" · ON · ON + our training
   ↓
RESULTS     Accuracy vs thinking length, with error bars
   ↓
CONCLUSION  When training is worth it, how much data it needs, whether it carries over
```

**Everyday example.** A student writes 5 pages for every exam question, even "2 + 2".
We teach them to write short when short is enough, without more wrong answers.
We also check whether just saying "don't think, just answer" works as well.

---

## 2. You are here

```text
┌─────────────────────────────────────────────────────────┐
│  ✅ Topic chosen, gaps found, plan written (2026-09-13)  │
│  ✅ Proposal PDF written → proposal/ (2026-09-13)        │
│  ⬜ Part 1: learn what AI is          ← YOU ARE HERE     │
│  ⬜ Part 2: learn the tools                              │
│  ⬜ Part 3: research skills                              │
│  ⬜ Part 4: measure (baselines + gates)                  │
│  ⬜ Part 5: improve (train + test)                       │
│  ⬜ Part 6: write + defend                               │
└─────────────────────────────────────────────────────────┘
Nothing has been run yet. $0 spent.
```

---

## 3. How the course works

- **One lesson = one idea.** Each lesson answers **What is it? Why do we need it? How does it work?**
- **Same shape every time:** In one sentence · What is it? · Why do we need it? · How does it work? · Try it (free) · ✅ Check yourself · You are here.
- **The done test:** you explain the lesson back in your own words. If you can, move on. If not, we try another way.
- **Lessons are written as you reach them,** so nothing gets stale.
- **Learn first, then do.** A notebook (code) step comes only after the lesson that explains it.

---

## 4. The course map

✅ = written · ⬜ = comes when you reach it

### Part 0 — The map
| # | Lesson | One line |
|---|---|---|
| ✅ [00](lessons/00-what-is-a-thesis.md) | What a thesis is | A question, answered with evidence, that adds something new |

### Part 1 — What AI is (no code)
| # | Lesson | One line |
|---|---|---|
| ✅ [01](lessons/01-what-is-an-llm.md) | What an LLM is, and why | A machine that learned to guess the next word from huge amounts of text |
| ⬜ 02 | Tokens | The small pieces of text a model reads and writes |
| ⬜ 03 | How a model learns | Training, and fine-tuning: teaching an existing model a new habit |
| ⬜ 04 | Reasoning models and "thinking" | Writing hidden notes before the answer; the ON/OFF switch |
| ⬜ 05 | Overthinking | Our problem: long thinking where short would do |
| ⬜ 06 | Cutoff dates | "Has the model already seen the test?" |

### Part 2 — The tools
| # | Lesson | One line |
|---|---|---|
| ⬜ 07 | GPU memory | Why 16 GB of model fits in a 15 GB GPU (16-bit vs 4-bit) |
| ⬜ 08 | Python basics | Just enough to read and run notebooks |
| ⬜ 09 | Colab and Kaggle | Free computers with GPUs, in the browser |
| ⬜ 10 | Hugging Face | The free library of models and datasets |
| ⬜ 11 | First model call | Ask Gemma one question, thinking ON vs OFF, count the tokens |

### Part 3 — Research skills
| # | Lesson | One line |
|---|---|---|
| ⬜ 12 | Reading a paper | Abstract, method, results, limits, in 20 minutes |
| ⬜ 13 | Finding a gap | What others did, what's missing, using our [PAPERS.md](PAPERS.md) |

### Part 4 — Measuring
| # | Lesson | One line |
|---|---|---|
| ⬜ 14 | Code benchmarks + safe grading | Problems with tests, and running AI code in a sandbox |
| ⬜ 15 | Statistics you need | Averages, error bars, comparing the same problems before/after |
| ⬜ 16 | Baselines | Thinking OFF, budget, "think briefly": the things we must beat |
| ⬜ 17 | The gates | Memory test + headroom test: is there something to learn? |

### Part 5 — Improving
| # | Lesson | One line |
|---|---|---|
| ⬜ 18 | Fine-tuning and LoRA | Training a small add-on instead of the whole model |
| ⬜ 19 | Making training data | Keep the shortest correct answer |
| ⬜ 20 | Training with Unsloth | Running the training on a free GPU |
| ⬜ 21 | The learning curve | 100 → 2,000 examples: how much data is enough? |
| ⬜ 22 | Fresh test + math transfer | Unseen problems, and does it work on math too? |
| ⬜ 23 | (stretch) GRPO | Reinforcement learning with a length reward |

### Part 6 — The thesis
| # | Lesson | One line |
|---|---|---|
| ⬜ 24 | Question and hypotheses | Writing them properly |
| ⬜ 25 | Related work chapter | Turning PAPERS.md into a chapter |
| ⬜ 26 | The chapters | Method, results, discussion, limits |
| ⬜ 27 | The defence | The questions an examiner will ask, and your answers |

---

## 5. The research plan in 6 lines

1. **Model:** Gemma-4-E4B (2026, thinking switch, cutoff Jan 2025). Backup: Qwen3.5-4B.
2. **Problems:** easy + medium code. Training ≈ thousands; testing ≈ 1,000–2,000; plus math for the transfer test.
3. **Method:** the model answers 4 times → keep the shortest correct answer → train a LoRA add-on on those.
4. **Compare:** thinking OFF · budget · "think briefly" · ON · ON + LoRA.
5. **Gates first:** does it fit in memory? Is there something to learn (short answers ≥25% shorter)?
6. **Contributions:** training vs switch (G-A) · how much data (G-B) · code → math transfer (G-C).

Details: [PLAN.md](PLAN.md).

---

## What to do next

**Read [lesson 00](lessons/00-what-is-a-thesis.md), then [lesson 01](lessons/01-what-is-an-llm.md).**
Then tell me in your own words:
1. What is a thesis?
2. What is an LLM, and why does "thinking" cost time?
