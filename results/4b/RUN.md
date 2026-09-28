# How to run the 4B Colab (do this FIRST)

1. Open Google Colab → **Runtime → Change runtime type → A100** (or H100).
2. Upload or open [`notebooks/15b_qwen35_4b.ipynb`](../../notebooks/15b_qwen35_4b.ipynb).
   - Or clone the repo in Colab (the notebook does this in step 2).
3. **Runtime → Run all.**
4. When asked, press Enter (the shared hour ledger on Drive is the real budget).
5. Let it finish: smoke → Stage A (limits) → Stage B (LoRA-1) → Stage C if hours remain.
6. After it finishes, copy from Drive:
   `MyDrive/stop-overthinking/results/4b/` → this folder in the git repo.
7. On your laptop:
   ```bash
   python scripts/make_size_summary.py --dir results/4b/raw --run 4b --summary results/4b/SUMMARY.md
   python scripts/make_all_results.py
   ```

**Hard rules**
- Shared pot with 0.8B: **≤150 hours combined**.
- Suggested for 4B: ≤90 hours.
- Do **not** write into `results/thesis/` (that is the finished 2B run).
- LoRA-1 only (no LoRA-2).

**Status:** notebook ready. GPU run = you on Colab.
