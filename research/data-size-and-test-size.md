# Research note — how much training data, how big a test set (2026-09-13)

> **How this was made:** a web search agent read arXiv abstracts and HTML pages. Not
> every table in every PDF was read.
>
> **Why it matters:** the user asked "how do we make sure the dataset is big enough
> that the model definitely learns and improves?"
>
> Decisions drawn from this: [DECISIONS.md](../DECISIONS.md) #14, #16, #17, #18.

**Main finding:** close matches exist for our method, but **no paper reports a
data-size learning curve for shortest-correct SFT.** Munkhbat et al. (the closest
match) trained on the full GSM8K/MATH sets for one epoch with no data ablation.
A learning-curve study is a real gap we can fill.

---

## Papers

| Paper | Method | Model sizes | Domain | Training examples | N per problem | Token change | Accuracy change | Data-scaling result |
|---|---|---|---|---|---|---|---|---|
| **Self-Training Elicits Concise Reasoning** ([2502.20122](https://arxiv.org/abs/2502.20122), Munkhbat et al., ACL Findings 2025) | Shortest correct of N, full SFT (not LoRA), 1 epoch, lr 1e-5 | Llama-3.2-3B, Gemma-2-2B, Qwen2.5-3B, Qwen2.5-Math-1.5B, DeepSeekMath-7B; scaling Llama 1B/3B/8B | Math | 7,473 (GSM8K) / 7,500 (MATH) | 16 | Plain: −12.8% GSM8K, −10.1% MATH. Few-shot: −35.8% / −23.7% | Relative 98.8% / 101.7% (plain), 97.0% / 102.6% (few-shot) | No data-size ablation. **Length reduction grows log-linearly with N** |
| **TokenSkip** ([2502.12067](https://arxiv.org/abs/2502.12067), EMNLP 2025, Xia et al.) | Own correct CoTs pruned by token importance, LoRA r=8, α=16 | Qwen2.5-Instruct 3B/7B/14B, Llama-3.1-8B | Math | 7,473 / 7,500 | Not stated | −30 to −40% | Qwen-14B <0.4 pt drop at −40%; Llama-8B −3.7 pts at −30%, −8 at −40% | Only compression-ratio sweeps |
| **O1-Pruner** ([2501.12570](https://arxiv.org/abs/2501.12570)) | Pre-sample, off-policy length-harmonizing fine-tuning | Marco-o1-7B, QwQ-32B | Math | 5,000 MATH | 16 / 12 | 7B: −35 to −43% | 7B: +2.2 to +4.5 | λ sweeps only |
| **L1 / LCPO** ([2503.04697](https://arxiv.org/abs/2503.04697), COLM 2025) | GRPO with a target-length reward | 1.5B (DeepScaleR), 7B | Math | DeepScaleR 40K, 700 steps | Unverified | Controllable within ~3% | 20–25 pts above s1 budget forcing at 512–1,024 tokens | None |
| **ThinkPrune** ([2504.01296](https://arxiv.org/abs/2504.01296)) | GRPO, hard limit tightened 4k→3k→2k | R1-Distill-1.5B, DeepScaleR-1.5B, QwQ-32B | Math | **2,470** AIME/AMC | 16 | −65% / −43% / −49% | +0.6 / −2.5 / −3.2 | Staged beats single stage |
| **ShorterBetter** ([2504.21370](https://arxiv.org/abs/2504.21370)) | GRPO: correct − distance to shortest correct | R1-Distill 1.5B/7B, Llama-8B | Math | DeepScaleR 40K pool, 100–300 steps | 8 | −50 to −80% | In-domain +2.5 to +7; out-of-domain −0.5 to −1.6 | Most reduction in first ~100 steps |
| **AdaptThink** ([2505.13417](https://arxiv.org/abs/2505.13417), EMNLP 2025) | RL choosing thinking vs no thinking | R1-Distill 1.5B/7B | Math | 40K, ~1 epoch | 16 | −53% / −40% | +2.4 / +2.3 | Skips thinking more on easy problems |
| **Concise Reasoning via RL** ([2504.05185](https://arxiv.org/abs/2504.05185)) | Second-stage PPO on solvable problems | R1-Distill 1.5B/7B, Qwen2.5-Math, Phi-4 | Math | **4–8 problems** | 8 | MATH500 −54% / −40% | −3.2 / −2.6 | Strongest small-data evidence (but RL) |
| **Training LMs to Reason Efficiently** ([2502.04463](https://arxiv.org/abs/2502.04463)) | RL: correct × (1 − α · normalized length) | R1-Distill 1.5B/7B | Math | **3,200**, ~100 steps | 8 | 7B: −36% MATH500, −65% GSM8K | −2.2 / −1.7 | α sweeps |
| **Kimi k1.5** ([2501.12599](https://arxiv.org/abs/2501.12599)) | Length reward + "shortest rejection sampling" (8 → SFT on shortest correct), DPO, merging | Undisclosed | Math/code | Not stated | 8 | AIME 60.8 at ~3.3k tokens | — | Long-to-short RL most efficient |
| **DAST** ([2503.04472](https://arxiv.org/abs/2503.04472)) | SimPO, length-budget pairs | R1-Distill 7B/32B | Math | ~10K pairs | 20 | −18% / −46% | +0.4 / +1.4 | None |
| **Do NOT Think That Much for 2+3=?** ([2412.21187](https://arxiv.org/abs/2412.21187)) | Self-training, shortest / first-correct; SFT, DPO, RPO, SimPO | QwQ-32B-Preview | Math | PRM12K | 10 | −22 to −45% | 93.0 → 92.8 | SimPO > SFT; defines "outcome efficiency" |
| **Don't Overthink It** ([2505.17813](https://arxiv.org/abs/2505.17813)) | SFT on shortest vs longest vs random s1 traces | Qwen2.5 7B/32B | Math | 1,000 | — | Only −5.8% | +2.8% relative (32B) | Shortest chains up to 34.5% more accurate |
| **SEER** ([2509.14093](https://arxiv.org/abs/2509.14093)) | Best-of-N + median+MAD filter, SFT; LoRA tested | R1-Distill-7B (+ Qwen3-8B) | Code (SE tasks) + math | 1,883 / 2,732 / 9,604 | **3** | −28 to −57% (LoRA 34.8% vs full 39.8%) | +5 to +11 (fewer truncations/loops) | None |
| **S3-CoT** ([2602.01982](https://arxiv.org/abs/2602.01982)) | Self-sampled variable-length CoT, curriculum | Qwen2.5-7B, Llama3-8B, R1-7B, **Qwen3-4B-Thinking** | Math | ~6.4K GSM8K | — | ~−17 to −20% | ~flat | **Warning: SFT on only the shortest CoT "substantially degrades accuracy"** |
| **Correct, Concise and Complete** ([2601.02972](https://arxiv.org/abs/2601.02972)) | SFT then RL penalising tokens after first correct answer | 8B, 32B | Math | Unverified | — | −28% / −40% | −1.6 / −2.5 | — |
| **Acoer** ([2606.22716](https://arxiv.org/abs/2606.22716)) | GRPO + LoRA r=16, reward on correct only | Qwen3-1.7B | Math | ~15K, 1,200 steps | 16 | MATH500 −62% | Comparable | **Tiny length penalty on wrong answers (β=0.01) → collapse by step 800** |
| **s1** ([2501.19393](https://arxiv.org/abs/2501.19393)) | SFT on curated traces | Qwen2.5-32B | Math | **1,000** | — | — | AIME 50.0 | Full 59K only +3.3 AIME for 56× compute; random 1K: 36.7 |
| **LIMO** ([2502.03387](https://arxiv.org/abs/2502.03387)) | SFT on curated traces | Qwen2.5-32B (+ 3B–72B) | Math | 817 / 800 | — | — | AIME 63.3 | **400 → 57.5; 800 → 63.3; 1,200+ diminishing** |

**Also:** survey "Stop Overthinking" [2503.16419](https://arxiv.org/abs/2503.16419) (Sui et al., TMLR 2025), plus [2508.02120](https://arxiv.org/abs/2508.02120) and [2507.09662](https://arxiv.org/abs/2507.09662). DLER [2510.15110](https://arxiv.org/abs/2510.15110): >70% shorter. Step-GRPO [2604.16890](https://arxiv.org/abs/2604.16890): −32% on Qwen3-8B. VeriThinker [2505.17941](https://arxiv.org/abs/2505.17941): −44% on MATH500 (7B, ~340K pairs).

**Not verified:** TokenSkip's full author list and N; L1's group size; ShorterBetter's batch size; Kimi model sizes; data details for 2601.02972; DAST's first author.

---

## 1. Minimum data for SFT to change length reliably

- **No direct learning curve** found for shortest-correct SFT.
- **Indirect evidence:**
  - LIMO/s1 changed reasoning behaviour with 400–1,000 curated examples; LIMO got most of its gain at 400.
  - Munkhbat and TokenSkip used ~7.5K (full set, 1 epoch).
  - SEER used 1.9K–9.6K with N=3.
  - RL needed 4–8 problems (Fatemi) or 2.5–3.2K (ThinkPrune, Arora).
- **Caution:** Hassid's 1K shortest-trace SFT cut only ~6%. How much length drops depends on *how much shorter the selected traces are*, not just the count.
- **Suggestion:** run your own curve (~250 / 500 / 1K / 2K / 4K). That's a thesis contribution.

## 2. Pre-training check: is there something to learn?

Sample N answers per training problem from the base model, then compute:

- **Headroom ratio** = mean over problems of (shortest correct ÷ mean correct length). Near 1 means little to learn.
- **Selection bias:** do kept problems differ in solve rate or difficulty from dropped ones?
- **Coverage:** share of problems with ≥1 correct sample.
- **Diminishing returns:** plot the ratio for N = 1, 2, 4, 8, 16. It should fall roughly log-linearly.
- **Outcome efficiency** (Chen et al.): tokens until the first correct answer ÷ total tokens.
- **Guardrail (S3-CoT):** if shortest traces are far below the median (e.g. below half), pick a moderate-length trace instead.

## 3. Test-set size for a 2–3 point accuracy change

- **Unpaired:** SE = √(p(1−p)/n). At p=0.8, n=500: 1.8 pts, 95% CI ±3.5. The difference of two runs has SE ≈ 2.5 pts, so MATH-500 alone can't resolve 2–3 pts unpaired.
- **Paired** (same questions, base vs fine-tuned; McNemar or paired bootstrap): SE of the difference ≈ √(d/n), where d = share of questions where exactly one model is right (often 8–15%).
  - Δ = 2.5 pts, α = 0.05, 80% power: n ≈ d × 7.84 / Δ².
  - d = 0.10 → **~1,250** questions; d = 0.15 → **~1,900**.
  - Δ = 2 pts → ~2,000–2,900.
  - Just reaching significance (no power requirement): ~600–900.
- **Recommendation:** pool ~1,500–3,000 questions, average 4–8 samples per question, report paired bootstrap CIs clustered by question (Miller, [2411.00640](https://arxiv.org/abs/2411.00640)).
- **AIME** (30 questions) = 3.3 pts per question, so anecdotal only. Hochlehnert et al. ([2504.07086](https://arxiv.org/abs/2504.07086)) show seed/setup variance there exceeds many claimed gains.
