# 34 — Lean 0.8B test plan (≤50 compute hours)

## The step in 2 sentences

4B used almost **100 Colab compute hours**. For 0.8B we run a **lean** plan: OFF · ON · limits 512/1024/2048 · LoRA-1 · **1 try** · **no Stage C** · same 234 problems.

## Questions a teacher may ask

### What are you testing on 0.8B?

Whether a **smaller** model shows the same pattern: a free thinking limit beats LoRA-1, and which limit wins.

### Why not the full 4B menu again?

4B already used ~100 compute hours. We have ~100 left and must keep **≥50**. A full copy would burn the buffer. Lean is enough for the size comparison.

### What did you drop, and why?

| Dropped | Why |
|---|---|
| limit 4096 | Not best on 4B (2048 won); costly |
| Stage C (2nd try) | Cuts answering cost a lot; 1 try still ranks the ways |
| LoRA-2 / “think briefly” | Already decided: LoRA-1 only for this extension |

### What did you keep?

Same 234 problems · OFF · ON · limits around 4B’s winner (512 / 1024 / 2048) · LoRA-1.

### How do you run it?

Notebook **15a** on Colab A100 → **Runtime → Run all**. Cap: ≤50 more compute hours.

## Hard questions

### Is one try “not enough”?

For ranking ways, one try is fine. Two tries mainly tighten error bars. 4B already has the 2-try story.

### What if 0.8B’s best limit is not 2048?

That is still a result. We keep 512 and 1024 so we can see if the winner moves with size.

## Checked vs. assumed

| Checked | Assumed |
|---|---|
| 4B numbers + ~100 Colab compute hours (user) | 0.8B lean run will finish under 50h |
| Notebook 15a rebuilt with lean settings | Fast path will work like on 4B |

## Where it is written

DECISIONS #74 · `results/0.8b/RUN.md` · `notebooks/15a_qwen35_0_8b.ipynb` · ROADMAP
