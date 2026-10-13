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

Checked 14 October 2026. Source: [completed result](../results/lora-limit-2b/README.md).
Next: [missing-40 plan](../results/lora-missing40/PLAN.md).
