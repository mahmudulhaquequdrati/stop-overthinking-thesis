# Research note — verifying the research gaps (2026-09-13)

> **How this was made:** a web search agent tried to *refute* each claimed gap by
> searching arXiv and 2025–2026 venues.
> ✔ = checked on the arXiv page or full text. No mark = from search-result text only.
> "Not found" means *we didn't find* a paper, not that none exists.
>
> Decisions drawn from this: [DECISIONS.md](../DECISIONS.md) #4, #15, #19, #20 and
> [PLAN.md](../PLAN.md) §4.

**Summary:** only **G2** (how much training data) is clearly OPEN. G1, G4, G5, G6 are
PARTLY FILLED. G3 is mostly FILLED as phrased (the 2026-model version is thin).
The open space is narrower than first claimed. The closest work is **SEER 2509.14093**,
which already does shortest-correct fine-tuning on code tasks and compares LoRA with
full fine-tuning.

---

## G1. Short reasoning for code gets less attention than math → PARTLY FILLED

| Paper | arXiv / date | What it did |
|---|---|---|
| ASAP "Pruning the Unsurprising" ✔ | 2508.05988, Aug 2025 (v2 Jan 2026) | Prunes long code reasoning traces, then full fine-tunes R1-Distill-Qwen-7B and Llama-8B on CodeForces traces. Tested on HumanEval/+, LCB v1–v3, v4–v5, LeetCodeDataset. ~23.5% fewer tokens on LCB v4–v5 at 36.2% pass@1 |
| SEER (adaptive compression) ✔ | 2509.14093, Sep 2025 | **Not math:** software-engineering data (MathQA-Python, defect detection, code search). Shortest-correct-of-N + length filter, full FT of R1-Distill-Qwen-7B on 4×A800. ~40% shorter. Transfers to HumanEval/MBPP, 30–40% shorter. **LoRA 67.7% vs full FT 74.9%** |
| EvoThink ✔ (summary page) | 2607.19962, Jul 2026, IJCAI 2026 | Self-pruning + preference optimisation, math and code |
| SEER (different paper, same name) ✔ | 2510.17130, Oct 2025 | Code generation switching between direct answer and step-by-step |
| RoutingGen / Intention CoT | 2512.14048, AAAI 2026 | Prompting only, routes by difficulty; −46% tokens on McEval |
| LogitsCoder | 2602.14054 | Decoding-time reasoning-length control for code |
| TACT | 2605.05980 | Training-free activation steering against overthinking, 27B coding agent; +5.8 pts |
| The Danger of Overthinking | 2502.08235 | Analysis on SWE-bench Verified: picking less-overthinking runs gives ~+30% performance, −43% cost |
| Reasoning steps in thinking code LLMs ✔ | 2511.05874 | 6 reasoning models, 100 BigCodeBench tasks. **Cutting 10–30% of steps keeps standard tasks but hurts hard ones.** No training |
| Reasoning as a Resource ✔ | 2506.09396 | Position paper, fast vs slow thinking for code |
| DART ✔ | 2606.23181, EMNLP Findings | Training-free thinking-budget routing; code accuracy up to +22.5 with 51–63% fewer tokens |
| Semantic early exit | 2605.17672 | −26.2% tokens on code |
| OckBench | 2511.05722 | Benchmark of accuracy + token use, incl. coding |

**Count:** ~3 papers train for shorter reasoning mainly on code (ASAP, SEER, EvoThink). All use R1-Distill-7B-class always-thinking models with full fine-tuning. Math has dozens.
**Consequence:** we can say code is under-studied, **not** that nobody did shortest-correct training on code.

## G2. How many training examples are needed → OPEN (not found)

| Paper | arXiv | Relevance |
|---|---|---|
| Hint Tuning ✔ | 2605.08665 | 1,000 examples → 24–66% fewer tokens (Qwen3-Thinking, R1-Distill, 4–32B). No data-size curve |
| STOP ✔ | 2605.13165 | Prunes to earliest correct point, low-data FT, R1-Distill-7B/8B, math. No curve in abstract |
| The Art of Efficient Reasoning ✔ | 2602.20945 | ~0.2M GPU-h ablation on Qwen3 0.6–30B; warns of the "short-is-correct trap". Unclear whether it varies example count |
| Demystifying Hybrid Thinking ✔ | 2510.12680 | ~140k examples for a stable think/no-think switch (about the switch, not length) |
| Self-Training Elicits Concise Reasoning ✔ | 2502.20122 | Full FT on 8×H100; equal sampling budget, but example count not varied |

**Conclusion:** no learning curve of accuracy and token savings vs number of shortest-correct examples was found. It's cheap to run on a T4.

## G3. Possibly-seen test sets → mostly FILLED; the 2026-model version is OPEN but thin

- Many 2025–26 papers already use AIME 2025, LCB v5/v6, or post-cutoff LeetCodeDataset (SmartThinker 2603.08000, ASAP, NoWait 2506.08343). For R1-Distill models those are post-cutoff.
- "Reasoning or Memorization?" 2507.10532: Qwen2.5 contamination on math benchmarks (not about shorter reasoning).
- For 2026 models, AIME 2025 and older LCB are probably pre-cutoff. No paper found using AIME 2026 or 2026 LCB problems.
- No paper found asking whether length reduction behaves differently on memorized vs fresh problems.

**Consequence:** fresh test sets are good practice, not a main contribution. Memorized-vs-fresh can be a small secondary finding (G-E in PLAN).

## G4. Models with a thinking switch → PARTLY FILLED

| Paper | arXiv | Relevance |
|---|---|---|
| Demystifying Hybrid Thinking ✔ | 2510.12680 | Reasoning leaks into no-think mode; training recipe for a cleaner switch |
| HRBench ✔ | 2605.28398 | Benchmarks switch strategies (training-free, FT, offline/online RL), Qwen3.5-2B → Kimi-K2.5, math/science/code. No single best |
| DART ✔ | 2606.23181 | Training-free; compared with always-thinking and no-thinking |
| Mid-Think | 2601.07036 | Intermediate budgets on Qwen3 via trigger tokens |
| NoThinking ✔ | 2504.09858 | Skipping thinking beats budget-limited thinking under ~3k, incl. coding (R1-Distill) |
| TFPI ✔ | 2509.26226 | RL with thinking removed, 4B, AIME24 + LCB |
| 3TF ✔ | 2511.03408 | Trains hybrid so no-think keeps reasoning quality |
| TNT ✔ | 2601.04805 | RL for when to think; ~50% fewer tokens (R1-Distill, math) |
| D-COT ✔ | 2602.21786 | Qwen3-8B, 5k examples, less overthinking on GPQA/MMLU-Pro |
| Art of Efficient Reasoning ✔; ETR 2604.05355 | 2026 | Length RL directly on Qwen3 hybrid models |
| Thinkless 2505.13379, AdaCoT, LHRM, AutoThink, ARM, OThink-R1 2506.02397 | 2025 | Learn when to think; mostly R1-Distill/custom, math |
| Gemma 4 Tech Report ✔ | 2607.02770; eval 2604.07035 | Confirms thinking mode. **No length-reduction training on Gemma-4-E4B found** |

**What remains open:** one controlled comparison, on the same ~4B hybrid model, of thinking ON, OFF, budget, and ON + shortest-correct fine-tuning, broken down by domain. Not found, and not on Gemma-4-E4B. → **our main gap G-A.**

## G5. LoRA on a single free GPU → PARTLY FILLED, weak as a contribution

- TokenSkip ✔: LoRA r=8 on 2× RTX 3090, ~2 h for 7B.
- SEER ✔: LoRA works but loses ~7 points vs full FT. A warning, and testable (our G-D rank check).
- Tina (LoRA RL, ~$9) and medical CoT QLoRA 2510.05003 (Kaggle GPUs): cheap reasoning FT, not for shorter reasoning.
- Nothing found on a T4 (16 GB, no bf16/FA2).

**Consequence:** "fits on a T4" is an engineering fact. Present it as a constraint and reproducibility bonus.

## G6. Transfer between math and code → math→code FILLED; code→math OPEN (not found)

| Paper | Direction | Result |
|---|---|---|
| HAPO 2505.11225 (AAAI 2026) | Math → LCB | 34% shorter, accuracy slightly up; weaker than in-domain. GPQA −27% length, −2 pts |
| LC-R1 2506.14755 | Math → LCB, GPQA | Holds out of domain; in-domain −46 to −52%, ~−2 pts |
| One-Domain-to-All ✔ 2601.06052 | Math → code, SWE, instruction following | Up to −44% out of domain; 13% fewer SWE-bench rounds |
| Reconsidering Overthinking 2508.02178 | Math → LCB | Gains transfer |
| ETR 2604.05355 (ACL 2026) | Math → HumanEval | Search text: Qwen3-4B 41.5% → 53.7%, 3,397 → 1,838 tokens (unverified) |
| Manifold Steering 2505.22411 | Math → code (no training) | Transfers |
| Art of Efficient Reasoning ✔ | Cross-domain | Learned length preferences transfer |
| SEER 2509.14093 ✔ | SE tasks → HumanEval/MBPP | Code to code only |

→ **our gap G-C: train on code, test on math.**

---

## Top 3 open gaps (from the search)

1. **Same-model comparison on a ~4B hybrid model:** OFF, budget, ON + shortest-correct LoRA, by domain. Does training beat flipping the switch? (HRBench and DART compare routing, not length-trained models.)
2. **Learning curve over data size:** accuracy and token savings at ~100/250/500/1k/2k examples. Not found, cheap, easy to read.
3. **Code → math transfer**, with math → code as a replication check against HAPO / LC-R1 / ETR.

## Recommendation from the search: code or math?

**Code as the main training domain, easy–medium difficulty, math as the transfer target.**
- **Novelty:** only ~3 code papers, all full FT on R1-Distill-7B with no switch; code → math not found.
- **Feasibility:** math is easier (string matching vs sandbox). Code traces are long (5–15k), so on a T4 sampling is slow and training sequences are capped at ~4k tokens, pushing toward easier problems. Say so explicitly.
- **Plan:** train on MBPP/TACO/LeetCode easy–medium; test on post-cutoff LCB (+ HumanEval+); MATH-500 + AIME 2026 for transfer; include the thinking-OFF baseline, the data-size curve, and a LoRA rank ablation.
- **Cite carefully:** SEER 2509.14093 is not math; HAPO/LC-R1 already showed math → code.
- **Not verified:** Gemma 4 fp16 stability on T4; Qwen3.5 and Gemma 4 cutoffs; whether LCB has problems after those cutoffs.

---

## Sources

- **G1, code:** [ASAP](https://arxiv.org/abs/2508.05988) · [SEER 2509.14093](https://arxiv.org/html/2509.14093) · [SEER 2510.17130](https://arxiv.org/abs/2510.17130) · [EvoThink](https://arxiv.org/abs/2607.19962) · [RoutingGen](https://arxiv.org/abs/2512.14048) · [LogitsCoder](https://arxiv.org/pdf/2602.14054) · [TACT](https://arxiv.org/abs/2605.05980) · [Danger of Overthinking](https://arxiv.org/abs/2502.08235v1) · [2511.05874](https://arxiv.org/abs/2511.05874) · [2506.09396](https://arxiv.org/abs/2506.09396) · [OckBench](https://arxiv.org/pdf/2511.05722)
- **G2, data size:** [Hint Tuning](https://arxiv.org/abs/2605.08665) · [STOP](https://arxiv.org/abs/2605.13165) · [Art of Efficient Reasoning](https://arxiv.org/abs/2602.20945) · [2502.20122](https://arxiv.org/html/2502.20122v2) · [TokenSkip](https://arxiv.org/html/2502.12067)
- **G4, thinking switch:** [Demystifying Hybrid Thinking](https://arxiv.org/abs/2510.12680) · [HRBench](https://arxiv.org/abs/2605.28398) · [DART](https://arxiv.org/abs/2606.23181) · [Mid-Think](https://arxiv.org/html/2601.07036v2) · [NoThinking](https://arxiv.org/pdf/2504.09858) · [TFPI](https://arxiv.org/abs/2509.26226) · [3TF](https://arxiv.org/abs/2511.03408) · [TNT](https://arxiv.org/abs/2601.04805) · [D-COT](https://arxiv.org/abs/2602.21786) · [OThink-R1](https://arxiv.org/abs/2506.02397) · [Thinkless](https://arxiv.org/abs/2505.13379) · [Gemma 4 report](https://arxiv.org/abs/2607.02770) · [2604.07035](https://arxiv.org/abs/2604.07035)
- **G3, G6, transfer and contamination:** [HAPO](https://arxiv.org/html/2505.11225) · [LC-R1](https://arxiv.org/html/2506.14755) · [One-Domain-to-All](https://arxiv.org/abs/2601.06052) · [Reconsidering Overthinking](https://arxiv.org/abs/2508.02178) · [ETR](https://arxiv.org/abs/2604.05355) · [Manifold Steering](https://arxiv.org/abs/2505.22411) · [SmartThinker](https://arxiv.org/abs/2603.08000) · [Reasoning or Memorization](https://arxiv.org/html/2507.10532v3) · [LiveCodeBench](https://livecodebench.github.io/) · [QLoRA medical CoT](https://arxiv.org/html/2510.05003v1)
