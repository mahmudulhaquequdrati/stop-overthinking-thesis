# Chapter 5: Discussion

## 5.1 Interpretation of the Main Results

The findings support a practical starting point: evaluate simple thinking controls before assuming that shortest-correct training is needed. In the all-attempt combined view, the best observed full-coverage free controls are OFF for 0.8B, limit 1,024 for 2B, and limit 2,048 for 4B. This is a statement about the measured collection and evaluated policies. It is not a claim that these settings are optimal for every prompt, code distribution, or deployment constraint.

The completed combinations add an important qualification. Training and thinking controls are not mutually exclusive alternatives. The same LoRA-1 add-on can be used with OFF or a limit. For 2B, the limit combination achieves the highest observed full-set accuracy at 191/464, or 41.2%. Yet its lead over the matching free limit has an interval that includes zero. The report can identify the highest observed score without presenting the method as an established improvement over that reference.

For 4B, LoRA-1 plus limit 2,048 passes 332 problems, while the free-limit first attempt passes 330. A two-problem difference should be understood at its actual scale. The paired interval ranges from a possible disadvantage to a possible advantage. At the same time, the combination uses fewer output tokens than that first-attempt reference. This supports a measured token reduction with uncertain accuracy change, rather than a claim that accuracy has been proved equal.

For 0.8B, OFF without LoRA remains the highest observed full-coverage free score and is also slightly above both trained combinations. LoRA-1 plus limit improves over the weak free limit at the same budget, but that comparison is not the whole practical decision. A user considering additional training would also compare with the stronger OFF option. This illustrates why selecting only a favorable baseline can exaggerate an intervention's value.

## 5.2 Why a Matching Baseline Changes the Conclusion

Suppose the trained limited model is compared only with unrestricted thinking. Any gain could come from the learned add-on, from ending the thinking notes, or from their interaction. The comparison alone cannot separate these effects. A matching free limit makes the inference policy more comparable and asks whether training adds an observable benefit after the simple control is already present.

The completed 2B result demonstrates this distinction. LoRA plus limit is clearly above its historical unrestricted-thinking reference under the saved first-attempt analysis. Its much smaller difference from the free limit remains uncertain. The narrower conclusion is more useful for a deployment decision because the free limit is easier to try than collecting candidates and training an add-on.

The OFF combinations tell a similar story. LoRA plus OFF does not consistently beat OFF without LoRA across the three sizes. There is therefore no general finding that the add-on improves direct answering. The evidence does not establish that LoRA is inherently unsuitable for code generation; it evaluates these particular trained add-ons and their supervision.

Baseline choice is also connected to coverage. The higher percentage of a partially evaluated budget cannot replace a lower full-set baseline unless both are compared on the same relevant problems. A future study should choose its main comparison before viewing final test scores. In this retrospective report, the practical baselines are explicitly labeled as best observed among the full-coverage free settings.

## 5.3 A Possible Role for Repetition

The historical 2B diagnostic suggests that unfinished repeated thinking can consume a substantial part of the output budget. Under normal thinking, 190 of 468 attempts reached the cap, and 69.5% of those capped attempts met the loop rule. Under LoRA-2, 192 attempts reached the cap, and 88.5% of the capped attempts met that rule. These are measurements from the original 234 problems with two attempts each. They are not a 464-problem loop estimate.

A fixed thinking limit can force a transition out of the notes. This could leave enough output room for a program that would otherwise never appear. OFF avoids the explicit notes entirely. Both mechanisms are consistent with the observed improvements over unrestricted thinking. However, the study has not isolated the effect of repetition from every other change in response behavior.

Training only on completed correct examples may be poorly matched to a failure that involves not completing an answer. A successful target shows what a final response looks like, but it may not teach recovery once the model has entered a repeated pattern. This is a hypothesis about training coverage. A future intervention would need examples or controls that specifically target repetition and then measure whether that failure mode changes.

Cap hits must still be interpreted cautiously. A capped answer can contain executable code, and an uncapped answer can be wrong. Likewise, not every long response is redundant. The thesis therefore reports correctness, output length, and cap behavior separately. Combining them into a single label such as overthinking failure would lose useful distinctions.

## 5.4 What the Training Data Can Explain

The historical LoRA-2 data show that starting with 280 problems did not provide 280 short correct training targets. Only 157 examples were retained. Moreover, the contest examples remained much longer than the function examples, with little selected-length advantage over average correct candidates. This limits the strength of the concise supervision available for contest tasks.

The natural interpretation is that a selection procedure can only choose among the candidate behaviors it sees. If the model has no short passing solution for a task, selecting the shortest passing candidate may still yield a long trace. Adding more problems to the starting pool is therefore different from adding more examples of the desired behavior. The pool size, success rate, and retained-length distribution all matter.

LoRA-2's falling loss shows improved fit to its selected examples. The original held-out thinking-length ratio remains about 1.00, with an interval from 0.94 to 1.06. These observations can coexist. Optimization can succeed on its training objective without delivering the hoped-for generalization. This is a familiar distinction in empirical learning systems, and it should not be hidden by describing the training run alone as successful compression.

The LoRA-1 comparisons add another limit. The sizes do not share exactly the same retained training examples or identical response dynamics. The higher performance of 4B is therefore not a controlled estimate of the benefit of parameter count alone. The systems should be compared as tested configurations, with a future standardized experiment needed to isolate model scale.

## 5.5 Benchmark and Difficulty Differences

HumanEval+ function completion and LiveCodeBench contest tasks differ in interface, required solution structure, and problem distribution. The result tables show these groups separately because an overall score can hide severe weakness on medium contest tasks. A configuration that succeeds on many functions may still be unreliable when it must parse input, implement a longer algorithm, and print exact output.

The group sizes also shape the combined result. HumanEval+ contributes 164 of 464 problems, LiveCodeBench easy contributes 166, and medium contributes 134. Equal problem weighting means these groups contribute in proportion to those counts. The report does not assign equal weight to each benchmark category independently. Changing to equal category weights would define another statistic and should be labeled as such.

Group breakdowns are descriptive, not independent replications. The same 464 problems are being reorganized into subsets. A striking subgroup difference may suggest a follow-up question, but multiple subgroup comparisons also create opportunities for chance patterns. The thesis does not select a favorable subgroup and treat its result as the primary study conclusion.

The labels easy and medium do not imply that the 0.8B model finds those problems easy. Difficulty categories come from the source benchmark. A small model can fail almost every task in a category that is relatively accessible to a human contestant. The reader should interpret difficulty alongside the measured score rather than as a prediction of model success.

## 5.6 Accuracy, Tokens, and Practical Choice

Accuracy and output tokens express different priorities. If a user needs the highest observed passing rate for a fixed model, a limit can be attractive. If the user needs short output, OFF may be a better starting point. A scatter plot helps show the tradeoff, but it does not determine a universal winner because the acceptable cost of an error depends on the application.

[[FIG:decision]]

For 4B, the trained limit combination's approximately 11.4% reduction in total output tokens relative to the historical first-attempt free limit is relevant. It indicates fewer generated tokens in this comparison. It does not prove a corresponding 11.4% latency or cost reduction. Time per token, batch utilization, model loading, and training amortization can all affect an operational decision.

For 2B, training plus a limit yields a higher point estimate than the free limit, but the remaining uncertainty matters. A small apparent advantage may be valuable in one setting and insufficient to justify training in another. Before deployment, the user should evaluate a separate development collection representative of the intended workload and then confirm the chosen policy on held-out problems.

For 0.8B, the simple OFF policy offers a strong practical reference within this study. Its observed accuracy is low in absolute terms, which also matters. A method can be the best measured option for a weak model and still be unsuitable for unsupervised use. The thesis recommends a starting policy for testing; it does not claim that the resulting programs require no review.

## 5.7 Comparison with Prior Work

The results are compatible with a broad lesson from the reviewed literature: useful reasoning efficiency depends on the model, task, and intervention. Concise self-training is a motivated approach, and explicit thinking can also be unnecessary under some conditions. Our evidence adds a specific case in which strong free controls change how the trained method should be interpreted.

This study is not a numerical reproduction of any cited compression paper. The base models, parameter scales, datasets, retained examples, inference rules, and outcome definitions differ. It would be misleading to compare a reduction percentage from another paper directly with this thesis's total-token change and declare one approach superior. The measures may concern different portions of the output and different test populations.

The most useful comparison is conceptual. Prior methods show why successful concise supervision is worth testing. The present results show why a matching free control and an explicit attempt rule belong in that test. This combination improves the quality of the empirical question even when a method does not achieve the hoped-for outcome.

## 5.8 Threats to Validity

Internal validity concerns whether the measured difference can be attributed to the intervention. Historical package changes, differing batch layouts, stopping behavior, and unequal attempt counts limit that attribution. Matching problem IDs and first attempts improves clarity, but does not create a contemporaneous randomized experiment after the fact. A future replication should standardize the environment and execution order.

Construct validity concerns whether the metrics represent the intended concept. Passing used tests is a practical measure of functional correctness, but not a formal proof. Token count measures response length, but not directly elapsed time or energy. A cap hit indicates a stopping event, but not necessarily a loop. The report keeps these constructs separate.

External validity concerns transfer beyond the measured setting. The study covers one model family, Python code, 464 problems, and no hard contest tasks. It does not establish results for larger instruction models, different languages, interactive debugging, or real repositories. The selected task mixture also influences the combined score.

Statistical conclusion validity concerns uncertainty and selection. The intervals are unadjusted, many comparisons are possible, and the combined view was selected after the results. The displayed precision reflects arithmetic, not freedom from bias. An inconclusive interval is not evidence of equivalence, and a positive interval is not a guarantee on a new population.

Training/test separation is checked at the ID level, with historical text exclusions preserved. Semantic similarity and pretraining exposure remain possible. The absence of a matching ID should not be described as contamination-free evaluation. Benchmark release timing can reduce one concern without proving what the base model encountered during its creation.

## 5.9 Reporting Lessons and Implications

The study illustrates why clear labels are part of experimental quality. The 4B free limit can correctly appear as 71.9% in one table and 71.1% in another when the attempt rules differ. Without an explanation, the reader could interpret that as an error or select whichever figure helps a preferred story. The same principle applies to the all-attempt and first-attempt LoRA values for 2B.

The completed-control results also show the value of reporting a negative or uncertain answer directly. A study does not need to demonstrate a new winner to be useful. Establishing that a trained add-on has not shown a reliable accuracy gain over a simpler setting can guide the next use of research time. It narrows the intervention that needs testing rather than encouraging more of the same experiments without a clear question.

For researchers, the next design should make the matched free control part of the original protocol. For practitioners, the first step should be a low-cost evaluation of OFF and a few development-chosen limits. For readers, the main discipline is to ask what changed between the compared rows and which problems and attempts support the percentages.

## 5.10 Chapter Summary

Simple controls explain much of the practical improvement over unrestricted thinking in the saved study. The completed combinations are informative, but the 2B and 4B accuracy gains over their matching free limits remain uncertain. Historical repetition and training-data analyses suggest plausible mechanisms without proving them. The conclusion therefore emphasizes measured tradeoffs, explicit uncertainty, and a more controlled next experiment.
