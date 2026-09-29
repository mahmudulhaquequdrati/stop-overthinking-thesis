# 2B · limit 2048 fill-in (LEAN) — what happened

**Checked** from Drive zip `2b-limit2048-20260929T165722Z-1-001.zip` (2026-09-29).  
Same **234** problems · **1 try** · **limit2048 only** (DECISIONS #83–#84).

## Main number

| Way | Accuracy | Thinking | All tokens | Cut off |
|---|---|---|---|---|
| **limit2048** | **46.6%** | 1377 | 1834 | 29% |

## 2B limit curve (answer: peaks at 1024)

| Limit | Accuracy | Tries |
|---|---|---|
| 512 | 45.1% | 2 |
| **1024** | **49.8%** ← peak | 2 |
| 2048 | 46.6% | **1** (lean) |

```text
512 → 1024 → 2048
45.1%  49.8%   46.6%
   up     then DOWN

On 2B, longer than 1024 did not help.
(On 4B, 2048 still won — size matters.)
```

Honest note: 2048 used **1 try**; 512/1024 used **2**. Direction is still clear: 2048 did not beat 1024.

Raw: `results/2b-limit2048/raw/` · Notebook: `17_qwen35_2b_limit2048.ipynb`
