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
