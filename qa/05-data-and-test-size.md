# Q&A 05: Choosing the data, and how many test problems

⬅️ [All Q&A](README.md) · Hard word? See [GLOSSARY.md](../GLOSSARY.md)

---

## 1. The step in 2 sentences

We train on thousands of code problems that come with tests, and we test on about
1,000 or more **different** problems.
We need that many test problems because a small drop in accuracy (2–3 points) is hard to see.

---

## 2. Questions a teacher may ask

**Q: What data do you train on?**

| Dataset (Hugging Face id) | Why |
|---|---|
| `agentica-org/DeepCoder-Preview-Dataset` (primeintellect + taco parts) | Thousands of code problems **with tests**. MIT licence |
| `codeparrot/apps` (introductory problems) | Easy problems **with tests**. MIT licence |

We keep only training examples of 3,500 tokens or less.

**Q: What do you test on?**

| Test set | Size |
|---|---|
| HumanEval+ | 164 problems |
| MBPP+ | 378 problems |
| LiveCodeBench (`livecodebench/code_generation_lite`), easy + medium | to be counted |
| **Total** | about 1,000+ |

**Q: Why must every problem have tests?**
We grade answers by **running the benchmark's real tests** in a safe sandbox.
We never judge by looking at the output ourselves. Tests are fair and automatic.

**Q: How do you make sure test problems are not in the training data?**
1. We **drop DeepCoder's `lcbv5` part**, because it overlaps with LiveCodeBench.
2. Before training, we run an **overlap check**: remove every training problem
   that matches a test problem, exactly or nearly.

**Q: Why do you need so many test problems?**
*Everyday example:* flip a coin 10 times and get 6 heads. That doesn't prove the coin is unfair.
Flip it 1,000 times, and small differences become clear.

A 2–3 point accuracy change is small. To see it clearly:
- We compare **the same problems** before and after training (a *paired comparison*).
- Even then, we need about **1,250–1,900** problems (for a 2.5-point change).
- A big change in length (−25%) shows with only a few hundred problems.

---

## 3. Hard questions

**Q: Why not use a small, famous contest set, like 30 AIME problems?**
With 30 problems, one problem = 3.3 points. Random noise is bigger than the change we want to see.
A paper (Hochlehnert et al., 2504.07086) showed noise there is bigger than many claimed gains.

**Q: Your test set is about 1,000, but you said 1,250–1,900 are needed. Is that a problem?**
It is a real risk. Some ways we reduce it:
1. We ask each problem **4 times** and average. This makes the numbers more stable.
2. The main claim (−25% thinking length) is easy to see with fewer problems.
3. We report error bars honestly. If the accuracy difference is unclear, we say so.

**Q: Are your test problems "fresh" (not seen by the model)?**
Partly. Gemma's cutoff is January 2025. LiveCodeBench problems from Feb–Apr 2025 are after it.
HumanEval+ and MBPP+ are older, so the model may have seen them.
But both the base model and the trained model see **the same** problems, so the comparison stays fair.

---

## 4. Checked vs. assumed

| We checked (2026-09-13) | We assume |
|---|---|
| DeepCoder has about 24.7K training problems (primeintellect 16,252; taco 7,436; lcbv5 599) | The exact dataset ids still work: re-check in the first data notebook |
| LiveCodeBench lite release_v6 has 1,055 problems, up to April 2025 | How many LiveCodeBench problems are easy + medium |
| The test-size math (from the statistics note) | That the model solves enough training problems |

---

## 5. Where it is written

- [DECISIONS.md](../DECISIONS.md) row #18
- [PLAN.md](../PLAN.md) §6
- [research/datasets.md](../research/datasets.md)
- [research/data-size-and-test-size.md](../research/data-size-and-test-size.md) §3 (the test-size math)
