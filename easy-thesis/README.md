# Easy thesis — start here

This version presents **464 unique test problems** as one combined study view.
Accuracy gives every problem equal weight. Every method shows its actual coverage.

Start with [PAPER.md](PAPER.md) for a teacher-ready summary.
Read [FULL-THESIS.md](FULL-THESIS.md) for all chapters, or [00-one-page.md](00-one-page.md) for the short version.

- [Method](03-how-we-did-it.md): weighting, grading, and intervals.
- [Datasets](04-the-datasets.md): test and training counts.
- [Results](05-results.md): accuracy, tokens, coverage, and shared-problem comparisons.
- [Explanation](06-why-it-works.md): historical loop evidence, clearly scoped.
- [Limitations](07-advice-and-limits.md).
- [Questions](08-all-answers.md).
- [Collection history](09-extra-problems.md).
- [All counts](10-all-counts.md).
- [Words](WORDS.md).

The [formal thesis](../thesis/THESIS.md) preserves the original study.
Its historical scores differ from the retrospective combined analysis here.
The [combined audit](../results/combined/README.md) is the source for this version.

Rebuild from the project root:

```sh
python3 scripts/combine_results.py
python3 scripts/build_combined_easy_thesis.py
```

No model calls or Colab units are needed.

## Completed extension: 2B LoRA-1 + limit 1,024

**41.2% accuracy — 191/464 passed. Coverage: 464/464, one attempt per problem.**
This uses Qwen3.5-2B and the existing LoRA-1 trained add-on.

The missing40 LoRA-alone runs are complete: 2B passed 1/40; 4B passed 12/40.
Their all-attempt, equal-problem-weight scores now cover all 464:
**2B LoRA-1 alone 34.4%; 4B LoRA-1 alone 56.8%.**

On the same 464 first attempts, the 2B comparison is:
**LoRA + limit 41.2% (191/464), LoRA alone 34.9% (162/464), OFF 32.5% (151/464).**
The combination gains 6.2 points over LoRA alone, interval +2.4 to +10.1.
It gains 8.6 points over OFF, interval +4.5 to +12.9.
LoRA alone's 2.4-point lead over OFF is inconclusive: interval −1.7 to +6.7.
The combination uses 13.4% fewer output tokens than LoRA alone.
OFF uses 66.5% fewer output tokens than the combination.

Limit alone remains 38.6% (179/464). The combination gains 2.6 points,
interval −1.5 to +6.7. A reliable gain over the free limit is not established.

Earlier tables use all attempts per problem; 2B LoRA alone is 34.4% under that rule.
The 34.9% reference above uses first attempts, matching the combination's one attempt.
Archived 424-problem reports retain their original numbers as history.
The extension is retrospective, with historical references and unadjusted intervals.
No result proves a universal winner. Other incomplete methods retain their coverage.

Checked 14 October 2026. Source: [completed result](../results/lora-limit-2b/README.md).
Updated comparison: [missing40 results](../results/lora-missing40/README.md).
