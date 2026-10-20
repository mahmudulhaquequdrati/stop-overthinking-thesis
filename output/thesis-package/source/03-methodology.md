# Chapter 3: Methodology

## 3.1 Overall Research Design

This is a retrospective computational study using saved model outputs and benchmark grades. The original experiments generated answers, graded them, and stored the associated settings. The present report combines those records without training models or generating new test answers. This distinction allows the report to be rebuilt locally while keeping the experimental evidence fixed.

The main unit is a unique coding problem. A problem can have one or more saved attempts for a given method, but extra attempts do not turn it into extra independent problems. The combined analysis first averages outcomes within each problem. It then gives each covered problem equal weight. A separate analysis compares first attempts on the same IDs when evaluating the completed LoRA controls.

The collection grew through an original set of 234 problems, a later group of 40, and a later group of 190. The final union has 464 distinct test IDs. The decision to combine the collections was made after their outcomes were available. This report therefore describes a retrospective combined view rather than a prospectively registered experiment with a single test date.

[[FIG:workflow]]

The design has two levels. At the experiment level, each configuration specifies a model, an add-on state, and a thinking policy. At the analysis level, the report specifies the covered IDs, attempt rule, outcome calculation, and uncertainty method. A result is interpretable only when both levels are known. For example, a 464-problem one-attempt score and a 234-problem two-attempt average cannot be ranked as if they were the same measurement.

## 3.2 Models and Software

The study uses Qwen3.5-0.8B, Qwen3.5-2B, and Qwen3.5-4B checkpoints. These are members of the same family, which reduces some variation in interface and model lineage. It does not make the sizes identical systems or isolate model size as the only changing factor. The results describe the specific checkpoints and saved configurations.

The saved completed-control environment records Python 3.13.15, PyTorch 2.9.1 with CUDA 12.8, Transformers 5.18.0, PEFT 0.21.1, Flash Linear Attention 0.5.2, and causal-conv1d 1.7.0. Model calculations used bfloat16. These values describe that recorded environment, not a requirement that every historical reference used the same package set. Full environment records remain alongside the raw runs.

Notebook 24 records an A100 80GB accelerator and requested a batch size of 128, with the possibility of reducing batches when needed. A batch request is not proof that every generated example was processed in the same batch shape. Since batch layout and numerical kernels can affect sampled outputs, the historical environment difference remains a limitation even where prompts and seeds match.

The adapter files record their model association, rank, scaling, and target modules. For the saved 0.8B and 4B LoRA-1 adapters, rank and alpha are both 16 and dropout is zero. These values are read from their configurations rather than assumed from a generic LoRA tutorial. The report preserves the distinction between adapters trained for different base models.

[[TABLE:software]]

## 3.3 Test Datasets and Collection

The complete test collection consists of 164 HumanEval+ tasks and 300 LiveCodeBench tasks. Of the contest tasks, 166 are labeled easy and 134 medium. The total is therefore 164 + 166 + 134 = 464. Each problem has a stable ID, allowing matching across methods and detection of duplicate entries. Counts are calculated on unique IDs rather than summed blindly from every file.

[[FIG:dataset]]

HumanEval+ generally asks the system to complete a Python function. LiveCodeBench tasks include contest-style programs and class methods. These interfaces require different forms of answer extraction and execution. The analysis preserves benchmark groups because interface and difficulty differences can influence observed performance. It does not attribute every group difference to algorithmic reasoning alone.

No hard contest tasks are included. This limits the population to which the findings can be applied. The selected easy and medium tasks are still informative about everyday code generation, but they do not establish that a control scales to advanced contests or large software repositories. The 464 problems are the measured collection, not a random draw from all possible programming work.

The saved audit reports no duplicated test IDs in the final union. This is a structural check, not a claim that every problem is semantically unrelated. Two distinct tasks may share an algorithm, and similar wording may occur across benchmarks. Such dependencies can reduce the diversity of the evaluation even when ID uniqueness is perfect.

## 3.4 Training Pools and Shortest Correct Selection

LoRA-1 begins from a pool of 100 easy function problems. For each practice problem, the procedure samples candidate answers with thinking enabled, checks correctness, and selects a short successful example where one is available. The retained example count can be smaller than the pool because some problems produce no passing candidate. The saved audit contains 37 retained LoRA-1 examples for 0.8B and 73 for 4B. These are model-specific retained sets, not the full pool size.

The historical LoRA-2 procedure uses a larger 280-problem pool: 200 MBPP+ function tasks and 80 older LiveCodeBench tasks, split into 40 easy and 40 medium. Four candidate attempts per problem produce 800 MBPP+ and 320 contest answers. The saved summary reports 357 correct MBPP+ candidates and 44 correct contest candidates. Selection retains 133 function examples and 24 contest examples, making 157 training examples in total.

[[FIG:training]]

The selection rule seeks the shortest correct candidate while applying the saved guard against choosing an answer shorter than half the middle correct length. The purpose is to avoid an extreme short target. This rule is part of the historical method and must not be quietly replaced by a different filtering procedure in the report. Where the saved experiment has only one successful candidate, there is correspondingly little freedom to choose a shorter successful strategy.

The retained LoRA-2 function examples have a median thinking length of 515 tokens, while the retained contest examples have a median of 4,709. The selected length divided by average correct length is reported as 0.83 for the function material and 0.99 for the older contest material. The latter leaves little measured compression in that training source. This describes the retained examples; it is not proof that no concise contest solution exists.

LoRA-2 trained for three passes over its 157 examples. The saved summary reports about six minutes of training and a loss decrease from about 0.25 to about 0.16. These historical values are approximate and have their original scope. They indicate that training fit changed, while the independent test results determine whether the desired response behavior transferred.

Training and test problems are kept separate in the ID audit. The audit compares 280 saved training-pool IDs with the final test IDs and also checks candidate and retained-example files. Exact overlap is zero. Earlier function-name and five-word exclusions remain part of the historical record. This report does not claim a newly completed semantic-overlap audit of all training and test text.

## 3.5 Inference Configurations

Thinking ON permits explicit notes until generation ends or the overall cap is reached. Thinking OFF asks for an answer without explicit thinking notes. A thinking limit stops the notes at the chosen budget and then allows answer generation. A brief prompt asks for concise reasoning through text instructions. These policies are distinct experimental conditions.

LoRA-1 alone means the saved add-on with thinking ON and no extra thinking-token limit. LoRA-1 plus OFF uses the same add-on with explicit thinking disabled. LoRA-1 plus limit uses the add-on with the selected budget. The completed budgets are 512 thinking tokens for 0.8B, 1,024 for 2B, and 2,048 for 4B. The numbers apply to thinking, not to the complete output.

The total output caps are 4,096 tokens for HumanEval+ and 8,192 for LiveCodeBench. A 512-token thinking limit can therefore be followed by several thousand answer tokens. This distinction helps explain why a model with limited thinking can still have a large total output. For example, a short note section does not prevent a long or repeated answer section.

Sampling uses temperature 0.6, top-p 0.95, top-k 20, and seed 3407 in the saved completed-control settings. These choices preserve stochastic generation rather than making every answer a deterministic greedy decode. The same seed is useful provenance, but it does not guarantee identical sampled answers after changing packages, batching, or hardware behavior.

Repeat stopping is enabled in the 0.8B and 4B extensions, while 2B retains its original handling. This is an important comparability limit. A cross-size chart is a summary of the actual systems tested, not an experiment that varies parameter count and holds all stopping behavior constant. Within-size paired comparisons remain useful, subject to their historical reference differences.

[[TABLE:policies]]

## 3.6 Answer Extraction and Grading

The saved generation pipeline produces text, from which runnable code is extracted. The grader then evaluates the extracted code in a separate process under time limits. A pass is recorded only when the code succeeds on every test actually used for that attempt. A missing answer, an execution failure, or an incorrect output is not converted into a successful sample by reading a persuasive explanation.

HumanEval+ uses the extended tests from its evaluation framework. The saved LiveCodeBench runs use up to 20 tests per problem. This means that the report's LiveCodeBench accuracy should not be described as performance on every hidden test available in the full benchmark. The testing cap is part of the operational definition of success in this study.

This document build reads grades rather than running model-generated programs. The approach supports repeatable reporting from the saved evidence. It also means the report does not independently verify every historical grader decision through new execution. The numerical audit checks structural consistency, source hashes where recorded, and recalculated summaries; it does not replace the original execution environment.

Code extraction is part of the measured system. A model can fail because it never reaches its final answer, because the extracted answer has the wrong interface, or because the code computes the wrong result. The aggregate pass/fail tables do not separately identify all of these causes. Causal explanations about failure type are therefore limited to analyses that actually inspect the relevant saved content.

## 3.7 Accuracy and Equal Problem Weight

Let y(i,j) be 1 when attempt j on problem i passes and 0 otherwise. Let n(i) be the number of available attempts on that problem. Its success fraction is p(i) = sum of y(i,j) divided by n(i). For a method with N covered problems, the combined accuracy is A = sum of p(i) divided by N. This gives each problem equal influence after its available attempts are summarized.

[[FIG:weighting]]

Consider an illustrative two-problem example. Problem A has one pass and one failure, so its fraction is 0.5. Problem B has a single passing attempt, so its fraction is 1.0. Equal problem weighting gives (0.5 + 1.0)/2 = 0.75. Pooling all attempts instead gives 2/3. The example is explanatory arithmetic, not a measured subset of the study.

Equal weighting addresses unequal contribution by problem. It does not make the uncertainty of a one-attempt problem identical to that of a repeatedly sampled problem, and it does not remove historical differences in sampling. The report uses it as a transparent summary rule rather than a cure for every feature of the collection. Attempt counts remain visible in result tables.

Coverage is the number of unique problems with results for that method. Missing problems are excluded from that method's summary and never counted as failures. For a direct comparison, the relevant set is the intersection of covered IDs. A higher percentage on a smaller, easier subset cannot establish a better score on the full 464-problem collection.

## 3.8 First Attempt Comparisons

Each completed LoRA combination has exactly one attempt per problem. To compare it with a historical control, the completed-control analysis uses that control's saved first attempt on the same IDs. This yields a clearly defined one-answer comparison. It avoids comparing a new single attempt with an older average and calling both values the same kind of single-shot score.

The all-attempt summary is retained because it uses the available repeated evidence. Its values may differ from first-attempt accuracy. For instance, 4B limit 2,048 is 71.9% in the equal-problem all-attempt view and 71.1% in the first-attempt reference. Both can be correct. The method name is the same, while the estimator and selected attempts differ.

The same distinction applies to 2B LoRA-1 alone: its all-attempt score is 34.4%, while the completed first-attempt comparison uses 34.9%. These differences are explained at the point of use. They must not be hidden as rounding or reconciled by replacing one estimator with another after looking at which result is more favorable.

## 3.9 Paired Uncertainty Analysis

The saved analyses use 2,000 bootstrap replicates with seed 3407. A bootstrap replicate samples whole problems with replacement from the relevant shared set and recomputes the statistic. For a difference, both methods stay attached to the same sampled problem. The 2.5th and 97.5th percentiles form the reported 95% interval.

[[FIG:bootstrap]]

Pairing is useful because a difficult problem can affect both methods. Comparing the methods on the same resampled IDs keeps that shared difficulty in the difference calculation. Sampling individual attempts as if they were unrelated problems would instead overstate the amount of independent information when attempts are repeated within a task.

These intervals describe variation over the observed problem collection under the saved procedure. They do not include all uncertainty from training seeds, future prompts, package changes, or a different distribution of programming work. They are also unadjusted for multiple comparisons and for choosing interesting methods after results were seen. A positive interval is evidence within this analysis, not a universal guarantee.

When an interval includes zero, the report calls the measured gain uncertain or inconclusive. That does not prove the methods are equivalent. Equivalence would require a prespecified acceptable margin and an appropriate design. When an interval excludes zero, the direction is reported along with the same retrospective and multiplicity limitations.

## 3.10 Tokens, Cap Hits, and Resource Reporting

Thinking tokens measure the explicit notes portion. Total new tokens measure the full generated response counted by the saved pipeline. OFF records zero thinking tokens but can still generate a long answer. A thinking limit is therefore evaluated against both components rather than assumed to control the total response perfectly.

Token summaries use the saved problem-based averaging convention. The report does not infer GPU speed from tokens alone. A larger model can take different time per token, and a different batch layout can change throughput. Training and candidate generation add an up-front resource requirement that is not captured by inference output length.

A cap hit is the saved indicator that an output reached the overall maximum. It does not by itself diagnose repetition. The original 234-problem analysis separately investigated loops in capped 2B outputs. Those values are reported as historical diagnostics. The full-coverage cap-rate figures show only the cap event measured for their corresponding configurations.

Notebook 24's ledger estimates about 57.0 Colab units for its five runs. This is a local record of that extension, not a complete project cost statement. It excludes the earlier 2B combination and other work. The number must not be converted into hours without a stated rate, or described as an externally verified bill.

## 3.11 Validation and Reproducibility

Validation begins with IDs. Each completed configuration must contain the expected 464 unique IDs, exactly one raw answer per ID, and a corresponding grade. Unexpected IDs or duplicate attempts would invalidate a simple 464-denominator calculation. The completed archive checks report that these structural conditions are satisfied.

The next layer checks model settings, thinking policy, adapter hashes, raw/graded token agreement, and the historical reference manifests. These checks reduce the risk of labeling one run as another. Hashes establish identity of files, not scientific correctness of their contents. They must be interpreted as provenance controls rather than proof that a model answer is right.

The numerical layer recalculates percentages and paired differences from the saved records. This thesis builds its tables and plots from the checked JSON summaries and records their source hashes in the delivery package. Assertions verify the main sample counts and completed-combination pass totals. The appendices identify the source files and local reproduction commands.

The reporting layer checks whether text, figures, and tables use the same estimator and denominator. It also checks whether a result from a partial method is labeled with its actual coverage. This is a scientific validation step because inconsistent captions can create a false claim even when every number was copied correctly.

## 3.12 Chapter Summary

The methodology uses fixed saved evidence, unique problem IDs, clearly defined estimators, and paired uncertainty intervals. Its strongest comparisons are those with matched problems and explicit attempt rules. Its main limitations are retrospective selection, historical environment differences, restricted benchmark coverage, and incomplete measurement of resource costs. Chapter 4 presents the numerical outcomes under these definitions.
