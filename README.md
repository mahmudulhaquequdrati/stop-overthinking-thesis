# Stop Overthinking, Keep Passing the Tests

## Next: five LoRA controls, one session

[Notebook24](notebooks/24_lora1_off_and_limits.ipynb) runs0.8B OFF/limit512,2B OFF,and4B limit2048/OFF.
Each uses the same464 problems once. No training or completed2B-limit rerun.
Enter the current resource balance, rate, and total unit ceiling at startup.
[Instructions](qa/49-five-lora-controls.md). Scores remain unmeasured until the ZIP is checked.


**Shortest-correct LoRA training versus free thinking controls in small Qwen3.5 code models.**

The easy thesis now combines **464 unique test problems**.
Each problem has equal weight, using all available attempts.

Best observed free controls with full coverage:

- **0.8B: thinking OFF — 14.7%.**
- **2B: limit 1,024 — 38.6%.**
- **4B: limit 2,048 — 71.9%.**

2B and 4B LoRA-1 now cover 464/464. Comparisons use the same 464 problems.
Missing results are not failures. The 0.8B free control's small lead over LoRA remains uncertain.

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
