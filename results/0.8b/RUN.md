# 0.8B run — what happened (lean plan)

**Checked** from Drive zip `0.8b-20260929T143603Z-1-001.zip` (2026-09-29).  
Same **234** problems · **1 try** · limits **512 / 1024** only · LoRA-1 · no Stage C (DECISIONS #75–76).

## Main table

| Way | Accuracy | Thinking | All tokens | Cut off |
|---|---|---|---|---|
| **OFF** | **20.5%** (best) | 0 | 1118 | 12% |
| ON | 7.3% | 4509 | 4557 | 78% |
| limit512 | 17.5% | 509 | 4198 | 68% |
| limit1024 | 13.2% | 969 | 4299 | 69% |
| LoRA-1 | 17.9% | 3472 | 3627 | 55% |

## Plain story

```text
0.8B is too small to “think well” on these code tests.

ON    → loops / hits the wall a lot (78% cut off) → only 7.3%
limit → better than ON, but still weak
LoRA  → a bit better than limits, still loses to OFF
OFF   → best accuracy, cheapest thinking (0 tokens)
```

So on **0.8B**, the free winner is **thinking OFF**, not a length limit.  
That is different from **2B** (best = limit 1024) and **4B** (best = limit 2048).

## Hours

Zip had no `hours_budget.json`. Wall time from Colab file times ≈ **~3 hours** (smoke → SUMMARY). Ledger updated with that estimate.

Raw files: `results/0.8b/raw/` · Rebuild SUMMARY: `python scripts/make_size_summary.py --dir results/0.8b/raw --run 0.8b --summary results/0.8b/SUMMARY.md`
