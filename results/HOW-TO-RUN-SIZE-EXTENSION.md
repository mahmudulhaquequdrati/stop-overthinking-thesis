# Size extension — status (DONE)

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
