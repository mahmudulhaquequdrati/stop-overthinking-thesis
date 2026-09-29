# Size comparison: 0.8B · 2B · 4B

> One page for the teacher and for the paper extension.  
> Numbers checked from graded files in `results/0.8b/`, `results/4b/`, the 2B thesis run, and `results/2b-limit512/`.

## 1. The idea in one picture

```text
Same 234 code problems
        │
   ┌────┴────┐
   ▼         ▼         ▼
 0.8B       2B        4B
   │         │         │
 OFF wins  limit1024  limit2048
 20.5%     49.8%      78.2%
```

**Everyday example.** A weak student (0.8B) does best when told “don’t overthink — just answer.”  
A stronger student (2B/4B) does best with a short thinking budget, not with open-ended thinking.

## 2. Accuracy side by side

| Way | 0.8B (1 try) | 2B (2 tries) | 4B (2 tries) |
|---|---|---|---|
| Thinking OFF | **20.5%** | 40.8% | 69.7% |
| Thinking ON | 7.3% | 42.1% | 64.3% |
| Limit 512 | 17.5% | **45.1%** | 75.4% |
| Limit 1,024 | 13.2% | **49.8%** | 76.5% |
| Limit 2,048 | — | — *(nb 17 lean)* | **78.2%** |
| Limit 4,096 | — | — | 76.7% |
| LoRA-1 | 17.9% | 45.5% | 69.9% |

**Best free way per size**

| Size | Best free way | Score | Beats LoRA-1? |
|---|---|---|---|
| 0.8B | **OFF** | 20.5% | yes (LoRA-1 17.9%) |
| 2B | **limit 1024** | 49.8% | yes (LoRA-1 45.5%) |
| 4B | **limit 2048** | 78.2% | yes (LoRA-1 69.9%) |

**Limit 512 across sizes:** 0.8B 17.5% · 2B **45.1%** · 4B 75.4%.  
On 2B, 512 beats ON (42.1%) but loses to 1024 (49.8%).

## 3. What this means

1. **Bigger → more accurate** on every way. Size matters a lot.  
2. **Open thinking (ON) is risky** when the model loops: worst on 0.8B (7.3%, 78% cut off), beaten by OFF on 4B too.  
3. **A free limit wins on 2B and 4B.** On 0.8B the model is too weak: **OFF** wins.  
4. **LoRA-1 never beats the best free way** on any of the three sizes (in these runs).  
5. **Best limit grows with size** where limits help: 1024 on 2B → 2048 on 4B. On 2B, 512 is useful but not enough.  
6. **2B limit512 fill-in is done** (notebook 16): 45.1%. No need for 2048 on 2B for the paper table.

## 4. Honest limits of the comparison

| Checked | Assumed / caveat |
|---|---|
| Same 234 problems, same family (Qwen3.5) | 0.8B = **1 try**; 2B/4B = **2 tries** (wider bars on 0.8B) |
| Graded with real benchmark tests | 0.8B skipped limits 2048/4096 on purpose (≤50h) |
| 2B limit512 = separate fill-in run (#82) | Not the same training mix as 2B’s LoRA-2 |

## 5. One recommendation for users

For small code models on one GPU: **try OFF and a short thinking limit first**.  
On ~2B, try about **1,024** thinking tokens (512 helps, 1024 helps more).  
Train with LoRA only if free ways are not enough — in these three sizes, training did not beat the best free option.

Join table: [ALL-RESULTS.md](ALL-RESULTS.md) · [RESULTS-INDEX.md](RESULTS-INDEX.md) · DECISIONS #72–#83.

**Next lean fill-in:** 2B × limit 2048 (1 try) — [2b-limit2048/RUN.md](2b-limit2048/RUN.md) · notebook `17_qwen35_2b_limit2048.ipynb`. Skip 4096.
