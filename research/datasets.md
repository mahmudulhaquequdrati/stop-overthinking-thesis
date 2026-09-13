# Research note — fresh test sets and training data (2026-09-13)

> **How this was made:** a web search agent checked Hugging Face dataset pages
> (`https://huggingface.co/api/datasets/<id>`), official GitHub repos and MathArena.
>
> **Why it matters:** the test problems must be ones the model has *not* seen,
> i.e. published after its training cutoff.
>
> Decisions drawn from this: [DECISIONS.md](../DECISIONS.md) #4, #8, #18 and
> [PLAN.md](../PLAN.md) §6.
>
> ⚠️ This search was done when math was still the main domain. After the gap search,
> **code became main and math the transfer test**. With Gemma-4-E4B (cutoff Jan 2025),
> LiveCodeBench problems from Feb–Apr 2025 count as fresh.

---

## Summary

The July 2026 finding mostly still holds: **no public benchmark of standalone 2026 code
problems with hidden tests.** There are two partial exceptions (SWE-rebench, a LeetCode
dump). Math is better, but only up to Feb 2026. After March 2026 only research-level
math sets exist.

---

## A1. Fresh code evaluation sets

| Set / HF id | Problem dates | # problems | Tests? | License / gating | Status |
|---|---|---|---|---|---|
| `livecodebench/code_generation_lite` | May 2023 – Apr 2025 (release_v6) | 1,055 | Yes (hidden) | Public | Checked: HF last modified 2025-06-05; nothing after v6 on GitHub |
| `QAQAQAQAQ/LiveCodeBench-Pro` + `QAQAQAQAQ/LiveCodeBench-Pro-Testcase` | 2025 quarters (HF modified 2025-10-18; tests 2025-09-21) | 1K–10K tag | Yes (separate repo) | Problems gated ("auto"), Apache-2.0; tests ungated | Checked; splits not listable (401). No 2026 update |
| `nebius/SWE-rebench-leaderboard` | Monthly 2025_01 … **2026_01 (48), 2026_02 (57), 2026_03 (110)** | 860 | Yes, repo tests in Docker | CC-BY-4.0 | Checked (modified 2026-07-28). Jul/Aug 2026 tasks mentioned elsewhere, not checked |
| `whiskwhite/leetcode-complete` | Oct 2013 – **Sep 2026** (dates guessed) | 3,951 | **Only the statement's example tests** | "unknown" | Checked (modified 2026-09-09); 2026 count not checked |
| `LiveOIBench/LiveOIBench` (+ `_tests`) | Olympiads 2023–2025 | 403 | Yes (~60/problem) | Public | Checked (modified 2025-12-15) |
| `open-r1/codeforces` | Up to early 2025 | 10,024 | Yes, official tests truncated; generated tests ~110 GB | CC-BY-4.0 | Checked |
| `Nan-Do/atcoder_abc_contests`, `Nan-Do/leetcode_contests` | Up to ABC 468 (2026-07-25) / LeetCode weekly 511 (2026-07-19) | 2,738 / 2,810 | **No tests** | Gated, not public | Checked. Not usable |
| CodeElo, AetherCode, UOJ-Bench (2606.12864) | — | — | — | — | **Not checked.** No HF repo with 2026 problems found |

Aggregator sites say LiveCodeBench was "updated Aug 2026". Official GitHub/HF stop at
v6, so treat it as unverified.

## A2. Fresh math evaluation sets (MathArena, ungated)

| HF id | Date | # | Answer type | License |
|---|---|---|---|---|
| `MathArena/aime_2026` (`aime_2026_I` = Part I) | Feb 2026 | 30 | Integer | CC BY-NC-SA 4.0 |
| `math-ai/aime26` | Feb 2026 | 30 | Integer | Apache-2.0 |
| `MathArena/hmmt_feb_2026` | Feb 2026 | 33 | String (fractions, radicals, expressions) | CC BY-NC-SA 4.0 |
| `MathArena/usamo_2026` | Mar 2026 | 6 | Proofs + rubric (no automatic grading) | CC BY-NC-SA 4.0 |
| `MathArena/arxivmath-0326` / `-0426` / `-0526` / `-0626` | Mar–Jun 2026 | 30 / 41 / 40 / 48 | String expressions, research-level | CC BY-SA 4.0 |
| `MathArena/brokenarxiv-0626`, `arxivlean-0626` | Jun 2026 | 54 / 46 | Disprove / Lean proofs | — |
| `MathArena/project_euler` | Problems 943–992 | 50 | **No answers** (PE policy) | CC BY-NC-SA 4.0 |

**Not found:** BRUMO 2026, SMT 2026, CMIMC 2026, IMO 2026.
**Not checked:** 2025 versions (`MathArena/aime_2025`, `hmmt_feb_2025`). Verify before using.

## B. Large training sets with verifiable answers (all checked on the HF API)

| HF id | Size | Tests / answers | License |
|---|---|---|---|
| `agentica-org/DeepCoder-Preview-Dataset` | ~24.7K train (primeintellect 16,252; taco 7,436; lcbv5 599) + test | Tests | MIT |
| `KodCode/KodCode-V1` | 484,097 + 3,335 "use_with_caution" | Pytest or stdio tests | CC-BY-NC-4.0 |
| `open-r1/codeforces` | 9,556 / 468 (verifiable: 8,338 / 422) | Truncated tests + generated tests + checkers | CC-BY-4.0 |
| `nvidia/OpenCodeReasoning` | 567,850 + 167,405 | **No tests** (R1 traces) | CC-BY-4.0 |
| `PrimeIntellect/verifiable-coding-problems` | 144,169 | stdin/stdout tests | Not stated |
| `PrimeIntellect/SYNTHETIC-1` | 1,994,262 | Verified traces (mixed) | Apache-2.0 |
| `BAAI/TACO` | 25,443 / 1,000 | I/O tests | Apache-2.0 |
| `codeparrot/apps` | ~10,000 | I/O tests | MIT |
| `agentica-org/DeepScaleR-Preview-Dataset` | ~40K | Answers | MIT |
| `open-r1/OpenR1-Math-220k` | 93,733 default / 225,129 all | Answers | Apache-2.0 |
| `SynthLabsAI/Big-Math-RL-Verified` | 251,122 | Answers | Apache-2.0, gated "auto" |
| `AI-MO/NuminaMath-1.5` | ~900K | Answers for most rows | Apache-2.0 |

All are 2025 or earlier. Fine for **training**, not for "unseen" **testing**.
⚠️ DeepCoder's `lcbv5` part overlaps LiveCodeBench, so drop it (DECISIONS / PLAN §6).

## C. Grading difficulty on Colab

| Set | Grading | Difficulty |
|---|---|---|
| AIME 2026 | Integer exact match | Trivial |
| HMMT Feb 2026, ArXivMath | Symbolic equivalence (`math-verify` / sympy) | Easy–moderate |
| LeetCode-complete (2026 rows) | Example tests only (weak) | Easy but noisy |
| LiveCodeBench v6 / LCB-Pro | Sandboxed stdin/stdout runs | Moderate; CPU is fine |
| SWE-rebench 2026 | Docker + full repo test suites | Not practical on free Colab |
| USAMO, BrokenArXiv, ArXivLean | Proof judging / Lean | Not a simple script |

## Assessment from the search

1. Math is easier for fresh tests: AIME 2026 (30) + HMMT Feb 2026 (33), exact answers, trivial grading. They only count as unseen if the model's cutoff is before mid-Feb 2026.
2. After March 2026: only ArXivMath (159, research-level, too hard for small models). Code: no standalone 2026 set with hidden tests.
3. **For a model with a Jan 2025 cutoff (Gemma-4)**, 2025 code problems with tests (LiveCodeBench Feb–Apr 2025, LiveCodeBench-Pro 2025, LiveOIBench 2025) become usable fresh tests.

---

## Sources

- **LiveCodeBench:** [GitHub](https://github.com/LiveCodeBench/LiveCodeBench) · [LiveCodeBench-Pro GitHub](https://github.com/GavinZhengOI/LiveCodeBench-Pro) · [livecodebenchpro.com](https://livecodebenchpro.com/) · [BenchLM](https://benchlm.ai/benchmarks/livecodebench) · [llm-stats](https://llm-stats.com/benchmarks/livecodebench)
- **Math:** [MathArena competitions](https://matharena.ai/competitions) · [aime_2026](https://huggingface.co/datasets/MathArena/aime_2026) · [hmmt_feb_2026](https://huggingface.co/datasets/MathArena/hmmt_feb_2026) · [math-ai/aime26](https://huggingface.co/datasets/math-ai/aime26) · [arxivmath-0626](https://huggingface.co/datasets/MathArena/arxivmath-0626) · [project_euler](https://huggingface.co/datasets/MathArena/project_euler)
- **Other code sets:** [SWE-rebench-leaderboard](https://huggingface.co/datasets/nebius/SWE-rebench-leaderboard) · [leetcode-complete](https://huggingface.co/datasets/whiskwhite/leetcode-complete) · [atcoder_abc_contests](https://huggingface.co/datasets/Nan-Do/atcoder_abc_contests) · [leetcode_contests](https://huggingface.co/datasets/Nan-Do/leetcode_contests) · [LiveOIBench](https://liveoibench.github.io/) · [UOJ-Bench](https://arxiv.org/abs/2606.12864)
- **Training sets:** [open-r1/codeforces](https://huggingface.co/datasets/open-r1/codeforces) · [OpenCodeReasoning](https://huggingface.co/datasets/nvidia/OpenCodeReasoning) · [verifiable-coding-problems](https://huggingface.co/datasets/PrimeIntellect/verifiable-coding-problems) · [KodCode-V1](https://huggingface.co/datasets/KodCode/KodCode-V1)
