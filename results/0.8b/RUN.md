# How to run the 0.8B Colab — lean plan (≤50 compute hours)

## Why lean?

4B already used ~**100 Colab compute hours**. You have ~100 left and must keep **≥50**.  
So 0.8B gets **≤50**. We do **not** repeat the full 4B menu.

## What we test

```text
Same 234 problems
  OFF
  ON
  limit 512
  limit 1024     ← max (won on 2B at 49.8%)
  LoRA-1
1 try only
NO Stage C
NO limit 2048 / 4096
```

| Keep | Drop |
|---|---|
| OFF, ON | second try (Stage C) |
| limits 512 / 1024 | limits 2048, 4096 |
| LoRA-1 | “think briefly” |

**Why max 1024?** On 2B, limit 1024 was the best free way (49.8%). 0.8B is smaller, so it does not need a longer thinking budget. 4B already answered “2048 can win on a bigger model”.

## Steps

1. Copy to Drive: `notebooks/15a_qwen35_0_8b.ipynb`, `scripts/`, and `results/shared/hours_budget.json`
2. Colab A100 → open **15a** → **Runtime → Run all**
3. Wait for **`FAST PATH ON ✓`**
4. When DONE, copy Drive `results/0.8b/` into the repo and run `make_all_results.py`

DECISIONS #75.
