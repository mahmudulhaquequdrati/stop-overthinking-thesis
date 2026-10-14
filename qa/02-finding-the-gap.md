# Q&A 02: Finding the gap (what nobody did yet)

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

We searched research papers from 2025–2026 to see what is already done.
We found one clear open question: on one small model with a thinking switch,
is **training** it to think shorter better than the **free options**?

---

## 2. Questions a teacher may ask

**Q: What is a research gap?**
A question that nobody has answered yet. A thesis must answer one.

**Q: How did you search?**
A search helper looked on arXiv (the free paper website) and 2025–2026 conferences.
It tried to **prove each gap wrong**, by looking for a paper that already did it.
Some papers we opened and checked (✔). Others we only saw in search results.

**Q: What is your gap?**
We call it **G-A**. Nobody tested these 5 ways of answering on **the same small model** for code:

```text
1. Thinking OFF              (free)
2. Thinking budget (limit)   (free)
3. "Think briefly" prompt    (free)
4. Thinking ON               (the normal way)
5. Thinking ON + our training
```

The question is: does number 5 give a better balance of accuracy and length than 1, 2 and 3?

**Q: What are the closest papers to yours?**

| Paper | What it did | What it did not do |
|---|---|---|
| Munkhbat et al. 2025 (2502.20122) | Kept the shortest correct answer and trained on it | Math only. No thinking switch |
| SEER (2509.14093) | Same idea on code tasks, 7B model, about 40% shorter | Older model without a switch |
| ASAP (2508.05988) | Cut code thinking, 23.5% fewer tokens | Older 7–8B models, no OFF comparison |
| NoThinking (2504.09858) | Thinking OFF can beat a small thinking budget | No training for shorter thinking |
| HRBench (2605.28398) | Compares ways to use the switch | Does not compare against a model trained to think shorter |

**Q: Why is the OFF switch so important for you?**
Because it is free. If switching OFF works as well as training, training adds nothing.
The NoThinking paper showed OFF can beat limited thinking. So OFF is a strong rival.

---

## 3. Hard questions

**Q: Are you the first to shorten reasoning for code?**
**No.** SEER and ASAP already did it. We don't claim that.

**Q: Are you the first to do it on cheap GPUs?**
**No.** TokenSkip already used LoRA on cheap GPUs. We don't claim that.

**Q: Are you the first to show math training helps code?**
**No.** HAPO and LC-R1 showed math → code. We don't claim that either.

**Q: How do you know nobody did G-A? Maybe you missed a paper.**
Honest answer: "not found" means **we did not find** it, not that it does not exist.
We will search again before writing the related-work chapter.

**Q: SEER found LoRA loses about 7 points versus full training (67.7% vs 74.9%). Why do you still use LoRA?**
Full training does not fit on a free GPU. LoRA does.
We know this risk, and we report it honestly.

---

## 4. Checked vs. assumed

| We checked | We assume |
|---|---|
| The ✔ papers in PAPERS.md were opened on arXiv (2026-09-13) | Papers without ✔: their numbers may be slightly off |
| No paper found doing G-A on Gemma-4-E4B | That no such paper exists at all |

---

## 5. Where it is written

- [DECISIONS.md](../DECISIONS.md) rows #19, #20, #25
- [PLAN.md](../PLAN.md) §4
- [research/gaps.md](../research/gaps.md) (full search notes)
- [PAPERS.md](../PAPERS.md) (reading list)
