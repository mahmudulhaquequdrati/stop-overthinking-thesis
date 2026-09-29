# How to run the 0.8B Colab — lean plan (≤50 compute hours)

## Why lean?

4B already used ~**100 Colab compute hours**. You have ~100 left and must keep **≥50**.  
So 0.8B gets **≤50**. We do **not** repeat the full 4B menu.

## What we test (enough, not too much)

```text
Same 234 problems
  OFF
  ON
  limit 512
  limit 1024
  limit 2048     ← 4B's best was 2048; keep neighbours too
  LoRA-1         ← teacher: did training help?
1 try only
NO Stage C (no second try)
NO limit 4096
```

| Keep | Drop |
|---|---|
| OFF, ON | second try (Stage C) |
| limits 512 / 1024 / 2048 | limit 4096 |
| LoRA-1 | “think briefly” |

## Steps

1. Copy to Drive: `notebooks/15a_qwen35_0_8b.ipynb`, `scripts/`, and `results/shared/hours_budget.json`
2. Colab A100 → open **15a** → **Runtime → Run all**
3. Wait for **`FAST PATH ON ✓`**
4. When DONE, copy Drive `results/0.8b/` into the repo and run `make_all_results.py`

## What a teacher gets from this

- Smaller size vs 2B / 4B  
- Which free limit wins on 0.8B  
- Whether LoRA-1 beats those free ways  

DECISIONS #74.
