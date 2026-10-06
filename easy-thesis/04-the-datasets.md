# The datasets, and how we checked them

We did not invent the problems.
We used public code tests, then checked that training problems were not copies of test problems.

## Everyday example

A teacher writes the exam in September.
The homework is from last year's book.
Before the exam, someone checks that no homework question is the same as an exam question.
If one is too close, it is thrown out.

That check is the overlap check.

## The test set (234 problems)

The list was **fixed on 2026-09-20**, before any score.

```text
234 test problems
 ├─ HumanEval+      164   easy     finish one Python function
 └─ LiveCodeBench    70   from February 2025 on
      ├─ easy         31           read input, print output (a few are class methods)
      └─ medium       39           the same job, harder
```

## Later lists, counted apart

The first exam stays 234.
Two later contest lists were marked on their own sheet.

![How many problems](figures/counts.svg)

| Pile | How many |
|---|---|
| First exam | 234 |
| Extra contest | 40 |
| More contest | 190 (118 easy, 72 medium) |
| Tests in total | **464** |
| LoRA-1 pool | 100 |
| LoRA-2 pool | 280, of which **157** were kept |

464 is a count. It is not one score.
The charts and the stats are in [10-all-counts.md](10-all-counts.md).

Hard LiveCodeBench problems were left out.
A 2 billion model solves almost none of them.
They could not show a difference between ways.

| Set | What the model must do | How a test works |
|---|---|---|
| HumanEval+ | Complete one function | A call such as `has_close_elements([1.0, 2.8, 3.0], 0.3)` plus the right result. HumanEval+ adds many more tests than the old HumanEval set. |
| LiveCodeBench | A full program, or a class method | An input text goes in. The program must print the exact output. We use up to 20 tests per problem. |

Time limits: 30 seconds for a HumanEval+ test program, 20 seconds per LiveCodeBench test.

The question text was the same for every way, except the one extra sentence for "think briefly".

```text
HumanEval+:    "Complete this Python function. Answer with one Python code block only,
                containing the complete function."  + the function to finish

LiveCodeBench: the problem text + "Write a complete Python program. It reads from
                standard input and prints the answer. Answer with one Python code block only."
                (class problems ask you to finish the given class instead)
```

## A real HumanEval problem

This is **HumanEval/0**, the first test problem.
The text below is copied from our saved answer file
`results/2026-09-24-thesis-run/test-off-he.jsonl`.
Thinking was OFF.
The model returned the function it was asked to finish, including the official description.

```python
from typing import List


def has_close_elements(numbers: List[float], threshold: float) -> bool:
    """ Check if in given list of numbers, are any two numbers closer to each other than
    given threshold.
    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)
    False
    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)
    True
    """
```

The examples in the quotes are part of the problem.
The hidden HumanEval+ tests are stricter.
An answer passes only if **every** test passes.
On the main 2B run, the limit, LoRA-1, and LoRA-2 each solved HumanEval/0 on both tries.
Normal thinking solved it on one try.
The full row is in [../results/full-results/FULL-RESULTS.md](../results/full-results/FULL-RESULTS.md).

## A real LiveCodeBench problem

The question body is **not stored in this git repo**.
It lives in the LiveCodeBench file the notebook downloads.
We can still show the problem we actually graded.

| | |
|---|---|
| Id | `lcb/3705` |
| Level | easy |
| Shape in our saved answer | a class method `largestInteger(self, nums, k)` |
| Date rule | test problems are from **after 31 January 2025** |
| Score on the main 2B run | **no way** solved it (0 of 2 tries each) |

That zero is useful.
It shows an easy label does not mean every model passes.
66 of the 234 problems were solved by no way at all.

The instruction we add is in `scripts/lcb_data.py`.
For a class problem it says: complete the given Python class, and answer with one code block.

## The training set

Training problems are **not** the test problems.
LoRA-1 used a pool of **100** easy functions.
LoRA-2 used the bigger pool below.

| Pool | Problems | Why this pool |
|---|---|---|
| MBPP+ | 200 | Easy Python functions with strong tests. The early test showed they work. |
| Older LiveCodeBench | 80 (40 easy + 40 medium) | Same kind of task as the LiveCodeBench exam, but from release v1, **before February 2025**, so they cannot be the test problems. |

```text
200 MBPP+  +  80 older LiveCodeBench  =  280 problems
        │
        ▼
4 thinking-ON tries each
        │
        ▼
keep the shortest correct answer
(never shorter than half the middle correct length)
        │
        ▼
157 training examples  →  LoRA-2
133 from MBPP+   +   24 from older LiveCodeBench
```

![Training data funnel](../results/full-results/figures/fig7-training-data-funnel.svg)

| | MBPP+ | Older LiveCodeBench |
|---|---|---|
| Problems | 200 | 80 |
| Answers (4 tries) | 800 | 320 |
| Correct answers | 357 (44.6%) | 44 (13.8%) |
| Kept examples | 133 | 24 |
| Middle thinking length of kept examples | 515 tokens | **4,709 tokens** |

The LiveCodeBench training examples were already long.
There was almost nothing short to learn there.
The kept length divided by the average correct length was **0.83** on MBPP+ and **0.99** on older LiveCodeBench.

LoRA-2 trained on those 157 examples for 3 passes.
That took about 6 minutes.
The loss fell from about 0.25 to about 0.16, so the add-on did learn the examples.
The later chapter explains why that still did not shorten test thinking.

## The overlap check

No test problem may appear in the training data.

The script `scripts/overlap_check.py` compares every training problem with every test problem.
It removes a training problem if:

- the function name is the same, or
- they share 30% or more of their 5-word pieces.

**Main 2B run.**
One training problem was removed after it had a correct answer: **`Mbpp/309`**.
That is the removal named in the full results page.

**Later size runs.**
The saved files `results/0.8b/raw/overlap-exclude.json`, `results/4b/raw/overlap-exclude.json`, `results/2b-limit512/raw/overlap-exclude.json`, and `results/2b-limit2048/raw/overlap-exclude.json` list four ids:

- `Mbpp/119`
- `Mbpp/309`
- `Mbpp/626`
- `Mbpp/99`

Those files belong to the later notebooks, not to a second story about the main run.
The main written result still names **`Mbpp/309`** as the problem removed from LoRA-2's kept set.

## What "valid" means here

| Check | Result |
|---|---|
| Test list fixed before scores | Yes, 2026-09-20, 234 problems |
| Train and test are different pools | Yes. MBPP+ and older LiveCodeBench versus HumanEval+ and LiveCodeBench from February 2025 on |
| Overlap script ran | Yes. Main run removed `Mbpp/309` |
| Grader checked on official solutions | Yes. 30 HumanEval+ and 20 MBPP+ official solutions passed |
| Answers judged by eye | No. Real tests only |
| Every test problem listed with scores | Yes, in the full results appendix |

We do **not** claim the model has never seen HumanEval or MBPP on the internet.
Qwen3.5 does not publish a cutoff date that would prove that.
The February 2025 LiveCodeBench cut is a **recent-problem** filter, not a proof the model has never seen the text.
