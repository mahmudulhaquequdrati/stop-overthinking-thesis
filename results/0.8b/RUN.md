# 0.8B run — what happened (lean plan)

<!-- CURRENT-STUDY:START -->

**Historical record below.** Its earlier scores, model choices and plans describe that stage only.
Use the current results linked here for the completed study.

**Current study — 14 October 2026:** **464 unique test problems**.
Benchmarks: **164 HumanEval+**, **166 LiveCodeBench easy**, **134 LiveCodeBench medium**.
All six planned LoRA combinations are complete, one attempt per problem:

- **0.8B:** LoRA + OFF **14.0% (65/464)**; LoRA + limit 512 **14.4% (67/464)**.
- **2B:** LoRA + OFF **35.6% (165/464)**; LoRA + limit 1,024 **41.2% (191/464)**.
- **4B:** LoRA + OFF **64.7% (300/464)**; LoRA + limit 2,048 **71.6% (332/464)**.

LoRA alone means thinking ON without a thinking-token limit.
Older methods' all-attempt averages and first-attempt comparisons are labelled separately.
LoRA + OFF does not consistently improve on free OFF; the 2B/4B gains over free limits remain uncertain.

[Every method, benchmark, difficulty, token count and interval](../CURRENT-RESULTS.md) · [Full easy thesis](../../easy-thesis/FULL-THESIS.md) · [Full formal Markdown thesis](../../thesis/THESIS.md).

<!-- CURRENT-STUDY:END -->

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
