# How to run 2B · limit 512 only

Fills the empty cell: **2B × Limit 512** in the size table.  
**Not** 2048. **Not** OFF/ON/LoRA. Same 234 problems · **2 tries**.

## Steps

1. Copy to Drive: `notebooks/16_qwen35_2b_limit512.ipynb`, `scripts/`, and `results/shared/hours_budget.json`
2. Colab **A100** → open **16** → **Runtime → Run all**
3. Wait for **`FAST PATH ON ✓`**
4. When DONE, copy Drive `results/2b-limit512/` into the laptop repo
5. We then put the % into SIZE-COMPARISON / ALL-RESULTS / thesis §5.13

## Output files

```text
results/2b-limit512/
  SUMMARY.md
  raw/
    test-limit512-he.jsonl (+ graded.csv)
    test-limit512-lcb.jsonl (+ graded.csv)
    smoke/
```

Does **not** write into `results/2026-09-24-thesis-run/`.

DECISIONS #81.
