# Size extension — status (DONE)

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

[Every method, benchmark, difficulty, token count and interval](CURRENT-RESULTS.md) · [Full easy thesis](../easy-thesis/FULL-THESIS.md) · [Full formal Markdown thesis](../thesis/THESIS.md).

<!-- CURRENT-STUDY:END -->

```text
✅ 4B  (notebook 15b)  → results/4b/
✅ 0.8B lean (notebook 15a) → results/0.8b/
✅ Join pages updated
```

**Read numbers here:** [RESULTS-INDEX.md](RESULTS-INDEX.md) · [SIZE-COMPARISON.md](SIZE-COMPARISON.md) · [ALL-RESULTS.md](ALL-RESULTS.md)

---

## What each run was

| | 4B | 0.8B (lean) |
|---|---|---|
| Problems | 234 | 234 |
| Tries | 2 | **1** |
| Ways | OFF · ON · lim 512/1024/2048/4096 · LoRA-1 | OFF · ON · lim 512/1024 · LoRA-1 |
| Best free | **limit 2048 → 78.2%** | **OFF → 20.5%** |
| LoRA-1 | 69.9% (loses to limits) | 17.9% (loses to OFF) |

## If you ever re-run

1. Drive copy of `scripts/` + notebook  
2. Colab A100 → **Run all**  
3. Need **`FAST PATH ON ✓`** (else ~40 tok/s — stop)  

| GPU | 4B batch | 0.8B batch |
|---|---|---|
| A100 80GB | 64 | 128 |
| A100 40GB | 32 | 64 |

Details: [4b/RUN.md](4b/RUN.md) · [0.8b/RUN.md](0.8b/RUN.md)
