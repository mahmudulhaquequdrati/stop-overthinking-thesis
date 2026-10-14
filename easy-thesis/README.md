# Easy thesis — start here

This version presents **464 unique test problems** as one combined study view.
Accuracy gives every problem equal weight. Every method shows its actual coverage.
The completed LoRA + OFF and LoRA + limit results are included for all three sizes.

Start with [PAPER.md](PAPER.md) for a teacher-ready summary.
Read [FULL-THESIS.md](FULL-THESIS.md) for all chapters, including every benchmark table, or [00-one-page.md](00-one-page.md) for the short version.

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
.venv/bin/python scripts/audit_lora_controls.py
python3 scripts/combine_results.py
python3 scripts/build_combined_easy_thesis.py
```

No model calls or Colab units are needed.

## Completed LoRA controls

All six combinations are complete, with 464/464 results each.
0.8B: LoRA + OFF **14.0%**, LoRA + limit 512 **14.4%**.
2B: LoRA + OFF **35.6%**, LoRA + limit 1,024 **41.2%**.
4B: LoRA + OFF **64.7%**, LoRA + limit 2,048 **71.6%**.
These use one attempt per problem. Historical controls also have a labelled
first-attempt comparison; their all-attempt scores remain separate.
See [the completed analysis](11-completed-lora-controls.md) and [benchmark tables](05-results.md).
