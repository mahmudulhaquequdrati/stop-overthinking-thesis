# 34 — Lean 0.8B test plan (≤50 compute hours)

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

[Every method, benchmark, difficulty, token count and interval](../results/CURRENT-RESULTS.md) · [Full easy thesis](../easy-thesis/FULL-THESIS.md) · [Full formal Markdown thesis](../thesis/THESIS.md).

<!-- CURRENT-STUDY:END -->

## The step in 2 sentences

4B used almost **100 Colab compute hours**. For 0.8B we run a **lean** plan: OFF · ON · limits **512 / 1024** (max 1024) · LoRA-1 · **1 try** · **no Stage C** · same 234 problems.

## Questions a teacher may ask

### What are you testing on 0.8B?

Whether a **smaller** model shows the same pattern: a free thinking limit beats LoRA-1, and which limit wins.

### Why not the full 4B menu again?

4B already used ~100 compute hours. We have ~100 left and must keep **≥50**. A full copy would burn the buffer. Lean is enough for the size comparison.

### What did you drop, and why?

| Dropped | Why |
|---|---|
| limit 2048 / 4096 | On **2B**, max useful limit was **1024** (49.8%). 0.8B is smaller — longer budget not needed |
| Stage C (2nd try) | Cuts answering cost a lot; 1 try still ranks the ways |
| LoRA-2 / “think briefly” | Already decided: LoRA-1 only for this extension |

### What did you keep?

Same 234 problems · OFF · ON · limits **512 / 1024** · LoRA-1.

### Why not 2048 on 0.8B?

2B’s best free way was already limit 1024. 4B needed 2048 because it is bigger. 0.8B should not need more than 2B.

### How do you run it?

Notebook **15a** on Colab A100 → **Runtime → Run all**. Cap: ≤50 more compute hours.

## Hard questions

### Is one try “not enough”?

For **ranking** ways, one try is fine. Two tries mainly **tighten** error bars a little. 4B already has the 2-try story.

### Will the paper / figures still have 0.8B?

**Yes.** After the run we put 0.8B in:
- `results/0.8b/SUMMARY.md`
- `results/ALL-RESULTS.md` (join table + charts)
- the size-comparison section / figures in the write-up

Every table caption must say: **0.8B = 1 try; 2B/4B = 2 tries**.

### What about looser error bars on 0.8B?

Error bars come mainly from **which of the 234 problems** pass, not only from “how many tries”.

```text
2 tries → each problem score can be 0, ½, or 1  → a bit smoother
1 try  → each problem score is 0 or 1           → bars a bit wider
```

We still show bars (or say when a difference is not proven). We **do not** pretend 0.8B has the same precision as 2B/4B. That honesty is part of the result (DECISIONS #76).

### What if 512 beats 1024 on 0.8B?

That is still a useful result: smaller models may prefer a shorter cap. We keep both so we can see which wins.

## Checked vs. assumed

| Checked | Assumed |
|---|---|
| 4B numbers + ~100 Colab compute hours (user) | 0.8B lean run will finish under 50h |
| Notebook 15a rebuilt with lean settings | Fast path will work like on 4B |

## Where it is written

DECISIONS #75 · #76 · `results/0.8b/RUN.md` · `notebooks/15a_qwen35_0_8b.ipynb` · ROADMAP
