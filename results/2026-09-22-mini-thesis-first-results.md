# Mini-thesis (notebook 13): results — 2026-09-22

**GPU:** Colab A100 (paid units, DECISIONS #48, #63) · **Model:** unsloth/Qwen3.5-2B in **bfloat16** ·
**Batch:** 64 · **Test:** **100** MBPP+ test problems, 1 try each, 4,096-token limit, the same seed
and settings for every way · **LoRAs:** trained on 25% / 50% / 100% of the kept training examples.

## 1. The final table (printed by `scripts/compare_mini.py`)

```text
way       problems  accuracy  tokens  thinking  cut off   vs thinking ON: accuracy (95%)   tokens ratio (95%)
off            100     56.0%     100         0        0    +6.0 pts [ -5.0, +17.0]   x0.05 [0.04, 0.06]
on             100     50.0%    1936      1883       27
brief          100      3.0%    4056      4055       92   -47.0 pts [-57.0, -37.0]   x2.09 [1.80, 2.47]
lora25         100     65.0%    1269      1183       14   +15.0 pts [ +7.0, +23.0]   x0.66 [0.52, 0.81]
lora50         100     68.0%    1116      1025       13   +18.0 pts [ +9.0, +27.0]   x0.58 [0.46, 0.72]
lora100        100     65.0%    1145      1067       15   +15.0 pts [ +6.0, +25.0]   x0.59 [0.46, 0.75]

LEARNING CURVE   lora25 65.0% x0.66 · lora50 68.0% x0.58 · lora100 65.0% x0.59 · TARGET x0.81

R1 YES training works: tokens x0.59 (need <= 0.75), accuracy +15.0 pts (need >= -3)
R2 YES beats 'think briefly': 65.0% vs 3.0%, 1145 vs 4056 tokens
R3 NO  thinking OFF is enough on easy problems: 56.0% vs 65.0%
R4     50% -> 100%: tokens -0.01 lower, accuracy -3.0 pts: UNCLEAR
R5     LoRA x0.59 vs TARGET x0.81 (gap -0.22): reached what the examples show
```

(Tokens and thinking are **averages** per answer here; the median ON thinking was 1,152.)

## 2. What it means

| Question | Answer | How sure |
|---|---|---|
| Does training cut thinking? | **Yes: 41% fewer tokens** than thinking ON (x0.59) | error bars [0.46, 0.75]: clearly below 1 |
| Does it cost accuracy? | **No: it GAINED 15 points** (50% → 65%) | error bars [+6, +25]: clearly above 0 |
| Why did accuracy go up? | Fewer answers that never finish: **27 → 15** cut off | measured |
| Does it beat "think briefly"? | Yes, by far (65% vs 3%) | clear |
| Does it beat thinking OFF? | **More accurate (65% vs 56%)**, but OFF is ~11× cheaper (100 tokens) | LoRA vs OFF has **no paired error bar yet** |
| Would more data help? | **Probably not much**: 25%, 50% and 100% all give ~65–68% and ~x0.6 | the curve is flat, but ±10 points of noise |

## 3. "Think briefly" is a real result, not a bug

Reading the raw answers: the model treats "think briefly" as one more rule to check, and keeps
re-checking it until the limit:

```text
Constraint 3: Keep thinking brief (few short sentences).
Wait, I'll use split() because it's the most common expectation.
Okay, I'll use split().
Wait, I'll use split() because it's the most common expectation.    (repeats to 4,096)
Wait, I need to make sure I don't output the thinking text in the final response.
```

Our prompt was sent correctly. **Limit:** only one wording was tested.

## 4. Two things to read carefully (honest limits)

- **R5 compares two different things.** TARGET (x0.81) is measured only among *correct, finished*
  training answers. The LoRA ratio (x0.59) is against *all* thinking-ON answers, including 27 that
  ran to 4,096. So the LoRA is not "shorter than its examples". Most of its saving comes from
  **looping less**. R5's advice ("make shorter examples") should not be followed on this evidence.
- **Easy, in-distribution problems only.** The LoRA trained on MBPP+ and was tested on other MBPP+
  problems of the same kind. Whether it helps on HumanEval+ and on medium LiveCodeBench problems is
  not known. 1 try per problem.

## 5. The LoRA safety check worked (before the fix)

The first run stopped with `STOP: the LoRA ... did not load (96 layers, weight sum 0.0)`. Unsloth
saved the weights as `...model.language_model.layers.N...`; the plain model expects
`...model.layers.N...`. Fixed in `scripts/gen_colab.py` by matching names from `layers.N.` on
(commit 9bdc087). Checked in Colab: all 3 LoRAs have 192 weights, non-zero B weights
(2,701 / 3,479 / 4,177), and training loss fell (0.29→0.14, 0.27→0.11, 0.34→0.09).

## 6. Speed

A100, batch 64: a full batch of thinking-ON answers took ~230 s. The free T4 needed ~735 s for a
batch of 8 (see `2026-09-22-t4-speed-first-run.md`).
