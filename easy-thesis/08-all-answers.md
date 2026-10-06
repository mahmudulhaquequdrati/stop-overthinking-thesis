# All the answers

Short answers you can say out loud.
Cover the answer, try it, then check.
Hard words are in [WORDS.md](WORDS.md).

## A. The research chain

**Q: What problem did you study?**
A: Small code models think for too long. That costs tokens and time.

**Q: What is the gap?**
A: Nobody had checked, on one small model with a real thinking switch, whether training to think shorter beats the free options.

**Q: What is the question?**
A: Is that training better than thinking OFF, a length limit, or the words "think briefly"?

**Q: What did you expect?**
A: The trained add-on would think at most 0.75 times as long, lose at most 3 accuracy points, and beat each free way.

**Q: What did you change?**
A: Only the way of answering. Same model, same 234 problems, same token room, same seeds.

**Q: What did you measure?**
A: How often the code passes every test, and how many tokens the answer uses.

**Q: What supports the idea that training is worth it?**
A: Shorter thinking, accuracy held, and a win over the free ways.

**Q: What result rejects it?**
A: On 2B, thinking length was x1.00, and the 1,024 limit scored 49.8% against the trained model's 45.1%.

## B. Teacher questions

**Q: What should I say in one sentence?**
A: On small Qwen3.5 code models, a free control beats shortest-correct LoRA. OFF wins on 0.8B, a 1,024 limit on 2B, and a 2,048 limit on 4B, because the waste is looping.

**Q: Did training fail completely?**
A: It did not make thinking shorter (H1 no). Accuracy did not drop (H2 yes). It lost to the limit (H3 no). On easy homework-like problems it had worked: 65% vs 50%, with 41% fewer tokens.

**Q: Why call it loops, not overthinking?**
A: Finished answers were already short. Median finished thinking on HumanEval+ was 672 tokens. 69.5% of normal thinking's unfinished answers repeated themselves.

**Q: Is +7.7 points proven?**
A: On this test, yes. The error bar is [+4.3, +11.3]. It does not include 0. The bar comes from resampling the same 234 problems, 2,000 times, seed 3407.

**Q: Why are some gains not proven?**
A: LoRA-2 versus normal thinking is +3.0 points with bar [−1.1, +7.3]. Zero is inside the bar.

**Q: Why did "think briefly" score 6.6%?**
A: That one sentence fought the rule "one Python code block only". The model argued and usually never finished. Only 36 of 468 answers finished. This is about that wording.

**Q: Why was the limit 1,024?**
A: The early trained model thought for about 1,000 tokens. The limit asks whether a hard cut matches training.

**Q: Why is LoRA-2 the main trained result, not LoRA-1?**
A: We named LoRA-2 before the run. Picking the prettier one afterwards would be cheating.

**Q: Why only two tries?**
A: GPU budget. Four tries would have cost much more Colab time. Two tries still give a paired comparison.

**Q: Why is 0.8B one try?**
A: To stay inside the hour cap. We label it. The bars are wider. OFF at 20.5% still leads LoRA-1 at 17.9% and normal thinking at 7.3%.

**Q: Why is 2B limit 2,048 one try?**
A: It was a lean fill-in. It scored 46.6%, below 49.8% at 1,024. The curve peaks at 1,024. Do not pretend that cell has two tries.

**Q: Did a bigger token room save normal thinking?**
A: A little. On HumanEval+, 16,384 tokens moved a cut-off retry from 53.7% to 59.1%. The limit was 60.4% with much less room.

**Q: Are the tests in the training data?**
A: The training pools are different: MBPP+ and LiveCodeBench from before February 2025. The overlap script removed matches. The main run removed `Mbpp/309` from the kept set. We cannot prove the model never saw HumanEval on the internet. Qwen publishes no cutoff that would prove that.

**Q: Why not a 9B or 70B model?**
A: Training a 9B LoRA did not fit our memory plan, and the week was short. The open question is whether bigger models loop less. Our own 4B run still lost to a free limit.

## C. Who, why, and why not a giant model

**Q: Who is this useful for?**
A: People writing easy Python on one GPU, a school lab, or their own machine.

**Q: Why should they use your finding?**
A: The best accuracy on these sizes was free. They can change a setting and skip training.

**Q: What are the benefits?**
A: Higher accuracy with a limit on 2B and 4B. About 4× fewer tokens with thinking OFF on 2B (860 vs 3,446). No training for the winning way. A size rule: OFF, then about 1,024, then about 2,048.

**Q: Why is it efficient?**
A: The extra tokens were mostly loops. Cutting the loop removes waste and raises the pass rate. The 2B limit uses 2,722 tokens and scores 49.8%. Normal thinking uses 3,446 and scores 42.1%.

**Q: Why not just use a giant model?**
A: Three practical reasons, with honest limits.

1. **Small GPU.** 0.8B, 2B, and 4B ran on one Colab GPU. A giant model needs a much bigger machine.
2. **Easy problems.** On these tests a 4B model with a 2,048 limit already reached 78.2%. A giant model costs more for problems this size can attempt. We did not test hard problems, where a giant model may still win.
3. **Keep code on your machine.** A local small model does not have to send the problem to a cloud model. We did **not** run a security test. Do not call this a measured security result.

**Q: Is the small model "more secure"?**
A: It can stay on your computer, so the code need not leave. That is a setup benefit. We did not measure attacks, leaks, or jailbreaks.

**Q: Should I use 0.8B for real work?**
A: Only for very easy checks. Its best score here was 20.5%. Bigger in this family was much more accurate. Use OFF if you do use it, because open thinking fell to 7.3%.

## D. Dataset questions

**Q: What datasets did you test on?**
A: Three lists, marked apart. First exam 234. Extra contest 40. More contest 190. Total count **464**. The 49.8% and 78.2% stay on the 234.

**Q: What did you train on?**
A: LoRA-1 used **100** easy functions. LoRA-2 used a pool of **280** (200 easy functions plus 80 older contest problems) and kept **157** short correct answers.

**Q: Show me one test problem.**
A: HumanEval/0 asks whether any two numbers in a list are closer than a threshold. The description is in [04-the-datasets.md](04-the-datasets.md). It was copied from our saved answer file.

**Q: Show me one LiveCodeBench id.**
A: `lcb/3705`, marked easy. No 2B way solved it. The full question text is in the LiveCodeBench download, not in this git repo.

**Q: How do you know a pass is real?**
A: The benchmark runs the code. One failed test means fail. Official solutions were graded first, and they passed.

**Q: What did the overlap check remove?**
A: On the main run, `Mbpp/309`. Later size-run files also list `Mbpp/119`, `Mbpp/626`, and `Mbpp/99`.

**Q: Why leave out hard problems?**
A: A 2B model solves almost none, so the ways cannot be compared. Medium LiveCodeBench is already near the floor.

**Q: How many training examples did LoRA-2 see?**
A: 157. That is 133 from MBPP+ and 24 from older LiveCodeBench. Many problems had no correct answer to keep.

## E. If the teacher pushes

**Q: Your hypothesis was wrong. Is that a failed thesis?**
A: No. A clear no, with a measured reason, is a result. The reason is loops, not careful overthinking. The next study should measure loops first.

**Q: Then what did you contribute?**
A: A fair comparison of training against three free controls on one small code model, plus the same 234 problems on two more sizes. The practical rule is: match a free cap to the size. Training did not beat that rule.

**Q: Did 40 more problems change the winner?**
A: The first exam stays 234 problems, with 49.8% and 78.2%. On the 40 newer contest problems, thinking OFF was best or tied the limit. Thinking ON scored 0% on 2B and 18.8% on 4B. Training was only rechecked on 0.8B, where it scored 0 out of 40.

**Q: Did 190 more problems change the winner?**
A: No. They stay in their own table. OFF wins on 0.8B at 9.5%. The 1,024 limit wins on 2B at 31.1%. The 2,048 limit wins on 4B at 69.5%. Training lost on 0.8B (7.9%) and on 4B (46.3%). The 2B add-on was skipped, and that Colab session was deleted. On 4B medium only, OFF was higher (44.4% vs 38.9%). The pictures are in [10-all-counts.md](10-all-counts.md).

**Q: What is the single next step?**
A: On your own problems, try thinking OFF and a short limit before you train anything.
