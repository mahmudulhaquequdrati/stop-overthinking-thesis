# Research note: fresh test sets and training data (2026-09-13)

> Hard word? See [GLOSSARY.md](../GLOSSARY.md).

> **How this note was made**
> - A web search helper read Hugging Face dataset pages
>   (`https://huggingface.co/api/datasets/<id>`). *Hugging Face* ("HF") is a free
>   website where people share models and datasets. A *dataset* is a collection of
>   problems or examples.
> - It also read the official GitHub repos and MathArena (a website that collects
>   new math competitions for testing models).
>
> **Why this matters**
> - The test problems must be ones the model has *not* seen.
> - That means: published after its *training cutoff* (the last date of text the model learned from).
>
> Decisions that came from this note: [DECISIONS.md](../DECISIONS.md) #4, #8, #18 and
> [PLAN.md](../PLAN.md) §6.
>
> ⚠️ **This search is a bit old.** It was done when math was still the main topic.
> After the gap search, **code became the main topic and math became the transfer test**.
> With Gemma-4-E4B (cutoff Jan 2025), LiveCodeBench problems from Feb–Apr 2025 count as fresh.

---

## Summary

A *benchmark* is a fixed set of test problems used to score models.
*Hidden tests* are grading tests the model never sees.

1. The July 2026 finding mostly still holds: **there is no public benchmark of
   standalone 2026 code problems with hidden tests.**
2. There are two partial exceptions: SWE-rebench and a LeetCode dump.
3. Math is better, but only up to Feb 2026.
4. After March 2026, only research-level math sets exist.

---

## A1. Fresh code test sets

### What the columns mean

- **Problem dates:** when the problems were first published.
- **Tests?:** does the set come with tests to grade the code?
- **License / gating:** the rules for using it. *Gated* means you must ask or
  click "accept" before you can download. "auto" means access is given automatically.
- **Status:** what we checked, and what we did not.

| Set / HF id | Problem dates | # problems | Tests? | License / gating | Status |
|---|---|---|---|---|---|
| `livecodebench/code_generation_lite` | May 2023 – Apr 2025 (release_v6) | 1,055 | Yes (hidden) | Public | Checked: HF last changed 2025-06-05. Nothing after v6 on GitHub |
| `QAQAQAQAQ/LiveCodeBench-Pro` + `QAQAQAQAQ/LiveCodeBench-Pro-Testcase` | 2025 quarters (HF changed 2025-10-18; tests 2025-09-21) | 1K–10K (size tag) | Yes (in a separate repo) | Problems gated ("auto"), Apache-2.0. Tests not gated | Checked. Could not list the splits (error 401). No 2026 update |
| `nebius/SWE-rebench-leaderboard` | Monthly 2025_01 … **2026_01 (48), 2026_02 (57), 2026_03 (110)** | 860 | Yes, the repo's own tests, run in Docker | CC-BY-4.0 | Checked (changed 2026-07-28). Jul/Aug 2026 tasks are mentioned elsewhere, not checked |
| `whiskwhite/leetcode-complete` | Oct 2013 – **Sep 2026** (dates are guessed) | 3,951 | **Only the example tests from the problem text** | "unknown" | Checked (changed 2026-09-09). Number of 2026 problems not checked |
| `LiveOIBench/LiveOIBench` (+ `_tests`) | Olympiads 2023–2025 | 403 | Yes (~60 per problem) | Public | Checked (changed 2025-12-15) |
| `open-r1/codeforces` | Up to early 2025 | 10,024 | Yes. Official tests are cut short. Generated tests are ~110 GB | CC-BY-4.0 | Checked |
| `Nan-Do/atcoder_abc_contests`, `Nan-Do/leetcode_contests` | Up to ABC 468 (2026-07-25) / LeetCode weekly 511 (2026-07-19) | 2,738 / 2,810 | **No tests** | Gated, not public | Checked. Not usable |
| CodeElo, AetherCode, UOJ-Bench (2606.12864) | — | — | — | — | **Not checked.** No HF repo with 2026 problems found |

Small notes:
- *Docker* is a tool that runs code inside a sealed box with its own setup.
- *Olympiads* are school-level programming competitions.
- *Splits* are the parts of a dataset, for example "train" and "test".

**Unverified claim:** some summary websites say LiveCodeBench was "updated Aug 2026".
The official GitHub and HF pages stop at v6. So treat that claim as unverified.

## A2. Fresh math test sets (MathArena, not gated)

| HF id | Date | # | Answer type | License |
|---|---|---|---|---|
| `MathArena/aime_2026` (`aime_2026_I` = Part I) | Feb 2026 | 30 | Integer | CC BY-NC-SA 4.0 |
| `math-ai/aime26` | Feb 2026 | 30 | Integer | Apache-2.0 |
| `MathArena/hmmt_feb_2026` | Feb 2026 | 33 | Text (fractions, roots, expressions) | CC BY-NC-SA 4.0 |
| `MathArena/usamo_2026` | Mar 2026 | 6 | Proofs + a marking guide (no automatic grading) | CC BY-NC-SA 4.0 |
| `MathArena/arxivmath-0326` / `-0426` / `-0526` / `-0626` | Mar–Jun 2026 | 30 / 41 / 40 / 48 | Text expressions, research-level | CC BY-SA 4.0 |
| `MathArena/brokenarxiv-0626`, `arxivlean-0626` | Jun 2026 | 54 / 46 | Prove a claim wrong / Lean proofs | — |
| `MathArena/project_euler` | Problems 943–992 | 50 | **No answers** (Project Euler's rule) | CC BY-NC-SA 4.0 |

Small notes:
- AIME, HMMT and USAMO are school math competitions.
- *Lean* is a computer language for writing proofs that a computer can check.
- "Roots" means things like √2 (the source calls them "radicals").

**Not found:** BRUMO 2026, SMT 2026, CMIMC 2026, IMO 2026.

**Not checked:** the 2025 versions (`MathArena/aime_2025`, `hmmt_feb_2025`). Check them before using.

## B. Big training sets with answers we can check (all checked on the HF API)

"Answers we can check" means each problem has tests or a known answer. So a
computer can tell if a model's answer is right.

| HF id | Size | Tests / answers | License |
|---|---|---|---|
| `agentica-org/DeepCoder-Preview-Dataset` | ~24.7K train (primeintellect 16,252; taco 7,436; lcbv5 599) + test | Tests | MIT |
| `KodCode/KodCode-V1` | 484,097 + 3,335 "use_with_caution" | Pytest or stdio tests | CC-BY-NC-4.0 |
| `open-r1/codeforces` | 9,556 / 468 (checkable: 8,338 / 422) | Cut-short tests + generated tests + checkers | CC-BY-4.0 |
| `nvidia/OpenCodeReasoning` | 567,850 + 167,405 | **No tests** (R1 traces) | CC-BY-4.0 |
| `PrimeIntellect/verifiable-coding-problems` | 144,169 | stdin/stdout tests | Not stated |
| `PrimeIntellect/SYNTHETIC-1` | 1,994,262 | Checked traces (mixed) | Apache-2.0 |
| `BAAI/TACO` | 25,443 / 1,000 | Input/output tests | Apache-2.0 |
| `codeparrot/apps` | ~10,000 | Input/output tests | MIT |
| `agentica-org/DeepScaleR-Preview-Dataset` | ~40K | Answers | MIT |
| `open-r1/OpenR1-Math-220k` | 93,733 default / 225,129 all | Answers | Apache-2.0 |
| `SynthLabsAI/Big-Math-RL-Verified` | 251,122 | Answers | Apache-2.0, gated "auto" |
| `AI-MO/NuminaMath-1.5` | ~900K | Answers for most rows | Apache-2.0 |

Small notes:
- *Pytest* is a common Python testing tool.
- *stdin/stdout* (or *stdio*, *I/O*) tests: we feed text in, and compare the text the program prints out.
- *Traces* are full model answers with the thinking. *R1* is the DeepSeek-R1 model that wrote them.
- *Checkers* are small programs that decide if an output is correct.

**What this means for us:**
- All these sets are from 2025 or earlier.
- They are fine for **training**. They are not fine for "unseen" **testing**.
- ⚠️ DeepCoder's `lcbv5` part overlaps LiveCodeBench, so we drop it (DECISIONS / PLAN §6).

## C. How hard is grading on Colab?

*Colab* is Google's free notebook website with a GPU.
A *sandbox* is a safe, closed place to run code the model wrote.

| Set | How we grade | How hard |
|---|---|---|
| AIME 2026 | The integer must match exactly | Very easy |
| HMMT Feb 2026, ArXivMath | Check the two math expressions mean the same (`math-verify` / sympy) | Easy to medium |
| LeetCode-complete (2026 rows) | Example tests only (weak) | Easy, but the results are noisy |
| LiveCodeBench v6 / LCB-Pro | Run the code in a sandbox with stdin/stdout | Medium. A normal CPU is enough |
| SWE-rebench 2026 | Docker + the full test suites of each repo | Not practical on free Colab |
| USAMO, BrokenArXiv, ArXivLean | Judging proofs / Lean | Not a simple script |

(*sympy* is a free Python library for math symbols.)

## Assessment from the search

1. **Math is easier for fresh tests.** AIME 2026 (30) + HMMT Feb 2026 (33) have exact
   answers and very easy grading. But they only count as unseen if the model's cutoff
   is before mid-Feb 2026.
2. **After March 2026:** only ArXivMath (159, research-level, too hard for small models).
   For code, there is no standalone 2026 set with hidden tests.
3. **For a model with a Jan 2025 cutoff (Gemma-4)**, 2025 code problems with tests
   become usable fresh tests: LiveCodeBench Feb–Apr 2025, LiveCodeBench-Pro 2025,
   LiveOIBench 2025.

---

## Sources

- **LiveCodeBench:** [GitHub](https://github.com/LiveCodeBench/LiveCodeBench) · [LiveCodeBench-Pro GitHub](https://github.com/GavinZhengOI/LiveCodeBench-Pro) · [livecodebenchpro.com](https://livecodebenchpro.com/) · [BenchLM](https://benchlm.ai/benchmarks/livecodebench) · [llm-stats](https://llm-stats.com/benchmarks/livecodebench)
- **Math:** [MathArena competitions](https://matharena.ai/competitions) · [aime_2026](https://huggingface.co/datasets/MathArena/aime_2026) · [hmmt_feb_2026](https://huggingface.co/datasets/MathArena/hmmt_feb_2026) · [math-ai/aime26](https://huggingface.co/datasets/math-ai/aime26) · [arxivmath-0626](https://huggingface.co/datasets/MathArena/arxivmath-0626) · [project_euler](https://huggingface.co/datasets/MathArena/project_euler)
- **Other code sets:** [SWE-rebench-leaderboard](https://huggingface.co/datasets/nebius/SWE-rebench-leaderboard) · [leetcode-complete](https://huggingface.co/datasets/whiskwhite/leetcode-complete) · [atcoder_abc_contests](https://huggingface.co/datasets/Nan-Do/atcoder_abc_contests) · [leetcode_contests](https://huggingface.co/datasets/Nan-Do/leetcode_contests) · [LiveOIBench](https://liveoibench.github.io/) · [UOJ-Bench](https://arxiv.org/abs/2606.12864)
- **Training sets:** [open-r1/codeforces](https://huggingface.co/datasets/open-r1/codeforces) · [OpenCodeReasoning](https://huggingface.co/datasets/nvidia/OpenCodeReasoning) · [verifiable-coding-problems](https://huggingface.co/datasets/PrimeIntellect/verifiable-coding-problems) · [KodCode-V1](https://huggingface.co/datasets/KodCode/KodCode-V1)
