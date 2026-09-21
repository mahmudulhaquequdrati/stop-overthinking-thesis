# Q&A 27: The real thesis run (notebook 14): the rules, fixed before the run

⬅️ [All Q&A](README.md) · Hard word? See [GLOSSARY.md](../GLOSSARY.md) · Decisions: [#65, #66](../DECISIONS.md) · Budget: [PLAN §10](../PLAN.md)

---

## 1. The step in 2 sentences

Notebook 14 runs all the ways of answering on the fixed 234 test problems, trains a better LoRA
that also sees medium problems, and stays inside 69 Colab units. Every rule (token limits, the main
LoRA, the budget) was written down **before** the run, and the notebook runs start to finish
without edits.

```text
smoke (0.7) → A: 5 ways × 234 (10.3, must) → B: LoRA-2 (10.7) → C: 2nd try (12.8) → D: 16k check (2.7)
                  each stage runs only if  units left − its cost ≥ 20
```

---

## 2. Questions a teacher may ask

**Q: Why 4,096 tokens for HumanEval+ but 8,192 for LiveCodeBench?**
HumanEval+ is easy; in the mini-thesis almost every answer that reached 4,096 was a loop, not
useful thinking. LiveCodeBench has medium problems, where honest reasoning can be longer. Each
test set has one limit, and **every way of answering gets the same one**, so the comparison stays fair.

**Q: Why not 16k or 32k for everything?**
A batch of answers waits for its slowest answer, so the cost grows with the limit: 16k is about 4×
the cost, 32k about 8×. That would not fit the budget. Instead, stage D re-runs only the thinking-ON
answers that were cut off, at 16k, and measures how many would have finished.

**Q: What is the "limit" way, and why 1,024?**
The model thinks, but we cut its thinking at 1,024 tokens and make it answer. 1,024 is about how long
our trained model thinks. So it tests a fair question: is a simple hard cut as good as training?

**Q: Why train a second LoRA?**
The first LoRA learned only from easy MBPP+ problems. Our test also has medium LiveCodeBench
problems. LoRA-2 also learns from 80 older LiveCodeBench problems (from before 2025, so they can't be
test problems).

**Q: Which LoRA is "the" result?**
Fixed in advance: LoRA-2 if the budget allows training it, otherwise LoRA-1. We never choose the
one that happens to look better afterwards.

---

## 3. Hard questions

**Q: How do you know no test problem leaked into training?**
Three protections: LiveCodeBench training problems are all from before the test problems' dates;
`overlap_check.py` removes any training problem with the same function name as a test problem or
with a lot of shared wording; and the rule is strict on purpose.

**Q: Why did you skip the T4 test this time?**
Switching runtimes costs setup time and units. Instead, a smoke test on the A100 runs **every** way,
including both LoRA loads and the limit way, on 2 problems per test set, for about 0.7 units.

**Q: What if the budget runs out?**
It can't run out by surprise: before each stage the notebook checks *units left − cost ≥ 20*. If not,
that stage is skipped, from the least important one up. Stage A, the core result, comes first.

**Q: Why no hard problems?**
A 2B model solves almost none, so there is nothing to shorten and nothing to measure (PLAN §3).

---

## 4. What we checked, and what we only assume

| ✅ We checked this | ❌ We only assume this |
|---|---|
| The A100 price: 5.3 units/hour (Colab) | The stage costs (built on one measured batch time) |
| One A100 batch of 64 at 4,096 ≈ 230 s (mini-thesis) | That batch 128 fits and is faster |
| HumanEval+ on Hugging Face ships its plus tests (5 columns, 164 rows) | That the new scripts run without a bug (the smoke test checks) |
| The mini-thesis method works on easy problems | That it transfers to medium problems |

---

## 5. Where this is written down

- **Notebook:** [notebooks/14_thesis_run.ipynb](../notebooks/14_thesis_run.ipynb)
- **Decisions:** [DECISIONS.md](../DECISIONS.md) #65 (budget), #66 (rules)
- **Plan:** [PLAN.md](../PLAN.md) §6 (data), §10 (budget)
- **Code:** `scripts/gen_colab.py`, `grade_plus.py`, `grade_lcb.py`, `lcb_train_data.py`,
  `overlap_check.py`, `make_train_set.py`, `compare_thesis.py`, `budget.py`, `build_problem_set.py`
