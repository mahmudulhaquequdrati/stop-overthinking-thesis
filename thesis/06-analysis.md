# 6. Analysis

Chapter 5 showed **what** happened. This chapter explains **why**, compares it with earlier work, and says honestly what
could be wrong.

## 6.1 The answer to the research question

> *On a small model with a thinking switch, does training on its own shortest correct code answers give a better balance
> of accuracy and thinking length than the free options?*

**For Qwen3.5-2B, the answer is no.**

```text
                 accuracy        tokens per answer
Thinking limit   49.8%  ◄ best   2,722
LoRA-2 (trained) 45.1%           3,392   ◄ not shorter than ON
Thinking ON      42.1%           3,446
Thinking OFF     40.8%             860   ◄ cheapest
```

The trained model did not think shorter (x1.00), and its small accuracy gain could not be proven. The free thinking limit
was more accurate than the trained model (+4.7, proven), more accurate than normal thinking (+7.7, proven), and cheaper.
Thinking OFF was 4× cheaper than normal thinking, at about the same overall accuracy.

## 6.2 Why training did not shorten thinking

### Reason 1 (the main one): the waste was loops, not long careful thinking

Shortest-correct training is built on one idea of overthinking: *the model finds the answer, then keeps checking*. If that
were true, showing the model short correct answers would teach it to stop earlier.

Our data shows a different kind of waste:

```text
What we expected (overthinking)          What we found (looping)
───────────────────────────────          ────────────────────────────────
think ... answer found ... check ...     think ... think ... [repeat] [repeat]
check ... check ... </think> answer      [repeat] [repeat] ... ✂ cut off, no answer
→ finishes, just too long                → never finishes
→ training CAN shorten it                → training on finished answers can't fix it
```

The evidence:

- Answers that **finished** were already short: median 672 thinking tokens on HumanEval+ (Section 5.5).
- Most answers that **didn't finish** were loops: 69.5% for thinking ON, 88.5% for LoRA-2 (Table 5.4).
- ON, LoRA-1 and LoRA-2 have almost the same length curves up to about 1,000 tokens. They differ in how many answers never finish (Figure 5.4).
- The makers of the model say the same thing. Its official model card warns: *"Qwen3.5-2B is more prone to entering thinking
  loops compared to other Qwen3.5 models, which may prevent it from terminating generation properly."*

Training only ever shows the model **finished** answers. It never shows how to get **out** of a loop. So it could not
remove the main source of waste.

### Reason 2: the training signal was weak

- **Little to learn:** for MBPP+, the kept examples were only 17% shorter than an average correct answer (0.829). For
  LiveCodeBench they were almost exactly average (0.987).
- **Nothing to learn from on medium problems:** 1 correct answer in 160 tries. A model can't learn from problems it can't solve.
- **The wrong lesson on LiveCodeBench:** its few LiveCodeBench examples were long (median 4,709 tokens). LoRA-2 then thought
  **longer** than LoRA-1 on LiveCodeBench (3,974 against 1,066 tokens on finished answers).

This fits a known finding about small models: *"small models (≤3B parameters) do not consistently benefit from long
chain-of-thought (CoT) reasoning"* (Li et al., 2025).

### Reason 3: the effect did not carry over to new kinds of problems

In the pilot, where training and test problems came from the same benchmark (MBPP+), LoRA-1 cut thinking by 41% and gained
15 points. On HumanEval+, which has similar easy function problems from a different source, the effect almost disappeared
(x0.94, +1.2). The training seems to teach **habits for one kind of problem**, not a general "think shorter" skill.

### A possible fourth reason (not tested)

SEER (2025) reported that LoRA training was about 7 points less accurate than training the whole model. We only used LoRA.
Training the whole model might learn more.

## 6.3 Why the thinking limit worked

**It stops loops by force.** When thinking reaches 1,024 tokens, the model must answer.

```text
Thinking ON:      think ... [loop] [loop] [loop] ... ✂ cut off at 4,096 → no code → FAIL
Thinking limit:   think ... [loop] ✂ stop at 1,024 → </think> → writes code → often PASS
```

On easy problems, most useful thinking fits inside 1,024 tokens (Figure 5.4: 183 of 328 ON answers on HumanEval+, 55.8%,
finished thinking within 1,024 tokens). So when the loop is cut, the model usually already knows enough to write working
code. That is why the limit made only 12 problems worse and 38 better.

**Its limits:**

1. **It moves some of the writing; it doesn't remove all of it.** After the forced stop, the model often keeps reasoning inside
   its answer (1,879 tokens on average). The real saving is 21% of all tokens, not the 74% the thinking count suggests.
2. **It doesn't help on hard problems.** On LiveCodeBench medium, it solved nothing. The model had not worked out the answer by
   1,024 tokens, and it often kept going in the answer part until the overall limit.
3. **On easy problems, part of its win comes from our token limit.** With 16,384 tokens, thinking ON nearly caught up on
   HumanEval+ (59.1% against 60.4%, Section 5.7). But ON needed up to 16 times more thinking room to get there.

## 6.4 Thinking OFF is a strong, cheap option

Thinking OFF used 860 tokens per answer, 4× fewer than thinking ON, with about the same overall accuracy (−1.3, not proven).
The groups differ:

- On **HumanEval+**, thinking helps: OFF is 7.9 points worse (proven).
- On **LiveCodeBench**, OFF is **better** than normal thinking, on easy (+22.6) and on medium problems (+7.7), because normal
  thinking so often looped until the limit.

NoThinking (2025) reported that skipping thinking can beat thinking with a small budget, also on code. In our study, the
1,024-token limit beat OFF overall (+9.0, proven), but OFF beat the limit on LiveCodeBench medium (−9.0 for the limit). The
studies use different models and budgets, so they don't directly disagree. Both show that "thinking off" must always be part
of the comparison.

## 6.5 How this fits earlier work

| Earlier work | What they found | What we add |
|---|---|---|
| Munkhbat et al. (2025): shortest-correct training on math | ~12% fewer tokens, same accuracy | On a small code model, training did **not** shorten thinking on new problems |
| SEER (2025), ASAP (2025): code, 7–8B models | 23–40% shorter thinking | Our pilot agrees (41% shorter) **only** when test problems are like training problems |
| NoThinking (2025) | Thinking off is a strong option | Confirmed: 4× cheaper, same overall accuracy; better on the harder problems |
| s1 (2025), Qwen3 report (2025): thinking budgets | Budgets can control how much a model thinks | A budget was the **most accurate** way for a small model, because it stops loops |
| Pipis et al. (2025): why models loop | *"Larger models tend to loop less"* | We measured looping as the main waste in a 2B model, and showed that training on short answers doesn't fix it |

Our main new point: **for a small reasoning model, the main waste is thinking that never finishes, not correct thinking that
runs long.** Methods that learn only from finished answers cannot address it.

## 6.6 What could be wrong? (threats to validity)

**Is the comparison fair?**
- ✅ All ways used the same problems, settings, seeds, token limits and checker. The main LoRA and the hypotheses were fixed before the run.
- ⚠️ The token limits cut off some useful thinking on HumanEval+. We measured it: +5.5 points for thinking ON with 16,384 tokens (Section 5.7).
- ⚠️ "Think briefly" was tested with one wording, which clashed with our answer rule.
- ⚠️ Our loop test is strict and under-counts loops. The true share is probably higher.

**Does it hold elsewhere?**
- ⚠️ One model only. Its makers say it loops more than the other Qwen3.5 models, so **larger models may behave differently**
  (Chapter 7).
- ⚠️ Only easy and medium problems. LiveCodeBench medium is at the floor (0–9%) and can't separate the ways.
- ⚠️ Code only.

**Is it just luck?**
- ⚠️ 234 problems, 2 tries each. Error bars are about ±4–6 points over all problems and much wider on the small LiveCodeBench
  groups (31 and 39 problems). Only fairly large differences can be proven. The main findings (the limit +7.7, LoRA-2 x1.00)
  are well outside that noise.

**Are we measuring the right thing?**
- ✅ Accuracy uses the benchmarks' own tests, and the checker passed the official solutions first.
- ⚠️ LiveCodeBench answers were checked on up to 20 tests per problem, not always all of them.
- ⚠️ GPU time depends on batching, so we use tokens for cost.

## 6.7 Summary of the analysis

```text
Small model thinks ─► often gets STUCK IN A LOOP ─► never finishes ─► fails
                                   │
        Training on short correct answers: never shows how to get unstuck ─► no change (x1.00)
        Thinking limit:                    cuts the loop, forces an answer   ─► +7.7 points
        Thinking OFF:                      never enters the loop             ─► 4× cheaper
```
