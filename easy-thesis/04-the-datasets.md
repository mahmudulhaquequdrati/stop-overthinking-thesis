# The datasets, and how we checked them

<!-- CURRENT-STUDY:START -->

**Current study — 14 October 2026:** **464 unique test problems**.
Benchmarks: **164 HumanEval+**, **166 LiveCodeBench easy**, **134 LiveCodeBench medium**.
All six planned LoRA combinations are complete, one attempt per problem:

- **0.8B:** LoRA + OFF **14.0% (65/464)**; LoRA + limit 512 **14.4% (67/464)**.
- **2B:** LoRA + OFF **35.6% (165/464)**; LoRA + limit 1,024 **41.2% (191/464)**.
- **4B:** LoRA + OFF **64.7% (300/464)**; LoRA + limit 2,048 **71.6% (332/464)**.

LoRA alone means thinking ON without a thinking-token limit.
Older methods' all-attempt averages and first-attempt comparisons are labelled separately.
LoRA + OFF does not consistently improve on free OFF; the 2B/4B gains over free limits remain uncertain.

[Every method, benchmark, difficulty, token count and interval](../results/CURRENT-RESULTS.md) · [Full easy thesis](FULL-THESIS.md) · [Full formal Markdown thesis](../thesis/THESIS.md).

<!-- CURRENT-STUDY:END -->

The combined study has **464 distinct test problems**.
Training problems are not part of this total.

![Problem counts](figures/counts.svg)

| Dataset and difficulty | Problems |
|---|---|
| HumanEval+ easy functions | 164 |
| LiveCodeBench easy | 166 |
| LiveCodeBench medium | 134 |
| Total | 464 |


HumanEval+ asks for Python functions. LiveCodeBench includes contest programs and class methods.
There are no hard problems in this study.
We checked IDs across all collection lists and found no duplicate test problems.
The combined total is 164 function problems and 300 contest problems.

## The training set

Training problems are **not** the test problems.
LoRA-1 used a pool of **100** easy functions.
LoRA-2 used the bigger pool below.

| Pool | Problems | Why this pool |
|---|---|---|
| MBPP+ | 200 | Easy Python functions with strong tests. The early test showed they work. |
| Older LiveCodeBench | 80 (40 easy + 40 medium) | Older contest training problems from release v1. Distinct IDs were checked against the combined test set; dates alone do not establish separation. |

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

## Overlap and limitations

The combined audit compares all 464 test IDs with **280 saved training-pool IDs**.
Exact ID overlap is **zero**. It also checks IDs in saved training-answer and retained-example files.
The source list is in [the audit](../results/combined/results.json).
This update does not repeat a full text-similarity audit.
Different IDs can still hide related wording or equivalent tasks.

Earlier runs used function-name and 5-word text-overlap exclusions.
Those historical exclusions are preserved, not rewritten by this update.
We cannot prove the base model never saw these benchmarks during pretraining.
A problem's release date alone is not proof of unseen data.

## Completed LoRA controls

All six combinations are complete, with 464/464 results each.
0.8B: LoRA + OFF **14.0%**, LoRA + limit 512 **14.4%**.
2B: LoRA + OFF **35.6%**, LoRA + limit 1,024 **41.2%**.
4B: LoRA + OFF **64.7%**, LoRA + limit 2,048 **71.6%**.
These use one attempt per problem. Historical controls also have a labelled
first-attempt comparison; their all-attempt scores remain separate.
See [the completed analysis](11-completed-lora-controls.md) and [benchmark tables](05-results.md).
