# Q&A 17: Free GPUs and notebooks (Colab, Kaggle, Python)

⬅️ [All Q&A](README.md) · Hard word? See [GLOSSARY.md](../GLOSSARY.md) · Lessons: [08 Python](../lessons/08-python-basics.md) · [09 Colab and Kaggle](../lessons/09-colab-and-kaggle.md)

---

## 1. The step in 2 sentences

We learned enough Python to read our notebooks, and how to get a free GPU on Colab and Kaggle.
We also learned the rule that makes free GPUs usable: every job saves as it goes and can continue later.

---

## 2. Questions a teacher may ask

**Q: What hardware does your thesis run on?**
Free T4 GPUs on Google Colab and Kaggle. Total cost: $0. No paid service is used anywhere.

**Q: How long is a free session?**
Colab: "at most 12 hours", often less, and the tab must stay open. Kaggle: about 12 hours, about 30 GPU-hours per week, and it can run with the browser closed.

**Q: Which is your main machine?**
Kaggle, because "Save & Run All" runs a notebook unattended and it gives 2 × T4. Colab is the second worker and the place to fix bugs.

**Q: On Kaggle you can pick a P100. Why don't you?**
Current PyTorch needs a newer GPU type (compute capability ≥ 7.0). The P100 is 6.0, so it doesn't work for us. We always pick 2 × T4.

**Q: Your work needs tens of GPU-hours but sessions are 12 hours. How?**
Every job is split into independent problems and saves results as it goes:
read the "done" list → skip finished problems → work → append results every ~20 problems → if the session dies, start again and continue.

**Q: Why do you write results with "append" and not "write"?**
Append adds to the end and keeps everything already saved. Write would erase the file first. After writing we also force the file to disk, so a sudden session end loses nothing.

**Q: Do you need to be a programmer for this thesis?**
No, but you must be able to read the notebooks: variables, lists, dictionaries, loops, if, functions, and imports. That is what lesson 08 covers.

---

## 3. Hard questions

**Q: Free GPUs are unreliable. Doesn't that threaten the thesis?**
It threatens the calendar, not the results. Every job continues after a crash, every item has a fixed seed, and raw outputs are saved. We also plan calendar time at about 3–5× the GPU time.

**Q: Do results change if a job restarts in a new session?**
No. Each item's seed is fixed (for example seed + problem + try number), so the same item gives the same output in any session.

**Q: What do you do first if you need more speed?**
Write many answers at the same time (vLLM, 32–64 prompts at once): 2–5× faster, no effect on the science. Only after that would we look for more session time.

**Q: What is still unchecked here?**
Whether a Kaggle 2 × T4 session uses 1 or 2 hours of the weekly quota per real hour. Lesson 09 explains how to check it in ~15 minutes.

---

## 4. Checked vs. assumed

| We checked | We assume |
|---|---|
| Unsloth's notebook really ran on a free T4 (14.563 GB, Bfloat16 = FALSE) | Kaggle's ~30 GPU-hours/week and ~12-hour sessions (secondary sources) |
| Colab FAQ: sessions "at most 12 hours" | Kaggle's phone verification and menu names (common knowledge) |
| Our own notebook 08 runs top to bottom | How Kaggle counts quota for 2 GPUs |

---

## 5. Where it is written

- [lessons/08-python-basics.md](../lessons/08-python-basics.md) · [lessons/09-colab-and-kaggle.md](../lessons/09-colab-and-kaggle.md)
- [notebooks/08_python_basics.ipynb](../notebooks/08_python_basics.ipynb)
- [PLAN.md](../PLAN.md) §11 · [DECISIONS.md](../DECISIONS.md) rows #2, #31
- [research/gpu-time-budget.md](../research/gpu-time-budget.md) §8
