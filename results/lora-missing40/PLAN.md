# Plan: fill only the missing LoRA-1 results

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
[Updated results and both weighting rules](../lora-missing40/README.md).


Status: COMPLETE. Both 40 runs checked and combined; do not rerun Notebook 22. Updated 14 October 2026.
The completed 2B LoRA-1 + limit 1,024 result is **41.2% (191/464)**.
See [the saved result](../lora-limit-2b/README.md).

## Historical pre-run gaps (the2B/4B LoRA-1 extra40 gaps are now filled)

The frozen test set is 464 IDs: original 234, extra 40, and later 190.
These collections are disjoint. Missing results are not failures.

- **0.8B:** LoRA-1, OFF, ON, and limit512 cover all 464.
  Alternative limit1024 misses the later 190 (coverage 274).
- **2B:** LoRA-1 misses exactly the extra 40 (coverage 424).
  OFF, ON, limit1024, and the new LoRA-1 + limit1024 cover all 464.
  Alternatives brief, limit512, and limit2048 miss the later 190 (coverage 274).
  LoRA-2 misses the extra 40 and later 190 (coverage 234).
- **4B:** LoRA-1 misses exactly the extra 40 (coverage 424).
  OFF, ON, and limit2048 cover all 464.
  Alternatives limit512, limit1024, and limit4096 miss 230 (coverage 234).
  A 4B LoRA + limit combination has not been tested and is outside this plan.

Only the 2B and 4B LoRA-1 gaps will be filled.
Other gaps remain labelled with their coverage. They are outside the user's chosen scope.
Their subset scores do not prove they are worse on all 464 problems.

## Why and what we will test

Question: how does LoRA-1 alone compare with the free controls over all 464?
We will complete existing evidence, not choose new questions after seeing results.
The changed setting is the trained add-on, with ordinary thinking and no 1,024 cap.
Measure whether generated code passes the saved tests, plus output-token use.
Compare 2B with limit1024 and 4B with limit2048, using identical IDs.
A higher LoRA score supports it on this set; a lower score favors the control.
Report uncertainty even when the score improves.

## Run plan: 80 new answers total

1. Use [Notebook 22](../../notebooks/22_lora1_missing40_2b_4b.ipynb), following notebooks18–21.
   Use the existing adapters. No training, alternative limits, or combination rerun.
2. Read [plan-manifest.json](plan-manifest.json), containing the exact 40 frozen IDs.
   Confirm each model has 424 existing LoRA-1 IDs and exactly these 40 missing IDs.
   Assert there is no overlap with training IDs or the original/later test collections.
3. Check both adapter paths and hashes before paid generation.
   Reuse the successful package and kernel setup from Notebook 21.
   Check CPU adapter compatibility before loading each base model.
4. Run **2B LoRA-1 alone: 40 problems, one attempt each**, seed 3407.
   Match the earlier LoRA-alone prompts, sampling, and model-specific output caps.
5. Unload 2B, then run **4B LoRA-1 alone: the same 40, one attempt each**.
   Match the earlier 4B configuration, including its repeat-stopping setting.
   Record package versions and batch layout; a matching seed is not identical sampling.
6. Save each answer immediately. On resume, subtract saved raw-answer IDs too.
   Skip already generated answers; grade saved answers without regenerating them.
   Reject duplicate IDs, changed run settings, or changed adapters.
7. Grade against the same saved tests and check 40/40 coverage for each model.
   Stop and label a partial run if a model is incomplete. Never count missing rows as failures.
8. Save the two new result sets separately and release the GPU after saving.
   Measure speed from the first saved batch, which counts toward the 40.
   Use a separate budget ledger and a predeclared ceiling; do not inherit 45 units as new spending permission.
   Notebook 22 uses a separate **20-unit total estimated ceiling**, including setup and resumes.
   Enter the current rate and balance. Stop when done; the ceiling is not a spending target.

This repeats the same questions across different methods by design.
It does not repeat any completed **model + LoRA-1-alone + problem** attempt.
The combination already answered these 40, but that is a different method.
Do not rerun the existing 424 answers, the free controls, or Notebook 21.

## After both result sets arrive

Validate IDs, sample indices, adapter hashes, duplicate attempts, and grade coverage.
Then combine existing 424 results with new 40 results: **464 per model**.
Use all saved attempts, averaging within problems before averaging problems equally.
Also update first-attempt comparisons separately to match the new combination.
Recalculate paired uncertainty and token means on identical shared IDs.

Update the easy-thesis chapters, paper, full version, one-page summary, charts,
combined results, result index, and project notes together.
Do not invent the missing-40 score or a new combined score before results arrive.
Preserve the formal thesis and all original raw files.

The frozen manifest was checked against all saved graded results.
For each model, its missing IDs are exactly the original extra-40 collection.

## Ready notebook and local checks

[Notebook 22](../../notebooks/22_lora1_missing40_2b_4b.ipynb) is19.2KB with readable cells.
Push the notebook, both new scripts, and this manifest before opening the latest Colab copy.
The notebook requires the original2B Drive adapter;4B weights are already in the project.
Both adapter hashes are checked before package installation.

Eleven offline checks pass in the project Python environment.
They cover frozen-ID/source checks, training exclusions, resume skipping, duplicate/settings rejection,
skipping GPU loading when all answers exist, independent grade resume, and honest failure reports.
The earlier thirteen Notebook21 checks still pass. Code cells compile.
Actual2B/4B inference in this new notebook has not been run locally.
