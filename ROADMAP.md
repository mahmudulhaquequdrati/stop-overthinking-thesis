# ROADMAP: start here

<!-- CURRENT-STUDY:START -->

**Current study — 14 October 2026:** **464 unique test problems**.
Benchmarks: **164 HumanEval+**, **166 LiveCodeBench easy**, **134 LiveCodeBench medium**.
All six planned LoRA combinations are complete, one attempt per problem:

- **0.8B:** LoRA + OFF **14.0% (65/464)**; LoRA + limit 512 **14.4% (67/464)**.
- **2B:** LoRA + OFF **35.6% (165/464)**; LoRA + limit 1,024 **41.2% (191/464)**.
- **4B:** LoRA + OFF **64.7% (300/464)**; LoRA + limit 2,048 **71.6% (332/464)**.

LoRA alone means thinking ON without a thinking-token limit.
Older methods' all-attempt averages and first-attempt comparisons are labelled separately.
LoRA + OFF does not consistently improve on free OFF; the 2B/4B gains over free limits remain uncertain.

[Every method, benchmark, difficulty, token count and interval](results/CURRENT-RESULTS.md) · [Full easy thesis](easy-thesis/FULL-THESIS.md) · [Full formal Markdown thesis](thesis/THESIS.md).

<!-- CURRENT-STUDY:END -->

## Completed LoRA combinations — 14 October 2026

All six planned combinations now have results for the same **464 problems**, one attempt each.

- **0.8B:** LoRA + OFF **14.0% (65/464)**; LoRA + limit 512 **14.4% (67/464)**.
- **2B:** LoRA + OFF **35.6% (165/464)**; LoRA + limit 1,024 **41.2% (191/464)**.
- **4B:** LoRA + OFF **64.7% (300/464)**; LoRA + limit 2,048 **71.6% (332/464)**.

LoRA + OFF does not consistently improve on OFF without LoRA.
The 2B and 4B limit combinations have not established a reliable accuracy gain over the free limit.
Compare first attempts with first attempts; keep all-attempt problem averages labelled separately.
No further run is needed to complete these six configurations.
The document rebuild uses saved results and spends no Colab units.

Read [the full easy thesis](easy-thesis/FULL-THESIS.md), including benchmark, difficulty, token and uncertainty tables.
The formal Markdown thesis is also updated; its original version is preserved in the dated archive.
[Checked result archive and calculations](results/lora-controls/README.md).

## Full 464 update — 14 October 2026

**2B LoRA-1 alone: 34.4%;4B LoRA-1 alone: 56.8%. Both now cover 464/464.**
The exact missing40 runs passed 1/40 (2B) and 12/40 (4B), with one attempt each.
No existing 424 LoRA-alone IDs were repeated.
The scores above average attempts within problems, then weight problems equally.

For 2B on the same 464 first attempts:
**LoRA + limit1024: 41.2% (191/464); LoRA alone: 34.9% (162/464); OFF: 32.5% (151/464).**
The combination's gain over LoRA alone is 6.2 points, interval +2.4 to +10.1.
Its gain over OFF is 8.6 points, interval +4.5 to +12.9.
LoRA alone's smaller lead over OFF remains inconclusive.
Limit alone is 38.6%; the combination's gain over it remains inconclusive.

Missing40 work is complete. Do not rerun Notebook 22 or the existing 424 answers.
Other incomplete methods remain outside scope.
[Updated results and both weighting rules](results/lora-missing40/README.md).

The easy thesis retains the original all-attempt combined tables, plus the labelled extension.
The formal Markdown thesis is updated. Earlier project stages remain historical.

---

## Historical roadmap

> **This is the front door.** It shows the whole thesis, where you are, and the next step.
>
> | File | What is in it |
> |---|---|
> | **[TEACHER-A-TO-Z.md](TEACHER-A-TO-Z.md)** | **Before a meeting:** A→Z map, where to check numbers, what to say |
| **[easy-thesis/FULL-THESIS.md](easy-thesis/FULL-THESIS.md)** | **Plain-language thesis** in one file (short chapters in the same folder) |
> | **[results/RESULTS-INDEX.md](results/RESULTS-INDEX.md)** | **All 0.8B / 2B / 4B numbers for the paper** |
> | [PLAN.md](PLAN.md) | The research design: what exactly we will do |
> | [DECISIONS.md](DECISIONS.md) | Every choice we made, and why |
> | [qa/](qa/) | **Teacher Q&A:** one file per step, with questions and simple answers |
> | [GLOSSARY.md](GLOSSARY.md) | Every hard word, explained simply |
> | [PAPERS.md](PAPERS.md) | Papers by other researchers on the same topic |
> | [research/](research/) | Full notes from our searches |

---

## 1. The thesis in one picture

Short title: **"Stop Overthinking, Keep Passing the Tests"**

Full title: *Stop Overthinking, Keep Passing the Tests: Shortest-Correct LoRA Fine-Tuning versus Free Thinking Controls in a Small Code Model (Qwen3.5-2B)* (updated 2026-09-25, DECISIONS #70; was "…versus the Thinking Switch… (Gemma-4-E4B)")

**📖 The complete thesis: [thesis/THESIS.md](thesis/THESIS.md) · 🖨️ print: [thesis/Stop-Overthinking-Thesis.pdf](thesis/Stop-Overthinking-Thesis.pdf)**

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
│       ✅ Results + analysis chapter, first draft (#69)        │
│       ✅ COMPLETE THESIS drafted (#70, 2026-09-25)            │
│           thesis/THESIS.md: 10 chapters + qa/30             │
│       ✅ Size × limit: 4B DONE (#72–73, 2026-09-29)           │
│           best = limit2048 78.2% · LoRA-1 69.9%               │
│           ~100 Colab compute hours used for 4B               │
│       ✅ Lean 0.8B DONE (#75–77): OFF best 20.5%              │
│       ✅ Size story in thesis (#78) · Teacher A→Z (#79)       │
│       ✅ Notebook 16 DONE: 2B limit512 = 45.1% (#82)          │
│       ✅ Notebook 17 DONE: 2B limit2048 = 46.6% (#84)         │
│           2B curve peaks at limit1024 (49.8%)                │
│       ✅ Easy thesis folder (#85)                            │
│           easy-thesis/FULL-THESIS.md                         │
│       ✅ Extra 40 problems listed (#86)                       │
│       ✅ Notebook 18 fast path fixed (#87)                    │
│       ✅ Notebook 18 returns to /content/thesis (#88)         │
│       ✅ Extra 40 scored (#89)                                │
│           free way still wins · OFF best or tied              │
│           2B OFF 12.5% · 4B OFF = limit2048 at 46.2%          │
│           first exam stays 234 · 49.8% and 78.2%              │
│           written into easy-thesis results + one page         │
│       ✅ Notebook 19 scored the 190 (#93) ←HERE            │
│           0.8B OFF 9.5% · 2B 31.1% · 4B 69.5%              │
│           free way wins · 2B LoRA skipped · 7.9 hours      │
│           one page shows 464 tests · train 100 and 280    │
│       ⬜ Fill name/supervisor; rebuild PDF; defend            │
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
PROBLEM ✅ → GAP ✅ → QUESTION ✅ → HYPOTHESIS ✅ → EXPERIMENT ✅ → DATA/CODE ✅ → RESULTS ✅ → ANALYSIS ✅ → CONCLUSION ✅
```

The first exam (234) is done. The extra 40 is done. The 190-problem side list is scored too.
Those later scores stay in their own tables. They do not replace 49.8% or 78.2%.

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

**Next, and it is one thing: fill your name and supervisor, then rebuild the PDF.**
Do **not** rerun notebooks 14–19. The 234, the extra 40, and the 190 are already scored.
Do **not** average the 190 into 49.8% or 78.2%.

The one hole on the 190 is 2B training. The weight file was not on the new Drive, so that way was skipped.
Leave it skipped unless a teacher asks for that one cell.

Also still open: you explain Parts 1–2 back in your own words.

## RPMR — Colab-only next step, 14 October 2026

The completed thesis remains finished. RPMR is an untested novelty candidate.
New work lives in [experiments/rpmr](experiments/rpmr/README.md): one Colab notebook,
a short README and the research proposal. Local-only tools were archived and removed.
About 50 compute units remain; preserve 20. Proposed smoke ceiling: five estimated units.
Next: upload the notebook to a fresh Colab GPU runtime and choose Run all.
The notebook is syntax-checked; no Colab smoke run has completed yet.
The verified baseline and cleanup archives remain in backups/ for undo.

## RPMR Colab smoke passed — 14 October 2026

User-provided report confirms calculation and cache compatibility on A100 80GB.
Elapsed 107.826 seconds; estimated 0.2028 units. No accuracy or loop-recovery result yet.
Next: online detector and complete repair-overhead measurement in Colab.
[Saved report](experiments/rpmr/results/20261014T125828Z-bf30149f/report.json).

## Next Colab step — Notebook 26, 14 October 2026

User confirms the previous GPU runtime disconnected. Notebook 25 remains passed.
[Notebook 26](experiments/rpmr/26_rpmr_colab_online_smoke.ipynb) is ready for online
loop detection, conditional repair and overhead measurement; not run yet.
Two prompts × three methods, 384 generated tokens each. Three-unit estimated cap; 20-unit reserve.
No eligible natural repair means recovery remains untested. Review its saved ZIP before expanding.

## Notebook 26 instrumentation result — 14 October 2026

Uploaded report confirms six capped responses, no loops detected and no online repairs.
Instrumentation passed; loop recovery and accuracy remain untested.
Next: inspect the downloaded answers.jsonl/ZIP before scheduling a longer diagnostic.
[Saved report](experiments/rpmr/results/20261014T131227Z-2ff3a723/report.json).

## Raw answers checked — next Notebook 27, 14 October 2026

All methods match per question. Even-sum final answer is cut off; substring thinking is cut off.
No harmful exact cycle is established. Notebook 27 is prepared for one longer substring
question, detection-only, 2,048 total-token cap and two-unit estimated ceiling.
[Next Colab notebook](experiments/rpmr/27_rpmr_colab_loop_search.ipynb). No new run started.

## Notebook 27 finished naturally — 14 October 2026

The longer substring response reaches EOS at 1,300 tokens with thinking closed.
Two identical thinking-code blocks appear, but no sustained exact cycle is detected.
No more reruns of this question. Next: identify candidate loops in saved training outputs.
[Saved report](experiments/rpmr/results/20261014T133535Z-da04a204/report.json).

## Stronger loop candidates found — 14 October 2026

Read-only screening finds 15 candidate 2B training attempts. Three inspected examples
show repeated reconsideration without thinking closure before their caps.
Next: one development candidate for provenance/separation checks and detector calibration,
then a budgeted Colab replay. No extra GPU run started. Decision #124.

## Next: Notebook 28 candidate reproduction — 14 October 2026

[Notebook 28](experiments/rpmr/28_rpmr_colab_known_loop.ipynb) is prepared for archived
loop calibration and at most two live tries on training candidate Mbpp/568.
Three-unit estimated cap; 20-unit reserve. No repair enabled.
Inspect its downloaded ZIP before a paired recovery experiment; not executed yet.
