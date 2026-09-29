# All results: 2B + 0.8B + 4B

> **What this is:** one page that joins every main table from the three separate runs.
> Each run’s raw files stay in their own folder. Rebuild with `python scripts/make_all_results.py`.

| Model | Status | Separate folder |
|---|---|---|
| **Qwen3.5-2B** (main thesis) | ✅ done 2026-09-24 | [2026-09-24-thesis-run.md](2026-09-24-thesis-run.md) · [full-results/FULL-RESULTS.md](full-results/FULL-RESULTS.md) |
| **Qwen3.5-0.8B** | ⬜ not run yet | [0.8b/SUMMARY.md](0.8b/SUMMARY.md) · raw: `0.8b/raw/` |
| **Qwen3.5-4B** | ✅ has graded files | [4b/SUMMARY.md](4b/SUMMARY.md) · raw: `4b/raw/` |

**Hour rule now:** Colab has ~**100** compute hours left; always keep **≥50**. So **0.8B may use ≤50 more hours**. Ledger: [shared/hours_budget.json](shared/hours_budget.json).

**Tries (say this in every table caption):** 2B and 4B used **2 tries**; lean 0.8B uses **1 try** (DECISIONS #75–76). Error bars still use the same problems (bootstrap). 0.8B bars will be a bit wider — that is expected, not missing data.

**Who this thesis is for:** people who run **small reasoning models for code** on a **limited GPU** (students, indie developers, one-GPU setups).

---

## 1. Accuracy (all problems)

| Way | 2B (checked) | 0.8B | 4B |
|---|---|---|---|
| Thinking OFF | 40.8% | — | 69.7% |
| Thinking ON | 42.1% | — | 64.3% |
| Limit 512 | — | — | 75.4% |
| Limit 1,024 | 49.8% | — | 76.5% |
| Limit 2,048 | — | — | 78.2% |
| Limit 4,096 | — | — | 76.7% |
| LoRA-1 | 45.5% | — | 69.9% |
| LoRA-2 (2B only) | 45.1% | n/a | n/a |

2B numbers from `results/2026-09-24-thesis-run/summary.csv`. LoRA-2 is **not** re-run on 0.8B/4B (DECISIONS #72).

**4B headline (checked):** best free way = **limit 2048 → 78.2%**. OFF 69.7% beats ON 64.3%. LoRA-1 69.9% does **not** beat the limits.

---

## 2. Per-model summaries

- [0.8b/SUMMARY.md](0.8b/SUMMARY.md)
- [4b/SUMMARY.md](4b/SUMMARY.md)
- [2B short](2026-09-24-thesis-run.md) · [2B full](full-results/FULL-RESULTS.md)

---

## 3. Shared hours ledger (raw JSON)

```json
{
  "cap_hours": 58.544,
  "used_hours": 8.544,
  "runs": {
    "4b": {
      "stages": {
        "smoke": {
          "t0": 1790628635.6487887,
          "hours": 0.156,
          "ended": "2026-09-28 20:59:56"
        },
        "A": {
          "t0": 1790649461.7429352,
          "hours": 0.939,
          "ended": "2026-09-29 03:34:03"
        },
        "B1": {
          "t0": 1790652890.9829416,
          "hours": 0.752,
          "ended": "2026-09-29 04:19:59"
        },
        "B2": {
          "t0": 1790655599.5545306,
          "hours": 0.093,
          "ended": "2026-09-29 04:25:34"
        },
        "B3": {
          "t0": 1790655934.308727,
          "hours": 0.802,
          "ended": "2026-09-29 05:13:41"
        },
        "C": {
          "t0": 1790658853.6479075,
          "hours": 5.802,
          "ended": "2026-09-29 11:02:20"
        }
      },
      "hours": 8.544
    }
  },
  "note": "4B done (8.544h). Colab has ~100 compute hours left; always keep \u226550. So 0.8B may use \u226450 more hours (shared ledger cap_hours=used+50).",
  "updated": "2026-09-29",
  "colab_compute_hours_left": 100,
  "buffer_keep_hours": 50,
  "max_hours_for_0_8b": 50
}
```

---

## 4. Notebooks

- [15a 0.8B](../notebooks/15a_qwen35_0_8b.ipynb) — run **next** (≤50h)
- [15b 4B](../notebooks/15b_qwen35_4b.ipynb) — ✅ done

