# Chapter 6: Conclusion and Future Work

## 6.1 Summary of the Study

This thesis examined shortest-correct LoRA training and thinking controls for Qwen3.5-0.8B, 2B, and 4B on a combined collection of 464 coding problems. The test set contains 164 HumanEval+ functions and 300 LiveCodeBench tasks, including 166 easy and 134 medium problems. The report uses saved outputs and grades, with no new model training or generation for the document build.

The study compares inference controls that require no additional training with saved trained add-ons. It also evaluates all six planned combinations of LoRA-1 with OFF or a selected thinking limit. The central comparison is whether the trained system improves over a matching free policy, rather than merely over unrestricted thinking. Accuracy and output tokens are reported together, with coverage and attempt rules kept visible.

## 6.2 Answers to the Research Questions

For RQ1, the best observed full-coverage free controls differ by model size. In the equal-problem all-attempt summary, OFF reaches 14.7% for 0.8B, limit 1,024 reaches 38.6% for 2B, and limit 2,048 reaches 71.9% for 4B. These are the best among the measured full-coverage free settings, not established globally optimal budgets. OFF generates the fewest output tokens among the main free controls at each size.

For RQ2, the selected free controls score above LoRA-1 alone in the all-attempt paired summaries. The 0.8B advantage remains uncertain, while the saved 2B and 4B intervals favor the selected free controls. This supports testing simple controls before investing in this training procedure. It does not show that every LoRA design or every possible concise training set is ineffective.

For RQ3, all six LoRA combinations are complete with one answer per problem. The OFF and limit pass totals are 65 and 67 for 0.8B, 165 and 191 for 2B, and 300 and 332 for 4B. The 2B trained limit has the highest observed full-set point estimate for that size, at 41.2%. Its gain over the matching free limit remains uncertain. The 4B trained limit reaches 71.6% and similarly has no established accuracy advantage over the free-limit first attempt.

For RQ4, the benchmark breakdowns show why the task mixture must remain visible. HumanEval+ and contest groups have different observed outcomes, and medium contest tasks remain particularly challenging for the smallest model. The combined score is a weighted summary of this specific collection. It cannot replace group-level inspection when the intended application resembles only one part of the benchmark.

For RQ5, the historical loop and training analyses provide possible explanations for long output and limited transfer. They retain their original 234-problem scope. LoRA-2 did not show the desired shortening in that experiment, and many capped outputs satisfied the saved loop rule. These observations motivate a targeted recovery intervention, but they do not establish a general causal account for every later result.

## 6.3 Main Conclusions

The clearest conclusion is methodological: compare a trained reasoning method with a strong, matching inference control. A gain over unrestricted thinking can be real while providing little evidence that the training component is needed. In this study, OFF and fixed thinking limits are essential references for understanding the trained combinations.

The practical conclusion is conditional. Begin with the observed free policy for the model size and evaluate it on representative development tasks. Consider a trained combination if its measured accuracy and token tradeoff justifies the added work in that application. In particular, the 4B limit combination provides a measured reduction in output tokens with an uncertain accuracy change, rather than demonstrated equivalence or a guaranteed improvement.

The scientific conclusion is bounded by the study design. The combined analysis is retrospective, uses historical references, and covers one model family and a limited code collection. The intervals are unadjusted, and the LiveCodeBench grader uses up to 20 tests per problem. These limitations remain part of the conclusion rather than being confined to a footnote.

## 6.4 Recommendations for Future Work

The first follow-up should use a single saved software environment and a prospectively fixed evaluation protocol. It should compare the base model and the same add-on under ON, OFF, and a development-chosen limit. Test problems should remain untouched until settings are fixed. Multiple generation and training seeds would help distinguish stable policy effects from sampling and optimization variation.

The second follow-up should change the training supervision in a specific way. One candidate is to train on correct answers generated under a thinking limit, rather than only selecting from unrestricted candidates. Another is to include recovery examples that demonstrate leaving a repeated reasoning pattern and completing code. These are proposed interventions, not completed experiments in the present report.

The third follow-up should separate answer-format failure, incomplete generation, detected repetition, runtime failure, and incorrect computation. This would require a documented classification procedure applied to saved outputs. Such an analysis could test whether a limit mainly improves answer completion or also changes the quality of algorithms that reach the final answer.

The fourth follow-up should measure end-to-end resources. It should record wall-clock latency, accelerator use, batch behavior, and the up-front expense of candidate generation and training. Token counts should remain available as a portable metric, but actual measurements are needed before making claims about cost savings or deployment speed.

The fifth follow-up should broaden validation with a separate benchmark collection, hard contest problems, and another model family. It should also conduct a semantic training/test similarity review rather than rely only on IDs. These extensions would test external validity while preserving the clear baseline and reporting rules established here.

## 6.5 Closing Statement

Small reasoning models should be judged by the code they successfully produce and the resources they actually use. The saved study shows that ending or disabling explicit thinking can be a strong practical intervention. Shortest-correct training remains a testable idea, but its benefit must be demonstrated beyond the simple controls already available. Clear denominators, matched comparisons, and honest uncertainty make that conclusion useful and reproducible.
