# How to run the 0.8B Colab (do this SECOND)

1. Finish the **4B** run first ([../4b/RUN.md](../4b/RUN.md)), so hours left are known.
2. Open Google Colab → **Runtime → Change runtime type → A100** (separate session from 4B).
3. Open [`notebooks/15a_qwen35_0_8b.ipynb`](../../notebooks/15a_qwen35_0_8b.ipynb).
4. **Runtime → Run all.**
5. The notebook reads `results/shared/hours_budget.json` on Drive and **skips** stages that would pass 150 hours.
6. After it finishes, copy from Drive:
   `MyDrive/stop-overthinking/results/0.8b/` → this folder in the git repo.
7. On your laptop:
   ```bash
   python scripts/make_size_summary.py --dir results/0.8b/raw --run 0.8b --summary results/0.8b/SUMMARY.md
   python scripts/make_all_results.py
   ```

**Hard rules**
- Shared pot with 4B: **≤150 hours combined**.
- Suggested for 0.8B: ≤60 hours (whatever remains after 4B).
- Prefer cutting Stage C (second try) or even LoRA-1 on 0.8B before cutting 4B work.
- LoRA-1 only (no LoRA-2).

**Status:** notebook ready. GPU run = you on Colab.
