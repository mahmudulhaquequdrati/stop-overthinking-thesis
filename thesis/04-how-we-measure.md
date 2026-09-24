# 4. How We Measure: Where the Evidence Comes From

Every number in this thesis comes from one of the steps below. This chapter explains each step with a small worked
example, so anyone can check our numbers by hand.

```text
answer text ─► take out the code ─► run the tests ─► PASS or FAIL ─► accuracy ─► compare two ways ─► error bar
     └──────► count tokens (thinking / answer) ─► cost ─► cut off? loop?
```

## 4.1 Step 1: take the code out of the answer

The model's answer is text. We look for the **last Python code block** in the answer part (the text after the
end-of-thinking marker `</think>`). That code is what we test.

If the model never reached `</think>`, there is **no answer part**, so there is no code to test. That answer is a
**fail** (Section 4.9).

## 4.2 Step 2: run the benchmark's own tests

We never judge code by reading it. We **run** it against the benchmark's own tests:

| | HumanEval+ | LiveCodeBench |
|---|---|---|
| What a test is | A call like `has_close_elements([1.0, 2.8, 3.0], 0.3)` with the correct result | An input text fed to the program, and the exact output it must print |
| Which tests | All of HumanEval+'s tests (the original ones extended *"by 80x"*, Liu et al., 2023) | The problem's public and hidden tests; we use up to **20** per problem to keep grading fast |
| How output is compared | The test program checks the result itself | Line by line, ignoring spaces at the end of lines |
| Time limit | 30 seconds for the whole test program | 20 seconds per test |

**Safety.** The code runs in a **separate process**, in a temporary folder, with the time limit. It never runs inside
our notebook.

## 4.3 Step 3: the pass rule

> **An answer PASSES only if it passes EVERY test.** One failed test = FAIL.

An answer fails if any of these happen:

| Why it failed | Real example from our data |
|---|---|
| Wrong result on a test | `wrong answer on test 1` (the most common reason: 337 times) |
| The code crashes | `NameError: name 'List' is not defined` (a missing import) · `SyntaxError: invalid syntax` |
| The code is too slow | `timeout` (13 times in all 2,808 answers) |
| No code at all (cut off) | the answer never finished thinking; the test then can't find the function, e.g. `NameError: name 'separate_paren_groups' is not defined` |

This is strict, and the same for every way.

## 4.4 Step 4: checking the checker

A broken checker would make every number wrong. So **before** grading any model answer, the notebook graded the
benchmarks' **official correct solutions** for 30 HumanEval+ and 20 MBPP+ problems. All had to pass, or the run would
stop. They all passed.

## 4.5 Accuracy

> **Accuracy = answers that passed ÷ all answers**

**Worked example (thinking ON, all 234 problems):**

```text
234 problems × 2 tries = 468 answers
passed: 197
accuracy = 197 ÷ 468 = 0.421 = 42.1%
```

Every problem has exactly 2 tries, so every problem counts equally.

## 4.6 Points, not percent

When we compare two accuracies, we use **percentage points** ("points"):

```text
Thinking limit 49.8%  −  Thinking ON 42.1%  =  +7.7 points
```

This is **not** "+7.7 percent". In relative terms, 7.7 ÷ 42.1 is an 18% improvement. We always report **points**,
because they are simpler and cannot be inflated by a small starting value.

## 4.7 Comparing on the same problems ("paired")

Some problems are easy and some are hard. If one way happened to get easier problems, it would look better for no real
reason. So we always compare two ways **on the same problems**, one problem at a time.

For each problem, each way's score is the share of its 2 tries that passed (0, ½ or 1). Then:

```text
Problem         Thinking ON   Thinking limit   difference (points)
HumanEval/12    1/2 = 50%     2/2 = 100%        +50
HumanEval/40    0/2 = 0%      0/2 = 0%            0
lcb/3705        0/2 = 0%      1/2 = 50%         +50
...             ...           ...               ...
average over all 234 problems                   +7.7 points
```

(The three rows are made-up examples to show the idea. The +7.7 is the real average.)

## 4.8 Error bars: is the difference real, or luck?

With only 234 problems and 2 tries each, some difference can appear just by luck. An **error bar** (a 95% interval)
shows how big the difference could reasonably be.

We compute it with the **bootstrap**, a method that uses the data itself:

```text
1. Take our 234 problems.
2. Draw 234 problems AT RANDOM from them, WITH replacement
   (so some problems appear twice and some not at all).
3. Compute the average difference on this new set.
4. Repeat 2,000 times.  → 2,000 slightly different averages
5. Sort them. The 50th and the 1,950th values are the error bar (the middle 95%).
```

**Tiny example with 5 problems.** Differences: +50, 0, 0, +100, −50. Average = +20.

```text
random draw 1:  +50, +50,   0, −50, +100  → average +30
random draw 2:    0,   0, −50, −50,   0   → average −20
random draw 3: +100, +50, +100,  0,   0   → average +50
... 2,000 draws ... sort ... keep the middle 95%
```

With only 5 problems the draws jump around a lot, so the error bar would be very wide. With 234 problems it is much
narrower.

**The rule we use:**

> If the whole error bar is **above 0**, the way is **proven better** on this test set.
> If it is **below 0**, it is proven worse. If it **includes 0**, we cannot tell.

**Real example:** thinking limit vs ON = **+7.7 [+4.3, +11.3]**. The whole bar is above 0, so the limit is proven better.
LoRA-2 vs ON = **+3.0 [−1.1, +7.3]**. The bar includes 0, so we cannot say LoRA-2 is better.

The random draws use a fixed **seed** (3407), so running the script again gives exactly the same error bars.

## 4.9 Counting tokens, and "cut off"

We count tokens with the model's own tokenizer:

```text
[ thinking tokens ........ ] </think> [ answer tokens ]
         thinking                            answer part
|───────────────────── all tokens ──────────────────────|
```

- **Thinking tokens:** everything before `</think>`.
- **Answer part:** everything after it.
- **All tokens:** both together. This is the real cost, because the model has to write all of it.

**Cut off.** Every way had the same overall limit: 4,096 tokens (HumanEval+) or 8,192 (LiveCodeBench). If an answer
reaches the limit before it ends, it is **cut off**. If it was still thinking, **all** its tokens count as thinking and
there is no code, so it **fails**. The rule is the same for every way.

## 4.10 The thinking ratio

To compare thinking length, we divide:

```text
thinking ratio = total thinking tokens of a way  ÷  total thinking tokens of thinking ON   (same problems)
```

- **x1.00** = the same as ON.
- **x0.75** = 25% shorter (the target in hypothesis H1).
- **x0.26** = 74% shorter.

It gets an error bar in the same way as accuracy (Section 4.8).

**Watch out:** the thinking limit stops thinking at 1,024 tokens, but the model can keep reasoning inside its answer
part. So for the limit we also report **all tokens**, which gives the honest saving (Chapter 5.3).

## 4.11 Median: the middle value

A few very long answers can pull an average up a lot. So we also report the **median**: sort all the values and take
the middle one.

```text
lengths 500, 600, 700, 800, 4,096   → average 1,339,  median 700
```

We use the median of **finished** answers (not cut off) to show how long normal, successful thinking is.

## 4.12 Finding loops

To check whether a cut-off answer is a **loop**, we use a simple rule:

> Take a piece of the answer's **last 200 characters**. If that exact piece already appears **at least twice** earlier
> in the same answer, the answer is a loop.

```text
"... I'll track opening and closing parentheses ... [same text] ... [same text] ... [same text]"
                                                                     ▲ last 200 characters
                                                                       also found twice earlier → LOOP
```

This rule is **strict**. It misses loops where the model repeats with small changes. So our loop counts are a **lower
bound**: the real number is probably higher.

## 4.13 Better or worse, problem by problem

For each problem we also ask: did a way solve **more** of its 2 tries than thinking ON, **fewer**, or the **same**?
Counting problems gives a simple picture that doesn't depend on averages (Chapter 5.6).

## 4.14 Checking whether the token limit was fair ("stage D")

A fixed limit might cut off long but useful thinking. To test this, we took every thinking-ON answer from try 1 that was
cut off, and ran it again with **16,384** tokens, four times the room. If many of them then finish and pass, the limit
was unfair to thinking ON. Chapter 5.7 gives the answer.

## 4.15 GPU time

We also record how long the GPU took. Each batch of answers has a measured time, which we share equally among its answers.
But a batch waits for its **slowest** answer, so GPU time mostly reflects how we grouped answers. That is why we use
**tokens**, not minutes, as the measure of cost.

## 4.16 Where every number comes from

| Evidence | File |
|---|---|
| Every raw answer, word for word (thinking + code) | `results/2026-09-24-thesis-run/test-*.jsonl` |
| Every grade (passed, why not, tokens, cut off) | `results/2026-09-24-thesis-run/test-*-graded.csv` |
| Error bars printed by the run | `results/2026-09-24-thesis-run-step12-output.txt` |
| All tables, charts and problem lists | `results/full-results/FULL-RESULTS.md` |
| The scripts that compute them | `scripts/compare_thesis.py`, `scripts/make_full_results.js`, `scripts/check_thesis_run.js` |

Anyone can re-grade or re-count everything from the raw answers, without a GPU.
