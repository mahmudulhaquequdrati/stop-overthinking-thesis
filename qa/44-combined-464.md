# Combined 464-problem easy thesis

## Completed result and next step — 14 October 2026

**Qwen3.5-2B + LoRA-1 + thinking limit 1,024: 41.2% (191/464).**
All 464 problems were generated and graded, one attempt each.
Limit alone: 38.6% on the same 464 first attempts.
Gap: +2.6 points; 95% interval −1.5 to +6.7. The gain remains inconclusive.
On 424 shared first attempts: combination 43.9%, LoRA-1 alone 38.0%.
Earlier all-attempt LoRA-1 accuracy is 37.4%; keep the weighting labels.
The v2 ledger records 20.51 estimated units under the 45-unit ceiling.

Next planned work: **2B LoRA-1 alone on the missing 40, then 4B LoRA-1 alone on the same 40**.
No training or rerun of their existing 424 answers. Other missing methods are outside scope.
Results are not available yet; new combined scores will be added after grading.
[Completed evidence](../results/lora-limit-2b/README.md) · [Exact missing IDs and plan](../results/lora-missing40/PLAN.md).


## The step in two sentences

We combined saved grades into one 464-problem view, with equal weight per problem.
We updated the easy thesis and kept missing coverage visible, without using Colab.

## What did we change and why?

The user wanted one study total, rather than three separate headline stories.
The complete-coverage free controls score 14.7% (0.8B OFF), 38.6% (2B limit 1,024),
and 71.9% (4B limit 2,048).

## Why not simply pool attempts?

Some problems have two attempts; others have one.
Pooling attempts would give extra weight to the former.
We average each problem's passing fraction, then average across problems.

## What happens to missing runs?

Nothing is guessed. 2B and 4B LoRA-1 each cover 424/464 problems.
We restrict their comparisons to the same 424 IDs for both methods.
LoRA-2 retains its original 234-problem coverage.

## Does a free control beat LoRA on every model?

Its observed score is higher on shared problems for each size.
The 0.8B interval includes zero; the 2B interval is narrowly positive.
The 4B interval is positive. These are unadjusted retrospective comparisons.

## Was this one preselected exam?

No. The collection history remains in a methods note.
The combined view was chosen after seeing results.

## Checked versus not checked

Checked: 464 distinct IDs; collection lists are disjoint; no duplicate attempt keys;
zero exact overlap with 280 saved training-pool IDs; original headline counts reconcile.
Calculated: per-problem accuracy and token means; paired problem-bootstrap intervals.
Not redone: model calls, grading, full text-similarity audit, loop detection, or the formal thesis.
No Colab units were spent.

## Where it is written

[Combined audit](../results/combined/README.md), [easy paper](../easy-thesis/PAPER.md),
[method](../easy-thesis/03-how-we-did-it.md), and Decision 101.

## What to do next

Review the combined easy thesis before choosing a new training experiment.
