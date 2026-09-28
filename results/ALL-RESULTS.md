# All results: 2B + 0.8B + 4B

> **What this is:** one page that joins every main table from the three separate runs.
> Each run’s raw files stay in their own folder. Rebuild with `python scripts/make_all_results.py`.

| Model | Status | Separate folder |
|---|---|---|
| **Qwen3.5-2B** (main thesis) | ✅ done 2026-09-24 | [2026-09-24-thesis-run.md](2026-09-24-thesis-run.md) · [full-results/FULL-RESULTS.md](full-results/FULL-RESULTS.md) |
| **Qwen3.5-0.8B** | ✅ has graded files | [0.8b/SUMMARY.md](0.8b/SUMMARY.md) · raw: `0.8b/raw/` |
| **Qwen3.5-4B** | ✅ has graded files | [4b/SUMMARY.md](4b/SUMMARY.md) · raw: `4b/raw/` |

**Shared hour pot:** ≤150 hours for 0.8B + 4B together. Ledger: [shared/hours_budget.json](shared/hours_budget.json).

**Who this thesis is for:** people who run **small reasoning models for code** on a **limited GPU** (students, indie developers, one-GPU setups).

---

## 1. Accuracy (all problems)

| Way | 2B (checked) | 0.8B | 4B |
|---|---|---|---|
| Thinking OFF | 40.8% | — | — |
| Thinking ON | 42.1% | — | — |
| Limit 512 | — | — | — |
| Limit 1,024 | 49.8% | — | — |
| Limit 2,048 | — | — | — |
| Limit 4,096 | — | — | — |
| LoRA-1 | 45.5% | — | — |
| LoRA-2 (2B only) | 45.1% | n/a | n/a |

2B numbers from `results/2026-09-24-thesis-run/summary.csv`. LoRA-2 is **not** re-run on 0.8B/4B (DECISIONS #72).

---

## 2. Per-model summaries

- [0.8b/SUMMARY.md](0.8b/SUMMARY.md)
- [4b/SUMMARY.md](4b/SUMMARY.md)
- [2B short](2026-09-24-thesis-run.md) · [2B full](full-results/FULL-RESULTS.md)

---

## 3. Shared hours ledger (raw JSON)

```json
{"cap_hours":150,"used_hours":0,"runs":{},"note":"shared pot for 0.8B + 4B; buffer 50h of the 200 stays unused"}
```

---

## 4. Notebooks

- [15a 0.8B](../notebooks/15a_qwen35_0_8b.ipynb) — run **second**
- [15b 4B](../notebooks/15b_qwen35_4b.ipynb) — run **first**

