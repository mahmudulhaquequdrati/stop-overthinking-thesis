# Completed extension: 2B LoRA-1 + thinking limit 1,024

Checked on 14 October 2026 from the user's completed ZIP.
Model: Qwen3.5-2B, with the existing LoRA-1 trained add-on.
A token is a small piece of text. The limit applies to thinking, not the whole answer.

**Accuracy: 41.2% — 191/464 passed. Coverage: 464/464. One attempt per problem.**
HumanEval+: 99/164 (60.4%). LiveCodeBench: 92/300 (30.7%).
All 464 frozen IDs have one answer and one grade. No duplicate attempts or missing grades.
There is no exact-ID overlap with saved training IDs.

## Compare the same problems and first attempts

- Limit 1,024 alone: **38.6% (179/464)**. Combination: **41.2% (191/464)**.
  Gap: **+2.6 percentage points**. 95% gap interval: **−1.5 to +6.7**.
  Average output tokens: **4,072 versus 4,348**, or **6.4% fewer**.
  This interval includes zero. A reliable gain over the limit alone is not established.
- LoRA-1 alone: **38.0% (161/424)** on its 424 saved first attempts.
  Combination on those same 424: **43.9% (186/424)**.
  Gap: **+5.9 points**, interval **+1.4 to +10.4**.
  Average output tokens: **3,764 versus 4,408**, or **14.6% fewer**.
- Thinking OFF: **32.5% (151/464)**. Gap: **+8.6 points**, interval **+4.5 to +12.9**.
- Normal thinking ON: **26.1% (121/464)**. Gap: **+15.1 points**, interval **+10.8 to +19.2**.

Intervals compare shared problems, with 2,000 resamples and seed 3407. They are unadjusted.
Saved references are historical. Package versions and batch layouts differ.
This is a retrospective extension on an existing test set, not a new held-out exam.

## Why older numbers differ

The earlier combined analysis averages all attempts within each problem.
It reports 2B LoRA-1 as **37.4% on 424 problems**.
The **38.0%** comparison here uses only its first attempts.
Keep those two summaries labelled. Neither is a recalculation error.
The new combination has one attempt per problem, so both weighting rules give 41.2%.
Do not compare its full-set score directly with a subset score.

## Cost and saved evidence

The v2 ledger records **20.51 estimated units**, under its 45-unit ceiling.
It covers recorded revised-workflow usage, not just successful generation.
The original failed attempt and logs remain historical evidence.
188 answers reached their overall output cap; the grader still decided whether code passed.

- [Notebook report](completed-464/SUMMARY.md)
- [Machine-readable summary](completed-464/summary.json)
- [Run settings and adapter hash](completed-464/run-config.json)
- [Compute ledger](completed-464/compute-ledger-v2.json)
- Raw answers, grades, environment records, and logs: `completed-464/`.
- Source ZIP: `lora-limit-2b-20261013T212216Z-1-001.zip`.
  Its SHA-256 is recorded in [the missing-40 plan](../lora-missing40/plan-manifest.json).

The report's grades, token counts, reference-source hashes, shared IDs, and gap intervals were reconciled locally.
No new GPU generation was needed for this check.
