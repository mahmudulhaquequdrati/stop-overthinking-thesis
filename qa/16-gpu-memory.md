# Q&A 16: GPU memory

⬅️ [All Q&A](README.md) · Hard word? See [GLOSSARY.md](../GLOSSARY.md) · Lesson: [07 GPU memory](../lessons/07-gpu-memory.md)

---

## 1. The step in 2 sentences

We learned how to work out if a model fits on a free GPU: memory = number of parameters × bytes per number.
This is why we use the 4-bit Gemma, why hard problems are out, and why training examples stop at 3,500 tokens.

---

## 2. Questions a teacher may ask

**Q: How much memory does your GPU have?**
A free T4. It is a 16 GB card and the software shows 14.563 GB usable. We round it to "15 GB".

**Q: How do you calculate a model's memory?**
Parameters × bytes per number. 16-bit = 2 bytes, 4-bit = 0.5 byte.

**Q: Show the calculation for your model.**
Gemma-4-E4B has 8.0 billion parameters.
- All 16-bit: 8.0 × 2 = **16.0 GB** → too big.
- Unsloth's 4-bit version: 3.50 billion squeezed (× 0.5 = 1.75 GB) + 4.60 billion kept at 16-bit (× 2 = 9.20 GB) = **10.95 GB** → fits.
The real file on Hugging Face is 10.95 GB, so the calculation matches.

**Q: Why isn't the whole model squeezed to 4-bit?**
The word lookup table and the image/audio parts stay 16-bit, because squeezing them costs more accuracy than it saves memory.

**Q: What else uses memory besides the model?**
While writing: notes about every earlier token (the KV cache), so memory grows with the answer length.
While training: also in-between results for the nudges, plus the LoRA add-on and its training notes.

**Q: What numbers have been measured?**
Unsloth measured on a free T4: 9.891 GB after loading Gemma 4-bit, and 10.715 GB peak in a short LoRA training with examples up to 1,024 tokens.

---

## 3. Hard questions

**Q: Your training examples are 3,500 tokens, but the measurement used 1,024. Isn't your plan built on the wrong number?**
Yes, that is why the memory check exists (week 3): train 50 examples at 3,500 tokens and read the peak.
Rule set in advance: ≤ 14 GB → keep Gemma; above → switch to Qwen3.5-4B (measured 9.6 GB).

**Q: Does 4-bit make the model worse?**
It loses a little accuracy, because the numbers are less exact. We accept it, because without it the model doesn't fit at all.
Both the base model and our trained model use the same 4-bit version, so the comparison stays fair.

**Q: GB or GiB?**
Hugging Face file sizes count 1,000-based GB; GPU tools usually count 1,024-based (about 7% difference).
When we check the 14 GB rule, we use the number the GPU tool prints.

---

## 4. Checked vs. assumed

| We checked | We assume |
|---|---|
| Gemma 16-bit file 15.99 GB; 4-bit 10.95 GB (Hugging Face) | That 3,500-token training examples stay under 14 GB |
| Unsloth's T4 run: 14.563 GB usable, 9.891 GB after loading, 10.715 GB peak | How much memory Gemma needs per written token (not measured) |

---

## 5. Where it is written

- [lessons/07-gpu-memory.md](../lessons/07-gpu-memory.md)
- [PLAN.md](../PLAN.md) §7 · [DECISIONS.md](../DECISIONS.md) rows #7, #8, #10, #13, #16
- [research/models-and-gpu.md](../research/models-and-gpu.md) · [research/2026-09-17-part2-tool-checks.md](../research/2026-09-17-part2-tool-checks.md)
