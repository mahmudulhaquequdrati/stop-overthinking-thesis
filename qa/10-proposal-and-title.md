# Q&A 10: The proposal and the title

<!-- CURRENT-STUDY:START -->

**Historical record below.** Its earlier scores, model choices and plans describe that stage only.
Use the current results linked here for the completed study.

**Current study — 14 October 2026:** **464 unique test problems**.
Benchmarks: **164 HumanEval+**, **166 LiveCodeBench easy**, **134 LiveCodeBench medium**.
All six planned LoRA combinations are complete, one attempt per problem:

- **0.8B:** LoRA + OFF **14.0% (65/464)**; LoRA + limit 512 **14.4% (67/464)**.
- **2B:** LoRA + OFF **35.6% (165/464)**; LoRA + limit 1,024 **41.2% (191/464)**.
- **4B:** LoRA + OFF **64.7% (300/464)**; LoRA + limit 2,048 **71.6% (332/464)**.

LoRA alone means thinking ON without a thinking-token limit.
Older methods' all-attempt averages and first-attempt comparisons are labelled separately.
LoRA + OFF does not consistently improve on free OFF; the 2B/4B gains over free limits remain uncertain.

[Every method, benchmark, difficulty, token count and interval](../results/CURRENT-RESULTS.md) · [Full easy thesis](../easy-thesis/FULL-THESIS.md) · [Full formal Markdown thesis](../thesis/THESIS.md).

<!-- CURRENT-STUDY:END -->

⬅️ [All Q&A](README.md) · Hard word? See [GLOSSARY.md](../GLOSSARY.md)

---

## 1. The step in 2 sentences

We wrote a 4-page thesis proposal in simple English, in black and white.
We gave the thesis a title that says what we do, with which model, and how we judge correctness.

---

## 2. Questions a teacher may ask

**Q: What is the title?**
**"Stop Overthinking, Keep Passing the Tests: Shortest-Correct LoRA Fine-Tuning versus the Thinking Switch in a Small Code Model (Gemma-4-E4B)"**

**Q: What does each part of the title mean?**

| Part of the title | Meaning |
|---|---|
| Stop Overthinking | We cut thinking that is not needed |
| Keep Passing the Tests | Correctness is judged by the benchmark's real tests |
| Shortest-Correct LoRA Fine-Tuning | Our method: train a LoRA add-on on the shortest correct answers |
| versus the Thinking Switch | Our contribution: the fair comparison with the free OFF switch |
| in a Small Code Model (Gemma-4-E4B) | The model and the domain |

**Q: Why did the title change?**
The old title was "Think Less, Code Just as Well: Teaching a Small Reasoning Model to Think Shorter on Code".
It was too vague. It named neither the model, the training method, nor how correctness is judged.

**Q: Why is the model name in brackets?**
If the memory check fails and we switch to Qwen3.5-4B, only the bracket changes.

**Q: Why no dataset names in the title?**
Three dataset names make the title too long. They belong in the summary.

**Q: What is in the proposal?**
10 sections: Summary · The Problem · What Is Known and What Is Missing ·
Research Question and Hypothesis · Method · Experiment Setup · Two Checks Before the Big Runs ·
Timeline · Risks · Expected Contribution. Plus 11 references.

**Q: Why did the proposal get shorter?**
The first version was too big and too colourful. So we rewrote it:
4 A4 pages, black and white, easy English, with hard words explained in the text.

---

## 3. Hard questions

**Q: The proposal says 12 weeks. Is that realistic for a beginner?**
Weeks 1–2 include learning the tools. The plan has checks in week 3, so problems show up early.
The GPU estimates say calendar time can be 3–5× the GPU time, so the timeline is tight but planned.

**Q: Which version of the proposal is the official one?**
The **PDF** is the version handed in. `proposal.html` is the source the PDF is printed from.
`proposal.md` is a copy for reading on GitHub. All three say the same thing.

---

## 4. Checked vs. assumed

| We checked | We assume |
|---|---|
| The md has the same 10 sections, numbers and 11 references as the HTML | That the supervisor accepts this proposal |

---

## 5. Where it is written

- [DECISIONS.md](../DECISIONS.md) rows #24, #26, #28, #29
- [proposal/proposal.md](../proposal/proposal.md)
