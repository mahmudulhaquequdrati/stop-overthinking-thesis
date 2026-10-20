# Chapter 1: Introduction

## 1.1 Background and Motivation

Language models can produce programs from a written problem statement. Some models first generate a reasoning trace, which is a sequence of notes before the final answer. These notes can help the model work through a difficult problem. They can also become long, repeat the same plan, or consume the space needed for the program. This thesis asks how much of that written reasoning is useful for small code-generating models. It studies an operational question: should a user train a small model to reason more briefly, or first try the thinking controls already available in the model?

The title, Stop Overthinking, Keep Passing the Tests, describes the desired behavior. A useful system should produce correct code without unnecessary output. However, the title is a research goal rather than a promise that every experiment achieves both aims. The evidence shows a more careful pattern. Different model sizes benefit from different controls, and an improvement over unrestricted thinking does not automatically show that training was necessary. A trained model must also be compared with an untrained model using the same thinking setting.

Research on efficient reasoning considers ways to control the amount of work a model expresses before answering [@survey]. This study focuses on three Qwen3.5 sizes: 0.8B, 2B, and 4B, where B refers approximately to billions of parameters [@q08;@q2;@q4]. Small models are a useful setting because they offer a practical route to experiments on a single accelerator. Nevertheless, a model being small does not make its output automatically short or reliable. Output behavior still needs direct measurement.

We compare thinking ON, thinking OFF, fixed thinking limits, and trained low-rank adaptation add-ons. Low-rank adaptation, abbreviated LoRA, changes a small set of trainable matrices while retaining the base weights [@lora]. The training idea is to generate several solutions to practice problems, retain short solutions that pass tests, and train an add-on on these examples. Self-training with concise solutions provides the motivation for this approach [@selftrain]. The thesis tests this idea in the repository's specific code setting; it does not assume that findings from another task transfer unchanged.

Correctness is checked through saved benchmark grades. An answer must pass the tests actually used by the grader. This is more concrete than judging whether an explanation sounds convincing. It is also narrower than proving that a program works on every possible input. The distinction matters because a program can pass a limited collection of tests and still contain an error. Accordingly, this thesis uses the term observed accuracy for the measured result and states the testing scope alongside it.

The practical motivation is a limited experimental budget. Before collecting many training examples, a researcher can switch thinking off or set a thinking-token budget. These controls require no additional training, although generating answers still consumes computing resources. We call them free controls only in that restricted sense. Whether an intervention saves time, energy, or money requires separate measurements. Here, output length is measured in tokens and is treated as a resource proxy rather than a direct bill.

[[FIG:motivation]]

## 1.2 Problem Statement

The central problem is whether shortest-correct LoRA training provides a useful advantage over simple thinking controls for small Qwen3.5 code models. The desired advantage concerns correctness and output length together. A method that writes fewer tokens but fails more problems may be unsuitable. A method that passes slightly more problems while adding training work may also be difficult to justify if a matched free control achieves a similar result.

There are two distinct comparisons. The first asks whether training alone improves on the base model with unrestricted thinking. The second asks whether the same trained add-on helps after thinking is switched off or limited. These questions cannot be answered by comparing a trained limited model only with an unrestricted base model. Such a comparison changes both training and inference policy at once. We therefore identify the matching untrained policy whenever interpreting an apparent training benefit.

The evidence comes from saved experiments collected in stages. It is not a newly randomized, single-session evaluation. The combined test set contains 464 unique problems, but older configurations can have more attempts on some problems than on others. Some exploratory methods cover only a subset. A central methodological requirement is to preserve those differences rather than make a large table that hides them. Equal weighting by problem and separately labeled first-attempt comparisons are used for that purpose.

## 1.3 Research Questions and Objectives

RQ1 asks how thinking ON, thinking OFF, and the selected full-coverage thinking limits compare in observed accuracy and output tokens for each model size. The objective is to establish useful untrained references before assessing an add-on. The comparison is restricted to measured settings and does not identify the best possible budget.

RQ2 asks whether LoRA-1 alone improves over the corresponding untrained controls. The objective is to separate the effect of learned concise examples from the effect of an inference-time switch. LoRA-1 alone always means that thinking is ON without an additional thinking-token limit.

RQ3 asks whether LoRA-1 combined with OFF or a selected limit improves over the same setting without LoRA. The objective is to evaluate all six completed combinations: two controls for each of three model sizes. Each combination has one saved answer on each of the same 464 problems.

RQ4 asks how the results vary between HumanEval+, LiveCodeBench easy, and LiveCodeBench medium problems. The objective is to show whether a combined score conceals a major difference between short function tasks and contest-style tasks. HumanEval+ is presented as its own benchmark group rather than treated as directly equivalent to a contest difficulty label.

RQ5 asks what the historical training and repetition evidence can explain, and where it stops. The objective is to distinguish observed associations from causal explanations. Earlier LoRA-2 and loop analyses retain their original 234-problem scope and are not generalized into measurements on the full combined set.

## 1.4 Scope and Limitations

The main study includes 164 HumanEval+ problems and 300 LiveCodeBench problems, comprising 166 easy and 134 medium contest tasks. There are no hard LiveCodeBench tasks in the combined set. The work evaluates Python code generation in one model family. It does not establish performance for mathematics, open-ended question answering, repository-level software maintenance, or other programming languages.

The outcome is based on existing grades. HumanEval+ uses extended tests, while the saved LiveCodeBench evaluation uses up to 20 tests per problem. A pass therefore means that the extracted code passed those used tests. The document rebuild neither executes the generated code again nor changes a grade. This keeps the report tied to the historical measurements and avoids silently creating a different evaluation.

The combined view was chosen after results were available. Some historical controls were run under different package versions or batch layouts from the completed combinations. A matching random seed does not remove every environmental difference. These are limitations of causal interpretation, not reasons to discard the measurements. The correct response is to state the comparison and its provenance clearly.

We do not measure human preference for explanations, source-code maintainability, wall-clock inference latency across all configurations, energy consumption, or deployment cost. Token reductions are reported directly. They are not converted into unsupported claims about money or environmental impact. Likewise, the absence of exact training/test ID overlap does not prove that the base model never encountered similar tasks during pretraining.

## 1.5 Contributions

The first contribution is a unified account of a completed three-size study using 464 distinct test problems. The report connects model settings, coverage, accuracy, output length, and uncertainty. Its contribution is an empirical comparison with transparent boundaries, rather than a new base-model architecture.

The second contribution is the completed evaluation of all six LoRA-1 combinations with OFF and selected thinking limits. Using the same test IDs makes it possible to ask whether a trained add-on contributes beyond a simple inference policy. The result is useful even when the answer is inconclusive: it identifies which apparent gains are supported and which require a stronger follow-up experiment.

The third contribution is a reporting framework that keeps two summaries distinct. The historical combined view averages available attempts within each problem and then averages across problems. The completed-control view uses one attempt per problem and compares with historical first attempts. These views answer related but different questions. Presenting both prevents a rounded percentage from changing meaning between sections.

The fourth contribution is an evidence-based explanation for readers new to reasoning models. Diagrams separate training from inference, thinking tokens from total output tokens, and cap hits from detected repetition. Tables and figures are built from the saved result files, so the simplified explanation remains connected to the numerical record.

## 1.6 Thesis Organization

Chapter 2 explains the relevant concepts and places the study within efficient reasoning, self-training, LoRA, and code evaluation research. Chapter 3 describes the datasets, training procedure, generation settings, scoring rules, uncertainty calculations, and validation checks. Chapter 4 presents the complete and partial results with their actual coverage. Chapter 5 interprets the findings and discusses alternative explanations and practical implications. Chapter 6 answers the research questions and proposes specific follow-up experiments. References provide the cited sources, and the appendices document the result files, test IDs, and reproduction steps.
