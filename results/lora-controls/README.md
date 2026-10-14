# Completed LoRA controls — 464 problems per configuration

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

[Every method, benchmark, difficulty, token count and interval](../CURRENT-RESULTS.md) · [Full easy thesis](../../easy-thesis/FULL-THESIS.md) · [Full formal Markdown thesis](../../thesis/THESIS.md).

<!-- CURRENT-STUDY:END -->

Checked 14 October 2026 from `lora-controls-download.zip`.
All five Notebook 24 configurations are complete: 2,320 answers and grades.
No model or generated answer was run during this local update.
Original ZIP contents are preserved under [completed-464/](completed-464/).
Archive hash, run settings and recomputed comparisons are in [checked-results.json](checked-results.json).
The frozen input manifest retains its historical pre-run status; it is not the completion record.

## Results

Each row below has one attempt on each of the same 464 problems.

| Model | Combination | Passed / tested | Accuracy |
|---|---|---|---|
| 0.8B | LoRA-1 + OFF | 65/464 | 14.0% |
| 0.8B | LoRA-1 + limit 512 | 67/464 | 14.4% |
| 2B | LoRA-1 + OFF | 165/464 | 35.6% |
| 4B | LoRA-1 + limit 2,048 | 332/464 | 71.6% |
| 4B | LoRA-1 + OFF | 300/464 | 64.7% |

The earlier [2B LoRA-1 + limit 1,024](../lora-limit-2b/README.md) remains 191/464, **41.2%**.
“LoRA alone” means thinking ON without a thinking-token limit.
These are Qwen3.5 models, not LLaMA models.

## What the comparisons support

0.8B LoRA + limit improves on limit alone, but does not beat OFF without LoRA.
The latter passes 68/464 (14.7%).
2B LoRA + limit passes 26 more problems than LoRA + OFF.
The difference is +5.6 points, with a 95% interval of +1.1 to +9.9.
Its +2.6-point lead over the free limit remains inconclusive: −1.5 to +6.7.
4B LoRA + limit passes two more problems than limit alone (332 versus 330).
Its +0.4-point lead remains inconclusive: −3.0 to +3.7.
It uses about 11.4% fewer total output tokens than that first-attempt reference.
LoRA + OFF does not consistently improve accuracy over OFF without LoRA.

These comparisons use first attempts, paired on identical problem IDs.
Intervals resample problems 2,000 times with seed 3407 and are unadjusted.
The references are historical; packages and batch layouts can affect samples.
The collection and analysis are retrospective, not a new pre-registered exam.

## All benchmarks and scoring rules

The [complete easy-thesis results](../../easy-thesis/05-results.md) include:

- Every configuration's accuracy, attempts, coverage, uncertainty and output length.
- HumanEval+ (164 problems), LiveCodeBench easy (166), and medium (134).
- All-attempt problem averages and separately labelled first-attempt comparisons.
- The earlier partial limit sweeps, LoRA-2, pilot and loop findings with their actual scope.

The [combined data](../combined/results.json) now include the six completed combinations.
Old methods still use all saved attempts, with equal weight for every problem.
The 34.4% versus 34.9% 2B LoRA scores reflect those different scoring rules.
Missing methods or attempts are never counted as failures.

## Checks and compute

Checked: no duplicate attempts; 464 frozen IDs per configuration; no training ID overlap;
expected model, thinking settings and adapter hashes; one grade per raw answer;
raw/graded token agreement; original reference hashes; and recalculated intervals.
The saved benchmark grades were inspected, rather than re-executed here.
Exact ID checks cannot rule out related wording or pretraining exposure.

Notebook 24's saved ledger estimates **56.996 units**, with A100 80GB at 6.77 units/hour.
The entered cumulative ceiling was 80 units; two sessions are recorded.
This is an estimate, not a bill or a compute-hour balance.
It excludes the earlier Notebook 21 experiment and other project work.
This local audit and document rebuild use no Colab units.

## Reproduce

```sh
.venv/bin/python scripts/audit_lora_controls.py
python3 scripts/combine_results.py
python3 scripts/build_combined_easy_thesis.py
```

No rerun of Notebook 21, 22, 23 or 24 is needed for these completed configurations.
