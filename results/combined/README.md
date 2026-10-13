# Combined results: 464 unique problems

Retrospective analysis, 13 October 2026. Equal weight per problem.
Main complete-coverage controls: **0.8B: Thinking OFF 14.7%** · **2B: Limit 1,024 38.6%** · **4B: Limit 2,048 71.9%**

Coverage means unique problems with results. A missing result is not counted as a failure. Only compare scores directly when they use the same problems.

| Model | Way | Accuracy | Coverage | Attempts |
|---|---|---|---|---|
| 0.8B | Limit 1,024 | 11.3% | 274/464 | 274 |
| 0.8B | Limit 512 | 10.6% | 464/464 | 464 |
| 0.8B | LoRA-1 | 12.3% | 464/464 | 464 |
| 0.8B | Thinking OFF | 14.7% | 464/464 | 464 |
| 0.8B | Thinking ON | 4.1% | 464/464 | 464 |
| 2B | Think briefly | 6.4% | 274/464 | 548 |
| 2B | Limit 1,024 | 38.6% | 464/464 | 738 |
| 2B | Limit 2,048 | 40.9% | 274/464 | 274 |
| 2B | Limit 512 | 39.4% | 274/464 | 548 |
| 2B | LoRA-1 | 37.4% | 424/464 | 658 |
| 2B | LoRA-2 | 45.1% | 234/464 | 468 |
| 2B | Thinking OFF | 31.8% | 464/464 | 738 |
| 2B | Thinking ON | 26.8% | 464/464 | 738 |
| 4B | Limit 1,024 | 76.5% | 234/464 | 468 |
| 4B | Limit 2,048 | 71.9% | 464/464 | 738 |
| 4B | Limit 4,096 | 76.7% | 234/464 | 468 |
| 4B | Limit 512 | 75.4% | 234/464 | 468 |
| 4B | LoRA-1 | 59.3% | 424/464 | 658 |
| 4B | Thinking OFF | 66.5% | 464/464 | 738 |
| 4B | Thinking ON | 50.0% | 464/464 | 738 |


## Shared-problem comparisons

| Model | Way vs reference | Shared problems | Way accuracy | Reference accuracy | Gap (points) | 95% gap interval |
|---|---|---|---|---|---|---|
| 0.8B | Thinking OFF vs Thinking ON | 464 | 14.7% | 4.1% | +10.6 | [+7.5, +13.8] |
| 0.8B | Thinking OFF vs LoRA-1 | 464 | 14.7% | 12.3% | +2.4 | [-0.4, +5.2] |
| 2B | Limit 1,024 vs Thinking ON | 464 | 38.6% | 26.8% | +11.7 | [+8.5, +15.1] |
| 2B | Limit 1,024 vs LoRA-1 | 424 | 41.4% | 37.4% | +4.0 | [+0.1, +7.8] |
| 2B | Limit 1,024 vs Thinking OFF | 464 | 38.6% | 31.8% | +6.8 | [+3.2, +10.5] |
| 4B | Limit 2,048 vs Thinking ON | 464 | 71.9% | 50.0% | +21.9 | [+18.3, +25.5] |
| 4B | Limit 2,048 vs LoRA-1 | 424 | 74.3% | 59.3% | +15.0 | [+11.2, +18.8] |
| 4B | Limit 2,048 vs Thinking OFF | 464 | 71.9% | 66.5% | +5.4 | [+1.6, +9.1] |


## Reproduce and audit

Run `python3 scripts/combine_results.py`, then `python3 scripts/build_combined_easy_thesis.py`.
No GPU calls are made. Original graded files remain unchanged.

- [results.json](results.json): full metrics, 95% intervals, problem IDs, and training ID audit.
- [per-problem.csv](per-problem.csv): success fractions and token means before averaging.
- [sources.csv](sources.csv): the 66 exact input files and their original pass counts.
- [Easy thesis](../../easy-thesis/PAPER.md): reader-facing combined account.

Checked: 464 distinct IDs, disjoint collections, no duplicate method/problem/attempt rows,
and zero overlap with 280 saved training-pool IDs.
Original headline pass counts are reconciled before output is written.
Text similarity and pretraining exposure are not ruled out by this ID check.
Intervals resample problems 2,000 times with seed 3407; they are unadjusted percentile intervals.
Partial coverage is not imputed. Never rank a subset score against a full-set score.

## Completed extension: 2B LoRA-1 + limit 1,024

**41.2% accuracy — 191/464 passed. Coverage: 464/464, one attempt per problem.**
This uses Qwen3.5-2B and the existing LoRA-1 trained add-on.

On the same 464 first attempts, limit alone scores 38.6% (179/464).
The combination gains 2.6 points and uses 6.4% fewer total output tokens.
The 95% gap interval is −1.5 to +6.7 points. A reliable gain is not established.
On the 424 shared first attempts, the combination scores 43.9%, versus LoRA-1 alone at 38.0%.
That gain is 5.9 points, with an interval of +1.4 to +10.4.

Earlier tables use all attempts per problem; LoRA-1 alone is 37.4% under that rule.
Do not confuse that number with the 38.0% first-attempt reference.
The extension is retrospective, with historical references and unadjusted intervals.
It does not prove training universally beats free controls.

2B and 4B LoRA-1 alone still each miss the same extra 40 problems.
Only these two gaps are planned next: 80 new answers, no training or completed-run repeats.
Other partial methods retain their stated coverage.

Checked 14 October 2026. Source: [completed result](../lora-limit-2b/README.md).
Next: [missing-40 plan](../lora-missing40/PLAN.md).
