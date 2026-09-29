# Results index — everything for the paper (0.8B · 2B · 4B)

> **Start here when you write the paper.**  
> Every main number lives in one of the files below. Rebuild join tables with:
> `python scripts/make_size_summary.py …` and `python scripts/make_all_results.py`.

---

## 1. One picture

```text
                    same 234 code problems
                            │
           ┌────────────────┼────────────────┐
           ▼                ▼                ▼
         0.8B              2B               4B
      (lean, 1 try)    (main, 2 tries)   (full, 2 tries)
           │                │                │
      OFF 20.5%      limit1024 49.8%   limit2048 78.2%
      LoRA 17.9%     LoRA 45.5%        LoRA 69.9%
```

**Paper sentence:** A free control beats LoRA-1 on every size; the best free way grows with size (OFF → 1k → 2k).

---

## 2. Where each number lives

| Need | File |
|---|---|
| **Side-by-side all sizes** | [SIZE-COMPARISON.md](SIZE-COMPARISON.md) |
| **Join accuracy table** | [ALL-RESULTS.md](ALL-RESULTS.md) |
| **0.8B summary + story** | [0.8b/SUMMARY.md](0.8b/SUMMARY.md) · [0.8b/RUN.md](0.8b/RUN.md) |
| **2B short results** | [2026-09-24-thesis-run.md](2026-09-24-thesis-run.md) |
| **2B full (charts, every problem)** | [full-results/FULL-RESULTS.md](full-results/FULL-RESULTS.md) |
| **4B summary + story** | [4b/SUMMARY.md](4b/SUMMARY.md) · [4b/RUN.md](4b/RUN.md) |
| **Hours ledger** | [shared/hours_budget.json](shared/hours_budget.json) |
| **Thesis chapters with these numbers** | [../thesis/THESIS.md](../thesis/THESIS.md) §5.13 · §6.7 · §7.5.4 |
| **Teacher talk track** | [../TEACHER-A-TO-Z.md](../TEACHER-A-TO-Z.md) |

### Raw graded files (re-check or re-plot)

| Size | Folder |
|---|---|
| 0.8B | `0.8b/raw/test-*-graded.csv` (+ `.jsonl` answers) |
| 2B | `2026-09-24-thesis-run/` and `full-results/` |
| 4B | `4b/raw/test-*-graded.csv` |

---

## 3. Headline numbers (checked)

### Accuracy (%)

| Way | 0.8B (1 try) | 2B (2 tries) | 4B (2 tries) |
|---|---|---|---|
| OFF | **20.5** | 40.8 | 69.7 |
| ON | 7.3 | 42.1 | 64.3 |
| limit512 | 17.5 | — | 75.4 |
| limit1024 | 13.2 | **49.8** | 76.5 |
| limit2048 | — | — | **78.2** |
| limit4096 | — | — | 76.7 |
| LoRA-1 | 17.9 | 45.5 | 69.9 |
| LoRA-2 | n/a | 45.1 | n/a |

### Best free way

| Size | Winner | Score | Beats LoRA-1? |
|---|---|---|---|
| 0.8B | OFF | 20.5% | yes (17.9%) |
| 2B | limit 1024 | 49.8% | yes (45.5%) |
| 4B | limit 2048 | 78.2% | yes (69.9%) |

### Thinking ON cut-off (hits the wall)

| Size | ON accuracy | Cut-off |
|---|---|---|
| 0.8B | 7.3% | 78% |
| 2B | 42.1% | ~41% |
| 4B | 64.3% | 28% |

---

## 4. What each size run included

| | 0.8B | 2B (main) | 4B |
|---|---|---|---|
| Problems | 234 | 234 | 234 |
| Tries | **1** | 2 | 2 |
| OFF / ON | yes | yes | yes |
| Limits | 512, 1024 | 1024 (+ brief, etc.) | 512–4096 |
| LoRA | LoRA-1 | LoRA-1 + LoRA-2 | LoRA-1 |
| Notebook | 15a | 14 | 15b |
| Status | ✅ done | ✅ done | ✅ done |

---

## 5. Status of related docs (for the paper)

| Doc | Updated with 0.8B/2B/4B? |
|---|---|
| `thesis/THESIS.md` (+ PDF) | ✅ §5.13 / §6.7 / §7.5.4 |
| `results/SIZE-COMPARISON.md` | ✅ |
| `results/ALL-RESULTS.md` | ✅ |
| `0.8b/` · `4b/` SUMMARY + RUN | ✅ |
| `TEACHER-A-TO-Z.md` | ✅ |
| `qa/32–37` | ✅ |
| This index | ✅ |
| Old proposal (`proposal/`) | Historical (written before size runs) — do not rewrite |
| Early `qa/01–29` | About older steps; leave as history |

---

## 6. Suggested paper outline (from these files)

1. **Intro / question** — thesis Ch 1  
2. **Method (2B)** — Ch 3–4  
3. **Main results (2B)** — Ch 5 + FULL-RESULTS figures  
4. **Why (loops)** — Ch 6  
5. **Size robustness** — SIZE-COMPARISON + Ch 5.13  
6. **Advice + limits** — Ch 7 + honest 1-try note on 0.8B  

DECISIONS #72–#79.
