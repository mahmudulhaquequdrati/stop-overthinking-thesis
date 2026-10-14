# Q&A 37: Thesis A→Z and what to tell the teacher

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

⬅️ [All Q&A](README.md) · Full guide: [TEACHER-A-TO-Z.md](../TEACHER-A-TO-Z.md) · Thesis: [THESIS.md](../thesis/THESIS.md)

---

## 1. The step in 2 sentences

We made one A→Z map: how to read the whole thesis, where to check every number, and short answers for the teacher.
Use [TEACHER-A-TO-Z.md](../TEACHER-A-TO-Z.md) before any meeting.

---

## 2. Say this (main finding)

On small Qwen3.5 code models, a **free** control beats shortest-correct LoRA.  
Best free way: **OFF** on 0.8B (20.5%), **limit 1024** on 2B (49.8%), **limit 2048** on 4B (78.2%).  
Reason: waste is **loops**, not careful overthinking.

## 3. Where to check (minimum)

| Claim | File |
|---|---|
| 2B limit 49.8% | `results/2026-09-24-thesis-run.md` |
| 0.8B OFF 20.5% | `results/0.8b/SUMMARY.md` |
| 4B limit2048 78.2% | `results/4b/SUMMARY.md` |
| All three | `results/SIZE-COMPARISON.md` |
| In the thesis | §5.13 · §6.7 · §7.5.4 |

## 4. Hard question

**Q: Why 1 try on 0.8B?**  
Hour budget after 4B; ranking ways is still fair; caption says 1 try (DECISIONS #75–76).

## 5. Where it is written

[TEACHER-A-TO-Z.md](../TEACHER-A-TO-Z.md) · DECISIONS #78–#79
