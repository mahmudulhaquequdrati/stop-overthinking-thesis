# Shared draft supervision — available 4B CPU audit

## Current next step

The user confirms the original 2B training file, saved answers, and grades are unavailable.
Stop the 2B recovery attempt. Do not rerun the old source search.
The active Notebook 29 now audits the **available 73-example 4B training set**.
This is new evidence about 4B examples, not an explanation of the old 2B adapter.
A 4B data audit does not commit us to expensive 4B training.

Upload `29_shared_draft_cpu_audit.ipynb` directly into Google Colab.
Select **Hardware accelerator: None**, then **Run all**. Allow Drive access.
No Git push, repository clone, or file-selection prompt is needed.
Estimated time: **5–15 minutes**, not yet measured for this source.
The first cell stops if it detects an attached GPU.

Only this Drive input is required:

`MyDrive/stop-overthinking/results/4b/raw/train-set-lora1.jsonl`

Its name was found by the user's Drive search. Its bytes have not yet been checked there.
The notebook verifies it against the exact exported 4B file hash.
The saved 4B training-log summary is frozen in the notebook: 73 examples, three epochs, fraction 1.0.
No separate Drive loss file is required. Wrong or missing data gives a blocked report.

## What it checks

- Frozen exported training-file hash, count, unique IDs, and exact test-ID separation.
- Parsed Python draft-code groups inside thinking. No generated code is executed.
- Token shares and full sequence lengths using the pinned official 4B tokenizer.
- Shared group budgets, code revision retention, answer protection, and shifted label weights.

[Official tokenizer repository](https://huggingface.co/Qwen/Qwen3.5-4B), revision
`851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`, checked using the public model API.
Only tokenizer files are loaded; model weights are never downloaded.
Historical Unsloth tokenizer identity is unverified. Counts use this declared tokenizer.
A token crossing a code boundary retains ordinary reasoning supervision.
Unsupported languages and invalid blocks remain ordinary reasoning.
The answer's raw repetition modifier stays one; its mean-loss coefficient stays one.
EOS and the thinking-end marker remain protected answer supervision.

No-duplicate modifiers are identity. Full group normalization also changes phase/length weighting.
It needs a matched comparison later. Downweighting does not directly punish repetition.
The source hash matches an exported file, not a recorded training-time hash.
Exact ID separation cannot rule out paraphrased questions.

## What happens after the audit?

A preset **5% redundant-token-equivalent share of thinking** screens this dataset.
It measures discounted supervision, not predicted time savings or accuracy.
Below 5%: park this candidate before GPU work.
Above 5%: inspect useful repetitions and source limits before pricing any pilot.
Passing never starts or authorizes training automatically. Keep the 20-unit GPU reserve.

Outputs go into `MyDrive/stop-overthinking/shared-draft-audit/<run-id>/`.
`report.json` contains checks and aggregate counts. `audit.jsonl` contains per-example counts.
Send the downloaded ZIP here, then disconnect the CPU runtime.

## Checks and preservation

Updated notebook code cells parse. Earlier weight/label mathematical fixtures pass.
Actual 4B Drive bytes, tokenizer audit, and Colab timing remain untested.
No inference or training code was added. Old adapters and results stay untouched.
The previous 2B notebook and README are saved under
`backups/shared-draft-2b-source-audit-2026-10-14/` for undo.

## Earlier 2B blocked reports

- [First missing-source report](results/20261014T171223Z-856fbe43/report.json): 2.074 seconds; no GPU.
- [Drive discovery report](results/20261014T171743Z-871aa0fe/report.json): only 0.8B/4B candidates; no 2B source.

Neither produced data audit counts. Preserve them as missing-input results.
Decisions #128–#131. [Research note](../../research/2026-10-14-shared-draft-supervision.md).

## First 4B audit: parser correction required

The source and mathematical checks passed in run `20261014T173308Z-c83f4503`.
Wall time was 27.125 seconds after Drive setup; no GPU used.
But its reported 1.59% share skips indented draft-code blocks.
Do not apply the 5% screen to this incomplete count or park the candidate based on it.
Notebook 29 now uses indentation-aware parser v2. Opening/closing indentation must match.
Fixtures include four/eight spaces and tabs.
Read-only parser checks match the earlier broad audit across all 73 traces.
Corrected token percentages remain unmeasured. Upload the revised notebook and run Colab CPU.
[Preserved original report and correction](results/20261014T173308Z-c83f4503/README.md).
