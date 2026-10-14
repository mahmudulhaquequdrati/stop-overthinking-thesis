# A different research direction — 14 October 2026

## 1. Where we are

PROBLEM → GAP → QUESTION → HYPOTHESIS. We have not tested a new method.

Park RPMR, the proposed memory repair method. Keep all notebooks and reports.
Its calculations work. Its useful effect on current model failures remains untested.
The live candidate finished normally twice. Do not chase more loops or replay prefixes now.
This supersedes the recommendation after Notebook 28, not its recorded results.

## Source correction after preparing Notebook 29

The current 2B LoRA-1 workflow used `results/mini/train-set.jsonl`.
Its saved lora100 training log records 35 examples, fraction 1.0, three epochs.
That training file is not present in this local repository. It must be read on Drive.
The 133/24 counts below describe different saved training sets, not this actual adapter set.
[Notebook 29 instructions](../experiments/shared-draft-supervision/README.md) check the actual source first.
No original training-time data hash was recorded; workflow linkage is not proof of unchanged bytes.

## 2. An observed issue in saved training examples

Some correct answers contain the same draft code several times inside thinking.
Imagine teaching a student the same draft three times before showing the final answer.
Our current training gives every copy a learning signal.
We can ask whether these copies deserve that much weight.

Read-only audit of saved selected-correct training examples:

- `results/2026-09-24-thesis-run/train-set-mbpp.jsonl`: 60 of 133 traces contain duplicate parsed code structures. There are 417 parseable thinking blocks and 3 unparseable blocks.
- `results/2026-09-24-thesis-run/train-set-lcb.jsonl`: 15 of 24 traces contain duplicate parsed code structures. There are 212 parseable thinking blocks and 15 unparseable blocks.

Method: read `completion` before the first `</think>`. Extract fenced blocks with
`r"```(?:python|py)?\s*\n(.*?)```"`, using DOTALL. Dedent each block.
Use `ast.parse`, then `ast.dump(..., include_attributes=False)` as the group key.
AST means a code structure tree. Parsing does not execute generated code.
A trace counts once when two parseable blocks have identical trees.
Unparseable blocks are counted separately, not silently discarded from training.

This ignores formatting and comments. It retains names, constants, and docstrings.
It does not prove semantic equivalence, uselessness, or harmful training effects.
Other fence languages are not explicitly filtered by this initial Python parser audit.
Confirm language tags and token spans before using it for loss weights.
These are saved training sets. Their exact mapping to each current adapter needs checking.
No benchmark tests were rerun. No GPU generation or training was performed.

## 3. Candidate: shared supervision for repeated drafts

Loss means the training score that tells the model what to learn.
LoRA changes a small set of trainable model weights using this score.
Change that calculation, rather than editing memory during generation.

Within each thinking trace, group code blocks with identical parsed trees.
Give each distinct group a shared loss budget, regardless of its copy count.
Keep revised code, reasoning prose, and the final answer supervised.
Do not remove thinking code from the input. It remains available as context.

One explicit candidate objective is:

`L = meanCE(answer) + lambda * meanCE(reasoning_prose) + mu * mean_g(mean_j(meanCE(block_gj)))`

CE measures next-token prediction error. Each `meanCE` averages over valid tokens.
Group `g` has `k_g` copies, so its inner mean gives each copy weight `1/k_g`.
The outer mean averages over distinct groups. Omit empty terms.
The final answer coefficient stays one. Set lambda and mu before any evaluation.
Unparseable code joins the ordinary reasoning term, with no repetition discount.
Token boundaries must respect shifted next-token labels and prompt masking.

This preserves each group's contribution when an identical copy is added.
It does not preserve gradients: identical code can occur in different contexts.
Downweighting repeated supervision also does not directly punish repeated generation.
Shorter thinking or higher accuracy is a hypothesis, not a mathematical consequence.

## 4. Closest papers and the possible gap

- [SCALe / Balanced Thinking](https://arxiv.org/abs/2603.18656) separates reasoning and answer learning weights. General loss balancing is already published. Compare against a matched length-balanced objective.
- [Disentangling Reasoning Tokens and Boilerplate Tokens](https://arxiv.org/abs/2412.14780) adapts token supervision by predictability. General selective token weighting is already published.
- [Pruning the Unsurprising / ASAP](https://arxiv.org/abs/2508.05988) compresses reasoning using structural alignment and surprisal. General removal of redundant thinking is already published.
- [Rethinking Repetition Problems / RPG](https://arxiv.org/html/2505.10402v1) studies code structure repetition and grammar-based decoding control. Structural repetition detection is already published.
- [OpenCodeReasoning](https://arxiv.org/html/2504.01943v1) section 2.3 excludes responses containing thinking code blocks. Simply filtering thinking code is already published.
- [Unlikelihood Training](https://arxiv.org/abs/1908.04319) reduces repetition using a training penalty. Training against repetition is already published.

Possible narrower contribution: normalize supervision across duplicate draft-code groups
inside reasoning, while keeping code revisions and final-answer supervision.
Target small hybrid reasoning models and compare against the same free thinking controls.
No exact match was found in this targeted search. That is not proof of novelty.
A publishable contribution requires useful results and a stronger literature review.
Renaming existing ideas or inventing an equation name is not enough.

## 5. Next step before paid training

Use a Colab CPU runtime for a tokenizer-only audit. No GPU model generation is needed.
First confirm the actual adapter training files and train/test separation.
Measure duplicate-token share, including truncation and code-language tags.
Check shifted labels, no-duplicate identity, and that final-answer weights stay one.
Record examples where repeated code is useful, not only obvious duplicates.
If the affected supervision is negligible, stop this candidate.

Before any GPU test, measure training step time on the chosen GPU.
Report projected setup, training, generation, and grading time separately.
Convert GPU time using Colab's live units/hour; keep the existing 20-unit reserve.
The four RPMR reports sum to about 1.049 estimated units, not verified billing.
Their repeated entered balance of 50 is not proof of the current balance.
No new spending ceiling is authorized by this note.

## 6. What the later experiment must answer

Question: Does duplicate-group weighting shorten thinking without losing code accuracy?
Hypothesis: repeated draft supervision partly teaches repeated draft generation.
Change: only the duplicate-group weights, under otherwise matched LoRA settings.
Measure: benchmark test passing, thinking tokens, repeated blocks, and wall time.
Data: training and development examples only for method choices; preserve the held-out test.
Comparisons: ordinary LoRA, matched phase/length balancing, and simple duplicate masking.
Also retain free OFF and thinking-limit controls from the thesis.
Use the same examples, optimization budget, prompts, and generation seeds.
Support: shorter reasoning with preserved accuracy, beyond the simpler comparisons.
Contradiction: accuracy drops, no reduction, or a simple comparison does equally well.
Start with 2B only if the CPU checks justify training. No 0.8B/4B sweep yet.

## 7. Change report

✚ This research note and Q&A explain the candidate and its limits.
✎ RPMR README and ROADMAP mark the old direction as parked.
✎ PLAN, DECISIONS, PAPERS, and GLOSSARY record this research-stage pivot.
No experiment code, model weights, completed thesis results, or backups were changed.
Read this note; there is no new notebook to run yet.

## Current source choice — user correction, Decision #131

The user confirms the original 2B set and its recovery inputs are unavailable.
End recovery. The active CPU audit now uses the available 73-example 4B training set.
This supersedes earlier recommendations to recover and audit the original 2B set.
It screens the new method's data basis and cannot explain the old 2B adapter.
It also does not choose the eventual training model or authorize expensive 4B training.
Source checks use the exported-file hash and frozen saved 4B training-log summary.
Token counts use the pinned [official 4B tokenizer](https://huggingface.co/Qwen/Qwen3.5-4B),
revision `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`.
Historical Unsloth tokenizer identity is unverified. Colab execution remains pending.

## First 4B token audit and correction — Decision #132

The source hash, 73-example count, exact ID checks, and loss-weight fixtures passed.
The 27.125-second CPU report found 12 duplicate traces and 1.5855% token-equivalent share.
Those counts are incomplete: parser v1 skipped fenced drafts indented beyond three spaces.
Indent-aware v2 retains matching indentation and includes four/eight spaces and tabs.
Read-only nonempty AST checks match the broad initial audit on all 73 examples:
238 parseable blocks, 27 duplicate traces, one invalid block.
The broad audit's 239 count included one empty parsed block, which v2 excludes.
No corrected tokenizer percentage exists yet. Keep the 5% screen unchanged and rerun CPU counting.
Do not claim either efficacy or candidate rejection from the first incomplete token audit.
