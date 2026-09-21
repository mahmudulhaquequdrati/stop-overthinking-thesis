# Mini-thesis (notebook 13): first test results — 2026-09-22

**GPU:** Colab A100 (paid units, DECISIONS #48) · **Model:** unsloth/Qwen3.5-2B in **bfloat16** ·
**Batch:** 64 · **Test:** **100** MBPP+ test problems (the notebook cell still had 100, not 50), 1 try,
4,096-token limit, the same seed and settings for every way.

## 1. The numbers so far (from Colab's printed output)

| Way | Passed | Median thinking tokens | Hit the 4,096 limit | Speed printed |
|---|---|---|---|---|
| Thinking OFF | **56 / 100** | 0 | 0 | 314 → 123 tok/s |
| Thinking ON | **50 / 100** | 1,152 | **27** | 523 → 348 tok/s |
| "Think briefly" | **3 / 100** ⚠️ | 4,096 | **92** | 1,070 → 706 tok/s |
| LoRA 25 / 50 / 100 | not run | — | — | stopped by the safety check |

## 2. What it means (first reading, 1 try each, no error bars yet)

- **Thinking ON is worse than OFF on these easy problems** (50% vs 56%), and **27 of 100 ON
  answers never finished thinking** within 4,096 tokens. That is overthinking, measured.
- **"Think briefly" at 3% is almost certainly not a real result.** 92 of 100 answers ran to the
  limit. A prompt asking for SHORT thinking should not make thinking LONGER. It must be checked by
  reading the raw answers before it is used anywhere (possible loops, or a prompt problem).

## 3. The LoRA safety check worked

```text
UserWarning: Found missing adapter keys ... 'base_model.model.model.layers.0.mlp.gate_proj.lora_A...'
STOP: the LoRA in .../lora/lora25 did not load (96 layers, weight sum 0.0).
      The answers would silently be the base model's.
```

- **What happened:** Unsloth saved the LoRA under different names than the plain model uses, so
  PEFT created 96 EMPTY LoRA layers (all zeros). Without the check, the "trained" model would have
  answered exactly like the base model, and we would have wrongly concluded "training does nothing".
  This is the silent failure DECISIONS #57 warned about.
- **Fix (2026-09-22, `scripts/gen_colab.py` `add_adapter`):** match each saved LoRA weight to the
  model's LoRA weight by the part of the name from `layers.N.` on, and stop if any is unmatched.
- **Not checked yet:** that the saved LoRA files really contain trained (non-zero) weights, and the
  exact saved names. The LoRAs on Drive do not need retraining if they do.

## 4. Speed

On the A100 with batch 64, a full batch of thinking-ON answers took about 230 s. The T4 needed
~735 s for a batch of 8 (see `2026-09-22-t4-speed-first-run.md`).
