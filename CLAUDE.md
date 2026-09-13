# CLAUDE.md — working rules for this thesis

Thesis (working title): **"Think Less, Code Just as Well"**. We teach a small 2026
reasoning model to think shorter on code problems without losing accuracy, and we
check whether that is better than just switching its thinking OFF.

**Read [ROADMAP.md](ROADMAP.md) first.** It says where we are and what comes next.
The research design is in [PLAN.md](PLAN.md). Every choice and its reason is in
[DECISIONS.md](DECISIONS.md).

This project is **separate from CARR** (`~/thesis`). Don't read or change that
folder unless the user asks.

---

## 0. How to talk to the user — read this first

The user is a **beginner, learning from zero**. They said: explain *what* we are
doing, *why*, and *how*, starting from "what is an LLM?". This section beats any
other style habit.

**Language**
- **Easy English.** Short sentences. One idea per sentence.
- Every technical word gets a one-line meaning the first time it appears
  ("a *token* is a small piece of text, about ¾ of a word").
- No walls of text. Many small numbered headings, one idea each.

**Shape of an answer**
1. Start with the idea in 1–2 plain sentences.
2. Give an **everyday example** before the technical detail.
3. **Draw it.** ASCII flows (`Question → Model → Answer`), boxes, small tables.
4. Say **why** before **how**.
5. Say which box of the research chain we are in:
   `PROBLEM → GAP → QUESTION → HYPOTHESIS → EXPERIMENT → DATA/CODE → RESULTS → ANALYSIS → CONCLUSION`
6. End with **"What to do next"** and **one** recommendation, not a menu.

**Before explaining or writing any code, answer the 5 code questions**
1. What problem does this solve? 2. Why do we need it? 3. What goes in?
4. What comes out? 5. Why did we build it this way?

**Before running or explaining any experiment, answer the 9 research questions**
What am I testing? · Hypothesis? · Independent variable (what I change)? ·
Dependent variable (what I measure)? · Baseline? · Data? · Metric? · What result
supports it? · What result contradicts it?

**Honesty, said simply**
- A bad result is fine. Say it plainly, then explain *why* it happened.
- Always separate **"we checked this"** from **"we assume this"**. Model names,
  dataset ids, GPU limits and paper claims are unverified until checked, so say so.

---

## 1. How we teach

- **One lesson at a time.** Lessons live in `lessons/`. Write the next one or two
  only when the user reaches them, not ahead.
- **Every lesson uses the same template:** In one sentence · What is it? (everyday
  example) · Why do we need it? (in *our* thesis) · How does it work? (picture) ·
  Try it (free) · ✅ Check yourself (answers hidden in `<details>`) · You are here.
- **Explain-back test.** The user explains the lesson in their own words before we
  move on. If they can't, teach it again differently. Don't just repeat it.
- **Learn before doing.** A notebook step comes only after the lesson that explains it.

---

## 2. Save everything to the docs — mandatory

The user asked that what we say in chat is **always written down**. At the end of
every session, before reporting back, update:

| File | What |
|---|---|
| **ROADMAP.md** | The "You are here" box + the next step |
| **DECISIONS.md** | One dated row per choice made, **with its reason**. Append only; don't delete old rows, strike them through |
| **PLAN.md** | When the research design changes (hypotheses, data, model, gates) |
| **PAPERS.md** | When a related paper is found or checked |
| `research/` | Full notes from any web or literature search, saved as a dated `.md` |
| `results/` | Numbers from runs (CSV) + a short `.md` saying what they mean |

Numbers must match everywhere. When one changes, grep for the old value.

---

## 3. Git — NEVER commit unless the user asks

- **Do not run `git commit` or `git push` on your own.** Not at the end of a
  session, not "to be safe". Only when the user says so.
- It's fine to show `git status` / `git diff` so the user sees what changed.
- When committing on request, end the message with:
  `Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>`

---

## 4. Hard rules

- **$0 only.** Free Colab / Kaggle GPUs, Hugging Face downloads. No paid APIs, no
  paid GPU, no Colab Pro. If something would cost money, stop and say so.
- **Run model-written code only inside a sandbox** (evalplus or the LiveCodeBench
  runner: separate process, timeouts). Never `exec` it in the notebook itself.
- **Grade with the benchmark's real tests**, never with `==` on printed output by hand.
- **Fixed seeds everywhere:** sampling, data splits, bootstrap.
- **Save work to Google Drive often** (every ~20 problems). Free sessions end without warning.
- **No test problem may appear in training data.** Run the overlap check before training.
- **Same rules for every policy at test time:** the same thinking limit, the same
  prompts (except the one being tested), the same seeds.
- **Store raw model outputs verbatim** (the thinking + the answer). Re-grading is then
  free; re-generating costs GPU days.
- **Pre-set gates decide, not wishes.** The memory gate, the headroom gate and the
  hard-problems rule are in PLAN.md §7. Check a gate before scaling up.
- **`.env`, tokens and API keys are never committed.**

---

## 5. Code style

- Small research project, not a framework. Plain functions, no speculative layers.
- Notebooks: a markdown cell above each code cell answers the 5 code questions in
  one or two lines.
- Comments explain *why*, not *what*.
