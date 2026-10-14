# 2B · limit 2048 fill-in (LEAN) — what happened

<!-- CURRENT-STUDY:START -->

**Historical record below.** Its earlier scores, model choices and plans describe that stage only.
Use the current results linked here for the completed study.

**Current study — 14 October 2026:** **464 unique test problems**.
Benchmarks: **164 HumanEval+**, **166 LiveCodeBench easy**, **134 LiveCodeBench medium**.
All six planned LoRA combinations are complete, one attempt per problem:

- **0.8B:** LoRA + OFF **14.0% (65/464)**; LoRA + limit 512 **14.4% (67/464)**.
- **2B:** LoRA + OFF **35.6% (165/464)**; LoRA + limit 1,024 **41.2% (191/464)**.
- **4B:** LoRA + OFF **64.7% (300/464)**; LoRA + limit 2,048 **71.6% (332/464)**.

LoRA alone means thinking ON without a thinking-token limit.
Older methods' all-attempt averages and first-attempt comparisons are labelled separately.
LoRA + OFF does not consistently improve on free OFF; the 2B/4B gains over free limits remain uncertain.

[Every method, benchmark, difficulty, token count and interval](../CURRENT-RESULTS.md) · [Full easy thesis](../../easy-thesis/FULL-THESIS.md) · [Full formal Markdown thesis](../../thesis/THESIS.md).

<!-- CURRENT-STUDY:END -->

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
