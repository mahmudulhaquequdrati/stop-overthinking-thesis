# Who should use this, and why

This study helps people choosing settings for small Python code models.
It covers Qwen3.5-0.8B, 2B, and 4B, run on a Colab GPU.
A GPU is the chip doing the model's calculations.

Imagine asking a student to plan a solution before writing code.
Some planning helps. Repeating the plan without finishing wastes time.
Our free controls either skip the notes or stop them at a fixed length.

## What to try first

**0.8B: Thinking OFF 14.7%** · **2B: Limit 1,024 38.6%** · **4B: Limit 2,048 71.9%**

These scores use 464 problems each. Try the same controls on your own tasks.
No additional training is needed. Answer generation still costs compute.

![Accuracy and coverage](figures/combined-accuracy.svg)

## Cost matters too

Thinking OFF uses fewer total tokens than normal thinking on every tested size.
The limits on 2B and 4B also reduce total tokens relative to normal thinking.
See the exact counts and coverage in [the results](05-results.md).

We did not test larger models, hard contest problems, math, or privacy attacks.
Local deployment can keep prompts on your machine, but this is not a security evaluation.
A result on these benchmarks does not promise the same accuracy on your code.

## Completed LoRA controls

All six combinations are complete, with 464/464 results each.
0.8B: LoRA + OFF **14.0%**, LoRA + limit 512 **14.4%**.
2B: LoRA + OFF **35.6%**, LoRA + limit 1,024 **41.2%**.
4B: LoRA + OFF **64.7%**, LoRA + limit 2,048 **71.6%**.
These use one attempt per problem. Historical controls also have a labelled
first-attempt comparison; their all-attempt scores remain separate.
See [the completed analysis](11-completed-lora-controls.md) and [benchmark tables](05-results.md).
