# Appendices

## Appendix A. Every problem, every number, every chart

The full results page lists **every** test problem (all 234, with how many of its 2 tries each way solved) and **every**
training problem (all 280, with how many of its 4 tries were correct and whether it was kept):

- **[results/full-results/FULL-RESULTS.md](../results/full-results/FULL-RESULTS.md)**, Appendix A (test problems) and Appendix B (training problems)
- The same as spreadsheets: [per-problem.csv](../results/full-results/tables/per-problem.csv),
  [training-problems.csv](../results/full-results/tables/training-problems.csv),
  [per-way-per-group.csv](../results/full-results/tables/per-way-per-group.csv),
  [gpu-time.csv](../results/full-results/tables/gpu-time.csv)
- All 10 charts: [results/full-results/figures/](../results/full-results/figures/)

## Appendix B. How to repeat this work

**Re-check every number (no GPU needed, about one minute):**

```text
node scripts/make_full_results.js     → rebuilds FULL-RESULTS.md, the charts and the tables
node scripts/check_thesis_run.js results/2026-09-24-thesis-run   → loops, stage D, training data
```

**Re-run the whole experiment (needs a Colab A100 and about 40 units):**

1. Open `notebooks/14_thesis_run.ipynb` in Google Colab. Choose **Runtime → Change runtime type → A100 GPU**.
2. Put the pilot LoRA (LoRA-1) in `MyDrive/stop-overthinking/results/mini/lora/lora100` (made by `notebooks/13_mini_thesis.ipynb`).
3. **Runtime → Run all.** Type the number of Colab units left when asked.
4. The notebook runs every stage, skips what is already done after a disconnect, and prints the results tables at the end.

**Key scripts:**

| Script | What it does |
|---|---|
| `scripts/gen_colab.py` | Makes the model answer, for every way (including the thinking limit and the LoRAs) |
| `scripts/prompts.py` | Builds the question and splits an answer into thinking and answer part |
| `scripts/grade_plus.py`, `scripts/grade_lcb.py` | Run the benchmarks' tests in a separate process |
| `scripts/overlap_check.py` | Removes training problems that are too close to a test problem |
| `scripts/make_train_set.py` | Keeps the shortest correct answer (at least half the median) |
| `scripts/train_lora.py` | Trains a LoRA |
| `scripts/compare_thesis.py` | Accuracy, token ratios, error bars, hypotheses |

## Appendix C. How the project developed

| Date (2026) | Step |
|---|---|
| 13 Sept | Topic, gap and plan written; proposal written |
| 19–20 Sept | First model calls. Gemma-4-E4B too slow on free GPUs; pilot on 30 HumanEval problems |
| 20 Sept | Moved to Google Colab and Qwen3.5-2B; test set fixed at 234 problems |
| 22 Sept | Pilot study (the "mini-thesis") on MBPP+: training shortened thinking by 41% and gained 15 points |
| 22 Sept | Rules for the main run fixed before any result (token limits, main LoRA, budget) |
| 21–24 Sept | Main run on a Colab A100 |
| 25 Sept | Raw answers checked (loops found); results and thesis written |

Every choice and its reason is logged, with dates, in [DECISIONS.md](../DECISIONS.md) (69+ entries).

## Appendix D. Words used in this thesis

| Word | Meaning |
|---|---|
| **Accuracy** | Answers that passed all tests ÷ all answers |
| **Benchmark** | A fixed set of problems with a fair way to check the answers |
| **Bootstrap** | A way to get error bars: re-draw the problems at random 2,000 times and see how much the result moves |
| **Cut off** | The answer reached the token limit before it finished; it counts as a fail |
| **Epoch** | One pass over all the training examples |
| **Error bar (95%)** | The range the true difference very likely lies in; if it doesn't include 0, the difference is proven |
| **Fine-tuning / training** | Nudging the model's numbers with examples, so it writes more like them |
| **GPU** | The graphics card that runs the model |
| **LoRA** | A small add-on trained on top of the model; the model itself stays unchanged |
| **Loop** | The model repeats the same lines until it runs out of room |
| **Median** | The middle value when the numbers are sorted |
| **Overthinking** | Thinking far longer than needed, but still finishing |
| **Parameter** | One of the billions of numbers that hold what the model learned |
| **Percentage point** | The simple difference between two percentages: 49.8% − 42.1% = 7.7 points |
| **Reasoning model** | A model that writes a thinking part before its answer |
| **Seed** | A fixed starting number for random choices, so results can be repeated exactly |
| **Test case** | One input and the output the code must give for it |
| **Thinking limit (budget)** | Stop the thinking after a fixed number of tokens and make the model answer |
| **Thinking ratio** | A way's thinking tokens ÷ normal thinking's, on the same problems (x1.00 = the same) |
| **Thinking switch** | A setting that turns the thinking part on or off |
| **Token** | A small piece of text, about ¾ of a word; the unit of cost |

More words are explained in [GLOSSARY.md](../GLOSSARY.md).
