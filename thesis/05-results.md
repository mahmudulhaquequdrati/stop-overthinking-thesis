# 5. Results

This chapter gives the numbers, without opinions. Chapter 6 explains them. Chapter 4 explains how each number was
computed. The full tables, every problem, and all charts are in
[results/full-results/FULL-RESULTS.md](../results/full-results/FULL-RESULTS.md).

**What was run:** 6 ways × 234 problems × 2 tries = **2,808 test answers**, all checked with the benchmarks' own tests,
on one Colab A100 GPU (2026-09-21 to 2026-09-24).

## 5.1 The headline: the free thinking limit was the most accurate way

> **Stopping the model's thinking at 1,024 tokens gave the highest accuracy of all six ways: 49.8%, against 42.1% for
> normal thinking. This is +7.7 points, and the error bar [+4.3, +11.3] is fully above zero.**

The evidence, all on the same 234 problems:

| # | Evidence | Number | Proven? |
|---|---|---|---|
| 1 | More accurate than normal thinking | **+7.7 points** [+4.3, +11.3] | ✅ yes |
| 2 | More accurate than our trained model (LoRA-2) | **+4.7 points** [+0.2, +9.0] | ✅ yes |
| 3 | More accurate than thinking OFF | **+9.0 points** [+3.8, +14.3] | ✅ yes |
| 4 | Rarely makes a problem worse | better than ON on **38** problems, worse on only **12** | — |
| 5 | Far fewer unfinished answers | **25.9%** cut off, against 40.6% for normal thinking | — |
| 6 | Cheaper than normal thinking | **2,722** tokens per answer, against 3,446 (**21% fewer**) | — |
| 7 | Works on easy problems of both test sets | HumanEval+ **+5.2** [+1.2, +9.1]; LiveCodeBench easy **+32.3** [+17.7, +46.8] | ✅ yes, both |

**Where it does not help:** on LiveCodeBench **medium** problems it solved nothing (0 of 78 answers). Stage D (Section 5.7)
also shows that part of its advantage on HumanEval+ comes from our 4,096-token limit.

## 5.2 Accuracy of every way

**Table 5.1.** Accuracy (answers passed ÷ answers). "vs ON" is the difference from thinking ON in points, with the 95% error bar.

| Way | All 234 | vs ON | HumanEval+ (164) | LCB easy (31) | LCB medium (39) |
|---|---|---|---|---|---|
| **Thinking limit** | **49.8%** (233/468) | **+7.7 [+4.3, +11.3]** | **60.4%** | **56.5%** | 0.0% |
| LoRA-1 | 45.5% (213/468) | +3.4 [−0.4, +7.7] | 56.4% | 41.9% | 2.6% |
| LoRA-2 (main) | 45.1% (211/468) | +3.0 [−1.1, +7.3] | 56.4% | 38.7% | 2.6% |
| Thinking ON | 42.1% (197/468) | — | 55.2% | 24.2% | 1.3% |
| Thinking OFF | 40.8% (191/468) | −1.3 [−6.6, +4.3] | 47.3% | 46.8% | **9.0%** |
| Think briefly | 6.6% (31/468) | −35.5 [−41.2, −29.3] | 3.7% | 30.6% | 0.0% |

![Figure 5.1: Accuracy by problem group](../results/full-results/figures/fig1-accuracy-by-group.svg)

**Figure 5.1.** Accuracy of each way, by problem group.

**Differences by group (vs thinking ON):**

| Way | HumanEval+ | LCB easy | LCB medium |
|---|---|---|---|
| Thinking limit | **+5.2** [+1.2, +9.1] | **+32.3** [+17.7, +46.8] | −1.3 [−3.8, 0.0] |
| LoRA-1 | +1.2 [−3.7, +6.4] | **+17.7** [+3.2, +32.3] | +1.3 [−2.6, +5.1] |
| LoRA-2 | +1.2 [−4.3, +6.7] | **+14.5** [+3.2, +29.0] | +1.3 [−2.6, +5.1] |
| Thinking OFF | **−7.9** [−14.6, −1.2] | **+22.6** [+8.1, +37.1] | **+7.7** [+1.3, +15.4] |
| Think briefly | **−51.5** [−57.9, −44.8] | +6.5 [−6.5, +19.4] | −1.3 [−3.8, 0.0] |

Bold = proven (the error bar doesn't include 0).

- On **HumanEval+**, thinking helps: turning it off costs 7.9 points.
- On **LiveCodeBench easy**, normal thinking is weak (24.2%). Every way except "brief" is clearly better.
- On **LiveCodeBench medium**, every way is near zero. Only thinking OFF solves a few (9.0%).

**Extra comparisons** (computed with the same method after the run; not part of the planned hypotheses):

| Comparison | All | HumanEval+ | LCB easy | LCB medium |
|---|---|---|---|---|
| Limit − OFF | **+9.0 [+3.8, +14.3]** | **+13.1 [+6.4, +19.2]** | +9.7 [−4.8, +24.2] | **−9.0 [−16.7, −2.6]** |
| Limit − LoRA-2 | **+4.7 [+0.2, +9.0]** | +4.0 [−1.5, +9.5] | **+17.7 [+1.6, +33.9]** | −2.6 [−6.4, 0.0] |
| LoRA-2 − LoRA-1 | −0.4 [−4.5, +3.8] | 0.0 [−5.5, +5.2] | −3.2 [−16.1, +9.7] | 0.0 [−3.8, +3.8] |

LoRA-2 and LoRA-1 were the same: the extra training data did not help.

## 5.3 Cost: how many tokens each way used

**Table 5.2.** Tokens per answer, all 234 problems.

| Way | All tokens (average) | Thinking (average) | Answer part (average) | Thinking of finished answers (median) | Thinking vs ON |
|---|---|---|---|---|---|
| Thinking OFF | **860** | 0 | 860 | 0 | x0.00 |
| **Thinking limit** | **2,722** | 843 | 1,879 | 880 | x0.26 [0.23, 0.29] |
| LoRA-1 | 3,158 | 2,838 | 320 | 740 | x0.87 [0.81, 0.93] |
| LoRA-2 (main) | 3,392 | 3,252 | 140 | 719 | **x1.00 [0.94, 1.06]** |
| Thinking ON | 3,446 | 3,262 | 185 | 751 | — |
| Think briefly | 5,080 | 5,064 | 16 | 3,547 | x1.55 [1.43, 1.70] |

![Figure 5.2: Accuracy against cost](../results/full-results/figures/fig2-accuracy-vs-tokens.svg)

**Figure 5.2.** Accuracy against tokens per answer. The best place is top-left: accurate and cheap.

1. **LoRA-2 did not shorten thinking at all** (x1.00). LoRA-1 shortened it a little (x0.87), mostly on LiveCodeBench easy (x0.67).
2. **The limit keeps writing after the cut.** Its thinking is 74% shorter than ON's, but its answer part is ten times longer
   (1,879 against 185 tokens). Counted honestly, over all tokens, it saves **21%**.
3. **Thinking OFF is by far the cheapest:** 4× fewer tokens than ON.
4. **"Think briefly" made thinking longer**, not shorter (x1.55).

## 5.4 The hypotheses

The hypotheses were fixed before the run, for the main trained model, LoRA-2.

**Table 5.3.** The hypotheses.

| | Hypothesis | Needed | Result | Verdict |
|---|---|---|---|---|
| H1 | Thinking at least 25% shorter than ON | ≤ x0.75 | x1.00 [0.94, 1.06] | ❌ **Rejected** |
| H2 | Accuracy at most 3 points below ON | ≥ −3 | +3.0 [−1.1, +7.3] | ✅ Supported |
| H3a | More accurate than thinking OFF | > 0 | +4.3 [−0.6, +9.2] | ⚠️ Not shown (bar includes 0) |
| H3b | More accurate than the thinking limit | > 0 | −4.7 [−9.0, −0.2] | ❌ **Rejected**: the limit is better |
| H3c | More accurate than "think briefly" | > 0 | +38.5 [+32.9, +44.2] | ✅ Supported (but see 5.8) |

**The overall hypothesis is rejected:** H1 and H3b fail.

## 5.5 Unfinished answers and loops

Many thinking answers never finished. We checked each unfinished answer for a **loop** (Section 4.12).

**Table 5.4.** Cut-offs and loops (468 answers per way).

| Way | Cut off | Of those, loops |
|---|---|---|
| Thinking OFF | 33 (7.1%) | 27 (81.8%) |
| **Thinking limit** | **121 (25.9%)** | 93 (76.9%) |
| LoRA-1 | 168 (35.9%) | 141 (83.9%) |
| Thinking ON | 190 (40.6%) | **132 (69.5%)** |
| LoRA-2 (main) | 192 (41.0%) | **170 (88.5%)** |
| Think briefly | 432 (92.3%) | 174 (40.3%) |

![Figure 5.3: What happened to every answer](../results/full-results/figures/fig3-cutoffs-and-loops.svg)

**Figure 5.3.** Finished, cut off in a loop, or cut off without a loop.

**Finished answers were short.** On HumanEval+, the median thinking of answers that finished was **672** tokens for ON,
**711** for LoRA-1 and **695** for LoRA-2. Up to about 1,000 tokens, the three curves in Figure 5.4 almost lie on top of
each other. They differ mainly in how many answers **never** finish.

![Figure 5.4: How long the model thinks](../results/full-results/figures/fig4-thinking-length-humaneval.svg)

**Figure 5.4.** Share of HumanEval+ answers that finished thinking within N tokens.

**A real loop** (thinking ON, HumanEval/1, the end of an answer cut off at 4,096 tokens):

```text
I'll track opening and closing parentheses, ensuring each group is properly balanced and separated. The
algorithm needs to handle potential edge cases like empty strings and ensure correct grouping.

The implementation requires careful tracking of parentheses groups, checking for balance, and collecting
valid groups into a list.

By iterating through the string, I can identify balanced groups without nested structures, ...
[the same three paragraphs repeat until the limit]
```

## 5.6 Problem by problem

**Table 5.5.** Problems (of 234) where each way solved more of its 2 tries than thinking ON ("better"), fewer ("worse"), or the same.

| Way | Better | Worse | Same |
|---|---|---|---|
| **Thinking limit** | **38** | **12** | 184 |
| LoRA-2 (main) | 45 | 29 | 160 |
| LoRA-1 | 44 | 31 | 159 |
| Thinking OFF | 45 | 40 | 149 |
| Think briefly | 8 | 114 | 112 |

![Figure 5.5: Better or worse than ON](../results/full-results/figures/fig5-better-worse-than-on.svg)

**Figure 5.5.** Problem by problem, against thinking ON.

The limit had the best balance: it made only 12 problems worse. Across all ways, **168** of the 234 problems were solved at
least once; **66** were solved by no way at all.

## 5.7 Was the token limit unfair to thinking ON? (stage D)

We gave every cut-off thinking-ON answer from try 1 four times more room (16,384 tokens).

**Table 5.6.** Thinking ON with 16,384 tokens for its cut-off answers (try 1 only).

| | HumanEval+ | LiveCodeBench |
|---|---|---|
| Cut-off answers re-run | 36 | 60 |
| Now finished | 23 | 10 |
| Now correct | 9 | 5 |
| Still cut off, in a loop | 12 | 48 |
| Thinking ON, normal limit | 53.7% | 10.0% |
| **Thinking ON, with 16,384 tokens** | **59.1%** | **17.1%** |
| Thinking limit (try 1) | 60.4% | 25.7% |
| Thinking OFF (try 1) | 48.2% | 28.6% |

![Figure 5.6: Stage D](../results/full-results/figures/fig6-stage-d-16k.svg)

**Figure 5.6.** Thinking ON with four times more room, against the limit and OFF.

- **HumanEval+:** with more room, thinking ON rose by 5.5 points (9 more of 164 problems), close to the limit's 60.4%.
  So the 4,096 limit did cost thinking ON something here, and part of the limit's advantage on HumanEval+ comes from it.
  But thinking ON needed up to 16,384 tokens to get there; the limit needs far fewer.
- **LiveCodeBench:** more room helped little. 48 of the 50 answers still cut off were loops. Thinking ON stayed below both
  the limit and OFF.

## 5.8 Why "think briefly" failed

Only 36 of 468 "think briefly" answers finished. Our question already said *"Answer with one Python code block only."* The
extra sentence said *"Think briefly … then give the answer."* The model treated these as two rules that clash, and argued
about them until it ran out of space (HumanEval/0):

```text
*   "Answer with one Python code block only" suggests I should not include conversational filler.
*   "Think briefly... then give the answer." suggests I should include the thinking.
...
*   Wait, if I output thinking text, is it "one Python code block only"?
```

This result is about **this wording** combined with our answer rule. It does not show that asking to be brief never works.

## 5.9 Why LoRA-2 had little to learn from

**Table 5.7.** From training problems to training examples (4 thinking-ON tries per problem).

| | MBPP+ | LiveCodeBench (older) |
|---|---|---|
| Problems | 200 | 80 (40 easy, 40 medium) |
| Correct answers | 357 of 800 (44.6%) | 44 of 320 (13.8%); **medium: 1 of 160** |
| Problems with ≥ 1 correct | 134 | 24 |
| Problems with ≥ 2 correct (a real choice of "shortest") | 111 | 12 |
| Kept as training examples | 133 | 24 |
| Median thinking of kept examples | 515 | **4,709** |
| Kept length ÷ average correct length (lower = more to learn) | 0.829 | **0.987** |

![Figure 5.7: Training data funnel](../results/full-results/figures/fig7-training-data-funnel.svg)

**Figure 5.7.** From problems to kept training examples.

- The medium problems gave **almost nothing** to learn from: 1 correct answer in 160 tries.
- The LiveCodeBench examples it did get were **long** (median 4,709 tokens), and barely shorter than an average correct
  answer (0.987). On LiveCodeBench answers that finished, LoRA-2 then thought for a median of **3,974** tokens, against
  **1,066** for LoRA-1.
- LoRA-2 did learn its examples: its training loss fell from about 0.25 to 0.16
  ([Figure 8 in FULL-RESULTS](../results/full-results/figures/fig8-lora2-training-loss.svg)).

## 5.10 From the pilot study to the real test

**Table 5.8.** LoRA-1 against thinking ON, on different test sets.

| Test set | Thinking vs ON | Accuracy vs ON (points) |
|---|---|---|
| MBPP+ (pilot: the same kind of problems as its training) | **x0.59** [0.46, 0.75] | **+15.0** [+6.0, +25.0] |
| HumanEval+ | x0.94 [0.84, 1.05] | +1.2 [−3.7, +6.4] |
| LiveCodeBench easy | x0.67 [0.55, 0.79] | +17.7 [+3.2, +32.3] |
| LiveCodeBench medium | x0.96 [0.87, 1.05] | +1.3 [−2.6, +5.1] |
| All 234 (real test) | x0.87 [0.81, 0.93] | +3.4 [−0.4, +7.7] |

![Figure 5.8: LoRA-1 transfer](../results/full-results/figures/fig9-lora1-transfer.svg)

**Figure 5.8.** LoRA-1's thinking length compared with thinking ON.

On problems like its training data, training worked well (41% less thinking, +15 points). On new kinds of problems, most of
the effect disappeared.

## 5.11 Computer time

- Answering all 234 problems twice took about **38 A100 minutes** for each thinking way and **29 minutes** for thinking OFF.
- The whole run, including making training data, training, and stage D, used about **38 Colab units**.
- OFF writes 4× fewer tokens but was only about 1.3× faster here, because each batch waits for its slowest answer. That is why
  we measure cost in tokens (Section 4.15).

## 5.12 Summary of results

| Finding | Number |
|---|---|
| Most accurate way | **Thinking limit, 49.8%** (+7.7 [+4.3, +11.3] vs ON) |
| The limit beat the trained model | +4.7 [+0.2, +9.0] |
| The limit beat thinking OFF | +9.0 [+3.8, +14.3] |
| Trained model's thinking length | x1.00 of ON (not shorter) |
| Cheapest way | Thinking OFF: 860 tokens per answer, 40.8% accuracy |
| Long answers were mostly loops | 69.5% of ON's cut-offs, 88.5% of LoRA-2's |
| More room for ON (16k) | HumanEval+ 53.7% → 59.1%; LiveCodeBench 10.0% → 17.1% |
| Training helped only on similar problems | x0.59 on MBPP+, x0.94 on HumanEval+ |
