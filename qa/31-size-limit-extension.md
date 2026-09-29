# Q&A 31: Size × limit extension (0.8B and 4B Colabs)

⬅️ [All Q&A](README.md) · Hard word? See [GLOSSARY.md](../GLOSSARY.md) · Decision: [#72](../DECISIONS.md)–[#77](../DECISIONS.md)

---

## 1. The step in 2 sentences

We ran two extra Colabs on Qwen3.5-**0.8B** and **4B**: same 234 problems, several thinking limits, **LoRA-1 only**.
**Both finished.** Best free way: **OFF 20.5%** (0.8B) · **limit 2048 → 78.2%** (4B). LoRA-1 lost on both. See [SIZE-COMPARISON.md](../results/SIZE-COMPARISON.md).

**Where we are:** `EXTENSION ✅ → written into thesis §5.13 / §7.5.4 ✅`

---

## 2. Questions a teacher may ask

**Q: Why more models?**
A: To answer "why only one model?" with three sizes of the **same family**.

**Q: Why several thinking limits?**
A: To answer "why only 1,024?" On 4B the best limit moved to **2,048**. On 0.8B we tested 512/1024 (lean plan).

**Q: Why LoRA-1 not LoRA-2?**
A: LoRA-2’s long LiveCodeBench examples taught long thinking on 2B. New sizes use LoRA-1 only.

**Q: What were the results?**
A: Free controls beat LoRA-1 on every size. Winners: OFF (0.8B), limit1024 (2B), limit2048 (4B).

**Q: Who is this for?**
A: People who run small reasoning models for code on a limited GPU.

---

## 3. Hard questions

**Q: Isn't this changing the thesis after seeing 2B results?**
A: The 2B result stays as reported. This extension was fixed in DECISIONS #72 before the new runs, then executed and written up (#77–#78).

**Q: Why was 0.8B lean (1 try, max limit 1024)?**
A: After 4B used ~100 compute hours we kept a ≥50h buffer (#73–#75). Ranking ways on 0.8B is still fair.

---

## 4. Checked vs. assumed

| Checked | Assumed |
|---|---|
| 0.8B and 4B graded on 234 problems | Exact Colab unit cost of the whole extension |
| Join tables + thesis §5.13 | 0.8B would not change if we had run limit 2048 |

---

## 5. Where it is written

- Numbers: [RESULTS-INDEX.md](../results/RESULTS-INDEX.md) · [SIZE-COMPARISON.md](../results/SIZE-COMPARISON.md)
- Notebooks: [15b](../notebooks/15b_qwen35_4b.ipynb) · [15a](../notebooks/15a_qwen35_0_8b.ipynb)
- Thesis: §5.13 · §6.7 · §7.5.4
- Decisions: [#72](../DECISIONS.md)–[#78](../DECISIONS.md)
