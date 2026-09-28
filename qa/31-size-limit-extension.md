# Q&A 31: Size × limit extension (0.8B and 4B Colabs)

⬅️ [All Q&A](README.md) · Hard word? See [GLOSSARY.md](../GLOSSARY.md) · Decision: [#72](../DECISIONS.md)

---

## 1. The step in 2 sentences

We prepared **two separate Colab notebooks** to re-check the thesis on Qwen3.5-**0.8B** and **4B**: same 234 problems, limits 512–4096, and **LoRA-1 only**, under a shared **150-hour** cap. The finished 2B results stay untouched; a join page waits for the new numbers.

**Where we are:** `CONCLUSION ✅ (2B draft) → EXTENSION ready → GPU runs ⬜ (you on Colab)`

---

## 2. Questions a teacher may ask

**Q: Why more models now?**
A: So we can answer "why only one model?" with three sizes of the **same family** (0.8B, 2B, 4B). Only size changes.

**Q: Why several thinking limits?**
A: So we can answer "why only 1,024?" We sweep **512, 1,024, 2,048, 4,096**.

**Q: Why LoRA-1 and not LoRA-2?**
A: LoRA-1 is the mini-thesis recipe (MBPP+ shortest-correct) that worked on easy data. LoRA-2 added long LiveCodeBench examples and taught the 2B model to think **long**. We do not repeat that mistake on the new sizes.

**Q: Why separate Colabs and folders?**
A: Two sessions cannot overwrite each other. The 2B thesis evidence stays clean. One common page ([ALL-RESULTS.md](../results/ALL-RESULTS.md)) joins the tables later.

**Q: Who is this thesis for?**
A: People who run **small reasoning models for code** on a **limited GPU** (students, indie developers, one-GPU setups).

---

## 3. Hard questions

**Q: Isn't this changing the thesis after seeing results?**
A: The 2B result stays as reported (#67). This extension is **robustness / future work executed**, fixed in DECISIONS #72 **before** the new runs see numbers. Hypotheses for size (loops drop on 4B?) are written in the plan before looking.

**Q: Why a 150-hour cap if you bought 200?**
A: Things break. We keep ≥50 hours as a buffer and will not buy more.

**Q: Why not 9B?**
A: Cost and time. 4B is the next step up; 0.8B is the step down. 9B only if hours clearly remain after both runs.

---

## 4. Checked vs. assumed

| Checked | Assumed / not run yet |
|---|---|
| Notebooks 15a/15b built; folders `results/0.8b`, `results/4b`; shared hours ledger | Real accuracy on 0.8B / 4B |
| `--stop-on-repeat` in `gen_colab.py` (default off for old runs) | That 4B loops less on our 234 problems |
| 2B numbers still match summary.csv | Exact hours each stage will use (estimates only) |

---

## 5. Where it is written

- Notebooks: [15b 4B](../notebooks/15b_qwen35_4b.ipynb) (run first) · [15a 0.8B](../notebooks/15a_qwen35_0_8b.ipynb)
- Run guides: [results/4b/RUN.md](../results/4b/RUN.md) · [results/0.8b/RUN.md](../results/0.8b/RUN.md)
- Join page: [results/ALL-RESULTS.md](../results/ALL-RESULTS.md)
- Decision: [DECISIONS #72](../DECISIONS.md)
