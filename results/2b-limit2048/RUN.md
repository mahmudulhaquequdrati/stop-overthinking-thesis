# How to run 2B · limit 2048 only (LEAN)

Question: on 2B, does accuracy keep rising after 1024?

We already have: limit512 = 45.1% · limit1024 = 49.8%.

## Cheap settings (few hours left)

| Save | Setting |
|---|---|
| ~½ cost | **1 try** (not 2) |
| No 8k waste | max tokens = **2048 + 1024** only |
| Loops | `--stop-on-repeat` |
| Scope | **limit2048 only** — no OFF/ON/LoRA/4096 |

## Steps

1. Copy to Drive: `notebooks/17_qwen35_2b_limit2048.ipynb`, `scripts/`, `results/shared/hours_budget.json`
2. Colab **A100** → open **17** → **Runtime → Run all**
3. Must see **`FAST PATH ON ✓`** (else ~40 tok/s — **stop**)
4. Zip Drive `results/2b-limit2048/` back to the laptop repo

## How to read the result

```text
if 2048%  > 49.8%  → still going up (like 4B)
if 2048%  < 49.8%  → 1024 was already the peak on 2B
```

Caption: **this run = 1 try**; main 2B numbers = 2 tries.

DECISIONS #83.
