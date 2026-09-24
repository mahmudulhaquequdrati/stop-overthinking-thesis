# ROADMAP: start here

> **This is the front door.** It shows the whole thesis, where you are, and the next step.
>
> | File | What is in it |
> |---|---|
> | [PLAN.md](PLAN.md) | The research design: what exactly we will do |
> | [DECISIONS.md](DECISIONS.md) | Every choice we made, and why |
> | [qa/](qa/) | **Teacher Q&A:** one file per step, with questions and simple answers |
> | [GLOSSARY.md](GLOSSARY.md) | Every hard word, explained simply |
> | [PAPERS.md](PAPERS.md) | Papers by other researchers on the same topic |
> | [research/](research/) | Full notes from our searches |

---

## 1. The thesis in one picture

Short title: **"Stop Overthinking, Keep Passing the Tests"**

Full title: *Stop Overthinking, Keep Passing the Tests: Shortest-Correct LoRA Fine-Tuning versus the Thinking Switch in a Small Code Model (Gemma-4-E4B)*

```text
PROBLEM     Small AI models "think" a lot before answering code questions, even easy ones.
            Thinking costs time and computer power.
   ↓
GAP         Nobody has checked, on one small model that has a thinking ON/OFF switch:
            is TRAINING it to think shorter better than just switching thinking OFF?
   ↓
QUESTION    Can we train the model to think shorter, keep its accuracy,
            and beat the free options (OFF, a length limit, "think briefly")?
   ↓
EXPERIMENT  Same model, same test problems, 5 ways of answering:
            OFF · limit · "think briefly" · ON · ON + our training
   ↓
RESULTS     Accuracy vs. thinking length, with error bars
   ↓
CONCLUSION  Is training worth it for code, on a small model?
```

**One question only.** On 2026-09-13 we cut the thesis down to this single question.
It has the best chance of a positive result (DECISIONS #25).

**Everyday example.** A student writes 5 pages for every exam question, even "2 + 2".
We teach them to write short when short is enough, without more wrong answers.
We also check whether just saying "don't think, just answer" works as well.

---

## 2. You are here

```text
┌──────────────────────────────────────────────────────────────┐
│  ✅ Topic chosen, gap found, plan written (2026-09-13)       │
│  ✅ Proposal: 4 pages, md + html + pdf (#26, #29, 2026-09-13)│
│  ✅ Title changed (DECISIONS #28, 2026-09-13)                │
│  ✅ GPU time estimated (DECISIONS #30–31, 2026-09-17)        │
│  ✅ All docs in simple English + teacher Q&A (2026-09-17)    │
│  ⬜ Part 1: learn what AI is                                  │
│       ✅ Lessons 00–01 explained back (2026-09-17)            │
│       ✅ Lesson 02 Tokens written + qa/11                     │
│       ✅ Lesson 03 How a model learns written + qa/12         │
│       ✅ Lesson 04 Reasoning models + thinking + qa/13        │
│       ✅ Lessons 05–06 + qa/14–15 (Part 1 all written)        │
│  ⬜ Part 2: the tools (all written 2026-09-17)                │
│       ✅ Lessons 07–11 + qa/16–19                             │
│       ✅ Notebook 08 (Python) and 10 (data): RUN, they work   │
│       ✅ Notebook 11 (first model call): RUN on Kaggle        │
│           ✅ Loads (table in CPU memory), switch works        │
│           ❌ Writes only ~4.4 tokens/s: far too slow (#46)    │
│       ✅ Tried the Mac: fast on easy, too slow on medium      │
│           easy 52 tok/s · medium 21 tok/s = 250 s/problem     │
│       ✅ PILOT: 30 HumanEval problems graded (#50, #51)       │
│           OFF 93% · ON 83% (4 answers cut off) · 5.5× tokens │
│       ✅ MOVED to Google Colab + Qwen3.5-2B (#52, #53)        │
│           Mac scripts deleted · notebook 12 written           │
│           thinking-counter bug found and fixed (#56)          │
│       ✅ Notebook 12 = free go/no-go test (#59, 2026-09-21)   │
│           + float16 check · + medium problems · + vLLM try   │
│       ✅ Notebook 13 = free mini-thesis (#60, 2026-09-22)     │
│           MBPP+ · 100 test problems · LoRA 25/50/100%      │
│       ✅ Notebook 13 RUN on A100 (#63, #64)                   │
│           LoRA 65% vs ON 50%, 41% fewer tokens: R1 YES       │
│       ✅ Notebook 14 written: the real run (#66, 2026-09-22)  │
│       ✅ Notebook 14 RUN on the A100 (2026-09-24)             │
│           all stages ran · LoRA-2: NOT shorter (H1 NO)      │
│           limit 49.8% beats ON 42.1% (proven, #67)          │
│       ✅ Raw files checked (2026-09-25) + qa/28               │
│           long answers = LOOPS · brief = prompt clash       │
│       ✅ Full results page: 10 charts + every problem         │
│           results/full-results/FULL-RESULTS.md (#68)        │
│       ⬜ Write the results + analysis chapter ← HERE          │
│       ⬜ You explain Parts 1–2 back in your own words         │
│  ⬜ Part 2: learn the tools                                   │
│  ⬜ Part 3: research skills                                   │
│  ⬜ Part 4: measure (compare the free options + the checks)   │
│  ⬜ Part 5: improve (train + test)                            │
│  ⬜ Part 6: write + defend                                    │
└──────────────────────────────────────────────────────────────┘
Notebooks 08, 10 and 11 have been run. The Mac pilot worked but medium problems were too slow,
so everything moved to Google Colab with a smaller model (Qwen3.5-2B). Notebook 12 is now a free
go/no-go test: we pay for nothing until it passes (#59). Notebook 13 runs the whole method small
and free first (#60). It ran on a paid A100: training cut tokens 41% AND raised accuracy 50% → 65%
on easy problems (#64). Paid Colab units are now in use.
```

**Where we are in the research chain:**

```text
PROBLEM ✅ → GAP ✅ → QUESTION ✅ → HYPOTHESIS ✅ → EXPERIMENT ⬜ → DATA/CODE ⬜ → RESULTS ⬜ → ANALYSIS ⬜ → CONCLUSION ⬜
                                                    ↑ next big box
```

The first four boxes are written down. They are only on paper; nothing is tested yet.

---

## 3. How the course works

- **One lesson = one idea.** Each lesson answers: **What is it? Why do we need it? How does it work?**
- **Same shape every time:** In one sentence · What is it? · Why do we need it? · How does it work? · Try it (free) · ✅ Check yourself · You are here.
- **The "done" test:** you explain the lesson back in your own words. If you can, we move on. If not, we try another way.
- **Lessons are written when you reach them,** so nothing gets old.
- **Learn first, then do.** A notebook (code) step comes only after the lesson that explains it.
- **Every step ends with a Q&A file** in [qa/](qa/), so you can answer your teacher.

---

## 4. The course map

✅ = written · ⬜ = comes when you reach it

### Part 0: The map
| # | Lesson | One line |
|---|---|---|
| ✅ [00](lessons/00-what-is-a-thesis.md) | What a thesis is | A question, answered with evidence, that adds something new |

### Part 1: What AI is (no code)
| # | Lesson | One line |
|---|---|---|
| ✅ [01](lessons/01-what-is-an-llm.md) | What an LLM is, and why | A machine that learned to guess the next word from a huge amount of text |
| ✅ [02](lessons/02-tokens.md) | Tokens | The small pieces of text a model reads and writes |
| ✅ [03](lessons/03-how-a-model-learns.md) | How a model learns | Training, and fine-tuning: teaching an existing model a new habit |
| ✅ [04](lessons/04-reasoning-models-and-thinking.md) | Reasoning models and "thinking" | Writing notes before the answer; the ON/OFF switch |
| ✅ [05](lessons/05-overthinking.md) | Overthinking | Our problem: long thinking where short would do |
| ✅ [06](lessons/06-cutoff-dates.md) | Cutoff dates | "Has the model already seen the test?" |

### Part 2: The tools
| # | Lesson | One line |
|---|---|---|
| ✅ [07](lessons/07-gpu-memory.md) | GPU memory | Why a 16 GB model fits in a 15 GB GPU (16-bit vs. 4-bit) |
| ✅ [08](lessons/08-python-basics.md) | Python basics | Just enough to read and run notebooks |
| ✅ [09](lessons/09-colab-and-kaggle.md) | Colab and Kaggle | Free computers with GPUs, in the browser |
| ✅ [10](lessons/10-hugging-face.md) | Hugging Face | The free library of models and datasets |
| ✅ [11](lessons/11-first-model-call.md) | First model call | Ask Gemma one question, thinking ON vs. OFF, count the tokens |

### Part 3: Research skills
| # | Lesson | One line |
|---|---|---|
| ⬜ 12 | Reading a paper | Summary, method, results, limits, in 20 minutes |
| ⬜ 13 | Finding a gap | What others did, what's missing, using our [PAPERS.md](PAPERS.md) |

### Part 4: Measuring
| # | Lesson | One line |
|---|---|---|
| ⬜ 14 | Code tests + safe grading | Problems with tests, and running AI code in a safe closed box (sandbox) |
| ⬜ 15 | Statistics you need | Averages, error bars, comparing the same problems before/after |
| ⬜ 16 | What we compare against | Thinking OFF, limit, "think briefly": the things we must beat |
| ⬜ 17 | The two checks | Memory check + room-to-shorten check: is there something to learn? |

### Part 5: Improving
| # | Lesson | One line |
|---|---|---|
| ⬜ 18 | Fine-tuning and LoRA | Training a small add-on instead of the whole model |
| ⬜ 19 | Making training data | Keep the shortest correct answer |
| ⬜ 20 | Training with Unsloth | Running the training on a free GPU |
| ⬜ 21 | Reading the result | The accuracy-vs-tokens chart: did training beat the free options? |
| ~~22~~ | ~~The learning curve · Fresh test + math transfer · GRPO~~ | Dropped 2026-09-13: future work, not part of the thesis |

### Part 6: The thesis
| # | Lesson | One line |
|---|---|---|
| ⬜ 24 | Question and hypotheses | Writing them properly |
| ⬜ 25 | Related work chapter | Turning PAPERS.md into a chapter |
| ⬜ 26 | The chapters | Method, results, discussion, limits |
| ⬜ 27 | The defence | The questions an examiner will ask, and your answers (start from [qa/](qa/)) |

---

## 5. The research plan in 6 lines

1. **Model:** Qwen3.5-2B (2026, thinking switch, runs fully on a free Colab T4). Backup: Qwen3.5-4B. *(Was Gemma-4-E4B until 2026-09-20 — DECISIONS #53.)*
2. **Problems:** easy + medium code. Training ≈ thousands. Testing = **234** (HumanEval+ 164 + LiveCodeBench easy/medium 70), cut to fit free Colab in one week (DECISIONS #58).
3. **Method:** the model answers 4 times → keep the shortest correct answer → train one LoRA add-on on those.
4. **Compare 5 ways of answering:** thinking OFF · limit · "think briefly" · ON · ON + LoRA.
5. **Checks first:** does it fit in memory? Is there room to shorten (short answers ≥25% shorter)? If not, ask 8 times instead of 4.
6. **Contribution:** one fair answer: is training better than the free options (gap G-A)?

Details: [PLAN.md](PLAN.md). Teacher questions: [qa/](qa/).

---

## What to do next

**Everything now runs on Google Colab, with Qwen3.5-2B** (DECISIONS #52, #53). The Mac was fast
on easy problems (52 tokens/s) but slow on the medium ones we actually need: **250 seconds for a
single problem**. A free T4 answers 16 at once, and the whole 2B model fits on it.

Done already, without a GPU:
- the Mac scripts are deleted and the reusable parts saved in `scripts/prompts.py`
- a real bug was caught: Qwen keeps `<think>` in the *prompt*, so our old counter would have
  reported **0 thinking tokens on every answer** and never complained (DECISIONS #56).
  `scripts/test_prompts.py` now checks this — 13 out of 13 checks pass.

**The rule since 2026-09-21 (DECISIONS #59): test everything for free first, pay only after it
passes.** If the plan fails on the free T4, we lost nothing.

**Done (2026-09-22): the mini-thesis ran on a paid A100** ([results](results/2026-09-22-mini-thesis-first-results.md), DECISIONS #64):

~~~text
thinking ON     50%   1,936 tokens   27 never finished
LoRA (ours)     65%   1,145 tokens   15 never finished   ← +15 points AND 41% fewer tokens
thinking OFF    56%     100 tokens
think briefly    3%   4,056 tokens   (the model loops on the instruction)
~~~

On easy problems, training works: rule R1 says YES. The learning curve is flat, so more of the
same data is unlikely to help much.

**Next, and it is one thing: run [notebooks/14_thesis_run.ipynb](notebooks/14_thesis_run.ipynb) on the A100.**
Runtime → A100 → **Run all**. Type the units left once. Paste back only the last cell.

~~~text
smoke (0.7) → A: 5 ways × 234 problems (10.3, must) → B: LoRA-2 (10.7) → C: 2nd try (12.8) → D: 16k check (2.7)
every stage checks the budget first: it runs only if  units left − its cost ≥ 20
~~~

Token limits: 4,096 (HumanEval+) · 8,192 (LiveCodeBench) · the same for every way (DECISIONS #66).

Also still open: you explain Parts 1–2 back in your own words.
