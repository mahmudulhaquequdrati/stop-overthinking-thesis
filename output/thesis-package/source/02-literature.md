# Chapter 2: Literature Review

## 2.1 Language Models and Program Generation

A language model generates a sequence by repeatedly predicting the next token. A token may be a word, part of a word, punctuation, or a piece of code. The relationship between tokens and words varies by text and tokenizer, so the token counts in this thesis are not converted into exact word counts. Parameters are the learned numbers that determine the model's predictions. The size labels 0.8B, 2B, and 4B describe approximate parameter scales, not the number of tokens used to answer a question.

For a coding task, the prompt describes the desired behavior and the model produces a function, class method, or complete program. This output has two kinds of requirements. It must be expressed in a form that the evaluation system can run, and it must implement the intended computation. A correct algorithm in an unusable response format can still fail evaluation. Conversely, a perfectly formatted program can produce the wrong answer. Studying generation therefore requires keeping task semantics and answer format in view.

The model does not inspect the future grader result when producing a normal test answer. Grading is a separate operation performed after generation. This separation is essential for interpreting the training pipeline: practice answers may be selected using their tests, but test answers cannot be selected by looking at their final grades and then called single-attempt performance. The present completed configurations each retain one answer per test problem.

## 2.2 Written Reasoning and Its Limits

In the study's generation format, thinking is the text before a designated boundary and the final answer follows that boundary. This is an observable output convention. It should not be taken as a complete description of every computation inside the model. Thinking OFF removes the explicit reasoning channel from the response policy; it does not mean that the neural network performs no computation.

Written reasoning can organize a solution, identify constraints, or check an algorithm. However, every additional note also consumes output space. If a model repeatedly restates its plan, fewer tokens may remain for executable code before the overall output cap is reached. A fixed thinking budget attempts to manage that allocation. It reserves the possibility of producing an answer by ending the notes, but it cannot guarantee that the notes contain a correct solution.

The efficient-reasoning survey by Sui and colleagues organizes a broad area concerned with reducing unnecessary reasoning work [@survey]. That literature motivates measuring resource use alongside answer quality. Our use of the term overthinking is narrower and operational: output may be longer than is useful under the tested conditions. We do not assign a hidden optimal reasoning length to every problem.

[[FIG:controls]]

## 2.3 Self Training with Concise Solutions

Munkhbat and colleagues study self-training from concise model-generated reasoning paths [@selftrain]. Their method uses the model's own successful outputs as learning material. Their reported setting includes mathematics tasks and shows that concise self-generated supervision can reduce output while preserving average accuracy. This provides a motivation for shortest-correct selection, but it does not establish that the same selection rule will work on this thesis's small coding models.

The general idea is easy to explain. A student tries a practice question several times, checks which attempts work, and studies one of the shorter successful approaches. The model version generates multiple candidates, checks them, and uses selected examples as supervised training targets. This process differs from merely telling the model to be brief at test time. The former updates a trained add-on; the latter changes only the prompt.

Selection introduces its own bias. A practice problem with no passing candidate contributes no successful target. A problem with many correct candidates offers more opportunity to find a short one. Therefore, the retained examples describe problems the model could already solve under the sampling procedure. They are not a random sample of all difficult situations encountered at test time. This observation is a methodological implication of the selection process and is not an additional experimental finding.

The current study also uses a length guard in its historical selection pipeline. The intention is to avoid learning from unusually short answers that omit useful reasoning. A guard can limit extreme selection, but it cannot create concise successful answers when all successful candidates are long. The retained training distribution must therefore be examined, rather than described only by the number of starting problems.

## 2.4 Compression and Software Engineering Research

SEER studies self-enhancing chain-of-thought compression for reasoning models in software engineering [@seer]. Its verified publication record describes best-of-N sampling, filtering, and fine-tuning on a DeepSeek-R1-Distill-Qwen-7B backbone. The reported average reasoning-length reduction is 34.6% across its evaluated software engineering benchmarks. The relevant lesson is that successful compression is possible in an explicitly studied setting; its percentage is not a target or predicted outcome for Qwen3.5-0.8B, 2B, or 4B.

ASAP uses anchor-guided and surprisal-based pruning to identify parts of a reasoning trace for compression [@asap]. Its intervention differs from simply choosing the shortest correct whole answer. That difference matters when comparing methods: two systems may both produce shorter text while learning from very different supervision. This thesis evaluates the saved shortest-correct add-ons and does not implement ASAP's pruning procedure.

These approaches suggest several possible sources of transfer differences. A larger model may have a broader pool of correct candidate solutions. A pruning procedure may preserve a useful intermediate step that whole-answer length selection overlooks. A training dataset may resemble the test distribution more closely in one study than another. These are candidate explanations to investigate, not claims that this thesis has isolated their effects.

## 2.5 Low Rank Adaptation

Hu and colleagues introduce LoRA as a way to adapt a pretrained model by learning low-rank updates while freezing the original weights [@lora]. The decomposition reduces the number of trainable parameters compared with updating every weight. In this study, the term add-on refers to the saved LoRA parameters used with the associated base checkpoint. It is an explanatory term for the reader, not a separate technical method.

For a weight matrix W, a simplified expression is W effective = W frozen + (alpha/r) BA. The matrices A and B form the learned update, r is the rank, and alpha controls its scale. This expression describes the adaptation idea. It does not imply that every implementation target, quantization choice, or inference kernel is identical across the historical runs. Those details belong in the saved adapter and environment records.

[[FIG:lora]]

LoRA is an optimization mechanism, not a guarantee of improved reasoning. Its outcome depends on the base model, target examples, training settings, and test distribution. A training loss can fall because the add-on fits its examples even when the measured test behavior does not improve. Thus the thesis treats loss as evidence about training fit and uses held-out code grades to assess the task outcome.

There is also an important distinction between a training pool and a retained training set. A pool is the collection of problems used to generate candidates. The retained set contains the selected examples that actually enter training. Stating only the pool size can overstate how much successful supervision was available. Chapter 3 reports both where they are supported by the saved records.

## 2.6 Thinking OFF and Budget Controls

Ma and colleagues show that bypassing explicit thinking can be a competitive strategy under constrained budgets [@nothink]. Their study includes coding among several task types. It establishes a reason to take OFF seriously as a baseline, rather than assuming that any reasoning trace must help. The present work uses its own model controls and single-answer outcomes; it does not reproduce that paper's parallel sampling or aggregation results.

The s1 work studies test-time scaling and includes budget forcing that can terminate or extend a model's reasoning [@s1]. For this thesis, the relevant concept is the ability to intervene on the amount of explicit reasoning before the answer. The tested fixed limits are an inference control. They do not require retraining a model each time the budget changes.

The official Qwen3.5 model cards document the model family and thinking-related usage [@q08;@q2;@q4]. Those cards establish the identity and supported interfaces of the checkpoints. They do not replace the experiment's actual configuration files. A thesis must report what the saved runs used, even if a later recommended library version or default setting differs.

The controls in this study are not interchangeable. OFF requests direct answering. A limit permits a bounded amount of notes. A brief prompt asks the model to regulate its own response. A model can obey one control and respond poorly to another. Consequently, this thesis reports a prompt-specific historical failure as a result for that wording, not a proof that every concise prompt is ineffective.

## 2.7 Benchmarks and Functional Correctness

EvalPlus strengthens code evaluation by adding test cases to existing benchmarks [@evalplus]. HumanEval+ is relevant here because all 164 tasks are included in the main test set. More extensive tests can expose programs that appear correct under a weaker check. This supports the thesis's use of explicit grading scope and its avoidance of treating a plausible program as a confirmed pass.

LiveCodeBench collects contest-based code problems over time and supports several code-related evaluation scenarios [@lcb]. This thesis uses a saved code-generation subset, not every scenario or every current problem in the benchmark. The selected test subset contains easy and medium problems. A difficulty category is meaningful within the benchmark's labeling system and should not be treated as a universal scale shared by every other dataset.

Austin and colleagues introduce MBPP as a collection of programming tasks designed around short Python programs [@mbpp]. In the present study, MBPP+ supplies practice material for candidate generation and training. It is not part of the 464-problem main test total. Keeping that distinction explicit prevents a training source from being accidentally presented as independent evidence of generalization.

An aggregate benchmark score is useful but incomplete. Two controls with similar average accuracy can solve different problems. A model may perform well on function tasks and poorly on contest input/output tasks. Breakdown tables therefore complement the combined score. They do not create more independent test problems; they describe subsets of the same measurement collection.

## 2.8 Repetition and Output Caps

A cap hit occurs when the saved output reaches its configured maximum. Repetition is a pattern in the content, such as recurring spans of notes. These concepts overlap, but neither implies the other in every case. A long valid solution can reach a cap, and repeated text can stop before a cap. Any report that labels all capped outputs as loops confuses an output-length event with a content diagnosis.

In a bounded generation system, repetition can prevent the answer boundary from appearing. A limit can interrupt that behavior and leave room for code. That explanation fits the observed direction of several results, but it remains an interpretation. The current thesis does not include a new randomized intervention that changes repetition alone while holding every other factor constant.

The historical loop analysis is still useful because it investigates actual saved outputs rather than guessing from an average length. Its scope is the original 2B experiment on 234 problems. We report those measurements separately and resist extending their percentages to the later combined 464-problem set. The later cap-rate summaries are described as cap rates unless a corresponding loop analysis exists.

## 2.9 Research Gap and Positioning

The study addresses a practical comparison within a defined setting: shortest-correct LoRA training versus available thinking controls in three small Qwen3.5 code models. The reviewed sources motivate concise supervision, efficient reasoning, and strong baselines. They do not make the present saved comparison redundant, because model scale, task collection, training method, and inference policy differ.

The thesis does not claim that no prior work has ever compared trained and untrained reasoning policies. Such a universal novelty claim would require a broader literature search than the one needed to support this report. Its defensible contribution is the measured comparison and its reproducible record. A clear local empirical question can be valuable without claiming to be the first possible study of a broad theme.

## 2.10 Chapter Summary

The literature gives reasons to test concise self-training and reasons to distrust a weak baseline. The essential comparison is not simply short reasoning against long reasoning. It is whether an intervention improves the measured correctness and output tradeoff relative to a suitable alternative. The next chapter turns that principle into a concrete description of the saved study, including its datasets, controls, scoring rules, and limits.
