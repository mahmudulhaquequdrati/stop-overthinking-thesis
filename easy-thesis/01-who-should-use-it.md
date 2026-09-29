# Who should use this, and why

A small code model with a thinking switch is enough for many easy Python tasks.
A free limit, or thinking turned off, is the first thing to try.

## Everyday example

You have a laptop, or one rented graphics chip.
You want a function that checks a list of numbers.
You do not want to send that code to a giant cloud model.
You also do not want the small model to talk to itself for pages.

That is the job this study is about.

## Who it is for

1. **A student or a small team** writing easy or medium Python.
2. **A lab with one GPU.** A GPU is the chip that runs the model. Our models are about 0.8, 2, and 4 billion numbers. They fit on one Colab GPU.
3. **Someone who must keep code on their own machine.** A small model can run locally. The code does not have to leave the building.
4. **Someone choosing a setting before they pay for training.** Training costs time. The free settings already won here.

## Why people should use the free way

On the 2 billion model, stopping thinking at 1,024 tokens solved **49.8%** of answers.
Normal thinking solved **42.1%**.
The gap is **+7.7 points**.
The error bar is **[+4.3, +11.3]**.
It sits fully above zero, so the gap is proven on this test.

The trained add-on did not think shorter.
Its length was **x1.00** of normal thinking.
Its accuracy was **45.1%**.
The gain over normal thinking was **+3.0 points**, and that gain is not proven.

So the useful product is not a new trained model.
It is a simple rule: **cap the thinking, or turn it off.**

## Why this is efficient

A *token* is a small piece of text, about three quarters of a word.

| Way on the 2B model | Tokens per answer | Accuracy |
|---|---|---|
| Thinking OFF | **860** | 40.8% |
| Limit 1,024 | **2,722** | **49.8%** |
| Normal thinking | **3,446** | 42.1% |
| Trained add-on (LoRA-2) | **3,392** | 45.1% |

Thinking OFF uses about **4 times fewer tokens** than normal thinking (860 against 3,446).
Accuracy stays close.
The limit uses **21% fewer tokens** than normal thinking (2,722 against 3,446) and scores higher.

The saving is real because long answers were mostly **loops**.
The model repeated itself.
A limit stops that repeat.
Careful long thinking was not the main waste.
Finished answers were already short.
On HumanEval+, the middle finished thinking length was **672** tokens.

## Benefits

- **Higher accuracy for free** on the 2B and 4B models, by using a thinking limit.
- **Much cheaper answers** if you turn thinking off, with only a small accuracy drop on the 2B model.
- **No training step** for the winning way. You change one setting.
- **A size rule you can copy:** OFF on the tiny model, about 1,024 tokens on 2B, about 2,048 tokens on 4B.
- **Honest failure on hard-for-this-model problems.** Medium LiveCodeBench stayed near zero. You know not to trust these models there.

## Why not a giant model

```text
Easy Python on one GPU
        │
        ├─ Small model + thinking limit     fits, private, already strong on easy tasks
        └─ Giant model                      more machine, more tokens, code may leave your computer
```

**Small GPU.**
We ran 0.8B, 2B, and 4B on one Colab A100.
A giant model needs a much bigger machine.
For a school lab, that cost is the whole point.

**Easy problems.**
These tests are easy functions and easy or medium programs.
A 4B model with a 2,048-token thinking limit already reached **78.2%**.
A giant model would spend more time and money on problems this size can already attempt.
We did **not** test a model bigger than 4B.
We did **not** test hard contest problems.
On those, a bigger model may still be the right tool.

**Keep code private.**
If the model runs on your own computer, the source code stays with you.
A giant cloud model often means sending the problem out.
We did **not** run a security test.
We did **not** measure leaks or attacks.
This is advice from the setup, not a measured security result.

## What we checked, and what we did not

| Checked | Not checked |
|---|---|
| Accuracy and tokens on 234 code problems | Privacy attacks or secret leaks |
| Three sizes in one family (Qwen3.5) | Models bigger than 4B |
| Real benchmark tests, not a human reading the code | Hard problems and math |
| A free limit beats the trained add-on on each size | Every possible "think briefly" wording |
