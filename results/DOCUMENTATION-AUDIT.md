# Complete thesis Markdown audit — 14 October 2026

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

[Every method, benchmark, difficulty, token count and interval](CURRENT-RESULTS.md) · [Full easy thesis](../easy-thesis/FULL-THESIS.md) · [Full formal Markdown thesis](../thesis/THESIS.md).

<!-- CURRENT-STUDY:END -->

The earlier update did not update every older thesis document. This audit closes that gap.
Both full Markdown theses, aggregate results and model summaries now use the checked 464-problem study.
Historical notes show current results and explicitly retain their earlier scope.
Every saved method, benchmark and difficulty appears in [the current tables](CURRENT-RESULTS.md).
Partial methods remain partial; missing answers are not invented or scored as failures.

## Coverage of this audit

**160 Markdown files reviewed**, including this audit.


- Current theses and result tables: rebuilt or synchronized.
- Earlier Q&A, proposals, lessons and run notes: current notice plus explicit historical/teaching scope.
- Eight downloaded run reports: immutable original evidence, checked against archived hashes.
- `CLAUDE.md`: project instructions, preserved.
- `DECISIONS.md`: append-only; the current change is recorded in decision 113.
- PDF/HTML files are outside this Markdown update and remain older exports.

The [dated original snapshot](../archive/2026-10-14-before-complete-md-sync/markdown-originals.tar.gz)
contains all 157 Markdown documents present before synchronization.
Raw JSONL, CSV, weights and downloaded reports were not edited.
The older 234-problem loop/LoRA-2 analyses and pilot are retained with their true scope.

## Every file and its disposition

| Markdown file | How it is handled |
|---|---|
| [CLAUDE.md](../CLAUDE.md) | Instruction file; preserved, not a results document |
| [DECISIONS.md](../DECISIONS.md) | Append-only decision log; current update in decision 113 |
| [GLOSSARY.md](../GLOSSARY.md) | Current results/chapter/index; synchronized and linked |
| [PAPERS.md](../PAPERS.md) | Current results/chapter/index; synchronized and linked |
| [PLAN.md](../PLAN.md) | Current results/chapter/index; synchronized and linked |
| [README.md](../README.md) | Current results/chapter/index; synchronized and linked |
| [ROADMAP.md](../ROADMAP.md) | Current results/chapter/index; synchronized and linked |
| [TEACHER-A-TO-Z.md](../TEACHER-A-TO-Z.md) | Current results/chapter/index; synchronized and linked |
| [easy-thesis/00-one-page.md](../easy-thesis/00-one-page.md) | Current results/chapter/index; synchronized and linked |
| [easy-thesis/01-who-should-use-it.md](../easy-thesis/01-who-should-use-it.md) | Current results/chapter/index; synchronized and linked |
| [easy-thesis/02-the-problem.md](../easy-thesis/02-the-problem.md) | Current results/chapter/index; synchronized and linked |
| [easy-thesis/03-how-we-did-it.md](../easy-thesis/03-how-we-did-it.md) | Current results/chapter/index; synchronized and linked |
| [easy-thesis/04-the-datasets.md](../easy-thesis/04-the-datasets.md) | Current results/chapter/index; synchronized and linked |
| [easy-thesis/05-results.md](../easy-thesis/05-results.md) | Current results/chapter/index; synchronized and linked |
| [easy-thesis/06-why-it-works.md](../easy-thesis/06-why-it-works.md) | Current results/chapter/index; synchronized and linked |
| [easy-thesis/07-advice-and-limits.md](../easy-thesis/07-advice-and-limits.md) | Current results/chapter/index; synchronized and linked |
| [easy-thesis/08-all-answers.md](../easy-thesis/08-all-answers.md) | Current results/chapter/index; synchronized and linked |
| [easy-thesis/09-extra-problems.md](../easy-thesis/09-extra-problems.md) | Current results/chapter/index; synchronized and linked |
| [easy-thesis/10-all-counts.md](../easy-thesis/10-all-counts.md) | Current results/chapter/index; synchronized and linked |
| [easy-thesis/11-completed-lora-controls.md](../easy-thesis/11-completed-lora-controls.md) | Current results/chapter/index; synchronized and linked |
| [easy-thesis/FULL-THESIS.md](../easy-thesis/FULL-THESIS.md) | Current results/chapter/index; synchronized and linked |
| [easy-thesis/PAPER.md](../easy-thesis/PAPER.md) | Current results/chapter/index; synchronized and linked |
| [easy-thesis/README.md](../easy-thesis/README.md) | Current results/chapter/index; synchronized and linked |
| [easy-thesis/WORDS.md](../easy-thesis/WORDS.md) | Current results/chapter/index; synchronized and linked |
| [lessons/00-what-is-a-thesis.md](../lessons/00-what-is-a-thesis.md) | Historical/teaching/research context retained; current results and scope added |
| [lessons/01-what-is-an-llm.md](../lessons/01-what-is-an-llm.md) | Historical/teaching/research context retained; current results and scope added |
| [lessons/02-tokens.md](../lessons/02-tokens.md) | Historical/teaching/research context retained; current results and scope added |
| [lessons/03-how-a-model-learns.md](../lessons/03-how-a-model-learns.md) | Historical/teaching/research context retained; current results and scope added |
| [lessons/04-reasoning-models-and-thinking.md](../lessons/04-reasoning-models-and-thinking.md) | Historical/teaching/research context retained; current results and scope added |
| [lessons/05-overthinking.md](../lessons/05-overthinking.md) | Historical/teaching/research context retained; current results and scope added |
| [lessons/06-cutoff-dates.md](../lessons/06-cutoff-dates.md) | Historical/teaching/research context retained; current results and scope added |
| [lessons/07-gpu-memory.md](../lessons/07-gpu-memory.md) | Historical/teaching/research context retained; current results and scope added |
| [lessons/08-python-basics.md](../lessons/08-python-basics.md) | Historical/teaching/research context retained; current results and scope added |
| [lessons/09-colab-and-kaggle.md](../lessons/09-colab-and-kaggle.md) | Historical/teaching/research context retained; current results and scope added |
| [lessons/10-hugging-face.md](../lessons/10-hugging-face.md) | Historical/teaching/research context retained; current results and scope added |
| [lessons/11-first-model-call.md](../lessons/11-first-model-call.md) | Historical/teaching/research context retained; current results and scope added |
| [proposal/proposal.md](../proposal/proposal.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/01-choosing-the-topic.md](../qa/01-choosing-the-topic.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/02-finding-the-gap.md](../qa/02-finding-the-gap.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/03-code-only-easy-and-medium.md](../qa/03-code-only-easy-and-medium.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/04-choosing-the-model.md](../qa/04-choosing-the-model.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/05-data-and-test-size.md](../qa/05-data-and-test-size.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/06-method-hypothesis-baselines.md](../qa/06-method-hypothesis-baselines.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/07-one-question-only.md](../qa/07-one-question-only.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/08-safety-checks-before-training.md](../qa/08-safety-checks-before-training.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/09-gpu-time-and-free-sessions.md](../qa/09-gpu-time-and-free-sessions.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/10-proposal-and-title.md](../qa/10-proposal-and-title.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/11-measuring-thinking-in-tokens.md](../qa/11-measuring-thinking-in-tokens.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/12-how-our-training-works.md](../qa/12-how-our-training-works.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/13-thinking-and-the-switch.md](../qa/13-thinking-and-the-switch.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/14-overthinking.md](../qa/14-overthinking.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/15-cutoff-dates-and-seen-tests.md](../qa/15-cutoff-dates-and-seen-tests.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/16-gpu-memory.md](../qa/16-gpu-memory.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/17-free-gpus-and-notebooks.md](../qa/17-free-gpus-and-notebooks.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/18-hugging-face-and-our-data.md](../qa/18-hugging-face-and-our-data.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/19-first-model-call.md](../qa/19-first-model-call.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/20-first-model-load-out-of-memory.md](../qa/20-first-model-load-out-of-memory.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/21-first-real-numbers.md](../qa/21-first-real-numbers.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/22-pilot-on-the-mac.md](../qa/22-pilot-on-the-mac.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/23-moving-to-colab-and-qwen.md](../qa/23-moving-to-colab-and-qwen.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/24-free-go-no-go-test.md](../qa/24-free-go-no-go-test.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/25-mini-thesis-and-learning-curve.md](../qa/25-mini-thesis-and-learning-curve.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/26-mini-thesis-results.md](../qa/26-mini-thesis-results.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/27-the-real-thesis-run.md](../qa/27-the-real-thesis-run.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/28-thesis-run-results.md](../qa/28-thesis-run-results.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/29-results-and-analysis-chapter.md](../qa/29-results-and-analysis-chapter.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/30-the-complete-thesis.md](../qa/30-the-complete-thesis.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/31-size-limit-extension.md](../qa/31-size-limit-extension.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/32-4b-run.md](../qa/32-4b-run.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/33-all-models-compared.md](../qa/33-all-models-compared.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/34-lean-0.8b-plan.md](../qa/34-lean-0.8b-plan.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/35-0.8b-run.md](../qa/35-0.8b-run.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/36-size-extension-in-thesis.md](../qa/36-size-extension-in-thesis.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/37-thesis-a-to-z-teacher.md](../qa/37-thesis-a-to-z-teacher.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/38-2b-limit512-fill.md](../qa/38-2b-limit512-fill.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/39-2b-limit2048-lean.md](../qa/39-2b-limit2048-lean.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/40-easy-thesis.md](../qa/40-easy-thesis.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/41-extra-problems.md](../qa/41-extra-problems.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/42-more-problems.md](../qa/42-more-problems.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/43-more-scores.md](../qa/43-more-scores.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/44-combined-464.md](../qa/44-combined-464.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/45-lora-with-limit-notebook.md](../qa/45-lora-with-limit-notebook.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/46-notebook21-readable-setup.md](../qa/46-notebook21-readable-setup.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/47-notebook21-torchao-failure.md](../qa/47-notebook21-torchao-failure.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/48-lora1-missing40.md](../qa/48-lora1-missing40.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/49-five-lora-controls.md](../qa/49-five-lora-controls.md) | Historical/teaching/research context retained; current results and scope added |
| [qa/50-completed-lora-controls.md](../qa/50-completed-lora-controls.md) | Current results/chapter/index; synchronized and linked |
| [qa/51-all-markdown-current.md](../qa/51-all-markdown-current.md) | Current results/chapter/index; synchronized and linked |
| [qa/README.md](../qa/README.md) | Current results/chapter/index; synchronized and linked |
| [research/2026-09-17-part2-tool-checks.md](../research/2026-09-17-part2-tool-checks.md) | Historical/teaching/research context retained; current results and scope added |
| [research/2026-09-20-e2b-mlx-option.md](../research/2026-09-20-e2b-mlx-option.md) | Historical/teaching/research context retained; current results and scope added |
| [research/2026-09-20-qwen-small-models.md](../research/2026-09-20-qwen-small-models.md) | Historical/teaching/research context retained; current results and scope added |
| [research/2026-09-20-which-gemma-model.md](../research/2026-09-20-which-gemma-model.md) | Historical/teaching/research context retained; current results and scope added |
| [research/2026-09-25-bigger-model-plan.md](../research/2026-09-25-bigger-model-plan.md) | Historical/teaching/research context retained; current results and scope added |
| [research/2026-09-25-bigger-models-and-loops-evidence.md](../research/2026-09-25-bigger-models-and-loops-evidence.md) | Historical/teaching/research context retained; current results and scope added |
| [research/2026-10-14-lora-limit-notebook.md](../research/2026-10-14-lora-limit-notebook.md) | Historical/teaching/research context retained; current results and scope added |
| [research/data-size-and-test-size.md](../research/data-size-and-test-size.md) | Historical/teaching/research context retained; current results and scope added |
| [research/datasets.md](../research/datasets.md) | Historical/teaching/research context retained; current results and scope added |
| [research/gaps.md](../research/gaps.md) | Historical/teaching/research context retained; current results and scope added |
| [research/gpu-time-budget.md](../research/gpu-time-budget.md) | Historical/teaching/research context retained; current results and scope added |
| [research/models-and-gpu.md](../research/models-and-gpu.md) | Historical/teaching/research context retained; current results and scope added |
| [results/0.8b/RUN.md](0.8b/RUN.md) | Historical/teaching/research context retained; current results and scope added |
| [results/0.8b/SUMMARY.md](0.8b/SUMMARY.md) | Current results/chapter/index; synchronized and linked |
| [results/0.8b/raw/lora/lora1/README.md](0.8b/raw/lora/lora1/README.md) | Historical/teaching/research context retained; current results and scope added |
| [results/2026-09-19-notebook11-first-call.md](2026-09-19-notebook11-first-call.md) | Historical/teaching/research context retained; current results and scope added |
| [results/2026-09-19-notebook11-out-of-memory.md](2026-09-19-notebook11-out-of-memory.md) | Historical/teaching/research context retained; current results and scope added |
| [results/2026-09-20-e2b-mlx-on-mac.md](2026-09-20-e2b-mlx-on-mac.md) | Historical/teaching/research context retained; current results and scope added |
| [results/2026-09-20-pilot-e2b-humaneval.md](2026-09-20-pilot-e2b-humaneval.md) | Historical/teaching/research context retained; current results and scope added |
| [results/2026-09-22-mini-thesis-first-results.md](2026-09-22-mini-thesis-first-results.md) | Historical/teaching/research context retained; current results and scope added |
| [results/2026-09-22-t4-speed-first-run.md](2026-09-22-t4-speed-first-run.md) | Historical/teaching/research context retained; current results and scope added |
| [results/2026-09-24-thesis-run.md](2026-09-24-thesis-run.md) | Historical/teaching/research context retained; current results and scope added |
| [results/2026-09-24-thesis-run/lora/lora2/README.md](2026-09-24-thesis-run/lora/lora2/README.md) | Historical/teaching/research context retained; current results and scope added |
| [results/2b-limit2048/RUN.md](2b-limit2048/RUN.md) | Historical/teaching/research context retained; current results and scope added |
| [results/2b-limit2048/SUMMARY.md](2b-limit2048/SUMMARY.md) | Historical/teaching/research context retained; current results and scope added |
| [results/2b-limit512/RUN.md](2b-limit512/RUN.md) | Historical/teaching/research context retained; current results and scope added |
| [results/2b-limit512/SUMMARY.md](2b-limit512/SUMMARY.md) | Historical/teaching/research context retained; current results and scope added |
| [results/4b/RUN.md](4b/RUN.md) | Historical/teaching/research context retained; current results and scope added |
| [results/4b/SUMMARY.md](4b/SUMMARY.md) | Current results/chapter/index; synchronized and linked |
| [results/4b/raw/lora/lora1/README.md](4b/raw/lora/lora1/README.md) | Historical/teaching/research context retained; current results and scope added |
| [results/ALL-RESULTS.md](ALL-RESULTS.md) | Current results/chapter/index; synchronized and linked |
| [results/CURRENT-RESULTS.md](CURRENT-RESULTS.md) | Current results/chapter/index; synchronized and linked |
| [results/DOCUMENTATION-AUDIT.md](DOCUMENTATION-AUDIT.md) | Complete Markdown inventory and validation report |
| [results/HOW-TO-RUN-SIZE-EXTENSION.md](HOW-TO-RUN-SIZE-EXTENSION.md) | Historical/teaching/research context retained; current results and scope added |
| [results/RESULTS-INDEX.md](RESULTS-INDEX.md) | Current results/chapter/index; synchronized and linked |
| [results/SIZE-COMPARISON.md](SIZE-COMPARISON.md) | Current results/chapter/index; synchronized and linked |
| [results/combined/README.md](combined/README.md) | Current results/chapter/index; synchronized and linked |
| [results/extra/LISTS.md](extra/LISTS.md) | Historical/teaching/research context retained; current results and scope added |
| [results/extra/SUMMARY.md](extra/SUMMARY.md) | Historical/teaching/research context retained; current results and scope added |
| [results/full-results/FULL-RESULTS.md](full-results/FULL-RESULTS.md) | Current results/chapter/index; synchronized and linked |
| [results/lora-controls/README.md](lora-controls/README.md) | Current results/chapter/index; synchronized and linked |
| [results/lora-controls/completed-464/0.8b/lora1-limit512/SUMMARY.md](lora-controls/completed-464/0.8b/lora1-limit512/SUMMARY.md) | Immutable downloaded report; original scope, current parent-page links |
| [results/lora-controls/completed-464/0.8b/lora1-off/SUMMARY.md](lora-controls/completed-464/0.8b/lora1-off/SUMMARY.md) | Immutable downloaded report; original scope, current parent-page links |
| [results/lora-controls/completed-464/2b/lora1-off/SUMMARY.md](lora-controls/completed-464/2b/lora1-off/SUMMARY.md) | Immutable downloaded report; original scope, current parent-page links |
| [results/lora-controls/completed-464/4b/lora1-limit2048/SUMMARY.md](lora-controls/completed-464/4b/lora1-limit2048/SUMMARY.md) | Immutable downloaded report; original scope, current parent-page links |
| [results/lora-controls/completed-464/4b/lora1-off/SUMMARY.md](lora-controls/completed-464/4b/lora1-off/SUMMARY.md) | Immutable downloaded report; original scope, current parent-page links |
| [results/lora-limit-2b/2026-10-14-failure.md](lora-limit-2b/2026-10-14-failure.md) | Historical/teaching/research context retained; current results and scope added |
| [results/lora-limit-2b/README.md](lora-limit-2b/README.md) | Current results/chapter/index; synchronized and linked |
| [results/lora-limit-2b/completed-464/SUMMARY.md](lora-limit-2b/completed-464/SUMMARY.md) | Immutable downloaded report; original scope, current parent-page links |
| [results/lora-missing40/PLAN.md](lora-missing40/PLAN.md) | Historical/teaching/research context retained; current results and scope added |
| [results/lora-missing40/README.md](lora-missing40/README.md) | Current results/chapter/index; synchronized and linked |
| [results/lora-missing40/completed40/2b/SUMMARY.md](lora-missing40/completed40/2b/SUMMARY.md) | Immutable downloaded report; original scope, current parent-page links |
| [results/lora-missing40/completed40/4b/SUMMARY.md](lora-missing40/completed40/4b/SUMMARY.md) | Immutable downloaded report; original scope, current parent-page links |
| [results/mini/lora/lora100/README.md](mini/lora/lora100/README.md) | Historical/teaching/research context retained; current results and scope added |
| [results/mini/lora/lora25/README.md](mini/lora/lora25/README.md) | Historical/teaching/research context retained; current results and scope added |
| [results/mini/lora/lora50/README.md](mini/lora/lora50/README.md) | Historical/teaching/research context retained; current results and scope added |
| [results/more/LISTS.md](more/LISTS.md) | Historical/teaching/research context retained; current results and scope added |
| [results/more/RUN.md](more/RUN.md) | Historical/teaching/research context retained; current results and scope added |
| [results/more/SUMMARY.md](more/SUMMARY.md) | Historical/teaching/research context retained; current results and scope added |
| [thesis/00-front-matter.md](../thesis/00-front-matter.md) | Current results/chapter/index; synchronized and linked |
| [thesis/01-introduction.md](../thesis/01-introduction.md) | Current results/chapter/index; synchronized and linked |
| [thesis/02-background.md](../thesis/02-background.md) | Current results/chapter/index; synchronized and linked |
| [thesis/03-method.md](../thesis/03-method.md) | Current results/chapter/index; synchronized and linked |
| [thesis/04-how-we-measure.md](../thesis/04-how-we-measure.md) | Current results/chapter/index; synchronized and linked |
| [thesis/05-results.md](../thesis/05-results.md) | Current results/chapter/index; synchronized and linked |
| [thesis/06-analysis.md](../thesis/06-analysis.md) | Current results/chapter/index; synchronized and linked |
| [thesis/07-conclusion-and-future-work.md](../thesis/07-conclusion-and-future-work.md) | Current results/chapter/index; synchronized and linked |
| [thesis/08-references.md](../thesis/08-references.md) | Current results/chapter/index; synchronized and linked |
| [thesis/09-appendices.md](../thesis/09-appendices.md) | Current results/chapter/index; synchronized and linked |
| [thesis/README.md](../thesis/README.md) | Current results/chapter/index; synchronized and linked |
| [thesis/THESIS.md](../thesis/THESIS.md) | Current full formal thesis; rebuilt from all updated chapters |

## Validation

Run `python3 scripts/sync_thesis_markdown.py --check`.
It checks inventory coverage, current notices, all six combination scores, source-table consistency,
local current-document links, immutable report hashes, and the formal/easy results match.
The current dataset has 464 unique test IDs, with zero exact overlap against saved training IDs.
Generated code and model inference were not executed during this documentation work.
