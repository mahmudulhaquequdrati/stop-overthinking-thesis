# Completed missing40 and full464 LoRA results

Checked 14 October 2026. Both runs finished, with one attempt per extra problem.

- **2B LoRA-1 extra40: 2.5% (1/40).**
- **4B LoRA-1 extra40: 30.0% (12/40).**

These were the exact missing IDs. Neither run repeated the existing 424 LoRA-alone IDs.
Both adapter/config hashes matched the frozen manifest.
Raw answers and grades match on task IDs, token counts, and sample indices.
All 464 test IDs remain separate from 280 saved training-pool IDs.

## Full 464 results using the thesis rule

Average passing attempts within each problem, then average problems equally.
Keep every saved attempt. Do not give two-attempt problems twice the weight.

- **2B LoRA-1 alone: 34.4%, coverage 464/464, 698 saved attempts.**
  95% accuracy interval: 30.3% to 38.4%.
- **4B LoRA-1 alone: 56.8%, coverage 464/464, 698 saved attempts.**
  95% accuracy interval: 52.5% to 61.0%.

The old 424 coverage is now historical. These percentages are problem-weighted scores,
not pooled passing-answer counts divided by 698.
All combined tables, shared-problem comparisons, and charts were recalculated.

## Which 2B method is better? Same 464 first attempts

First attempts give a consistent one-attempt comparison with the new combination.

- **LoRA-1 + limit1024: 41.2% (191/464).** Average output: 4,072 tokens.
- **LoRA-1 alone: 34.9% (162/464).** Average output: 4,701 tokens.
- **Thinking OFF: 32.5% (151/464).** Average output: 1,366 tokens.
- For context, **limit1024 alone: 38.6% (179/464).** Average output: 4,348 tokens.

The combination has the highest observed accuracy among the three requested methods.
Versus LoRA alone: **+6.2 percentage points**, 95% gap interval **+2.4 to +10.1**.
The exact unrounded gap is 6.25 points; displayed gaps use the project's rounding rule.
It uses **13.4% fewer output tokens** than LoRA alone.
Versus OFF: **+8.6 points**, interval **+4.5 to +12.9**.

LoRA alone versus OFF: **+2.4 points**, interval **−1.7 to +6.7**.
That interval includes zero; LoRA alone's smaller lead remains inconclusive.
OFF uses about **66.5% fewer output tokens than the combination**.
So the combination leads in observed accuracy; OFF is cheapest by output-token count.
Token counts are not a direct bill or elapsed-time measurement.

Versus limit alone, the combination gains 2.6 points, interval −1.5 to +6.7.
That gain remains inconclusive. Do not claim a reliable win over the free limit.

## Keeping weighting rules clear

Under the all-attempt, equal-problem-weight rule, the same 2B ranking is:
**combination 41.2% > LoRA alone 34.4% > OFF 31.8%**.
All three cover 464. The combination still has only one attempt per problem.
Its gaps are +6.8 points versus LoRA alone (interval +2.9 to +10.7),
and+9.4 versus OFF (interval +5.4 to +13.5).
The first-attempt comparisons above are the main extension comparison.
The old report comparing LoRA on 424 remains archived as run-time history.

This is retrospective, with historical references and differing package/batch environments.
Intervals resample problems 2,000 times with seed 3407 and are unadjusted.
These findings apply to this test set; they do not establish a universal winner.

## Evidence and rebuilding

[comparison-2b-464.json](comparison-2b-464.json) holds both weighting rules and intervals.
[archive-provenance.json](archive-provenance.json) records the supplied ZIP hash.
`completed40/` preserves the original ZIP contents, settings, environment, and logs.
Canonical extra40 answers/grades are added under `results/extra/2b/` and `4b/`.
Original234 and190 results remain unchanged.
The recorded missing40 ledger is **5.14 estimated units**, below its 20-unit ceiling.

Run locally, with no GPU generation:

```sh
python3 scripts/combine_results.py
python3 scripts/compare_2b_completed.py
python3 scripts/build_combined_easy_thesis.py
```

Do not rerun Notebook 22. The missing40 work is complete.
Other incomplete methods remain outside the agreed scope.
