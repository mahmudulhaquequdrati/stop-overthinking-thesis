# Research note — how much training data, how big a test set (2026-09-13)

> Hard word? See [GLOSSARY.md](../GLOSSARY.md).
>
> **How this was made:** a web search agent read arXiv abstracts and HTML pages.
> (*arXiv* is a free website where researchers post papers.)
> It did not read every table in every PDF.
>
> **Why it matters:** the user asked "how do we make sure the dataset is big enough
> that the model definitely learns and improves?"
> (A *dataset* is a collection of examples, like a big list of problems.)
>
> Decisions drawn from this: [DECISIONS.md](../DECISIONS.md) #14, #16, #17, #18.

**The main finding, in plain words:**

- Some papers use a method very close to ours.
- But **no paper shows how the result changes when you give "shortest correct answer"
  training more or less data.** A picture of that is called a *learning curve*.
- Munkhbat et al. is the closest paper. They trained on the full GSM8K and MATH sets
  (two math problem sets) for one *epoch* (one pass through all the training examples).
  They did not test smaller amounts of data.
- So a learning-curve study is a real gap. We can fill it.

---

## Papers

### How to read this list

A few words come up again and again. Here is what they mean.

| Word | Plain meaning |
|---|---|
| *token* | a small piece of text, about ¾ of a word |
| *SFT* | training on example answers |
| *fine-tuning* | extra training on top of a model that is already trained |
| *LoRA* | a cheap way to fine-tune: we train a small add-on, not the whole model. "r" (rank) and "α" (alpha) are its size settings |
| *full SFT* | training all of the model, not only a small add-on |
| *RL* (reinforcement learning) | the model tries, gets a score, and learns from the score |
| *GRPO*, *PPO* | two kinds of RL |
| *DPO*, *SimPO*, *RPO* | ways of training on pairs: one better answer and one worse answer |
| *CoT* / *trace* | "chain of thought": the model's written thinking steps |
| *N per problem* | how many answers the model wrote for each problem before one was picked |
| *lr* | learning rate: how big each training step is |
| *steps* | how many training updates were made |
| *ablation* | a test that removes one part to see if it mattered |
| *in-domain / out-of-domain* | problems like the training ones / problems of a different kind |
| *pts* | percentage points (80% → 78% is −2 pts) |
| AIME, AMC, GSM8K, MATH, MATH500 | math *benchmarks* (fixed test sets that everyone uses to compare models) |

For each paper: what they did, the numbers they found, and what it says about data size.

### Self-Training Elicits Concise Reasoning (Munkhbat et al., ACL Findings 2025)

- **Link:** [2502.20122](https://arxiv.org/abs/2502.20122)
- **What they did:** the model wrote N answers. They kept the shortest correct one.
  Then they trained on those. Full SFT (not LoRA), 1 epoch, lr 1e-5.
- **Models:** Llama-3.2-3B, Gemma-2-2B, Qwen2.5-3B, Qwen2.5-Math-1.5B, DeepSeekMath-7B.
  For size tests: Llama 1B/3B/8B.
- **Topic:** math.
- **Training examples:** 7,473 (GSM8K) / 7,500 (MATH).
- **N per problem:** 16.
- **Change in length:** plain prompt: −12.8% on GSM8K, −10.1% on MATH.
  Few-shot prompt (a prompt with a few worked examples): −35.8% / −23.7%.
- **Change in accuracy (compared with the old model = 100%):**
  98.8% / 101.7% (plain), 97.0% / 102.6% (few-shot).
- **About data size:** no ablation on data size.
  **Answers get shorter "log-linearly" as N grows.** That means each doubling of N
  gives about the same extra cut in length.

### TokenSkip (Xia et al., EMNLP 2025)

- **Link:** [2502.12067](https://arxiv.org/abs/2502.12067)
- **What they did:** took the model's own correct thinking. Removed the least important
  tokens. Trained on the result with LoRA r=8, α=16.
- **Models:** Qwen2.5-Instruct 3B/7B/14B, Llama-3.1-8B.
- **Topic:** math.
- **Training examples:** 7,473 / 7,500.
- **N per problem:** not stated.
- **Change in length:** −30 to −40%.
- **Change in accuracy:** Qwen-14B dropped less than 0.4 pt at −40%.
  Llama-8B dropped 3.7 pts at −30%, and 8 at −40%.
- **About data size:** they only tested how much to cut, not how much data.

### O1-Pruner

- **Link:** [2501.12570](https://arxiv.org/abs/2501.12570)
- **What they did:** sampled answers first. Then fine-tuned so the length fits
  ("length-harmonizing"). "Off-policy" means it learns from answers written earlier,
  not new ones during training.
- **Models:** Marco-o1-7B, QwQ-32B.
- **Topic:** math.
- **Training examples:** 5,000 MATH.
- **N per problem:** 16 / 12.
- **Change in length:** 7B: −35 to −43%.
- **Change in accuracy:** 7B: +2.2 to +4.5.
- **About data size:** only tested the setting λ (lambda), not data size.

### L1 / LCPO (COLM 2025)

- **Link:** [2503.04697](https://arxiv.org/abs/2503.04697)
- **What they did:** GRPO with a reward for hitting a target length.
- **Models:** 1.5B (DeepScaleR), 7B.
- **Topic:** math.
- **Training data:** DeepScaleR 40K, 700 steps.
- **N per problem:** unverified.
- **Change in length:** the length can be controlled to within about 3%.
- **Change in accuracy:** 20–25 pts better than s1 "budget forcing" at 512–1,024 tokens.
- **About data size:** nothing.

### ThinkPrune

- **Link:** [2504.01296](https://arxiv.org/abs/2504.01296)
- **What they did:** GRPO with a hard length limit. The limit got tighter in stages:
  4k→3k→2k tokens.
- **Models:** R1-Distill-1.5B, DeepScaleR-1.5B, QwQ-32B.
- **Topic:** math.
- **Training examples:** **2,470** AIME/AMC problems.
- **N per problem:** 16.
- **Change in length:** −65% / −43% / −49%.
- **Change in accuracy:** +0.6 / −2.5 / −3.2.
- **About data size:** tightening in stages works better than one single step.

### ShorterBetter

- **Link:** [2504.21370](https://arxiv.org/abs/2504.21370)
- **What they did:** GRPO. Reward = correct, minus how far the answer is from
  the shortest correct answer.
- **Models:** R1-Distill 1.5B/7B, Llama-8B.
- **Topic:** math.
- **Training data:** DeepScaleR 40K pool, 100–300 steps.
- **N per problem:** 8.
- **Change in length:** −50 to −80%.
- **Change in accuracy:** in-domain +2.5 to +7; out-of-domain −0.5 to −1.6.
- **About data size:** most of the shortening happened in the first ~100 steps.

### AdaptThink (EMNLP 2025)

- **Link:** [2505.13417](https://arxiv.org/abs/2505.13417)
- **What they did:** RL that teaches the model to choose: think, or don't think.
- **Models:** R1-Distill 1.5B/7B.
- **Topic:** math.
- **Training data:** 40K, ~1 epoch.
- **N per problem:** 16.
- **Change in length:** −53% / −40%.
- **Change in accuracy:** +2.4 / +2.3.
- **About data size:** it skips thinking more often on easy problems.

### Concise Reasoning via RL

- **Link:** [2504.05185](https://arxiv.org/abs/2504.05185)
- **What they did:** a second round of training with PPO, only on problems the model
  can already solve.
- **Models:** R1-Distill 1.5B/7B, Qwen2.5-Math, Phi-4.
- **Topic:** math.
- **Training data:** **4–8 problems**.
- **N per problem:** 8.
- **Change in length:** MATH500 −54% / −40%.
- **Change in accuracy:** −3.2 / −2.6.
- **About data size:** the strongest sign that very little data can work.
  But it is RL, not SFT.

### Training LMs to Reason Efficiently

- **Link:** [2502.04463](https://arxiv.org/abs/2502.04463)
- **What they did:** RL. Reward = correct × (1 − α · length on a 0-to-1 scale).
  Shorter correct answers get a bigger reward.
- **Models:** R1-Distill 1.5B/7B.
- **Topic:** math.
- **Training data:** **3,200** problems, ~100 steps.
- **N per problem:** 8.
- **Change in length:** 7B: −36% on MATH500, −65% on GSM8K.
- **Change in accuracy:** −2.2 / −1.7.
- **About data size:** only tested the setting α, not data size.

### Kimi k1.5

- **Link:** [2501.12599](https://arxiv.org/abs/2501.12599)
- **What they did:** several things together:
  - a reward for short length,
  - "shortest rejection sampling": write 8 answers, then SFT on the shortest correct one,
  - DPO,
  - merging models.
- **Models:** not disclosed.
- **Topic:** math and code.
- **Training data:** not stated.
- **N per problem:** 8.
- **Result:** AIME score 60.8 using about 3.3k tokens.
- **Change in accuracy:** —
- **About data size:** RL from long to short answers was the most efficient.

### DAST

- **Link:** [2503.04472](https://arxiv.org/abs/2503.04472)
- **What they did:** SimPO on pairs of answers, with a length budget.
- **Models:** R1-Distill 7B/32B.
- **Topic:** math.
- **Training data:** ~10K pairs.
- **N per problem:** 20.
- **Change in length:** −18% / −46%.
- **Change in accuracy:** +0.4 / +1.4.
- **About data size:** nothing.

### Do NOT Think That Much for 2+3=?

- **Link:** [2412.21187](https://arxiv.org/abs/2412.21187)
- **What they did:** the model trained on its own answers. They kept the shortest
  correct answer, or the first correct answer. Tried SFT, DPO, RPO and SimPO.
- **Model:** QwQ-32B-Preview.
- **Topic:** math.
- **Training data:** PRM12K.
- **N per problem:** 10.
- **Change in length:** −22 to −45%.
- **Change in accuracy:** 93.0 → 92.8.
- **About data size:** SimPO worked better than SFT.
  This paper defines "outcome efficiency" (see §2).

### Don't Overthink It

- **Link:** [2505.17813](https://arxiv.org/abs/2505.17813)
- **What they did:** SFT on s1's thinking traces. They compared picking the shortest,
  the longest, or a random trace.
- **Models:** Qwen2.5 7B/32B.
- **Topic:** math.
- **Training examples:** 1,000.
- **N per problem:** —
- **Change in length:** only −5.8%.
- **Change in accuracy:** +2.8% relative (32B).
- **About data size:** the shortest chains were up to 34.5% more accurate.

### SEER

- **Link:** [2509.14093](https://arxiv.org/abs/2509.14093)
- **What they did:** "best-of-N" (write N answers, pick one). Then a filter that removes
  unusual lengths (it uses the median and "MAD", a measure of spread). Then SFT.
  They also tested LoRA.
- **Models:** R1-Distill-7B (+ Qwen3-8B).
- **Topic:** code (software-engineering tasks) + math.
- **Training examples:** 1,883 / 2,732 / 9,604.
- **N per problem:** **3**.
- **Change in length:** −28 to −57%. LoRA cut 34.8%; full training cut 39.8%.
- **Change in accuracy:** +5 to +11. Fewer answers got cut off or stuck in loops.
- **About data size:** nothing.

### S3-CoT

- **Link:** [2602.01982](https://arxiv.org/abs/2602.01982)
- **What they did:** the model wrote its own thinking at different lengths.
  Training went from easy to hard (a "curriculum").
- **Models:** Qwen2.5-7B, Llama3-8B, R1-7B, **Qwen3-4B-Thinking**.
- **Topic:** math.
- **Training examples:** ~6.4K GSM8K.
- **N per problem:** —
- **Change in length:** about −17 to −20%.
- **Change in accuracy:** about flat.
- **⚠️ Warning:** SFT on only the shortest thinking **"substantially degrades accuracy"**.

### Correct, Concise and Complete

- **Link:** [2601.02972](https://arxiv.org/abs/2601.02972)
- **What they did:** SFT, then RL that punishes tokens written after the first correct answer.
- **Models:** 8B, 32B.
- **Topic:** math.
- **Training data:** unverified.
- **N per problem:** —
- **Change in length:** −28% / −40%.
- **Change in accuracy:** −1.6 / −2.5.
- **About data size:** —

### Acoer

- **Link:** [2606.22716](https://arxiv.org/abs/2606.22716)
- **What they did:** GRPO + LoRA r=16. The length reward was given on correct answers only.
- **Model:** Qwen3-1.7B.
- **Topic:** math.
- **Training data:** ~15K, 1,200 steps.
- **N per problem:** 16.
- **Change in length:** MATH500 −62%.
- **Change in accuracy:** comparable (about the same).
- **⚠️ Warning:** even a tiny length penalty on *wrong* answers (β=0.01)
  **made training break down ("collapse") by step 800.**

### s1

- **Link:** [2501.19393](https://arxiv.org/abs/2501.19393)
- **What they did:** SFT on hand-picked thinking traces.
- **Model:** Qwen2.5-32B.
- **Topic:** math.
- **Training examples:** **1,000**.
- **N per problem / change in length:** —
- **Result:** AIME 50.0.
- **About data size:** the full 59K set gave only +3.3 AIME, for 56× the computer work.
  1K random (not hand-picked) examples gave 36.7.

### LIMO

- **Link:** [2502.03387](https://arxiv.org/abs/2502.03387)
- **What they did:** SFT on hand-picked thinking traces.
- **Models:** Qwen2.5-32B (+ 3B–72B).
- **Topic:** math.
- **Training examples:** 817 / 800.
- **N per problem / change in length:** —
- **Result:** AIME 63.3.
- **About data size:** **400 examples → 57.5; 800 → 63.3; 1,200+ adds less and less.**

### Also found

- Survey "Stop Overthinking" [2503.16419](https://arxiv.org/abs/2503.16419)
  (Sui et al., TMLR 2025). A *survey* is a paper that summarizes many other papers.
- Also [2508.02120](https://arxiv.org/abs/2508.02120) and [2507.09662](https://arxiv.org/abs/2507.09662).
- DLER [2510.15110](https://arxiv.org/abs/2510.15110): answers >70% shorter.
- Step-GRPO [2604.16890](https://arxiv.org/abs/2604.16890): −32% on Qwen3-8B.
- VeriThinker [2505.17941](https://arxiv.org/abs/2505.17941): −44% on MATH500
  (7B model, ~340K pairs).

### ⚠️ Not checked (unverified)

- TokenSkip's full author list and N.
- L1's group size.
- ShorterBetter's batch size.
- Kimi model sizes.
- Data details for 2601.02972.
- DAST's first author.

---

## 1. Smallest amount of data for SFT to shorten answers reliably

### 1a. What we found

- **No paper draws a learning curve** for "shortest correct answer" SFT.

### 1b. Clues from nearby papers

- LIMO and s1 changed how the model reasons with only 400–1,000 hand-picked examples.
  LIMO got most of its gain at 400.
- Munkhbat and TokenSkip used ~7.5K (the full set, 1 epoch).
- SEER used 1.9K–9.6K, with N=3.
- RL needed only 4–8 problems (Fatemi), or 2.5–3.2K (ThinkPrune, Arora).

### 1c. Be careful

- Hassid trained on 1K shortest traces. Answers got only ~6% shorter.
- So the *number* of examples is not the whole story.
- What matters is **how much shorter the picked answers are** than normal answers.

### 1d. Suggestion

- Draw our own curve: train with ~250 / 500 / 1K / 2K / 4K examples.
- This is a real thesis contribution.

## 2. Check before training: is there something to learn?

**Everyday example:** before you coach someone to run faster, check their best time.
If their best run is the same as their normal run, there is little to coach.

For each training problem, let the base model write N answers. Then measure:

- **Headroom ratio (room to shorten).**
  For each problem: shortest correct length ÷ average correct length.
  Then take the average over all problems.
  Near 1 means the shortest answer is about as long as normal, so there is little to learn.
- **Selection bias.** We only keep problems the model solved.
  Are the kept problems easier, or solved more often, than the dropped ones?
- **Coverage (share of problems solved at least once).**
  The share of problems with ≥1 correct answer.
- **Less gain from more samples.** Draw the ratio for N = 1, 2, 4, 8, 16.
  It should drop about "log-linearly": each doubling of N gives about the same small drop.
- **Outcome efficiency** (Chen et al.): tokens until the first correct answer ÷ all tokens.
  It shows how much of the answer is extra talk after the answer was already found.
- **Safety rule (from S3-CoT).** If the shortest answers are much shorter than the median
  (for example, less than half), pick a medium-length answer instead.

## 3. How big must the test set be to see a 2–3 point accuracy change?

**Everyday example:** you flip a coin 10 times and get 6 heads. That does not prove the
coin is unfair. Small tests are noisy. To see a *small* change, you need *many* problems.

Some words first:

- **SE (standard error):** how much a score jumps around by chance.
- **95% CI (confidence interval):** the error bar. The true value is very likely inside it.
- **p:** the accuracy (0.8 = 80%). **n:** the number of test questions.
- **Δ (delta):** the size of change we want to see, in points.
- **α = 0.05:** we accept a 5% chance of a false alarm.
- **80% power:** if the change is real, we see it 8 times out of 10.
- **Significance:** the change is big enough that it is probably not luck.

### 3a. Unpaired: compare two runs as if they used different questions

- Formula: SE = √(p(1−p)/n).
- At p=0.8 and n=500: SE = 1.8 pts, so the 95% CI is ±3.5.
- The difference between two runs has SE ≈ 2.5 pts.
- **In plain words:** the noise is as big as the change we want to see.
  So MATH-500 alone can't show a 2–3 pt change this way.

### 3b. Paired: compare the same questions before and after

A paired test compares the same problem before and after training.
Most questions give the same result both times, so they add no noise.
Only the questions that *changed* matter. So it needs fewer problems to see a small change.

(McNemar's test and the paired bootstrap are two ways to do this. A *bootstrap*
re-samples the questions many times to build the error bar.)

- **d** = share of questions where exactly one of the two models is right
  (often 8–15%).
- SE of the difference ≈ √(d/n).
- For Δ = 2.5 pts, α = 0.05 and 80% power: n ≈ d × 7.84 / Δ².

What that gives:

| Change we want to see | d | Questions needed |
|---|---|---|
| 2.5 pts | 0.10 | **~1,250** |
| 2.5 pts | 0.15 | **~1,900** |
| 2 pts | 0.10–0.15 | ~2,000–2,900 |
| Just reach significance (no 80% power rule) | — | ~600–900 |

### 3c. Recommendation

- Pool ~1,500–3,000 questions.
- Let the model answer each question 4–8 times, and average.
- Report an error bar made by comparing the same problems before and after
  (paired bootstrap 95% intervals, grouped by question). Source: Miller,
  [2411.00640](https://arxiv.org/abs/2411.00640).

### 3d. Why AIME alone is not enough

- AIME has only 30 questions. One question = 3.3 pts.
- So an AIME result is only a story, not proof.
- Hochlehnert et al. ([2504.07086](https://arxiv.org/abs/2504.07086)) show that on AIME,
  just changing the seed or setup moves scores more than many claimed gains.
  (A *seed* is the number that fixes the random choices.)
