# Measurement and uncertainty

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

[Every method, benchmark, difficulty, token count and interval](../results/CURRENT-RESULTS.md) · [Full easy thesis](../easy-thesis/FULL-THESIS.md) · [Full formal Markdown thesis](THESIS.md).

<!-- CURRENT-STUDY:END -->

## How accuracy is calculated

For each problem, count the share of its attempts that passed.
Then average those shares across covered problems.

```text
Problem A: 1 pass from 2 attempts → 0.5
Problem B: 1 pass from 1 attempt  → 1.0
Combined accuracy: (0.5 + 1.0) / 2 = 75%
```

Pooling the three attempts would give 66.7%. That would give A twice the weight.
Our combined score gives each problem equal weight.
We do not average rounded percentages from the old summaries.

Coverage means unique problems with results. A missing result is not counted as a failure. Only compare scores directly when they use the same problems.

## Tests and uncertainty

An answer passes when it passes every test actually used by the saved grader.
HumanEval+ used its extended tests. LiveCodeBench used up to 20 tests per problem.
Thus these results do not establish success on every available LiveCodeBench hidden test.
Generated code was checked in a separate process with time limits.
This update reads scores only; it does not execute generated code.

For a comparison, use the intersection of both methods' problem IDs.
Resample whole problems 2,000 times with seed 3407.
The reported 95% intervals are percentile bootstrap intervals.
Both methods remain paired on each sampled problem; attempts are not independent problems.
Intervals reflect variation across problems, not all training or generation randomness.
They are unadjusted for multiple comparisons and post-result method selection.

## A retrospective combined view

The 464 problems came from several runs with different attempt counts.
The original 234 were selected before their results; later collections added 40 and 190.
We chose to combine them on 13 October 2026, after seeing results.
This history matters for interpreting claims, but it does not prevent a labelled combined summary.
Raw results remain unchanged. The pre-update Markdown files are preserved in
[the dated archive](../archive/2026-10-14-before-complete-md-sync/markdown-originals.tar.gz).
The formal Markdown thesis now uses the same checked 464-problem results.

Source: [combined results](../results/combined/README.md), calculated from saved graded answers. No model was run again.

## Completed LoRA controls

All six combinations are complete, with 464/464 results each.
0.8B: LoRA + OFF **14.0%**, LoRA + limit 512 **14.4%**.
2B: LoRA + OFF **35.6%**, LoRA + limit 1,024 **41.2%**.
4B: LoRA + OFF **64.7%**, LoRA + limit 2,048 **71.6%**.
These use one attempt per problem. Historical controls also have a labelled
first-attempt comparison; their all-attempt scores remain separate.
See [the completed analysis](../easy-thesis/11-completed-lora-controls.md) and [benchmark tables](../easy-thesis/05-results.md).


# Words used in this folder

Each word is used in the easy thesis.
The longer list is [../GLOSSARY.md](../GLOSSARY.md).

| Word | Meaning |
|---|---|
| Token | A small piece of text, about three quarters of a word. The model writes one token at a time. |
| Thinking | Notes the model writes to itself before the code. Thinking uses tokens and time. |
| Thinking ON | The normal way. The model may think as long as the token room allows. |
| Thinking OFF | The switch is off. The model writes the answer with no thinking notes. |
| Thinking limit | We stop the thinking notes at a fixed length, then the model must answer. |
| Think briefly | We add one sentence that asks for short thinking. |
| LoRA | A small trained add-on. The big model stays frozen. |
| LoRA-1 | The add-on from the small early test (easy problems only). |
| LoRA-2 | The add-on from the main 2B run. This was the main trained way, chosen before we saw scores. |
| Accuracy | Average of each problem’s share of passing attempts. |
| Pass | The code passes every test for that problem. One failed test means fail. |
| Points | The gap between two accuracies. 40% minus 30% is +10 points. |
| Error bar | An uncertainty interval from resampling problems; it does not prove a universal result. |
| Cut off | The saved output reached its cap. The grader still determines whether extracted code passes. |
| Loop | The model repeats the same lines until the room runs out. |
| Dataset | A fixed list of problems, with tests. |
| Overlap | A training problem that is too close to a test problem. We remove those. |
| Median | The middle value after you sort the numbers. A few huge answers do not pull it up. |
| GPU | The chip that runs the model. We used a Google Colab A100. |
| 0.8B / 2B / 4B | About 0.8, 2, or 4 billion numbers inside the model. Bigger usually means stronger and heavier. |
| Coverage | How many unique problems have results for one method. |
| Retrospective | Chosen after the results were available. |
| Equal problem weight | Each problem contributes equally, even when attempt counts differ. |
| Paired comparison | Compare two methods on exactly the same problems. |
| Bootstrap | Repeat the calculation on resampled problems to estimate uncertainty. |
