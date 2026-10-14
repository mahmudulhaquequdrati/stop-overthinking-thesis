# Combined results: 464 unique problems

Retrospective presentation chosen 13 October 2026; results updated 14 October 2026. Equal weight per problem.
Main complete-coverage controls: **0.8B: Thinking OFF 14.7%** · **2B: Limit 1,024 38.6%** · **4B: Limit 2,048 71.9%**

Coverage means unique problems with results. A missing result is not counted as a failure. Only compare scores directly when they use the same problems.

| Model | Way | Accuracy | Coverage | Attempts |
|---|---|---|---|---|
| 0.8B | Limit 1,024 | 11.3% | 274/464 | 274 |
| 0.8B | Limit 512 | 10.6% | 464/464 | 464 |
| 0.8B | LoRA-1 | 12.3% | 464/464 | 464 |
| 0.8B | LoRA-1 + limit 512 | 14.4% | 464/464 | 464 |
| 0.8B | LoRA-1 + OFF | 14.0% | 464/464 | 464 |
| 0.8B | Thinking OFF | 14.7% | 464/464 | 464 |
| 0.8B | Thinking ON | 4.1% | 464/464 | 464 |
| 2B | Think briefly | 6.4% | 274/464 | 548 |
| 2B | Limit 1,024 | 38.6% | 464/464 | 738 |
| 2B | Limit 2,048 | 40.9% | 274/464 | 274 |
| 2B | Limit 512 | 39.4% | 274/464 | 548 |
| 2B | LoRA-1 | 34.4% | 464/464 | 698 |
| 2B | LoRA-1 + limit 1,024 | 41.2% | 464/464 | 464 |
| 2B | LoRA-1 + OFF | 35.6% | 464/464 | 464 |
| 2B | LoRA-2 | 45.1% | 234/464 | 468 |
| 2B | Thinking OFF | 31.8% | 464/464 | 738 |
| 2B | Thinking ON | 26.8% | 464/464 | 738 |
| 4B | Limit 1,024 | 76.5% | 234/464 | 468 |
| 4B | Limit 2,048 | 71.9% | 464/464 | 738 |
| 4B | Limit 4,096 | 76.7% | 234/464 | 468 |
| 4B | Limit 512 | 75.4% | 234/464 | 468 |
| 4B | LoRA-1 | 56.8% | 464/464 | 698 |
| 4B | LoRA-1 + limit 2,048 | 71.6% | 464/464 | 464 |
| 4B | LoRA-1 + OFF | 64.7% | 464/464 | 464 |
| 4B | Thinking OFF | 66.5% | 464/464 | 738 |
| 4B | Thinking ON | 50.0% | 464/464 | 738 |


## Shared-problem comparisons

| Model | Way vs reference | Shared problems | Way accuracy | Reference accuracy | Gap (points) | 95% gap interval |
|---|---|---|---|---|---|---|
| 0.8B | Thinking OFF vs Thinking ON | 464 | 14.7% | 4.1% | +10.6 | [+7.5, +13.8] |
| 0.8B | Thinking OFF vs LoRA-1 | 464 | 14.7% | 12.3% | +2.4 | [-0.4, +5.2] |
| 2B | Limit 1,024 vs Thinking ON | 464 | 38.6% | 26.8% | +11.7 | [+8.5, +15.1] |
| 2B | Limit 1,024 vs LoRA-1 | 464 | 38.6% | 34.4% | +4.2 | [+0.8, +7.8] |
| 2B | Limit 1,024 vs Thinking OFF | 464 | 38.6% | 31.8% | +6.8 | [+3.2, +10.5] |
| 4B | Limit 2,048 vs Thinking ON | 464 | 71.9% | 50.0% | +21.9 | [+18.3, +25.5] |
| 4B | Limit 2,048 vs LoRA-1 | 464 | 71.9% | 56.8% | +15.1 | [+11.3, +19.0] |
| 4B | Limit 2,048 vs Thinking OFF | 464 | 71.9% | 66.5% | +5.4 | [+1.6, +9.1] |
| 0.8B | LoRA-1 + limit 512 vs Limit 512 | 464 | 14.4% | 10.6% | +3.9 | [+0.6, +7.1] |
| 0.8B | LoRA-1 + limit 512 vs LoRA-1 | 464 | 14.4% | 12.3% | +2.2 | [-0.4, +5.0] |
| 0.8B | LoRA-1 + limit 512 vs Thinking OFF | 464 | 14.4% | 14.7% | -0.2 | [-3.0, +3.0] |
| 0.8B | LoRA-1 + OFF vs Thinking OFF | 464 | 14.0% | 14.7% | -0.6 | [-3.2, +2.2] |
| 0.8B | LoRA-1 + OFF vs LoRA-1 | 464 | 14.0% | 12.3% | +1.7 | [-0.9, +4.5] |
| 2B | LoRA-1 + limit 1,024 vs Limit 1,024 | 464 | 41.2% | 38.6% | +2.6 | [-1.4, +6.5] |
| 2B | LoRA-1 + limit 1,024 vs LoRA-1 | 464 | 41.2% | 34.4% | +6.8 | [+2.9, +10.7] |
| 2B | LoRA-1 + limit 1,024 vs Thinking OFF | 464 | 41.2% | 31.8% | +9.4 | [+5.4, +13.5] |
| 2B | LoRA-1 + OFF vs Thinking OFF | 464 | 35.6% | 31.8% | +3.8 | [+0.2, +7.3] |
| 2B | LoRA-1 + OFF vs LoRA-1 | 464 | 35.6% | 34.4% | +1.2 | [-2.6, +5.1] |
| 4B | LoRA-1 + limit 2,048 vs Limit 2,048 | 464 | 71.6% | 71.9% | -0.3 | [-3.7, +2.8] |
| 4B | LoRA-1 + limit 2,048 vs LoRA-1 | 464 | 71.6% | 56.8% | +14.8 | [+10.8, +19.0] |
| 4B | LoRA-1 + limit 2,048 vs Thinking OFF | 464 | 71.6% | 66.5% | +5.1 | [+0.9, +9.2] |
| 4B | LoRA-1 + OFF vs Thinking OFF | 464 | 64.7% | 66.5% | -1.8 | [-5.4, +1.6] |
| 4B | LoRA-1 + OFF vs LoRA-1 | 464 | 64.7% | 56.8% | +7.9 | [+3.6, +12.2] |


## Reproduce and audit

Run `python3 scripts/combine_results.py`, then `python3 scripts/build_combined_easy_thesis.py`.
No GPU calls are made. Original graded files remain unchanged.

- [results.json](results.json): full metrics, 95% intervals, problem IDs, and training ID audit.
- [per-problem.csv](per-problem.csv): success fractions and token means before averaging.
- [sources.csv](sources.csv): the 80 exact input files and their original pass counts.
- [Easy thesis](../../easy-thesis/PAPER.md): reader-facing combined account.

Checked: 464 distinct IDs, disjoint collections, no duplicate method/problem/attempt rows,
and zero overlap with 280 saved training-pool IDs.
Original headline pass counts are reconciled before output is written.
Text similarity and pretraining exposure are not ruled out by this ID check.
Intervals resample problems 2,000 times with seed 3407; they are unadjusted percentile intervals.
Partial coverage is not imputed. Never rank a subset score against a full-set score.

## Completed combinations

| Model | Combination | Passed | Coverage | Accuracy | 95% interval | Mean total tokens |
|---|---|---|---|---|---|---|
| 0.8B | LoRA-1 + OFF | 65 | 464/464 | 14.0% | [11.0%, 17.0%] | 1,278 |
| 0.8B | LoRA-1 + limit 512 | 67 | 464/464 | 14.4% | [11.2%, 17.5%] | 4,979 |
| 2B | LoRA-1 + OFF | 165 | 464/464 | 35.6% | [31.2%, 39.7%] | 1,445 |
| 2B | LoRA-1 + limit 1,024 | 191 | 464/464 | 41.2% | [36.6%, 45.7%] | 4,072 |
| 4B | LoRA-1 + OFF | 300 | 464/464 | 64.7% | [59.9%, 69.0%] | 882 |
| 4B | LoRA-1 + limit 2,048 | 332 | 464/464 | 71.6% | [67.5%, 75.6%] | 3,511 |

### What the completed tests show

- **0.8B:** LoRA + OFF passes 65/464 (14.0%); LoRA + limit 512 passes 67/464 (14.4%).
  OFF without LoRA passes 68/464 (14.7%). There is no clear gain over OFF.
  LoRA + limit improves on the matching free limit by 3.9 points, interval +0.6 to +7.1.
- **2B:** LoRA + OFF passes 165/464 (35.6%); LoRA + limit 1,024 passes 191/464 (41.2%).
  The limit combination beats LoRA + OFF by 5.6 points, interval +1.1 to +9.9.
  Its 2.6-point gain over limit alone remains uncertain, interval −1.5 to +6.7.
- **4B:** LoRA + OFF passes 300/464 (64.7%); LoRA + limit 2,048 passes 332/464 (71.6%).
  Limit alone passes 330/464 (71.1%). The two-pass gain is inconclusive,
  interval −3.0 to +3.7 points. The combination uses about 11.4% fewer output tokens.

These are same-problem, first-attempt comparisons with historical references.
Intervals are unadjusted for multiple comparisons. They are not proof of universal wins.
Shorter output does not directly establish lower GPU time, energy, or money.

Full first-attempt and benchmark tables: [easy thesis](../../easy-thesis/05-results.md).
