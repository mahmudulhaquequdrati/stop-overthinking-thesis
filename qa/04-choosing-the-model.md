# Q&A 04: Choosing the model

⬅️ [All Q&A](README.md) · Hard word? See [GLOSSARY.md](../GLOSSARY.md)

---

## 1. The step in 2 sentences

Our main model is **Gemma-4-E4B** (`google/gemma-4-E4B-it`), from Google, March 2026.
Our backup is **Qwen3.5-4B**, used only if Gemma does not fit in GPU memory.

---

## 2. Questions a teacher may ask

**Q: Why Gemma-4-E4B?**

| Reason | Why it matters |
|---|---|
| New (March 2026) | The thesis is about current small models |
| Has a thinking ON/OFF switch | Our whole comparison needs it |
| Apache-2.0 licence | Free to use and share |
| **Published training cutoff: January 2025** | We can prove newer test problems were not in its training text |
| Unsloth has a free T4 notebook, with memory measured (10.7 GB peak) | We know it can train on a free GPU |

**Q: Why not a smaller model, like Qwen3-1.7B?**
It is too small, and it is from 2025.
Our free GPU has about 15 GB, so we can use a newer, bigger model.
(I noticed this problem myself during planning.)

**Q: Why not a bigger model, like Qwen3.5-9B?**
It can **run** in 15 GB. But **training** it with 16-bit LoRA needs about 22 GB.
Unsloth also advises against 4-bit training for Qwen3.5. So it does not fit.

**Q: The Gemma model file is 16 GB, but your GPU has 15 GB. How does it fit?**
We load a **squeezed** version (4-bit).

```text
The model = a huge list of numbers. Gemma-4-E4B has 8.0 billion of them.

16-bit version (2 bytes per number)   → 16.0 GB   ✗ too big for the GPU
4-bit version (partly squeezed)       → 11.0 GB   ✓ this is the file we load
Measured while training (short examples) → 10.7 GB peak
```

Only 3.5 billion of the 8.0 billion numbers are squeezed to 4-bit.
The word lookup tables and the image and audio parts stay 16-bit.
That is why the file is 11 GB, not 4 GB.
*Everyday example:* saving a big photo as a JPEG. A little less detail, much smaller.

**Q: Why is Qwen3.5-4B the backup?**
Its file is 9.3 GB. Unsloth measured 9.6 GB while training it on a T4.
So it fits easily if Gemma does not.

---

## 3. Hard questions

**Q: Why does the cutoff date matter so much?**
If the model saw a test problem during its training, a good score may be memory, not skill.
With a January 2025 cutoff, problems published after that are safe.

**Q: What is bad about the backup model?**
Qwen3.5-4B has **no published cutoff date**. So we can't prove it never saw the test problems.

**Q: What if Gemma crashes on the free GPU?**
There is a known Gemma-4 bug on the T4: a number gets too big in the **audio** part in 16-bit mode.
We use text only, so we expect to avoid it. We check this in weeks 1–3.
If the memory check fails, we switch to Qwen3.5-4B (a rule set in advance).

**Q: How do you decide "fits" or "does not fit"?**
The memory check in week 3: train 50 examples up to 3,500 tokens.
Peak memory ≤ 14 GB → keep Gemma. Otherwise → Qwen3.5-4B. (See [Q&A 08](08-safety-checks-before-training.md).)

---

## 4. Checked vs. assumed

| We checked (Hugging Face website, 2026-09-13) | We assume (not checked yet) |
|---|---|
| Gemma 16-bit file: 15.99 GB; 4-bit file: 10.95 GB | That training with 3,500-token examples stays ≤ 14 GB |
| Qwen3.5-4B file: 9.32 GB | That the audio bug doesn't affect text-only use |
| Unsloth's measured peaks: 10.715 GB (Gemma), 9.645 GB (Qwen) | The cutoff date: re-check on the model card |
| | Whether vLLM runs Gemma-4 on a T4 |

---

## 5. Where it is written

- [DECISIONS.md](../DECISIONS.md) rows #6, #7, #8, #9, #10
- [PLAN.md](../PLAN.md) §7
- [research/models-and-gpu.md](../research/models-and-gpu.md) (full search notes)
