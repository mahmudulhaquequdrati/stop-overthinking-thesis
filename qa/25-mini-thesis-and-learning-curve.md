# Q&A 25: The mini-thesis, and how we'll know if more training data helps

⬅️ [All Q&A](README.md) · Hard word? See [GLOSSARY.md](../GLOSSARY.md) · Decision: [DECISIONS #60](../DECISIONS.md)

---

## 1. The step in 2 sentences

Before spending a week of GPU time, we run the whole method once, small and free, on a T4:
answer 100 easy training problems, keep the shortest correct answers, train a LoRA, and test on
100 other problems. We train 3 LoRAs on 25%, 50% and 100% of the examples, so we can see
whether more training data would help.

```text
100 MBPP+ TRAIN ─► answer 4× ─► keep shortest correct ─► LoRA 25% · 50% · 100%
100 MBPP+ TEST  ─► OFF · ON · "think briefly" · LoRA 25% · LoRA 50% · LoRA 100%
```

> **Update 2026-09-22 (DECISIONS #62):** cut to **50 train / 50 test** problems and 2 LoRAs
> (50% and 100%), because 100 problems were too slow on a free T4. The rules did not change.

---

## 2. Questions a teacher may ask

**Q: Why run a small version first?**
To find problems while they're cheap. If training doesn't cut thinking on 100 easy problems,
it's better to know after 3 free hours than after a week. *Everyday example:* a baker bakes one
small cake before taking a wedding order.

**Q: Why MBPP+ and not HumanEval, which you already use?**
HumanEval is part of our **final test set**. If we trained on it, or chose anything based on its
results, the final test would no longer be fair. MBPP+ is also easy code with real tests, and we
had already removed it from the test set, so it's free to use. Its 100 train and 100 test problems
come from a fixed-seed shuffle made before any answer existed, and they don't overlap.

**Q: How do you know whether more training data would help?**
With a **learning curve**. We train 3 LoRAs: on 25%, 50% and 100% of the examples, with the same
settings. The smaller sets sit inside the bigger ones, so only the amount of data changes.
- If 100% is clearly better than 50%, the curve is still rising → more data should help.
- If they're about the same, it has levelled off → more of the same data won't help.

*Everyday example:* a runner who timed themselves after 2 and 4 weeks of practice. If week 4 was
much faster than week 2, keep practising.

**Q: Is there a second way to tell?**
Yes: the **TARGET** number. It says how short our training answers are, compared with a normal
correct answer (for example 0.70 = 30% shorter). A LoRA can't learn to be shorter than its examples.
- If the LoRA already reached the TARGET, more examples of the same kind won't cut more. We'd
  need **shorter** examples instead (asking 8 times instead of 4 gives more chances for a short one).
- If the LoRA is still far from the TARGET, more data or more training can still help.

So together the two numbers say not only *whether* to invest more, but *in what*.

**Q: What are you comparing the LoRA against?**
The free options: thinking ON, thinking OFF, and asking the model to "think briefly". If the
LoRA isn't better than those, training isn't worth it, whatever else it does.

---

## 3. Hard questions

**Q: 100 test problems, 1 try each. Isn't that too small to prove anything?**
Yes, to *prove* a small difference. That's why this is a **pilot**, not the thesis result. Every
number comes with error bars (resampling the same problems 2,000 times). A difference smaller
than its error bars is treated as noise. A big token cut (like 30%) can still show clearly.

**Q: MBPP+ is easy. What if thinking OFF is already as good as everything else?**
Then rule R3 says so, and it's still a useful result: it tells us easy problems can't show the
value of thinking, so the thesis must lean on medium problems. That's why notebook 12's medium
check comes next.

**Q: Why did you cut from 100 to 50 problems in the middle of the run?**
The free T4 was too slow: after a long wait only 16 of 400 training answers were done. 50/50 needs
about 55% less time. It is not cherry-picking: nothing had been graded yet, the 50 are fixed by the
same seed, and the rules stayed the same. The price is wider error bars, so only big differences show.

**Q: How do you know the trained LoRA really loaded? You said that could fail silently.**
A trained LoRA has non-zero numbers in its "B" parts; an empty one has only zeros. The answering
script adds up those numbers after loading. If they're all zero, it **stops** instead of quietly
answering like the base model.

**Q: Did you set the rules before seeing results?**
Yes. All 5 rules (R1–R5) are written in `scripts/compare_mini.py` and DECISIONS #60 before the
first answer exists. That stops us from reading whatever we want into the numbers afterwards.

---

## 4. What we checked, and what we only assume

| ✅ We checked this | ❌ We only assume this |
|---|---|
| MBPP+ has 378 problems with `prompt`, `code`, `test_list`, `test` (Hugging Face) | That Unsloth trains Qwen3.5-2B on a T4 without trouble |
| Unsloth's guide: 16-bit LoRA for Qwen3.5, not 4-bit; transformers v5 | That the whole notebook takes 2–4 hours |
| Train and test problems don't overlap (the script checks and prints it) | That 100 examples are enough for the LoRA to learn anything |
| The notebook file is valid (26 cells) | That PEFT loads Unsloth's LoRA into the plain model (the check catches it if not) |

---

## 5. Where this is written down

- **Decision:** [DECISIONS.md](../DECISIONS.md) row #60
- **Plan:** [PLAN.md](../PLAN.md) §8; **Roadmap:** [ROADMAP.md](../ROADMAP.md)
- **Code:** `notebooks/13_mini_thesis.ipynb`, `scripts/mbpp_data.py`, `scripts/grade_mbpp.py`,
  `scripts/make_train_set.py`, `scripts/train_lora.py`, `scripts/compare_mini.py`,
  `scripts/gen_colab.py` (`--split`, `--adapter`, `--label`)
- **Words:** [GLOSSARY.md](../GLOSSARY.md): learning curve, MBPP+, mini-thesis, TARGET
