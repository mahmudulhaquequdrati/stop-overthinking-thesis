# How to run the 0.8B Colab (SECOND) — Run all

## Before this

1. Finish **4B** ([../4b/RUN.md](../4b/RUN.md)).
2. Same Drive code mirror: `MyDrive/stop-overthinking/code/` (latest scripts).

## Every run

1. **New** Colab session → A100.
2. Open **`notebooks/15a_qwen35_0_8b.ipynb`**.
3. **Runtime → Run all.**  
   - Batch: **128 on 80GB**, **64 on 40GB**.  
   - Must see **`FAST PATH ON ✓`**.  
   - Shared hour ledger skips stages if the 150h pot is empty.
4. Results: `MyDrive/stop-overthinking/results/0.8b/`.

## After both runs (laptop)

```bash
python scripts/make_size_summary.py --dir results/4b/raw --run 4b --summary results/4b/SUMMARY.md
python scripts/make_size_summary.py --dir results/0.8b/raw --run 0.8b --summary results/0.8b/SUMMARY.md
python scripts/make_all_results.py
```
