# 2B · limit 512 fill-in — what happened

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

**Checked** from Drive zip `2b-limit512-20260929T161939Z-1-001.zip` (2026-09-29).  
Same **234** problems · **2 tries** · **limit512 only** (DECISIONS #81–#82).

## Main number

| Way | Accuracy | Thinking | All tokens | Cut off |
|---|---|---|---|---|
| **limit512** | **45.1%** | 492 | 2684 | 28% |

## How it sits next to other 2B ways

| Way | Accuracy |
|---|---|
| Thinking OFF | 40.8% |
| Thinking ON | 42.1% |
| **limit512** | **45.1%** ← this fill-in |
| LoRA-1 | 45.5% |
| **limit1024** | **49.8%** ← still best on 2B |

```text
limit512 helps vs ON (+3.0 points)
but limit1024 is still clearly better (+4.7 vs limit512)
```

So the empty chart cell is filled, and the main 2B story does **not** change: best free way stays **limit 1024**.

Raw: `results/2b-limit512/raw/` · Notebook: `16_qwen35_2b_limit512.ipynb`
