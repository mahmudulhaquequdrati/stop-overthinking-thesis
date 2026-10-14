# 52. RPMR research and Colab smoke check

RPMR is a proposed internal memory repair, not a validated improvement.
Its execution workflow is now Colab-only, as the user requested.

**What could be new?** Online repair of temporary DeltaNet memory with constraints
protecting selected current-prompt readouts. Related projection and steering mathematics
already exist; the specific combination still needs novelty review and real results.

**What is the next test?** A calculation and cache-compatibility smoke check on Colab.
It captures real query directions, edits one cached head, and checks a short continuation.

**Does it test loop recovery?** No. The smoke edit is forced. It checks plumbing.
**Does it run benchmark code?** No. Generated code is never executed here.
**Does it train LoRA?** No. It loads the official Qwen3.5-2B model without adapters.

**How much compute?** About 50 units remain. Keep 20. Smoke ceiling: five estimated units.
At the historical 6.77 A100 units/hour that allows about 44 minutes.
Planning estimate: 10–30 minutes; actual cost and speed are unmeasured.

**What is checked here?** Notebook JSON and code syntax. No Colab cells ran yet.
**What about the earlier local checks?** They are historical, archived and removed
from the active workflow. They do not establish GPU compatibility or model accuracy.

**Can we undo?** Yes. The verified 795-file baseline and removed-file archives remain
in backups/. Existing model workers and scored results were preserved.

**What should the user do?** Upload the notebook to Colab, choose GPU, and Run all.
The notebook asks for live resources, saves report.json on Drive and attempts disconnection.
If the report says failed, keep the report and stop before the larger pilot.

[Colab notebook and instructions](../experiments/rpmr/README.md).
[Research proposal](../experiments/rpmr/proposal.md). Decisions #114–118; previous Q&A files archived.

## First Colab smoke result

The user supplied a passing report: 107.826 seconds and estimated 0.2028 units.
The real cache edit changed next-token scores; selected immediate readout error was about 1.50e-9.
This establishes compatibility on that runtime, not better answers or loop escape.
Original Drive file, actual billing and disconnection were not independently checked.
[Saved pasted report](../experiments/rpmr/results/20261014T125828Z-bf30149f/report.json). Decision #119.

## What comes after the passed smoke?

Notebook 26 adds online exact-repeat detection and conditional RPMR, plus a detection-only control.
Ordinary and detection-only outputs must match. It measures the full detector/logging overhead.
Two prompts and short caps make this an instrumentation check, not an accuracy study.
Three estimated units maximum; keep 20. No repair is forced if no natural trigger occurs.
User confirms the earlier runtime is disconnected. Notebook 26 is prepared but not run.
[Next notebook](../experiments/rpmr/26_rpmr_colab_online_smoke.ipynb). Decision #120.

## Did Notebook 26 prove loop recovery?

No. All six responses reached 384 tokens, with no detected episode or online edit.
Detection-only matched ordinary output according to the worker. This validates basic instrumentation.
A short cap can miss later loops. The uploaded report contains no raw answer text.
Next: inspect answers.jsonl from the ZIP before choosing longer generation.
[Saved report](../experiments/rpmr/results/20261014T131227Z-2ff3a723/report.json). Decision #121.

## What do the uploaded answers show?

Ordinary, detection-only and RPMR outputs are identical for each question.
Even-sum thinking ends; the token cap truncates its final answer. Substring thinking
contains code and begins reconsideration, but no exact cycle appears in the saved prefix.
A reconsideration sentence alone does not establish harmful overthinking. Code was not graded.
Next: only that substring question with a longer detection-only cap in Notebook 27,
within two estimated units. No repair is forced or automatically evaluated. Decision #122.

## What did the longer run establish?

Notebook 27 finishes naturally at 1,300 tokens. It repeats the same thinking code
block twice, separated by prose, then gives its answer. The detector requires three
adjacent repeated short token blocks, so this is outside its rule. It is redundant
reasoning, not evidence of endless looping. Code was not executed or graded.
Next: inspect saved training traces rather than keep rerunning the same question.
[Report](../experiments/rpmr/results/20261014T133535Z-da04a204/report.json). Decision #123.

## Where can we find stronger loop examples?

Saved 2B training generations contain candidates. Word-cycle screening finds 15 attempts.
Three inspected cases repeat reconsideration until a cap without thinking closure.
This is stronger than the substring example, which finishes naturally.
The token detector must be calibrated; historical sampled loops may not reproduce under
current greedy decoding. Keep development candidates separate from final evaluation.
No extra GPU run was needed for this inspection. Decision #124.

## Why Notebook 28?

Mbpp/568 previously looped in saved training generation. Its exact question is available
and its ID is absent from the 464 evaluation tasks. The new detector checks a range of
period lengths, not just three selected lengths, while retaining persistent-repeat requirements.
It must recognize the archived positive trace and reject the completed substring trace.
Then two bounded live tries test reproduction; no artificial prefix or repair is used.
Historical sampling, batch layout and model provenance differ, so reproduction is not guaranteed.
Three estimated units maximum. Return the ZIP before evaluating recovery. Decision #125.
