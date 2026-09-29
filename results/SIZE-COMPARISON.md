# Size comparison: 0.8B · 2B · 4B

> One page for the teacher and for the paper extension.  
> Numbers checked from graded files in `results/0.8b/`, `results/4b/`, the 2B thesis run,
> `results/2b-limit512/`, and `results/2b-limit2048/`.

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

| Way | 0.8B (1 try) | 2B | 4B (2 tries) |
|---|---|---|---|
| Thinking OFF | **20.5%** | 40.8% (2 tries) | 69.7% |
| Thinking ON | 7.3% | 42.1% (2 tries) | 64.3% |
| Limit 512 | 17.5% | **45.1%** (2 tries) | 75.4% |
| Limit 1,024 | 13.2% | **49.8%** (2 tries) | 76.5% |
| Limit 2,048 | — | **46.6%** (1 try)* | **78.2%** |
| Limit 4,096 | — | — | 76.7% |
| LoRA-1 | 17.9% | 45.5% (2 tries) | 69.9% |

\* 2B limit2048 = lean fill-in (**1 try**). Caption that in the paper.

**2B limit curve:** 512 → 45.1% · 1024 → **49.8%** · 2048 → 46.6%. **Peaks at 1024.**

**Best free way per size**

| Size | Best free way | Score | Beats LoRA-1? |
|---|---|---|---|
| 0.8B | **OFF** | 20.5% | yes (LoRA-1 17.9%) |
| 2B | **limit 1024** | 49.8% | yes (LoRA-1 45.5%) |
| 4B | **limit 2048** | 78.2% | yes (LoRA-1 69.9%) |

**Limit 512 across sizes:** 0.8B 17.5% · 2B 45.1% · 4B 75.4%.

## 3. What this means

1. **Bigger → more accurate** on every way. Size matters a lot.  
2. **Open thinking (ON) is risky** when the model loops.  
3. **A free limit wins on 2B and 4B.** On 0.8B, **OFF** wins.  
4. **LoRA-1 never beats the best free way** on any of the three sizes.  
5. **Best limit grows with size:** 1024 on 2B → 2048 on 4B. On 2B, **2048 did not beat 1024** (46.6% vs 49.8%).  
6. Fill-ins done: 2B limit512 (#82) and lean limit2048 (#84). No need for 4096 on 2B.

## 4. Honest limits of the comparison

| Checked | Assumed / caveat |
|---|---|
| Same 234 problems, same family (Qwen3.5) | 0.8B and 2B-limit2048 = **1 try**; other 2B/4B = **2 tries** |
| Graded with real benchmark tests | 0.8B skipped limits 2048/4096 on purpose |
| 2B limit512 / limit2048 = fill-in runs | Not the same training mix as 2B’s LoRA-2 |

## 5. One recommendation for users

For small code models on one GPU: **try OFF and a short thinking limit first**.  
On ~2B, about **1,024** thinking tokens was best (512 helps; 2048 did not beat it here).  
On ~4B, about **2,048** was best.  
Train with LoRA only if free ways are not enough.

Join table: [ALL-RESULTS.md](ALL-RESULTS.md) · [RESULTS-INDEX.md](RESULTS-INDEX.md) · DECISIONS #72–#84.
