# How we did it

We kept the model, the problems, and the rules the same.
Only the way of answering changed.
That is what makes the comparison fair.

## Everyday example

Six students sit the same exam.
Same questions.
Same time room.
One student is told "do not plan".
One may plan freely.
One is told "plan in one short note".
One must stop planning after one page.
Two studied from their own best short answers.
We mark every script with the same hidden tests.

## The model

| | |
|---|---|
| Main model | Qwen3.5-2B (`unsloth/Qwen3.5-2B`) |
| Also tested | Qwen3.5-0.8B and Qwen3.5-4B |
| Thinking switch | ON or OFF is a real setting, not only a sentence in the prompt |
| Computer | Google Colab A100 GPU |

We changed from an earlier Gemma plan to Qwen because the small Qwen models fit, they have a thinking switch, and the Colab tools could train them.
That choice is decision 53 in [../DECISIONS.md](../DECISIONS.md).

## The six ways (main 2B run)

```text
Same model, same 234 problems
        │
        ├─ 1. Thinking OFF
        ├─ 2. Thinking ON          ← what we compare against
        ├─ 3. "Think briefly"      ← one extra sentence
        ├─ 4. Thinking limit       ← stop notes at 1,024 tokens
        ├─ 5. LoRA-1               ← small early add-on
        └─ 6. LoRA-2               ← main trained add-on
```

Ways 1 to 4 are free.
Ways 5 and 6 need training.

**Why 1,024?**
In the small early test, the trained model thought for about 1,000 tokens.
The limit asks a fair question: is a hard cut as good as training?

**Why LoRA-2 is the main trained way?**
We named it **before** the run.
That stops us from picking whichever add-on looks better afterwards.

## How an answer is marked

```text
model text → take the last Python block → run the benchmark tests → pass or fail
```

An answer **passes only if it passes every test**.
One failed test means fail.
If thinking never finishes, there is no code, so that answer fails.
The tests run in a separate process with a time limit.
They never run inside the notebook.

Before we graded model answers, we graded the official correct solutions on 30 HumanEval+ problems and 20 MBPP+ problems.
They all passed.
So the checker itself was working.

**Accuracy** = answers that passed ÷ all answers.

Worked example for normal thinking on all 234 problems:

```text
234 problems × 2 tries = 468 answers
passed: 197
197 ÷ 468 = 42.1%
```

**Points** are the gap between two accuracies.
49.8% minus 42.1% is **+7.7 points**.
That is not "7.7 percent more" in the relative sense.
We always report points.

The error bars come from comparing the **same problems** before and after.
We resample problems 2,000 times with seed 3407.
If the bar does not include 0, we call the gap proven on this test.

## Fair rules, fixed before the run

| Rule | Value | Why |
|---|---|---|
| Same problems | all 234 | a paired comparison |
| Same token room | 4,096 on HumanEval+, 8,192 on LiveCodeBench | nobody gets extra room |
| Same sampling | temperature 0.6, top-p 0.95, top-k 20 | only the way changes |
| Same prompt | except one sentence for "think briefly" | |
| Tries | 2 on the main 2B run | the GPU budget |
| Seeds | fixed, try 1 uses 3407 | anyone can repeat it |
| Grading | the benchmark's own tests | not a human looking at code |
| Raw answers | saved word for word | re-grading is free |

We later gave normal thinking more room (16,384 tokens) on answers that had been cut off.
That check is in the results.
It shows the room limit did cost a little on easy functions.
It did not erase the limit's win.

## The small test before the real run

On 100 other easy MBPP+ problems, the early add-on scored **65%** against **50%** for normal thinking.
It also used **41% fewer tokens**.
That was a green light to run the real test.
The real test then asked whether the same trick works on **different** problems.

## What the later size runs changed

| | 0.8B | 2B main | 4B |
|---|---|---|---|
| Tries | 1 | 2 | 2 |
| Limits | 512 and 1,024 | 1,024, plus later 512 and 2,048 | 512, 1,024, 2,048, 4,096 |
| Trained add-on | LoRA-1 only | LoRA-1 and LoRA-2 | LoRA-1 only |
| "Think briefly" | not repeated | yes | not repeated |

The 2B limit of 2,048 is a lean fill-in with **1 try**.
Say that whenever you quote **46.6%**.
