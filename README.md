# Stop Overthinking, Keep Passing the Tests

**Shortest-correct LoRA training versus free thinking controls in small Qwen3.5 code models.**

The easy thesis now combines **464 unique test problems**.
Each problem has equal weight, using all available attempts.

Best observed free controls with full coverage:

- **0.8B: thinking OFF — 14.7%.**
- **2B: limit 1,024 — 38.6%.**
- **4B: limit 2,048 — 71.9%.**

2B and 4B LoRA-1 each cover 424/464 problems.
Their comparisons use the same 424 problems for the free controls.
Missing results are not failures. The 0.8B free control's small lead over LoRA remains uncertain.

## Next experiment

[Notebook 21 — 2B LoRA-1 + limit 1,024](notebooks/21_2b_lora1_limit1024.ipynb).
Select A100 and Run all; the original LoRA-1 weights must be on Drive.
The user-approved total ceiling is 45 Colab units, with recorded failed-attempt usage retained. [Instructions and checks](qa/45-lora-with-limit-notebook.md).
Built locally; no new model result has been measured yet.

## Start here

- [Easy thesis for teachers](easy-thesis/PAPER.md).
- [Full easy thesis](easy-thesis/FULL-THESIS.md).
- [Combined results and audit](results/combined/README.md).
- [Progress and next step](ROADMAP.md).
- [Research design](PLAN.md) and [decision history](DECISIONS.md).

This is a retrospective summary of saved runs, chosen after results were available.
The [original formal thesis](thesis/THESIS.md) and raw files preserve the historical study.
Their original scores are not the combined 464-problem scores.

Rebuild the combined analysis locally:

```sh
python3 scripts/combine_results.py
python3 scripts/build_combined_easy_thesis.py
```

No training, model generation, or Colab units are needed.
