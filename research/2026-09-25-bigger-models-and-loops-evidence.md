# Evidence: do bigger models loop less? (web check, 2026-09-25)

Searched for the thesis's "Future work" section. **✔ = I opened the page and the quote matches word for word
(2026-09-25).** ☐ = found by a helper search, not re-opened by me.

## 1. Our model is known to loop — from its own makers ✔

**Qwen3.5-2B model card**, https://huggingface.co/Qwen/Qwen3.5-2B:
> "Qwen3.5-2B is more prone to entering thinking loops compared to other Qwen3.5 models, which may prevent it
> from terminating generation properly."

Same card, recommended thinking-mode settings for **coding**:
> "temperature=0.6, top_p=0.95, top_k=20, min_p=0.0, presence_penalty=0.0, repetition_penalty=1.0"

These are exactly our settings. Also: "Qwen3.5-2B operates in non-thinking mode by default." (We switched
thinking on with `enable_thinking=True`.)

The full paragraph continues: "We recommend further tuning the sampling parameters specific to your use case and
utilizing the API's streaming generation mode (if supported) to enable timely detection and interruption of such
anomalous generation behaviors." The card also says to "adjust the `presence_penalty` parameter between 0 and 2 to
reduce endless repetitions" (with trade-offs). ✔ re-opened 2026-09-25.

## 2. Larger models loop less ✔

Pipis, Garg, Kontonis, Shrivastava, Krishnamurthy, Papailiopoulos. **"Wait, Wait, Wait... Why Do Reasoning
Models Loop?"** arXiv:2512.12895:
> "Larger models tend to loop less, and distilled students loop significantly even when their teachers rarely do."
> "Higher temperature reduces looping by promoting exploration, but it does not fix the errors in learning, so
> generations remain much longer than necessary at high temperature."

## 3. Small models learn less from long reasoning ✔

Li et al. **"Small Models Struggle to Learn from Strong Reasoners"**, arXiv:2502.12143:
> "small models (≤3B parameters) do not consistently benefit from long chain-of-thought (CoT) reasoning or
> distillation from larger models."

## 4. Other findings (helper search, not re-opened) ☐

- Qwen3-8B card: thinking mode, "DO NOT use greedy decoding, as it can lead to performance degradation and
  endless repetitions"; `presence_penalty` 0–2 can "reduce endless repetitions" but may cause "language mixing
  and a slight decrease in model performance".
- Qwen3.5 sizes on Hugging Face: 0.8B, 2B, 4B, **9B**, 27B, 35B-A3B, 122B-A10B, 397B-A17B (Qwen org);
  `unsloth/Qwen3.5-4B`, `-9B`, `-27B`. The 9B card: thinking mode is the default; off with `enable_thinking: False`.
- Qwen3 Technical Report, arXiv:2505.09388: a unified thinking / non-thinking mode, and a "thinking budget mechanism".
- s1, arXiv:2501.19393: "budget forcing" = "forcefully terminating the model's thinking process or lengthening
  it by appending 'Wait'". s1 uses it mainly to make thinking *longer*; that cutting keeps accuracy is **our**
  finding, not s1's.
- EvalPlus, arXiv:2305.01210: "we extend the test-cases of the popular HumanEval benchmark by 80x to build HumanEval+".

## What this means for us

Our main explanation (a small model loops, and training on short correct answers doesn't fix loops) matches
the model card and the Pipis et al. finding. A bigger Qwen3.5 (4B or 9B) is a sensible next test: same family,
same switch, and expected to loop less.
