# 4B run — what happened

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

**Checked** from Drive zip / graded files (2026-09-29).  
Same **234** problems · **2 tries** · limits **512 / 1024 / 2048 / 4096** · LoRA-1 · Stage C included (DECISIONS #72–73).

## Main table

| Way | Accuracy | Thinking | All tokens | Cut off |
|---|---|---|---|---|
| OFF | 69.7% | 0 | 720 | 4% |
| ON | 64.3% | 2938 | 3096 | 28% |
| limit512 | 75.4% | 481 | 2168 | 17% |
| limit1024 | 76.5% | 763 | 2185 | 17% |
| **limit2048** | **78.2%** (best) | 1178 | 2448 | 15% |
| limit4096 | 76.7% | 1915 | 2821 | 17% |
| LoRA-1 | 69.9% | 2565 | 2732 | 22% |

## Plain story

```text
4B is much stronger than 2B overall.
ON still loses to OFF (loops / cut-offs).
Best free way = limit 2048 (not 1024 — best limit moved up with size).
LoRA-1 beats ON a bit, but loses to every limit and to OFF.
```

Wall hours on shared ledger ~**8.5**; user reported ~**100 Colab compute hours** for this run.

Raw: `results/4b/raw/` · Join: [SIZE-COMPARISON.md](../SIZE-COMPARISON.md)

---

## How this notebook was run (if you re-run)

1. Colab A100 → open `notebooks/15b_qwen35_4b.ipynb` → **Run all**  
2. Need **`FAST PATH ON ✓`**  
3. Results → Drive `results/4b/`
