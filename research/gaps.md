# Research note: checking the research gaps (2026-09-13)

> Hard word? See [GLOSSARY.md](../GLOSSARY.md).

---

## 1. What this note is

- A *research gap* is a question that no paper has answered yet.
- We first claimed six gaps, called **G1 to G6**.
- In this note we check each one. Is it really still open?

Everyday example: you have an idea for a new shop.
Before you open it, you walk down the street to see if someone already sells the same thing.

---

## 2. How we made it

> - A web search agent tried to *prove each gap wrong*.
>   It searched arXiv and 2025–2026 venues (conferences and journals).
> - *arXiv* is a free website where researchers post papers.
>   Each paper has an id, like 2509.14093.
> - ✔ = checked on the arXiv page or in the full text.
> - No mark = seen only in search-result text. We did not open the paper.
> - "Not found" means *we did not find* a paper. It does not mean that none exists.
>
> Decisions that came from this note: [DECISIONS.md](../DECISIONS.md) #4, #15, #19, #20 and
> [PLAN.md](../PLAN.md) §4.

### 2.1 What the verdicts mean

| Verdict | Plain meaning |
|---|---|
| OPEN | We found no paper that answers it |
| PARTLY FILLED | Some papers already answer part of it |
| FILLED | Papers already answer it |

---

## 3. Summary: the short answer

- Only **G2** (how much training data) is clearly OPEN.
- G1, G4, G5, G6 are PARTLY FILLED.
- G3 is mostly FILLED, the way we first wrote it. The version for 2026 models is thin (very few papers).
- So the open space is smaller than we first said.
- The closest paper to us is **SEER 2509.14093**.
  - It already does "shortest-correct fine-tuning" on code tasks.
    That means: let the model answer many times, keep the shortest answer that is correct, and train on it.
  - It also compares LoRA with full fine-tuning.

Three words we use a lot:
- *Fine-tuning* = extra training of a model that already exists, on our own examples.
- *LoRA* = a cheap way to fine-tune. It trains only a few small extra parts, not the whole model.
- *Full fine-tuning* (full FT) = training all of the model's numbers. It needs much more GPU memory.

---

## G1. Short reasoning for code gets less attention than math → PARTLY FILLED

### G1.1 Papers we found

Words in this table:
- A *token* is a small piece of text, about ¾ of a word. Fewer tokens = shorter thinking.
- A *trace* is the thinking text the model writes before its answer.
- *LCB* = LiveCodeBench, a code benchmark (a fixed test set) that keeps adding new problems.
- *pass@1* = how often the first try passes the tests.
- *R1-Distill-Qwen-7B* = a small reasoning model that always thinks. "7B" = 7 billion numbers inside the model.

| Paper | arXiv / date | What it did |
|---|---|---|
| ASAP "Pruning the Unsurprising" ✔ | 2508.05988, Aug 2025 (v2 Jan 2026) | Cuts unneeded parts out of long code traces. Then does full fine-tuning of R1-Distill-Qwen-7B and Llama-8B on CodeForces traces. Tested on HumanEval/+, LCB v1–v3, v4–v5, LeetCodeDataset. About 23.5% fewer tokens on LCB v4–v5, at 36.2% pass@1 |
| SEER (adaptive compression) ✔ | 2509.14093, Sep 2025 | **Not math.** Uses software-engineering data (MathQA-Python, defect detection = finding bugs, code search). Keeps the shortest correct of N answers, plus a length filter. Full FT of R1-Distill-Qwen-7B on 4×A800 GPUs. About 40% shorter. It also works on HumanEval/MBPP: 30–40% shorter. **LoRA 67.7% vs full FT 74.9%** |
| EvoThink ✔ (summary page) | 2607.19962, Jul 2026, IJCAI 2026 | The model cuts its own thinking (self-pruning). Then it learns from better/worse answer pairs (preference optimisation). Math and code |
| SEER (different paper, same name) ✔ | 2510.17130, Oct 2025 | Writes code. Switches between a direct answer and step-by-step thinking |
| RoutingGen / Intention CoT | 2512.14048, AAAI 2026 | Prompting only, no training. Picks the way to answer by how hard the problem is. −46% tokens on McEval |
| LogitsCoder | 2602.14054 | Controls reasoning length while the model writes (at decoding time), for code |
| TACT | 2605.05980 | No training. Nudges the model's inner signals (activation steering) against overthinking. 27B coding agent. +5.8 pts (points) |
| The Danger of Overthinking | 2502.08235 | A study on SWE-bench Verified. Picking the runs that overthink less gives about +30% performance and −43% cost |
| Reasoning steps in thinking code LLMs ✔ | 2511.05874 | 6 reasoning models, 100 BigCodeBench tasks. **Cutting 10–30% of steps keeps normal tasks OK but hurts hard ones.** No training |
| Reasoning as a Resource ✔ | 2506.09396 | Position paper (an opinion paper, no experiments). Fast vs slow thinking for code |
| DART ✔ | 2606.23181, EMNLP Findings | No training. Picks a thinking budget for each problem (routing). Code accuracy up to +22.5, with 51–63% fewer tokens |
| Semantic early exit | 2605.17672 | Stops thinking early. −26.2% tokens on code |
| OckBench | 2511.05722 | A benchmark that measures accuracy and token use together, including coding |

### G1.2 The count

- About 3 papers train for shorter reasoning mainly on code: ASAP, SEER, EvoThink.
- All of them use R1-Distill-7B-class models that always think.
- All of them use full fine-tuning.
- Math has dozens of such papers.

### G1.3 What it means for us

- We **can** say: code is under-studied (few people looked at it).
- We **can not** say: nobody did shortest-correct training on code.

---

## G2. How many training examples are needed → OPEN (not found)

### G2.1 Papers we found

| Paper | arXiv | Why it matters |
|---|---|---|
| Hint Tuning ✔ | 2605.08665 | 1,000 examples → 24–66% fewer tokens. Models: Qwen3-Thinking, R1-Distill, 4–32B. No curve of results vs data size |
| STOP ✔ | 2605.13165 | Cuts each answer at the earliest point where it is already correct. Fine-tunes with little data. R1-Distill-7B/8B, math. No such curve in the abstract (the short summary) |
| The Art of Efficient Reasoning ✔ | 2602.20945 | A very big ablation (tests that remove one part to see if it mattered): about 0.2M GPU-h (GPU-hours) on Qwen3 0.6–30B. Warns of the "short-is-correct trap". Not clear if it changes the number of examples |
| Demystifying Hybrid Thinking ✔ | 2510.12680 | About 140k examples for a stable thinking ON/OFF switch. (This is about the switch, not about length) |
| Self-Training Elicits Concise Reasoning ✔ | 2502.20122 | Full FT on 8×H100 GPUs. Same sampling budget for all runs, but the number of examples is not changed |

### G2.2 What it means for us

- A *learning curve* here = a chart of results as we give more training examples.
- We found no learning curve of accuracy and token savings vs the number of shortest-correct examples.
- It is cheap to run on a T4. (A *T4* is an older NVIDIA GPU that Colab and Kaggle give for free.)

---

## G3. Possibly-seen test sets → mostly FILLED; the 2026-model version is OPEN but thin

### G3.1 The idea

- A model may have already seen the test problems during training. This is called *contamination*.
- Then a high score may come from memory, not skill.
- Everyday example: a student who saw the exam questions the night before.
- A model's *cutoff* is the date its training data ends. Problems made after the cutoff are "fresh".

### G3.2 What we found

- Many 2025–26 papers already use fresh tests: AIME 2025, LCB v5/v6, or post-cutoff LeetCodeDataset.
  Examples: SmartThinker 2603.08000, ASAP, NoWait 2506.08343.
  For R1-Distill models, those tests come after the cutoff.
- "Reasoning or Memorization?" 2507.10532 shows Qwen2.5 contamination on math benchmarks.
  It is not about shorter reasoning.
- For 2026 models, AIME 2025 and older LCB are probably before the cutoff.
  We found no paper that uses AIME 2026 or 2026 LCB problems.
- We found no paper that asks: does shortening work differently on memorized problems vs fresh problems?

### G3.3 What it means for us

- Using fresh test sets is good practice. It is not a main contribution.
- Memorized-vs-fresh can be a small side finding (G-E in PLAN).

---

## G4. Models with a thinking switch → PARTLY FILLED

### G4.1 Papers we found

Words in this table:
- A *hybrid model* = a model with a thinking ON/OFF switch. "No-think mode" = the switch is OFF.
- *RL* (reinforcement learning) = the model learns from rewards, like a dog getting treats.
- *Training-free* = the model is not trained; only the way we use it changes.

| Paper | arXiv | Why it matters |
|---|---|---|
| Demystifying Hybrid Thinking ✔ | 2510.12680 | Reasoning leaks into no-think mode. Gives a training recipe for a cleaner switch |
| HRBench ✔ | 2605.28398 | A benchmark of ways to use the switch (training-free, FT, offline/online RL). Models from Qwen3.5-2B → Kimi-K2.5. Math/science/code. No single best way |
| DART ✔ | 2606.23181 | Training-free. Compared with always-thinking and no-thinking |
| Mid-Think | 2601.07036 | In-between thinking budgets on Qwen3, using trigger tokens |
| NoThinking ✔ | 2504.09858 | Skipping thinking beats thinking with a limited budget under about 3k tokens. Includes coding (R1-Distill) |
| TFPI ✔ | 2509.26226 | RL with thinking removed. 4B model. AIME24 + LCB |
| 3TF ✔ | 2511.03408 | Trains a hybrid model so that no-think mode keeps its reasoning quality |
| TNT ✔ | 2601.04805 | RL that learns when to think. About 50% fewer tokens (R1-Distill, math) |
| D-COT ✔ | 2602.21786 | Qwen3-8B, 5k examples. Less overthinking on GPQA/MMLU-Pro |
| Art of Efficient Reasoning ✔; ETR 2604.05355 | 2026 | RL for length, done directly on Qwen3 hybrid models |
| Thinkless 2505.13379, AdaCoT, LHRM, AutoThink, ARM, OThink-R1 2506.02397 | 2025 | Learn when to think. Mostly R1-Distill or custom models, math |
| Gemma 4 Tech Report ✔ | 2607.02770; eval 2604.07035 | Confirms the thinking mode. **We found no length-reduction training on Gemma-4-E4B** |

### G4.2 What is still open

- Nobody ran **one fair test on the same ~4B hybrid model** with all of these side by side:
  1. thinking ON
  2. thinking OFF
  3. a thinking budget
  4. thinking ON + shortest-correct fine-tuning
- ...with the results split by domain (type of problem).
- We did not find it. We also found nothing like it on Gemma-4-E4B.
- → **This is our main gap, G-A.**

---

## G5. LoRA on a single free GPU → PARTLY FILLED, weak as a contribution

### G5.1 What we found

- TokenSkip ✔: LoRA r=8 on 2× RTX 3090, about 2 h for 7B.
  (*r* = the rank = how big LoRA's small extra parts are.)
- SEER ✔: LoRA works, but loses about 7 points vs full FT.
  This is a warning. We can test it (our G-D rank check).
- Tina (LoRA RL, about $9) and medical CoT QLoRA 2510.05003 (Kaggle GPUs):
  cheap reasoning fine-tuning, but not for shorter reasoning.
  (*QLoRA* = LoRA on a model squeezed to use less memory.)
- Nothing found on a T4 (16 GB, no bf16/FA2).
  (*bf16* and *FA2* = speed and memory tricks that newer GPUs have and the T4 does not.)

### G5.2 What it means for us

- "It fits on a T4" is an engineering fact.
- We present it as a limit we work under, and as a bonus: others can repeat our work for free (reproducibility).

---

## G6. Transfer between math and code → math→code FILLED; code→math OPEN (not found)

### G6.1 The idea

- *Transfer* = train on one kind of problem, then test on another kind.
- Everyday example: you learn to drive a car. Does that help you drive a van?
- *In-domain* = test on the same kind of problem you trained on. *Out of domain* = a different kind.

### G6.2 Papers we found

| Paper | Direction | Result |
|---|---|---|
| HAPO 2505.11225 (AAAI 2026) | Math → LCB | 34% shorter, accuracy slightly up. Weaker than in-domain. GPQA: −27% length, −2 pts |
| LC-R1 2506.14755 | Math → LCB, GPQA | Still works out of domain. In-domain: −46 to −52%, about −2 pts |
| One-Domain-to-All ✔ 2601.06052 | Math → code, SWE, instruction following | Up to −44% out of domain. 13% fewer SWE-bench rounds |
| Reconsidering Overthinking 2508.02178 | Math → LCB | The gains transfer |
| ETR 2604.05355 (ACL 2026) | Math → HumanEval | From search text only: Qwen3-4B 41.5% → 53.7%, 3,397 → 1,838 tokens (unverified) |
| Manifold Steering 2505.22411 | Math → code (no training) | Transfers |
| Art of Efficient Reasoning ✔ | Cross-domain | Learned length preferences transfer |
| SEER 2509.14093 ✔ | SE (software-engineering) tasks → HumanEval/MBPP | Code to code only |

### G6.3 What it means for us

→ **Our gap G-C: train on code, test on math.**

---

## Top 3 open gaps (from the search)

1. **Same-model comparison on a ~4B hybrid model.**
   Compare OFF, budget, and ON + shortest-correct LoRA, split by domain.
   Question: does training beat just flipping the switch?
   (HRBench and DART compare routing, which means picking a way to answer per problem. They do not compare models trained for length.)
2. **Learning curve over data size.**
   Accuracy and token savings at about 100/250/500/1k/2k examples.
   Not found, cheap, and easy to read.
3. **Code → math transfer.**
   Also run math → code, to check that we get the same result as HAPO / LC-R1 / ETR.

---

## Recommendation from the search: code or math?

**Answer: code as the main training domain, easy–medium difficulty. Math as the transfer target.**

### Why it is new (novelty)

- Only about 3 code papers exist.
- All use full FT on R1-Distill-7B, with no thinking switch.
- Code → math was not found.

### Can we do it? (feasibility)

- Math is easier to grade: we just compare the answer text (string matching).
- Code must be run in a *sandbox* (a safe, closed box for running code) to check it.
- Code traces are long: 5–15k tokens.
- So on a T4, sampling (the model writing answers) is slow.
- Training examples are also capped at about 4k tokens.
- This pushes us toward easier problems. We must say this clearly in the thesis.

### The plan

- Train on MBPP/TACO/LeetCode easy–medium problems.
- Test on post-cutoff LCB (+ HumanEval+).
- Test transfer on MATH-500 + AIME 2026.
- Include: the thinking-OFF baseline (what we compare against), the data-size curve, and a LoRA rank ablation (a test of different LoRA sizes).

### Cite carefully

- SEER 2509.14093 is not math.
- HAPO/LC-R1 already showed math → code.

### ⚠️ Not verified yet

- Is Gemma 4 stable in fp16 on a T4? (*fp16* = a 16-bit number format that uses less memory.)
- The cutoffs of Qwen3.5 and Gemma 4.
- Does LCB have problems after those cutoffs?

---

## Sources

- **G1, code:** [ASAP](https://arxiv.org/abs/2508.05988) · [SEER 2509.14093](https://arxiv.org/html/2509.14093) · [SEER 2510.17130](https://arxiv.org/abs/2510.17130) · [EvoThink](https://arxiv.org/abs/2607.19962) · [RoutingGen](https://arxiv.org/abs/2512.14048) · [LogitsCoder](https://arxiv.org/pdf/2602.14054) · [TACT](https://arxiv.org/abs/2605.05980) · [Danger of Overthinking](https://arxiv.org/abs/2502.08235v1) · [2511.05874](https://arxiv.org/abs/2511.05874) · [2506.09396](https://arxiv.org/abs/2506.09396) · [OckBench](https://arxiv.org/pdf/2511.05722)
- **G2, data size:** [Hint Tuning](https://arxiv.org/abs/2605.08665) · [STOP](https://arxiv.org/abs/2605.13165) · [Art of Efficient Reasoning](https://arxiv.org/abs/2602.20945) · [2502.20122](https://arxiv.org/html/2502.20122v2) · [TokenSkip](https://arxiv.org/html/2502.12067)
- **G4, thinking switch:** [Demystifying Hybrid Thinking](https://arxiv.org/abs/2510.12680) · [HRBench](https://arxiv.org/abs/2605.28398) · [DART](https://arxiv.org/abs/2606.23181) · [Mid-Think](https://arxiv.org/html/2601.07036v2) · [NoThinking](https://arxiv.org/pdf/2504.09858) · [TFPI](https://arxiv.org/abs/2509.26226) · [3TF](https://arxiv.org/abs/2511.03408) · [TNT](https://arxiv.org/abs/2601.04805) · [D-COT](https://arxiv.org/abs/2602.21786) · [OThink-R1](https://arxiv.org/abs/2506.02397) · [Thinkless](https://arxiv.org/abs/2505.13379) · [Gemma 4 report](https://arxiv.org/abs/2607.02770) · [2604.07035](https://arxiv.org/abs/2604.07035)
- **G3, G6, transfer and contamination:** [HAPO](https://arxiv.org/html/2505.11225) · [LC-R1](https://arxiv.org/html/2506.14755) · [One-Domain-to-All](https://arxiv.org/abs/2601.06052) · [Reconsidering Overthinking](https://arxiv.org/abs/2508.02178) · [ETR](https://arxiv.org/abs/2604.05355) · [Manifold Steering](https://arxiv.org/abs/2505.22411) · [SmartThinker](https://arxiv.org/abs/2603.08000) · [Reasoning or Memorization](https://arxiv.org/html/2507.10532v3) · [LiveCodeBench](https://livecodebench.github.io/) · [QLoRA medical CoT](https://arxiv.org/html/2510.05003v1)
