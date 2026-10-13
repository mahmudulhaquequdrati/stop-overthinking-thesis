# The thesis in one page

We studied **464 unique code problems** using three small Qwen3.5 models.
The question: does training the model to think shorter beat free thinking controls?
A *LoRA* is a small trained add-on. A *token* is a small piece of text.

**0.8B: Thinking OFF 14.7%** · **2B: Limit 1,024 38.6%** · **4B: Limit 2,048 71.9%**

These are the best observed free controls with **464/464 coverage**.
“Free” means no additional training; generating answers still uses compute.

![Best full-coverage controls](figures/best-free.svg)

## What training added

| Model | Free control | Shared problems | Free accuracy | LoRA-1 accuracy | Gap (points) | 95% gap interval |
|---|---|---|---|---|---|---|
| 0.8B | Thinking OFF | 464 | 14.7% | 12.3% | +2.4 | [-0.4, +5.2] |
| 2B | Limit 1,024 | 424 | 41.4% | 37.4% | +4.0 | [+0.1, +7.8] |
| 4B | Limit 2,048 | 424 | 74.3% | 59.3% | +15.0 | [+11.2, +18.8] |


All three free controls score higher than LoRA-1 on shared problems.
The 0.8B interval crosses zero, so its small lead is uncertain.
The 2B lead has an interval only just above zero. The 4B lead is clearer.
These are retrospective, unadjusted comparisons, not proof of a universal winner.

## How to read the result

Each problem gets equal weight, whether it has one attempt or two.
For each problem, average its pass/fail results. Then average across problems.
2B and 4B LoRA-1 cover 424/464 problems. Do not treat missing results as wrong answers.
Earlier LoRA-2 and loop checks cover only 234 problems.

The combined view was chosen after the runs. It was not a single preselected exam.
Collection details stay in the methods note; the main story uses all 464 problems.

Source: [combined results](../results/combined/README.md), calculated from saved graded answers. No model was run again.
