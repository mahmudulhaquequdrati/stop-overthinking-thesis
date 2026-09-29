# Stop Overthinking, Keep Passing the Tests

**Shortest-Correct LoRA Fine-Tuning versus Free Thinking Controls in a Small Code Model (Qwen3.5-2B)**  
*Size check also on Qwen3.5-0.8B and Qwen3.5-4B.*

A thesis built step by step. We ask: on a small reasoning model for **code**, is **training** it to think shorter better than **free** options (thinking OFF, a thinking length limit)?

**Main answer (2B):** no — a free **limit of 1,024** tokens was best (**49.8%**). Training did not shorten thinking. The waste was mostly **loops**.

**Size check (same 234 problems):** best free way = **OFF 20.5%** (0.8B) · **limit 1024** (2B) · **limit 2048 78.2%** (4B). LoRA-1 never beat that free winner.

---

## Start here

| File | What |
|---|---|
| **[ROADMAP.md](ROADMAP.md)** | Front door: where we are |
| **[TEACHER-A-TO-Z.md](TEACHER-A-TO-Z.md)** | Before a meeting: what to say + where to check |
| **[thesis/THESIS.md](thesis/THESIS.md)** | Full thesis A→Z (also [PDF](thesis/Stop-Overthinking-Thesis.pdf)) |
| **[results/RESULTS-INDEX.md](results/RESULTS-INDEX.md)** | **All numbers for the paper** (0.8B · 2B · 4B) |
| **[results/SIZE-COMPARISON.md](results/SIZE-COMPARISON.md)** | Three-size comparison page |

## Other docs

| File | What is in it |
|---|---|
| `PLAN.md` | Research design |
| `qa/` | Teacher Q&A, one file per step |
| `GLOSSARY.md` | Hard words, simple meanings |
| `proposal/` | Early proposal (history; model name was later changed) |
| `DECISIONS.md` | Every choice and its reason |
| `PAPERS.md` | Related papers |
| `research/` | Search notes |
| `lessons/` | Course lessons |
| `notebooks/` | Colab notebooks (12–14 main; **15a** 0.8B; **15b** 4B) |
| `results/` | All run numbers (see RESULTS-INDEX) |
