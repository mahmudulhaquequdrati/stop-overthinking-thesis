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
