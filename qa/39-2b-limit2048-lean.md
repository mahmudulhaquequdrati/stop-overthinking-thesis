# Q&A 39: 2B limit-2048 lean fill-in (notebook 17)

⬅️ [All Q&A](README.md) · Decision: [#83](../DECISIONS.md) · Run: [results/2b-limit2048/RUN.md](../results/2b-limit2048/RUN.md)

---

## 1. The step in 2 sentences

We add a **cheap** 2B × limit **2048** run to see if accuracy keeps rising after 1024.
**1 try**, tight max tokens, no other ways — to save Colab hours.

---

## 2. Why lean?

| Full 2-try / 8k style | This lean run |
|---|---|
| ~2× answers | **1 try** |
| LCB up to 8192 tokens | **max = 2048+1024** |
| Many ways | **limit2048 only** |

---

## 3. Checked vs. assumed

| Checked | Assumed |
|---|---|
| Notebook 17 built | Accuracy after Colab |

---

## 5. Where it is written

`notebooks/17_qwen35_2b_limit2048.ipynb` · DECISIONS #83
