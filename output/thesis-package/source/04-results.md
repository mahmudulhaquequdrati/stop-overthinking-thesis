# Chapter 4: Results

## 4.1 Reading the Results

This chapter reports measurements before interpreting their possible causes. The full-coverage tables use equal problem weighting across available attempts. The completed-control tables identify first-attempt comparisons explicitly. Every full-coverage row covers 464 unique problems. Partial sweeps and historical diagnostics appear separately with their original scope.

The checked result summaries supply the numeric values used in this chapter. Percentages are rounded only for display. A rounded percentage multiplied by a denominator may not recover an integer pass total in the all-attempt view because individual problem scores can be fractions. Integer passed counts are therefore given only where the configuration has one answer per problem.

The 95% intervals use the saved problem bootstrap procedure. They do not correct for multiple comparisons or for selection after viewing results. Where an interval on a difference includes zero, the result is described as uncertain. All token counts refer to generated output, not to elapsed time or billed cost.

[[FIG:accuracy]]

## 4.2 Full Coverage Results for 0.8B

Table [[TABREF:full-0.8b]] reports the six complete configurations for Qwen3.5-0.8B. All use the same 464 problem IDs, while the number of saved attempts varies by historical method. The table states the attempt total, accuracy, percentile interval, and mean total output tokens. It is the all-attempt equal-problem summary, rather than a first-attempt ranking.

[[TABLE:full-0.8b]]

Unrestricted ON records 4.1% accuracy and 6,206 mean total tokens. OFF records 14.7% and 1,781 tokens. The selected free limit of 512 thinking tokens records 10.6% and 5,920 total tokens. These values describe complete response lengths, so the total can exceed the stated thinking budget.

LoRA alone records 12.3% with 464 saved attempts on the 464 problems. LoRA plus OFF records 14.0%, while LoRA plus the selected limit records 14.4%. Both combinations have 464 attempts, one per problem. Their results can be read as integer counts in the completed-combination table later in this chapter.

The table does not establish a universal winner. It lists the measured policies on the complete collection. A decision about whether training helps needs the corresponding paired comparison and its attempt rule, rather than a subtraction between arbitrary rows. The benchmark breakdown in Figure [[FIGREF:groups0.8b]] shows how the combined result is distributed across task groups.

[[FIG:groups0.8b]]

[[TABLE:groups-0.8b]]

Within HumanEval+, the highest observed value among these six complete methods is 26.8% for LoRA + Limit  512. The lowest is 10.4% for ON. This is a descriptive comparison within 164 problems, not a separate set of experiments. Ties and uncertainty can make an ordered ranking less informative than the displayed values themselves.

Within LiveCodeBench easy, the highest observed value among these six complete methods is 15.7% for OFF. The lowest is 0.6% for ON. This is a descriptive comparison within 166 problems, not a separate set of experiments. Ties and uncertainty can make an ordered ranking less informative than the displayed values themselves.

Within LiveCodeBench medium, the highest observed value among these six complete methods is 1.5% for LoRA + Limit  512. The lowest is 0.0% for OFF. This is a descriptive comparison within 134 problems, not a separate set of experiments. Ties and uncertainty can make an ordered ranking less informative than the displayed values themselves.

The small medium-task percentages deserve attention alongside the combined 0.8B score. A policy can increase success on functions while leaving contest performance very limited. The benchmark interfaces and task demands differ, so these group results locate the weakness without isolating its cause. The overall uncertainty interval is not a subgroup interval.

## 4.3 Full Coverage Results for 2B

Table [[TABREF:full-2b]] reports the six complete configurations for Qwen3.5-2B. All use the same 464 problem IDs, while the number of saved attempts varies by historical method. The table states the attempt total, accuracy, percentile interval, and mean total output tokens. It is the all-attempt equal-problem summary, rather than a first-attempt ranking.

[[TABLE:full-2b]]

Unrestricted ON records 26.8% accuracy and 5,331 mean total tokens. OFF records 31.8% and 1,337 tokens. The selected free limit of 1,024 thinking tokens records 38.6% and 4,337 total tokens. These values describe complete response lengths, so the total can exceed the stated thinking budget.

LoRA alone records 34.4% with 698 saved attempts on the 464 problems. LoRA plus OFF records 35.6%, while LoRA plus the selected limit records 41.2%. Both combinations have 464 attempts, one per problem. Their results can be read as integer counts in the completed-combination table later in this chapter.

The table does not establish a universal winner. It lists the measured policies on the complete collection. A decision about whether training helps needs the corresponding paired comparison and its attempt rule, rather than a subtraction between arbitrary rows. The benchmark breakdown in Figure [[FIGREF:groups2b]] shows how the combined result is distributed across task groups.

[[FIG:groups2b]]

[[TABLE:groups-2b]]

Within HumanEval+, the highest observed value among these six complete methods is 60.4% for Limit 1024. The lowest is 47.3% for OFF. This is a descriptive comparison within 164 problems, not a separate set of experiments. Ties and uncertainty can make an ordered ranking less informative than the displayed values themselves.

Within LiveCodeBench easy, the highest observed value among these six complete methods is 49.4% for LoRA + Limit  1024. The lowest is 18.4% for ON. This is a descriptive comparison within 166 problems, not a separate set of experiments. Ties and uncertainty can make an ordered ranking less informative than the displayed values themselves.

Within LiveCodeBench medium, the highest observed value among these six complete methods is 7.5% for LoRA + Limit  1024. The lowest is 2.2% for LoRA alone. This is a descriptive comparison within 134 problems, not a separate set of experiments. Ties and uncertainty can make an ordered ranking less informative than the displayed values themselves.

The 2B results show a substantial separation between function tasks and medium contest tasks. That separation remains visible after adding the trained controls. A user whose workload consists mainly of contest programs should inspect those columns before applying a conclusion from the combined score. No unreported subgroup significance test is inferred here.

## 4.4 Full Coverage Results for 4B

Table [[TABREF:full-4b]] reports the six complete configurations for Qwen3.5-4B. All use the same 464 problem IDs, while the number of saved attempts varies by historical method. The table states the attempt total, accuracy, percentile interval, and mean total output tokens. It is the all-attempt equal-problem summary, rather than a first-attempt ranking.

[[TABLE:full-4b]]

Unrestricted ON records 50.0% accuracy and 5,188 mean total tokens. OFF records 66.5% and 943 tokens. The selected free limit of 2,048 thinking tokens records 71.9% and 3,921 total tokens. These values describe complete response lengths, so the total can exceed the stated thinking budget.

LoRA alone records 56.8% with 698 saved attempts on the 464 problems. LoRA plus OFF records 64.7%, while LoRA plus the selected limit records 71.6%. Both combinations have 464 attempts, one per problem. Their results can be read as integer counts in the completed-combination table later in this chapter.

The table does not establish a universal winner. It lists the measured policies on the complete collection. A decision about whether training helps needs the corresponding paired comparison and its attempt rule, rather than a subtraction between arbitrary rows. The benchmark breakdown in Figure [[FIGREF:groups4b]] shows how the combined result is distributed across task groups.

[[FIG:groups4b]]

[[TABLE:groups-4b]]

Within HumanEval+, the highest observed value among these six complete methods is 86.9% for Limit 2048. The lowest is 78.7% for OFF. This is a descriptive comparison within 164 problems, not a separate set of experiments. Ties and uncertainty can make an ordered ranking less informative than the displayed values themselves.

Within LiveCodeBench easy, the highest observed value among these six complete methods is 86.1% for LoRA + Limit  2048. The lowest is 56.6% for ON. This is a descriptive comparison within 166 problems, not a separate set of experiments. Ties and uncertainty can make an ordered ranking less informative than the displayed values themselves.

Within LiveCodeBench medium, the highest observed value among these six complete methods is 38.1% for LoRA + Limit  2048. The lowest is 4.5% for ON. This is a descriptive comparison within 134 problems, not a separate set of experiments. Ties and uncertainty can make an ordered ranking less informative than the displayed values themselves.

The 4B model succeeds more often across the displayed groups, but the medium contest tasks remain harder under the tested policies. The group comparison also shows that an advantage on one benchmark need not have the same size on another. These descriptive values use the existing grades and do not add new tests or establish a causal explanation.

## 4.5 Completed LoRA Combinations with One Attempt

All six planned combinations are finished. Each has one raw answer and one grade for every problem. Five configurations come from Notebook 24 and the 2B limit combination comes from the earlier Notebook 21. This section reports the common one-attempt denominator directly. It does not average the completed-combination scores with older attempts.

[[TABLE:completed]]

The totals are 65 and 67 passes for 0.8B, 165 and 191 for 2B, and 300 and 332 for 4B, ordered as OFF then limit. The denominator is the same in every case. These counts establish completion and observed outcomes; they do not by themselves measure an improvement over the untrained policy.

The 2B limit combination has the largest observed complete-set accuracy among the tested 2B configurations. The 4B limit combination passes 332 problems and the 0.8B limit combination passes 67. The following paired comparisons determine whether these observations establish a gain beyond their corresponding free controls.

## 4.6 Matched First Attempt Comparisons

This section uses historical first attempts for the references. The control table and forest plot therefore use a different attempt selection from the earlier all-attempt tables. The 4B free limit is 330/464, or 71.1%, in this view. Its 71.9% all-attempt score is not substituted into this first-attempt difference.

[[TABLE:first]]

[[FIG:forest]]

For 0.8B LoRA + OFF, the difference from OFF is -0.6 percentage points, with a paired 95% interval of [-3.2, 2.2] points. The comparison uses 464 shared problems and the first-attempt reference. The interval includes zero, so a reliable accuracy gain is not established.

For 0.8B LoRA + Limit  512, the difference from Limit 512 is +3.9 percentage points, with a paired 95% interval of [0.6, 7.1] points. The comparison uses 464 shared problems and the first-attempt reference. The interval excludes zero in the positive direction under this unadjusted analysis.

For 2B LoRA + OFF, the difference from OFF is +3.0 percentage points, with a paired 95% interval of [-0.6, 6.9] points. The comparison uses 464 shared problems and the first-attempt reference. The interval includes zero, so a reliable accuracy gain is not established.

For 2B LoRA + Limit  1024, the difference from Limit 1024 is +2.6 percentage points, with a paired 95% interval of [-1.5, 6.7] points. The comparison uses 464 shared problems and the first-attempt reference. The interval includes zero, so a reliable accuracy gain is not established.

For 4B LoRA + OFF, the difference from OFF is -1.7 percentage points, with a paired 95% interval of [-5.6, 1.9] points. The comparison uses 464 shared problems and the first-attempt reference. The interval includes zero, so a reliable accuracy gain is not established.

For 4B LoRA + Limit  2048, the difference from Limit 2048 is +0.4 percentage points, with a paired 95% interval of [-3.0, 3.7] points. The comparison uses 464 shared problems and the first-attempt reference. The interval includes zero, so a reliable accuracy gain is not established.

The 2B trained limit exceeds the trained OFF policy by 5.6 points, with an interval of +1.1 to +9.9. This compares two trained configurations. It is evidence about the thinking policy used with the add-on, not proof of the benefit of training over an untrained model.

For 4B, the trained limit has two more passes than the free-limit first attempt. The corresponding gap is about +0.4 points, with an interval of -3.0 to +3.7. Both a modest loss and a modest gain remain compatible with this saved comparison. The interval does not establish practical equivalence.

## 4.7 Output Length and Accuracy Tradeoffs

[[FIG:tokens]]

[[FIG:tradeoff]]

For 0.8B, OFF uses 1,781 mean output tokens compared with 6,206 for ON and 5,920 for the free selected limit. In the all-attempt view, the trained limit uses 4,979. These are problem-weighted lengths. The chart retains all responses, rather than describing only successful solutions.

The accuracy-token plot places each complete 0.8B configuration by its two measured averages. Moving left means shorter generated output and moving up means greater observed accuracy. A point's location does not include the expense of training or candidate selection. No time-per-token conversion is used to turn this plot into a latency estimate.

For 2B, OFF uses 1,337 mean output tokens compared with 5,331 for ON and 4,337 for the free selected limit. In the all-attempt view, the trained limit uses 4,072. These are problem-weighted lengths. The chart retains all responses, rather than describing only successful solutions.

The accuracy-token plot places each complete 2B configuration by its two measured averages. Moving left means shorter generated output and moving up means greater observed accuracy. A point's location does not include the expense of training or candidate selection. No time-per-token conversion is used to turn this plot into a latency estimate.

For 4B, OFF uses 943 mean output tokens compared with 5,188 for ON and 3,921 for the free selected limit. In the all-attempt view, the trained limit uses 3,511. These are problem-weighted lengths. The chart retains all responses, rather than describing only successful solutions.

The accuracy-token plot places each complete 4B configuration by its two measured averages. Moving left means shorter generated output and moving up means greater observed accuracy. A point's location does not include the expense of training or candidate selection. No time-per-token conversion is used to turn this plot into a latency estimate.

In the specific 4B first-attempt comparison, the free limit averages about 3,961 tokens and the trained limit about 3,511, a reduction of approximately 11.4%. This reference token value differs from the all-attempt mean of about 3,921. The reduction statement uses the first-attempt reference consistently. An uncertain accuracy difference accompanies the measured length reduction.

## 4.8 Cap Rates and Historical Loop Evidence

[[FIG:caps]]

The full-coverage cap plot displays the saved hit-limit indicator. It reports whether the full response reached its output cap, not whether it met a repetition detector. OFF still has a cap rate because the answer itself can be long. A small thinking budget also does not guarantee a short complete response.

[[FIG:loops]]

The historical 2B ON condition hits the cap on 190/468 attempts, or 40.6%. Among those capped attempts, 69.5% meet the saved loop rule. LoRA-2 hits the cap on 192/468 attempts, or 41.0%, and 88.5% of those capped attempts meet the rule. The denominator for a cap percentage is all attempts; the denominator for each loop percentage here is only capped attempts.

These loop findings refer to 234 original problems with two attempts per method. They are not computed for all 464 problems and should not be read as whole-study loop rates. The historical median thinking length of completed normal-thinking HumanEval+ answers is 672 tokens. Completion, length, and cap status describe related but distinct aspects of an answer.

## 4.9 Partial Sweeps and the Historical LoRA 2 Experiment

[[FIG:coverage]]

[[TABLE:partial]]

Some exploratory limits have high percentages on their covered subset. For example, the 4B limit sweep covers the original 234 problems, while the full-coverage selected limit covers the complete 464. A ranking that ignores those denominators would mix different task populations. The partial rows are included for completeness and are not promoted to full-set conclusions.

LoRA-2 covers 234 problems and has a 45.1% equal-problem all-attempt accuracy in the combined record for that subset. It is a different add-on from LoRA-1. The original thinking-length ratio against normal thinking is 1.00 with an interval of 0.94 to 1.06. The historical study therefore did not observe the intended shortening under that analysis.

The brief-prompt result concerns one saved wording and its covered tasks. Saved examples indicate a conflict with the code-only instruction. The result does not measure every possible concise prompt. Similarly, a longer-output retry changes the generation conditions and remains a diagnostic outside the completed full-coverage comparisons.

## 4.10 Validation Results

[[TABLE:validation]]

The combined dataset contains 464 unique test IDs. The training audit checks 280 saved training-pool IDs and reports no exact ID overlap. Every completed combination has 464 unique answers, 464 corresponding grades, and one attempt per ID according to the checked archive. The five Notebook 24 configurations contribute 2,320 answers, while the earlier 2B limit combination contributes 464.

The saved audit also checks recorded model settings, add-on hashes, raw/graded token agreement, expected IDs, and reference hashes. The document build validates the six complete pass counts against the checked summary values and records SHA-256 hashes of the evidence files. These checks establish consistency of the reporting inputs. They do not rerun the generated code or prove the absence of all possible benchmark contamination.

The PDF and Word formatting checks are separate from scientific validation. They confirm that captions, page numbering, and tables present the evidence coherently. A clean layout cannot strengthen an uncertain result, just as a correct calculation can still be misrepresented by an unlabeled chart. Both layers are therefore inspected before delivery.

## 4.11 Summary of Key Findings

The all-attempt free-control reference scores are 14.7% for 0.8B OFF, 38.6% for 2B limit 1,024, and 71.9% for 4B limit 2,048. The completed trained limits reach 14.4%, 41.2%, and 71.6%, respectively, with one answer per problem. These numbers use the attempt rules stated in their tables and are not a single unqualified ranking.

LoRA plus OFF does not consistently improve over OFF without LoRA. The 0.8B trained limit improves over its matching weak free limit, but does not establish a gain over the stronger OFF reference. The 2B and 4B trained limits have uncertain accuracy differences from their matching free limits. The 4B first-attempt comparison also records fewer total output tokens for the trained limit.

The historical diagnostics and partial sweeps remain informative at their own scope. They do not establish complete-set outcomes for untested budgets or a universal explanation for every failure. Chapter 5 interprets the main findings and explains what evidence a stronger follow-up would need.
