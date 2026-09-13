# PAPERS — the related work, as a reading list

> **✔ checked** = someone opened the arXiv page and confirmed the claim (2026-09-13).
> **⚠️ check before citing** = found in search results only. The claim may be slightly off.
>
> A "not found" gap means *we did not find* a paper, not that none exists.
> Search again before writing the related-work chapter.
>
> Full search notes: [research/](research/).

---

## Read these first (in this order)

| # | Paper | Why read it |
|---|---|---|
| 1 | **Stop Overthinking: A Survey on Efficient Reasoning** — Sui et al., TMLR 2025 — [2503.16419](https://arxiv.org/abs/2503.16419) | The map of the whole field |
| 2 | **Self-Training Elicits Concise Reasoning in LLMs** — Munkhbat et al., ACL Findings 2025 — [2502.20122](https://arxiv.org/abs/2502.20122) ✔ | **Our exact method** (keep the shortest correct of N answers, train on it), on math. No data-size curve → our gap G-B |
| 3 | **SEER** (adaptive CoT compression) — [2509.14093](https://arxiv.org/abs/2509.14093) ✔ | **Closest to us:** shortest-correct + length filter on software-engineering code data, R1-Distill-7B, ~40% shorter. **LoRA lost ~7 points vs full fine-tuning** |
| 4 | **ASAP: Pruning the Unsurprising** — [2508.05988](https://arxiv.org/abs/2508.05988) ✔ | Shorter code reasoning, −23.5% tokens on LiveCodeBench v4–v5 |
| 5 | **NoThinking** — [2504.09858](https://arxiv.org/abs/2504.09858) ✔ | Thinking OFF can beat a limited thinking budget → why OFF is a serious baseline |
| 6 | **HRBench** — [2605.28398](https://arxiv.org/abs/2605.28398) ✔ | Compares ways to use the thinking switch (Qwen3.5-2B and up); no single winner. Compares switches, not length-trained models → our gap G-A |
| 7 | **S3-CoT** — [2602.01982](https://arxiv.org/abs/2602.01982) | ⚠️ **Warning:** training only on the very shortest answers hurts accuracy → our selection rule |

---

## A. Shortening reasoning by training (mostly math)

| Paper | What it did | Result | Mark |
|---|---|---|---|
| Self-Training Elicits Concise Reasoning — [2502.20122](https://arxiv.org/abs/2502.20122) | Shortest correct of 16 → full fine-tuning; Llama/Gemma/Qwen 1.5–8B; GSM8K + MATH (~7.5k examples) | −12% tokens (plain), −24 to −36% (few-shot); accuracy ~kept | ✔ |
| TokenSkip — [2502.12067](https://arxiv.org/abs/2502.12067) | Prunes unimportant tokens from its own correct answers, LoRA r=8, on 2×RTX 3090 | −30 to −40% tokens; big models lose little | ✔ |
| O1-Pruner — [2501.12570](https://arxiv.org/abs/2501.12570) | Length-harmonizing fine-tuning, 5k MATH problems | 7B: −35 to −43%, accuracy up | ⚠️ |
| L1 / LCPO — [2503.04697](https://arxiv.org/abs/2503.04697) | RL that follows a target length | Length controllable within ~3% | ⚠️ |
| ThinkPrune — [2504.01296](https://arxiv.org/abs/2504.01296) | RL with a token limit tightened in stages | −43 to −65% | ⚠️ |
| ShorterBetter — [2504.21370](https://arxiv.org/abs/2504.21370) | RL reward = correct − distance to shortest correct | −50 to −80% | ⚠️ |
| AdaptThink — [2505.13417](https://arxiv.org/abs/2505.13417) | RL that learns when to skip thinking | −40 to −53%, accuracy up | ⚠️ |
| Concise Reasoning via RL — [2504.05185](https://arxiv.org/abs/2504.05185) | RL on only 4–8 problems | −40 to −54% | ⚠️ |
| Training LMs to Reason Efficiently — [2502.04463](https://arxiv.org/abs/2502.04463) | RL, reward scaled down by length, 3.2k prompts | −36 to −65% | ⚠️ |
| Kimi k1.5 — [2501.12599](https://arxiv.org/abs/2501.12599) | Length reward; "shortest rejection sampling" (8 samples → SFT) | Long-to-short works | ⚠️ |
| DAST — [2503.04472](https://arxiv.org/abs/2503.04472) | Preference pairs with a length budget | −18 to −46% | ⚠️ |
| Do NOT Think That Much for 2+3=? — [2412.21187](https://arxiv.org/abs/2412.21187) | Defines overthinking; self-training with shortest answers | −22 to −45% | ⚠️ |
| Don't Overthink It — [2505.17813](https://arxiv.org/abs/2505.17813) | Shortest chains are up to 34.5% more accurate than longest | Only −6% tokens from SFT on 1k | ⚠️ |
| S3-CoT — [2602.01982](https://arxiv.org/abs/2602.01982) | Curriculum of self-sampled lengths, incl. Qwen3-4B-Thinking | **Shortest-only hurts accuracy** | ⚠️ |
| Correct, Concise and Complete — [2601.02972](https://arxiv.org/abs/2601.02972) | SFT then RL penalising tokens after the first correct answer | −28 to −40% | ⚠️ |
| Acoer — [2606.22716](https://arxiv.org/abs/2606.22716) | GRPO + LoRA on Qwen3-1.7B | **Penalising wrong answers' length → collapse** | ⚠️ |
| The Art of Efficient Reasoning — [2602.20945](https://arxiv.org/abs/2602.20945) | Huge ablation on Qwen3 0.6–30B | Warns of the "short-is-correct trap" | ✔ |
| Hint Tuning — [2605.08665](https://arxiv.org/abs/2605.08665) | 1k self-annotated examples | −24 to −66% tokens | ✔ |
| STOP — [2605.13165](https://arxiv.org/abs/2605.13165) | Cut at the earliest correct point, low-data fine-tuning | — | ✔ |
| Step-GRPO — [2604.16890](https://arxiv.org/abs/2604.16890) | RL on Qwen3-8B | −32% tokens | ⚠️ |
| DLER — [2510.15110](https://arxiv.org/abs/2510.15110) | Simple truncation penalty, better RL recipe | >70% shorter | ⚠️ |

**Small data can change behaviour:**
- s1 [2501.19393](https://arxiv.org/abs/2501.19393): 1,000 examples.
- LIMO [2502.03387](https://arxiv.org/abs/2502.03387): 400 gave most of the gain, 800 → 1,200+ gave little more.

Both ⚠️.

---

## B. Shorter reasoning for CODE (closest to us)

| Paper | What it did | Mark |
|---|---|---|
| **SEER** — [2509.14093](https://arxiv.org/abs/2509.14093) | Best-of-N shortest correct + length filter, software-engineering code data, R1-Distill-7B, full FT; transfers to HumanEval/MBPP with 30–40% shorter reasoning. **LoRA 67.7% vs full FT 74.9%** | ✔ |
| **ASAP** — [2508.05988](https://arxiv.org/abs/2508.05988) | Prunes code reasoning traces; R1-Distill-7B, Llama-8B; −23.5% tokens on LCB v4–v5 at 36.2% pass@1 | ✔ |
| EvoThink — [2607.19962](https://arxiv.org/abs/2607.19962) | Self-pruning + preference optimisation, math and code (IJCAI 2026) | ✔ (abstract only) |
| SEER (different paper, same name) — [2510.17130](https://arxiv.org/abs/2510.17130) | Code generation that switches between direct answer and step-by-step | ✔ |
| Reasoning steps in thinking code LLMs — [2511.05874](https://arxiv.org/abs/2511.05874) | Cutting 10–30% of steps keeps easy tasks, **hurts hard ones** (no training) | ✔ |
| Reasoning as a Resource — [2506.09396](https://arxiv.org/abs/2506.09396) | Position paper: fast vs slow thinking for code | ✔ |
| DART — [2606.23181](https://arxiv.org/abs/2606.23181) | Training-free thinking-budget routing; code accuracy up to +22.5 pts with 51–63% fewer tokens | ✔ |
| RoutingGen — [2512.14048](https://arxiv.org/abs/2512.14048) | Prompting only, routes by difficulty; −46% tokens | ⚠️ |
| LogitsCoder — [2602.14054](https://arxiv.org/abs/2602.14054) | Controls reasoning length during decoding, for code | ⚠️ |
| TACT — [2605.05980](https://arxiv.org/abs/2605.05980) | Activation steering against overthinking in a coding agent | ⚠️ |
| Semantic early exit — [2605.17672](https://arxiv.org/abs/2605.17672) | Early exit, −26% tokens on code | ⚠️ |
| The Danger of Overthinking — [2502.08235](https://arxiv.org/abs/2502.08235) | Overthinking in coding agents (SWE-bench) | ⚠️ |
| OckBench — [2511.05722](https://arxiv.org/abs/2511.05722) | Benchmark measuring accuracy and tokens together | ⚠️ |

---

## C. Models with a thinking ON/OFF switch

| Paper | What it did | Mark |
|---|---|---|
| HRBench — [2605.28398](https://arxiv.org/abs/2605.28398) | Benchmarks switch strategies (training-free, SFT, RL), Qwen3.5-2B → Kimi-K2.5, math/science/code | ✔ |
| NoThinking — [2504.09858](https://arxiv.org/abs/2504.09858) | Skipping thinking beats a small budget (<3k), incl. coding | ✔ |
| Demystifying Hybrid Thinking — [2510.12680](https://arxiv.org/abs/2510.12680) | Reasoning leaks into no-think mode; ~140k examples for a clean switch | ✔ |
| TNT — [2601.04805](https://arxiv.org/abs/2601.04805) | RL for when to think; ~50% fewer tokens | ✔ |
| 3TF — [2511.03408](https://arxiv.org/abs/2511.03408) | Trains hybrid models so no-think keeps quality | ✔ |
| TFPI — [2509.26226](https://arxiv.org/abs/2509.26226) | RL with thinking removed, 4B, AIME24 + LiveCodeBench | ✔ |
| D-COT — [2602.21786](https://arxiv.org/abs/2602.21786) | Qwen3-8B, 5k examples, less overthinking | ✔ |
| Mid-Think — [2601.07036](https://arxiv.org/abs/2601.07036) | In-between thinking budgets on Qwen3 | ⚠️ |
| Thinkless — [2505.13379](https://arxiv.org/abs/2505.13379) · OThink-R1 — [2506.02397](https://arxiv.org/abs/2506.02397) | Learn when to think (mostly math) | ⚠️ |
| Gemma 4 Tech Report — [2607.02770](https://arxiv.org/abs/2607.02770) | Confirms Gemma 4 has thinking mode | ✔ |

---

## D. Transfer between domains (all math → code; code → math not found)

| Paper | Result | Mark |
|---|---|---|
| HAPO — [2505.11225](https://arxiv.org/abs/2505.11225) | Math → LiveCodeBench: −34% length, accuracy slightly up | ⚠️ |
| LC-R1 — [2506.14755](https://arxiv.org/abs/2506.14755) | Holds out of domain | ⚠️ |
| One-Domain-to-All — [2601.06052](https://arxiv.org/abs/2601.06052) | Math → code/SWE, up to −44% | ✔ |
| Reconsidering Overthinking — [2508.02178](https://arxiv.org/abs/2508.02178) | Math → LiveCodeBench transfers | ⚠️ |
| ETR — [2604.05355](https://arxiv.org/abs/2604.05355) | Math → HumanEval (search text: Qwen3-4B, fewer tokens, higher accuracy) | ⚠️ |

---

## E. Contamination and statistics (for the method chapter)

- Reasoning or Memorization? — [2507.10532](https://arxiv.org/abs/2507.10532): contamination in math benchmarks. ⚠️
- Hochlehnert et al. — [2504.07086](https://arxiv.org/abs/2504.07086): on AIME, seed and setup noise is bigger than many claimed gains. ⚠️
- Miller, "Adding Error Bars to Evals" — [2411.00640](https://arxiv.org/abs/2411.00640): clustered and paired confidence intervals. ⚠️
