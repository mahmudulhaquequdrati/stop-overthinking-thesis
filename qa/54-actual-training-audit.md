# 54 — Actual 2B training-data audit

We prepared Notebook 29 for a Colab CPU audit.
It reads training data and checks loss weights without loading a model.

## Why another source check?

The current 2B LoRA-1 workflow used 35 examples, according to its saved log.
The earlier 133 MBPP and 24 LCB examples came from different saved sets.
We cannot use those counts as proof about this adapter's training data.

## What goes in and comes out?

Inputs: original Drive train-set.jsonl and lora100/loss.json from Notebook 13.
Outputs: report.json and per-example audit.jsonl in a new Drive folder, plus a downloaded ZIP.
A missing source produces a blocked report, not a replacement dataset.

## What calculations are checked?

Repeated parsed draft groups share their code-loss budget.
Distinct revisions remain separate. Final-answer supervision is protected.
Labels and weights both shift by one position for next-token prediction.
Prompt labels are ignored. Unsupported or invalid code stays ordinary reasoning.
No generated code is executed.

## Does passing mean our method works?

No. It only checks data prevalence and mathematical compatibility.
A 5% screen is a planning choice, not statistical evidence or a training authorization.
Useful repetitions need review. The original file has no historical training-time hash.
Exact ID separation does not prove absence of paraphrased questions.

## What is checked versus untested?

Checked: notebook syntax and small mathematical fixtures.
Untested: Colab setup, actual Drive sources, tokenizer mapping, runtime, and efficacy.
The 5–15 minute CPU estimate remains unmeasured.

## What next?

Choose CPU/None, upload Notebook 29, Run all, and send the downloaded ZIP.
No GPU training yet. Decision #128.
[Run instructions](../experiments/shared-draft-supervision/README.md).

## What happened in the first real run?

The report is blocked: the original training file is missing from the expected Drive path.
The training log exists. The run stopped after 2.074 seconds without GPU use.
This is a missing-input result, not a failed hypothesis or completed data audit.
Notebook 29 now lists possible Drive sources with a bounded search.
Choose only the original file; other saved training sets must not be substituted.
The search logic parses here; revised discovery has not run in Colab.
[Saved report](../experiments/shared-draft-supervision/results/20261014T171223Z-856fbe43/report.json).

## Did Drive discovery find the 2B file?

No. The second report lists only 0.8B and 4B training sets.
The bounded search reports completion after 69 directories and 10.212 seconds.
Total run time, including waiting for input, is 219.397 seconds. No GPU used.
Do not substitute these files or rerun the same search.
Check the original mini/train-answers.jsonl and mini/train-answers-graded.csv next.
They may support CPU reconstruction using saved grades, without new model generation.
A reconstructed source would need its own provenance and cannot prove original byte identity.

## What if the original 2B recovery files do not exist?

The user confirms they do not. Stop the recovery attempt.
We changed the active CPU audit to the available 73-example 4B training set.
It checks the exported-file hash and uses the frozen saved 4B training-log summary.
The official 4B tokenizer is pinned. No model weights are loaded.
No Drive search or path prompt remains. The previous notebook and README are backed up.
This checks a new hypothesis on available data, not the old 2B adapter's behavior.
A data audit does not authorize 4B training. Actual Colab checks remain pending.
Decision #131.
