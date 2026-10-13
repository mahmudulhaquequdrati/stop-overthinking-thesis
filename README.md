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

## Completed result and next step — 14 October 2026

**Qwen3.5-2B + LoRA-1 + thinking limit 1,024: 41.2% (191/464).**
All 464 problems were generated and graded, one attempt each.
Limit alone: 38.6% on the same 464 first attempts.
Gap: +2.6 points; 95% interval −1.5 to +6.7. The gain remains inconclusive.
On 424 shared first attempts: combination 43.9%, LoRA-1 alone 38.0%.
Earlier all-attempt LoRA-1 accuracy is 37.4%; keep the weighting labels.
The v2 ledger records 20.51 estimated units under the 45-unit ceiling.

Next planned work: **2B LoRA-1 alone on the missing 40, then 4B LoRA-1 alone on the same 40**.
[Notebook 22](notebooks/22_lora1_missing40_2b_4b.ipynb) is built: a separate 20-unit estimated ceiling, exact IDs, adapter checks, and resume skipping. [Run instructions](qa/48-lora1-missing40.md).
No training or rerun of their existing 424 answers. Other missing methods are outside scope.
Results are not available yet; new combined scores will be added after grading.
[Completed evidence](results/lora-limit-2b/README.md) · [Exact missing IDs and plan](results/lora-missing40/PLAN.md).

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
