# How to run: size × limit extension

## Order

```text
1. Colab A100 → notebooks/15b_qwen35_4b.ipynb     (4B first)
2. Colab A100 → notebooks/15a_qwen35_0_8b.ipynb   (0.8B second, leftover hours)
3. Laptop     → copy Drive folders → make_size_summary + make_all_results
```

Details: [results/4b/RUN.md](4b/RUN.md) · [results/0.8b/RUN.md](0.8b/RUN.md)

## Shared budget

≤ **150 hours** for both. Ledger: `MyDrive/stop-overthinking/results/shared/hours_budget.json`

## Folders (do not mix)

| Path | What |
|---|---|
| `results/2026-09-24-thesis-run/` | 2B — **do not touch** |
| `results/4b/` | 4B only |
| `results/0.8b/` | 0.8B only |
| `results/ALL-RESULTS.md` | join page |

**GPU runs are on your Colab account.** This machine cannot start them.
