# All results: 2B + 0.8B + 4B

> **What this is:** one page that joins every main table from the three separate runs.
> Each run’s raw files stay in their own folder. Rebuild with `python scripts/make_all_results.py`.

| Model | Status | Separate folder |
|---|---|---|
| **Qwen3.5-2B** (main thesis) | ✅ done 2026-09-24 | [2026-09-24-thesis-run.md](2026-09-24-thesis-run.md) · [full-results/FULL-RESULTS.md](full-results/FULL-RESULTS.md) |
| **Qwen3.5-0.8B** | ✅ has graded files | [0.8b/SUMMARY.md](0.8b/SUMMARY.md) · raw: `0.8b/raw/` |
| **Qwen3.5-4B** | ✅ has graded files | [4b/SUMMARY.md](4b/SUMMARY.md) · raw: `4b/raw/` |
| **2B limit512 fill-in** | ✅ done | [2b-limit512/SUMMARY.md](2b-limit512/SUMMARY.md) · raw: `2b-limit512/raw/` |

**Tries (table captions):** 2B and 4B = **2 tries**; lean 0.8B = **1 try** (DECISIONS #75–76). 2B limit512 fill-in = **2 tries** (#81–#82).

**Who this thesis is for:** people who run **small reasoning models for code** on a **limited GPU** (students, indie developers, one-GPU setups).

---

## 1. Accuracy (all problems)

| Way | 2B (checked) | 0.8B | 4B |
|---|---|---|---|
| Thinking OFF | 40.8% | 20.5% | 69.7% |
| Thinking ON | 42.1% | 7.3% | 64.3% |
| Limit 512 | 45.1% | 17.5% | 75.4% |
| Limit 1,024 | 49.8% | 13.2% | 76.5% |
| Limit 2,048 | — | — | 78.2% |
| Limit 4,096 | — | — | 76.7% |
| LoRA-1 | 45.5% | 17.9% | 69.9% |
| LoRA-2 (2B only) | 45.1% | n/a | n/a |

2B main numbers from `results/2026-09-24-thesis-run/summary.csv`. 2B **limit512 = 45.1%** from the fill-in run (`results/2b-limit512/`, DECISIONS #82). LoRA-2 is **not** re-run on 0.8B/4B (DECISIONS #72).

**0.8B headline (checked, 1 try):** best free way = **OFF → 20.5%**. ON only 7.3% (78% cut off). limit512 17.5% · LoRA-1 17.9%. On this tiny model, **switching thinking OFF beats limits and LoRA**.

**2B headline (checked, 2 tries):** best free way = **limit 1024 → 49.8%**. limit512 = **45.1%** (better than ON 42.1%, worse than 1024). LoRA did not beat limit 1024.

**4B headline (checked, 2 tries):** best free way = **limit 2048 → 78.2%**. OFF 69.7% beats ON 64.3%. LoRA-1 69.9% does **not** beat the limits.

**Join story:** [SIZE-COMPARISON.md](SIZE-COMPARISON.md).

---

## 2. Per-model summaries

- [0.8b/SUMMARY.md](0.8b/SUMMARY.md) · [0.8b/RUN.md](0.8b/RUN.md)
- [4b/SUMMARY.md](4b/SUMMARY.md)
- [2B short](2026-09-24-thesis-run.md) · [2B full](full-results/FULL-RESULTS.md)
- [2b-limit512/SUMMARY.md](2b-limit512/SUMMARY.md) · [2b-limit512/RUN.md](2b-limit512/RUN.md)
- [SIZE-COMPARISON.md](SIZE-COMPARISON.md)

---

## 3. Shared hours ledger (raw JSON)

```json
{
  "cap_hours": 58.544,
  "used_hours": 11.544,
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
    },
    "0.8b": {
      "hours": 3.0,
      "stages": {
        "note": "zip had no hours_budget.json; wall ~3h from Colab file times (smoke~04:36 \u2192 SUMMARY~07:18 UTC-ish)"
      }
    }
  },
  "note": "4B + 0.8B done. Wall ledger used_hours=11.544 (4B 8.544 + 0.8B ~3.0 estimated; zip lacked hours file). 0.8B lean: OFF best 20.5%; ON 7.3%; limit512 17.5%; LoRA-1 17.9%.",
  "updated": "2026-09-29",
  "colab_compute_hours_left": 100,
  "buffer_keep_hours": 50,
  "max_hours_for_0_8b": 50,
  "4b_colab_compute_hours_est": 100,
  "0_8b_wall_hours_est": 3.0
}
```

---

## 4. Notebooks

- [15a 0.8B](../notebooks/15a_qwen35_0_8b.ipynb) — ✅ lean run done
- [15b 4B](../notebooks/15b_qwen35_4b.ipynb) — ✅ done
- [16 2B limit512](../notebooks/16_qwen35_2b_limit512.ipynb) — ✅ fill-in done (45.1%)

Rebuilt by `scripts/make_all_results.py`.

