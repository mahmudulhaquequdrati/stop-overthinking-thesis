# 34 — Lean 0.8B test plan (≤50 compute hours)

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

For ranking ways, one try is fine. Two tries mainly tighten error bars. 4B already has the 2-try story.

### What if 512 beats 1024 on 0.8B?

That is still a useful result: smaller models may prefer a shorter cap. We keep both so we can see which wins.

## Checked vs. assumed

| Checked | Assumed |
|---|---|
| 4B numbers + ~100 Colab compute hours (user) | 0.8B lean run will finish under 50h |
| Notebook 15a rebuilt with lean settings | Fast path will work like on 4B |

## Where it is written

DECISIONS #75 · `results/0.8b/RUN.md` · `notebooks/15a_qwen35_0_8b.ipynb` · ROADMAP
