# Size comparison: 0.8B · 2B · 4B

> One page for the teacher and for the paper extension.  
> Numbers checked from graded files in `results/0.8b/`, `results/4b/`, and the 2B thesis run.

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


| Way          | 0.8B (1 try) | 2B (2 tries) | 4B (2 tries) |
| ------------ | ------------ | ------------ | ------------ |
| Thinking OFF | **20.5%**    | 40.8%        | 69.7%        |
| Thinking ON  | 7.3%         | 42.1%        | 64.3%        |
| Limit 512    | 17.5%        | — *(nb 16)*  | 75.4%        |
| Limit 1,024  | 13.2%        | **49.8%**    | 76.5%        |
| Limit 2,048  | —            | —            | **78.2%**    |
| Limit 4,096  | —            | —            | 76.7%        |
| LoRA-1       | 17.9%        | 45.5%        | 69.9%        |


**Best free way per size**


| Size | Best free way  | Score | Beats LoRA-1?      |
| ---- | -------------- | ----- | ------------------ |
| 0.8B | **OFF**        | 20.5% | yes (LoRA-1 17.9%) |
| 2B   | **limit 1024** | 49.8% | yes (LoRA-1 45.5%) |
| 4B   | **limit 2048** | 78.2% | yes (LoRA-1 69.9%) |


## 3. What this means

1. **Bigger → more accurate** on every way. Size matters a lot.
2. **Open thinking (ON) is risky** when the model loops: worst on 0.8B (7.3%, 78% cut off), beaten by OFF on 4B too.
3. **A free limit wins on 2B and 4B.** On 0.8B the model is too weak: **OFF** wins.
4. **LoRA-1 never beats the best free way** on any of the three sizes (in these runs).
5. **Best limit grows with size** where limits help: 1024 on 2B → 2048 on 4B. 0.8B did not need a long limit.

## 4. Honest limits of the comparison


| Checked                                  | Assumed / caveat                                            |
| ---------------------------------------- | ----------------------------------------------------------- |
| Same 234 problems, same family (Qwen3.5) | 0.8B = **1 try**; 2B/4B = **2 tries** (wider bars on 0.8B)  |
| Graded with real benchmark tests         | 0.8B skipped Stage C and limits 2048/4096 on purpose (≤50h) |
| LoRA-1 = full MBPP+ shortest-correct     | Not the same training mix as 2B’s LoRA-2                    |


## 5. One recommendation for users

For small code models on one GPU: **try OFF and a short thinking limit first**.  
Train with LoRA only if free ways are not enough — in these three sizes, training did not beat the best free option.

Join table: [ALL-RESULTS.md](ALL-RESULTS.md) · DECISIONS #72–#81.

**Next fill-in:** 2B × limit 512 only — [2b-limit512/RUN.md](2b-limit512/RUN.md) · notebook `16_qwen35_2b_limit512.ipynb`. Skip 2048 on 2B for now (1024 already won on 2B; 4B already showed 2048).