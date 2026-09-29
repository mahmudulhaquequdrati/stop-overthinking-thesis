# Q&A 37: Thesis A→Z and what to tell the teacher

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
