# PAPERS: the related work, as a reading list

<!-- CURRENT-STUDY:START -->

**Current study — 14 October 2026:** **464 unique test problems**.
Benchmarks: **164 HumanEval+**, **166 LiveCodeBench easy**, **134 LiveCodeBench medium**.
All six planned LoRA combinations are complete, one attempt per problem:

- **0.8B:** LoRA + OFF **14.0% (65/464)**; LoRA + limit 512 **14.4% (67/464)**.
- **2B:** LoRA + OFF **35.6% (165/464)**; LoRA + limit 1,024 **41.2% (191/464)**.
- **4B:** LoRA + OFF **64.7% (300/464)**; LoRA + limit 2,048 **71.6% (332/464)**.

LoRA alone means thinking ON without a thinking-token limit.
Older methods' all-attempt averages and first-attempt comparisons are labelled separately.
LoRA + OFF does not consistently improve on free OFF; the 2B/4B gains over free limits remain uncertain.

[Every method, benchmark, difficulty, token count and interval](results/CURRENT-RESULTS.md) · [Full easy thesis](easy-thesis/FULL-THESIS.md) · [Full formal Markdown thesis](thesis/THESIS.md).

<!-- CURRENT-STUDY:END -->

> Hard word? See [GLOSSARY.md](GLOSSARY.md).

---

## How to read this list

### What the marks mean

> - **✔ checked** = someone opened the arXiv page and confirmed the claim (2026-09-13).
> - **⚠️ check before citing** = found in search results only. The claim may be slightly off.
>
> A "not found" gap means *we did not find* a paper. It does not mean that none exists.
> Search again before writing the related-work chapter.
>
> Full search notes: [research/](research/).

### Words you will see a lot

- *arXiv* = a free website where researchers post papers. Each paper has an id, like 2503.16419.
- A *token* = a small piece of text, about ¾ of a word. "−30% tokens" = the thinking got 30% shorter.
- *Fine-tuning* (FT) = extra training of a model that already exists, on our own examples.
- *Full fine-tuning* = training all of the model's numbers.
- *LoRA* = a cheap way to fine-tune. It trains only a few small extra parts.
- *SFT* = training on example answers.
- *RL* (reinforcement learning) = the model learns from rewards, like a dog getting treats.
- *Shortest correct of N* = let the model answer N times. Keep the shortest answer that is correct.
- "7B" after a model name = 7 billion numbers inside the model.

---

## Read these first (in this order)

| # | Paper | Why read it |
|---|---|---|
| 1 | **Stop Overthinking: A Survey on Efficient Reasoning** — Sui et al., TMLR 2025 — [2503.16419](https://arxiv.org/abs/2503.16419) | A map of the whole field. (A *survey* = a paper that summarizes many other papers) |
| 2 | **Self-Training Elicits Concise Reasoning in LLMs** — Munkhbat et al., ACL Findings 2025 — [2502.20122](https://arxiv.org/abs/2502.20122) ✔ | **Our exact method:** keep the shortest correct of N answers, then train on it. They did it on math. No data-size curve → our gap G-B |
| 3 | **SEER** (adaptive CoT compression) — [2509.14093](https://arxiv.org/abs/2509.14093) ✔ | **Closest to us.** Shortest correct answer + a length filter. Uses software-engineering code data and R1-Distill-7B (a small reasoning model that always thinks). About 40% shorter. **LoRA lost about 7 points vs full fine-tuning** |
| 4 | **ASAP: Pruning the Unsurprising** — [2508.05988](https://arxiv.org/abs/2508.05988) ✔ | Shorter code reasoning: −23.5% tokens on LiveCodeBench v4–v5 (a code test set that keeps adding new problems) |
| 5 | **NoThinking** — [2504.09858](https://arxiv.org/abs/2504.09858) ✔ | Thinking OFF can beat thinking with a limited budget → this is why OFF is a serious baseline (a serious thing to compare against) |
| 6 | **HRBench** — [2605.28398](https://arxiv.org/abs/2605.28398) ✔ | Compares ways to use the thinking switch (Qwen3.5-2B and bigger). No single winner. It compares switch use, not models trained to think shorter → our gap G-A |
| 7 | **S3-CoT** — [2602.01982](https://arxiv.org/abs/2602.01982) | ⚠️ **Warning:** training only on the very shortest answers hurts accuracy → this is the reason for our rule for picking answers |

---

## A. Shortening reasoning by training (mostly math)

### A.1 The papers

| Paper | What it did | Result | Mark |
|---|---|---|---|
| Self-Training Elicits Concise Reasoning — [2502.20122](https://arxiv.org/abs/2502.20122) | Shortest correct of 16 → full fine-tuning. Llama/Gemma/Qwen, 1.5–8B. GSM8K + MATH (about 7.5k examples) | −12% tokens (plain prompt), −24 to −36% (few-shot = a few worked examples in the prompt). Accuracy about the same | ✔ |
| TokenSkip — [2502.12067](https://arxiv.org/abs/2502.12067) | Removes unimportant tokens from its own correct answers. LoRA r=8 (r = size of the LoRA parts), on 2×RTX 3090 | −30 to −40% tokens. Big models lose little | ✔ |
| O1-Pruner — [2501.12570](https://arxiv.org/abs/2501.12570) | Fine-tuning that evens out answer length (length-harmonizing). 5k MATH problems | 7B: −35 to −43%, accuracy up | ⚠️ |
| L1 / LCPO — [2503.04697](https://arxiv.org/abs/2503.04697) | RL that follows a target length | Length can be controlled within about 3% | ⚠️ |
| ThinkPrune — [2504.01296](https://arxiv.org/abs/2504.01296) | RL with a token limit that gets tighter in stages | −43 to −65% | ⚠️ |
| ShorterBetter — [2504.21370](https://arxiv.org/abs/2504.21370) | RL reward = correct − distance to the shortest correct answer | −50 to −80% | ⚠️ |
| AdaptThink — [2505.13417](https://arxiv.org/abs/2505.13417) | RL that learns when to skip thinking | −40 to −53%, accuracy up | ⚠️ |
| Concise Reasoning via RL — [2504.05185](https://arxiv.org/abs/2504.05185) | RL on only 4–8 problems | −40 to −54% | ⚠️ |
| Training LMs to Reason Efficiently — [2502.04463](https://arxiv.org/abs/2502.04463) | RL. The reward gets smaller for longer answers. 3.2k prompts | −36 to −65% | ⚠️ |
| Kimi k1.5 — [2501.12599](https://arxiv.org/abs/2501.12599) | Length reward. "Shortest rejection sampling": 8 samples → SFT on the shortest | Long-to-short works | ⚠️ |
| DAST — [2503.04472](https://arxiv.org/abs/2503.04472) | Pairs of better/worse answers (preference pairs) with a length budget | −18 to −46% | ⚠️ |
| Do NOT Think That Much for 2+3=? — [2412.21187](https://arxiv.org/abs/2412.21187) | Defines "overthinking". Self-training with the shortest answers | −22 to −45% | ⚠️ |
| Don't Overthink It — [2505.17813](https://arxiv.org/abs/2505.17813) | The shortest chains of thinking are up to 34.5% more accurate than the longest | Only −6% tokens from SFT on 1k examples | ⚠️ |
| S3-CoT — [2602.01982](https://arxiv.org/abs/2602.01982) | A step-by-step plan (curriculum) of the model's own answer lengths. Includes Qwen3-4B-Thinking | **Training on the shortest only hurts accuracy** | ⚠️ |
| Correct, Concise and Complete — [2601.02972](https://arxiv.org/abs/2601.02972) | SFT, then RL that penalises tokens written after the first correct answer | −28 to −40% | ⚠️ |
| Acoer — [2606.22716](https://arxiv.org/abs/2606.22716) | GRPO (a kind of RL) + LoRA on Qwen3-1.7B | **Penalising the length of wrong answers → collapse (training falls apart)** | ⚠️ |
| The Art of Efficient Reasoning — [2602.20945](https://arxiv.org/abs/2602.20945) | A huge ablation (tests that remove one part to see if it mattered) on Qwen3 0.6–30B | Warns of the "short-is-correct trap" | ✔ |
| Hint Tuning — [2605.08665](https://arxiv.org/abs/2605.08665) | 1k examples that the model labeled itself (self-annotated) | −24 to −66% tokens | ✔ |
| STOP — [2605.13165](https://arxiv.org/abs/2605.13165) | Cuts each answer at the earliest point where it is correct. Fine-tuning with little data | — | ✔ |
| Step-GRPO — [2604.16890](https://arxiv.org/abs/2604.16890) | RL on Qwen3-8B | −32% tokens | ⚠️ |
| DLER — [2510.15110](https://arxiv.org/abs/2510.15110) | A simple penalty when the answer gets cut off (truncation penalty), plus a better RL recipe | >70% shorter | ⚠️ |

### A.2 A small amount of data can change behaviour

- s1 [2501.19393](https://arxiv.org/abs/2501.19393): 1,000 examples.
- LIMO [2502.03387](https://arxiv.org/abs/2502.03387): 400 examples gave most of the gain. Going from 800 → 1,200+ added little more.

Both ⚠️.

---

## B. Shorter reasoning for CODE (closest to us)

Words in this table:
- *LCB* = LiveCodeBench. *pass@1* = how often the first try passes the tests.
- *Training-free* = no training; only the way we use the model changes.
- *Trace* = the thinking text the model writes before its answer.

| Paper | What it did | Mark |
|---|---|---|
| **SEER** — [2509.14093](https://arxiv.org/abs/2509.14093) | Best-of-N shortest correct answer + a length filter. Software-engineering code data. R1-Distill-7B, full FT. Also works on HumanEval/MBPP, with 30–40% shorter reasoning. **LoRA 67.7% vs full FT 74.9%** | ✔ |
| **ASAP** — [2508.05988](https://arxiv.org/abs/2508.05988) | Cuts unneeded parts from code traces. R1-Distill-7B, Llama-8B. −23.5% tokens on LCB v4–v5 at 36.2% pass@1 | ✔ |
| EvoThink — [2607.19962](https://arxiv.org/abs/2607.19962) | The model cuts its own thinking (self-pruning) + learns from better/worse pairs (preference optimisation). Math and code (IJCAI 2026) | ✔ (abstract only) |
| SEER (different paper, same name) — [2510.17130](https://arxiv.org/abs/2510.17130) | Writes code. Switches between a direct answer and step-by-step thinking | ✔ |
| Reasoning steps in thinking code LLMs — [2511.05874](https://arxiv.org/abs/2511.05874) | Cutting 10–30% of steps keeps easy tasks OK, but **hurts hard ones** (no training) | ✔ |
| Reasoning as a Resource — [2506.09396](https://arxiv.org/abs/2506.09396) | Position paper (an opinion paper): fast vs slow thinking for code | ✔ |
| DART — [2606.23181](https://arxiv.org/abs/2606.23181) | Training-free. Picks a thinking budget per problem (routing). Code accuracy up to +22.5 pts with 51–63% fewer tokens | ✔ |
| RoutingGen — [2512.14048](https://arxiv.org/abs/2512.14048) | Prompting only. Picks the way to answer by how hard the problem is. −46% tokens | ⚠️ |
| LogitsCoder — [2602.14054](https://arxiv.org/abs/2602.14054) | Controls reasoning length while the model writes (during decoding), for code | ⚠️ |
| TACT — [2605.05980](https://arxiv.org/abs/2605.05980) | Nudges the model's inner signals (activation steering) against overthinking, in a coding agent | ⚠️ |
| Semantic early exit — [2605.17672](https://arxiv.org/abs/2605.17672) | Stops thinking early. −26% tokens on code | ⚠️ |
| The Danger of Overthinking — [2502.08235](https://arxiv.org/abs/2502.08235) | Overthinking in coding agents (SWE-bench) | ⚠️ |
| OckBench — [2511.05722](https://arxiv.org/abs/2511.05722) | A benchmark (fixed test set) that measures accuracy and tokens together | ⚠️ |

---

## C. Models with a thinking ON/OFF switch

A *hybrid model* = a model with a thinking ON/OFF switch. "No-think mode" = the switch is OFF.

| Paper | What it did | Mark |
|---|---|---|
| HRBench — [2605.28398](https://arxiv.org/abs/2605.28398) | A benchmark of ways to use the switch (training-free, SFT, RL). Models from Qwen3.5-2B → Kimi-K2.5. Math/science/code | ✔ |
| NoThinking — [2504.09858](https://arxiv.org/abs/2504.09858) | Skipping thinking beats a small thinking budget (<3k tokens), including coding | ✔ |
| Demystifying Hybrid Thinking — [2510.12680](https://arxiv.org/abs/2510.12680) | Reasoning leaks into no-think mode. About 140k examples for a clean switch | ✔ |
| TNT — [2601.04805](https://arxiv.org/abs/2601.04805) | RL that learns when to think. About 50% fewer tokens | ✔ |
| 3TF — [2511.03408](https://arxiv.org/abs/2511.03408) | Trains hybrid models so no-think mode keeps its quality | ✔ |
| TFPI — [2509.26226](https://arxiv.org/abs/2509.26226) | RL with thinking removed. 4B model. AIME24 + LiveCodeBench | ✔ |
| D-COT — [2602.21786](https://arxiv.org/abs/2602.21786) | Qwen3-8B, 5k examples, less overthinking | ✔ |
| Mid-Think — [2601.07036](https://arxiv.org/abs/2601.07036) | In-between thinking budgets on Qwen3 | ⚠️ |
| Thinkless — [2505.13379](https://arxiv.org/abs/2505.13379) · OThink-R1 — [2506.02397](https://arxiv.org/abs/2506.02397) | Learn when to think (mostly math) | ⚠️ |
| Gemma 4 Tech Report — [2607.02770](https://arxiv.org/abs/2607.02770) | Confirms that Gemma 4 has a thinking mode | ✔ |

---

## D. Transfer between domains (all math → code; code → math not found)

*Transfer* = train on one kind of problem (a *domain*), then test on another kind.
Everyday example: you learn to drive a car. Does that help you drive a van?

| Paper | Result | Mark |
|---|---|---|
| HAPO — [2505.11225](https://arxiv.org/abs/2505.11225) | Math → LiveCodeBench: −34% length, accuracy slightly up | ⚠️ |
| LC-R1 — [2506.14755](https://arxiv.org/abs/2506.14755) | Still works out of domain (on a different kind of problem) | ⚠️ |
| One-Domain-to-All — [2601.06052](https://arxiv.org/abs/2601.06052) | Math → code/SWE, up to −44% | ✔ |
| Reconsidering Overthinking — [2508.02178](https://arxiv.org/abs/2508.02178) | Math → LiveCodeBench: the gains transfer | ⚠️ |
| ETR — [2604.05355](https://arxiv.org/abs/2604.05355) | Math → HumanEval (from search text only: Qwen3-4B, fewer tokens, higher accuracy) | ⚠️ |

---

## D2. Loops and model size (found 2026-09-25, for the analysis and future work)

Full notes: [research/2026-09-25-bigger-models-and-loops-evidence.md](research/2026-09-25-bigger-models-and-loops-evidence.md).

| Source | What it says | Mark |
|---|---|---|
| **Qwen3.5-2B model card** — [huggingface.co/Qwen/Qwen3.5-2B](https://huggingface.co/Qwen/Qwen3.5-2B) | *"Qwen3.5-2B is more prone to entering thinking loops compared to other Qwen3.5 models"*. Coding settings = ours (temp 0.6, top-p 0.95, top-k 20, no penalty) | ✔ |
| **Wait, Wait, Wait... Why Do Reasoning Models Loop?** — Pipis et al. — [2512.12895](https://arxiv.org/abs/2512.12895) | *"Larger models tend to loop less"*; higher temperature reduces looping | ✔ |
| **Small Models Struggle to Learn from Strong Reasoners** — Li et al. — [2502.12143](https://arxiv.org/abs/2502.12143) | Models ≤3B *"do not consistently benefit from long chain-of-thought"* | ✔ |
| **s1: Simple test-time scaling** — [2501.19393](https://arxiv.org/abs/2501.19393) | "Budget forcing": stop thinking at a budget (or lengthen it). Mainly used to make thinking longer | ⚠️ helper-checked |
| **Qwen3 Technical Report** — [2505.09388](https://arxiv.org/abs/2505.09388) | One model with thinking and non-thinking modes, plus a "thinking budget mechanism" | ⚠️ helper-checked |

---

## E. Contamination and statistics (for the method chapter)

- *Contamination* = the model may have already seen the test problems during training.
- Everyday example: a student who saw the exam questions the night before.

The papers:
- Reasoning or Memorization? — [2507.10532](https://arxiv.org/abs/2507.10532): contamination in math benchmarks. ⚠️
- Hochlehnert et al. — [2504.07086](https://arxiv.org/abs/2504.07086): on AIME, the noise from the seed (the random starting number) and the setup is bigger than many claimed gains. ⚠️
- Miller, "Adding Error Bars to Evals" — [2411.00640](https://arxiv.org/abs/2411.00640): clustered and paired confidence intervals. That means error bars that group results by problem and compare the same problems before and after. ⚠️

## Internal Qwen3.5 follow-up — checked 14 October 2026

- [Gated Delta Networks](https://arxiv.org/abs/2412.06464): architecture paper; memory retention and correction. Paper text checked.
- [ReBalance: Efficient Reasoning with Balanced Thinking](https://arxiv.org/abs/2603.12372): confidence-based internal steering. Paper text checked.
- [Gated DeltaNet-2](https://arxiv.org/abs/2605.22791): separate erase/write gates. Abstract checked.
- [ASAG](https://arxiv.org/abs/2606.15070): attention-state adaptive generation. Abstract checked.
- [When Chain-of-Thought Fails, the Solution Hides in the Hidden States](https://arxiv.org/abs/2604.23351): causal activation patching. Abstract checked.
- Official [0.8B](https://huggingface.co/Qwen/Qwen3.5-0.8B), [2B](https://huggingface.co/Qwen/Qwen3.5-2B), [4B](https://huggingface.co/Qwen/Qwen3.5-4B) cards and [Transformers code](https://github.com/huggingface/transformers/blob/main/src/transformers/models/qwen3_5/modeling_qwen3_5.py) checked. A dedicated dense-family technical report was not located in this search.

These establish prior work, not novelty or an internal cause of our loops.
[Full notes](experiments/rpmr/proposal.md).

## Narrow novelty screening — 14 October 2026

Primary literature inspected for a provisional recurrent-memory repair proposal:

- [SOPHIA](https://arxiv.org/html/2607.18100v1): online self-loop detection and transition-conditioned residual steering.
- [AlphaEdit](https://arxiv.org/html/2410.02355v3): null-space protection for parameter editing. Borrowed mathematical principle.
- [SSM subspace bottlenecks](https://arxiv.org/html/2602.22719v1): test-time Mamba activation scaling.
- [ACE](https://arxiv.org/html/2607.00588v1): repetition-direction subtraction in continuous diffusion feedback.
- [Wait, Wait, Wait](https://arxiv.org/html/2512.12895v1): learning errors and reasoning loops.
- [MARCH / Safin-1](https://arxiv.org/html/2609.00092v1): recurrent memory-history reading, including GDN.
- [Liquid Antidoom](https://www.liquid.ai/blog/antidoom): targeted final-token preference training against loops.
- [Dynamic Closed-Loop Steering](https://www.mdpi.com/2076-3417/16/13/6423): publisher search text inspected; full-page access failed. Closely related geometry-based steering; full review still needed.
- [MaLoRA](https://arxiv.org/abs/2607.19326) and [Efficient Reasoning on the Edge](https://arxiv.org/abs/2603.16867): abstracts checked; adaptive adapter scaling/switching already exists.

[Full method differences and bounded novelty statement](experiments/rpmr/proposal.md). No method was reproduced; no exact match found is not proof of novelty.
