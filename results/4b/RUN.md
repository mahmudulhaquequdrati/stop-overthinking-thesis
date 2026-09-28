# How to run the 4B Colab (FIRST) — Run all

## One-time setup (laptop → Drive)

So Colab gets the **latest** scripts (not an old GitHub clone):

1. Copy this whole repo folder to Google Drive as:

```text
MyDrive/stop-overthinking/code/
   ├── scripts/
   ├── notebooks/
   ├── data/   (optional; notebook can rebuild)
   └── …
```

On a Mac (example):

```bash
# from the stop-overthinking folder
rsync -a --exclude .git --exclude results/2026-09-24-thesis-run \
  ./ "/Users/YOU/Library/CloudStorage/GoogleDrive-…/My Drive/stop-overthinking/code/"
```

Or drag the folder into Drive in the browser.

## Every run

1. Colab → **Runtime → Change runtime type → A100** (40GB or **80GB** both OK).
2. Upload / open **`notebooks/15b_qwen35_4b.ipynb`** (the new one from this repo).
3. **Runtime → Run all.**  
   - No typing.  
   - Cell 3 must print **`FAST PATH ON ✓`**. If it errors, stop and fix (do not continue at ~40 tok/s).  
   - Batch auto-picks: **64 on 80GB**, **32 on 40GB** for 4B.
4. Wait for smoke → A → B (LoRA-1) → C (if hours left).
5. Results land on Drive: `MyDrive/stop-overthinking/results/4b/`.

## Rules

- Shared pot with 0.8B: **≤150 hours** together.
- Do not write into the old 2B `thesis/` results folder.
- LoRA-1 only.
- Already-finished JSONL files are skipped (safe to re-run).
