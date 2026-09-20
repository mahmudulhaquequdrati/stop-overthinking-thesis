# Q&A 23: Moving to Google Colab, and changing the model to Qwen3.5-2B

⬅️ [All Q&A](README.md) · Hard word? See [GLOSSARY.md](../GLOSSARY.md) · Notes: [research/2026-09-20-qwen-small-models.md](../research/2026-09-20-qwen-small-models.md)

---

## 1. The step in 2 sentences

Running the thesis on the user's Mac was fast on easy problems but far too slow on the medium
ones we actually need — 250 seconds for a single problem. So we moved everything to a free
Google Colab GPU, changed the model to the much smaller Qwen3.5-2B, deleted the Mac-only code,
and found and fixed a bug that would have reported zero thinking tokens on every answer.

---

## 2. Questions a teacher may ask

**Q: Why did you change your model?**
Speed, and one hard number behind it. On the Mac, easy problems ran at 52 tokens per second
with 8 questions at once, but the medium problems ran at **21 tokens per second — 250 seconds
for one problem**. Our test set is mostly medium problems answered 4 times each in 5 different
ways, so that pace does not finish inside a one-week deadline.

**Q: Fine, but why not just use a bigger GPU with the old model?**
Because the old model was the reason the GPU was slow. Gemma-4-E4B has a 5.25 GB "per-layer word
table" that does not fit on a free T4 next to the rest of the model, so it had to sit in slow
computer memory instead. That is exactly why it wrote at 4.4 tokens per second (DECISIONS #43,
#46). Qwen3.5-2B needs about 4.5 GB and the T4 has about 15 GB, so the **whole model sits on the
GPU**. The problem disappears instead of being paid for.

**Q: Why Qwen3.5-2B and not something even smaller?**
Smaller models are faster but much worse at code. Our plan has a rule (PLAN §7): the model must
solve at least 40% of problems at least once, otherwise there are no correct answers to make
shorter and the whole method has nothing to work with. A 0.8B model is a real risk of falling
under that line. 2B is the smallest size that is still a serious code model.

**Q: How do you know Qwen even has a thinking switch?**
We did not take anyone's word for it. We downloaded the model's own `chat_template.jinja` from
Hugging Face and read it. Line 149 checks `enable_thinking`; line 150 writes `<think>`. Thinking
is OFF by default. That is checked, not assumed.

**Q: What did you lose by switching?**
The proof that the test problems are new to the model. Google published Gemma's training cutoff
(January 2025), so we could point at problems from after that date and say the model cannot have
seen them. Alibaba publishes no cutoff for Qwen. So the thesis must now say plainly: *we cannot
rule out that the model saw some test problems during training.*

**Q: Isn't that a serious problem?**
It is a real limitation, and it must be written down. But it is smaller than it sounds: only
**70** problems were both fresh and easy/medium, which is far too few to prove anything on their
own (DECISIONS #41). It was always a side note, not the main result. The main comparison is
*the same model against itself*, with thinking on, off, or shortened — and contamination affects
all of those equally, so it cannot create a fake difference between them.

**Q: You deleted working code. Why?**
Because keeping it would have been worse than losing it. If some ways of answering ran on a Mac
and others on a GPU, with different number squeezing, the five ways would not be comparable any
more — and comparing them fairly is the whole thesis (CLAUDE.md §4). Keeping two half-used paths
also means two copies of the thinking counter, which drift apart. Every result file was kept.

**Q: So the deleted code can be recovered if you need it?**
Mostly not, and this is worth admitting. We assumed it was safe in git history. It was not:
four of the five files had **never been committed**, so deleting them destroyed them. Only
`mac_pilot_generate.py` — the script that actually produced the Gemma pilot numbers we still
cite — was committed and can be brought back. `run_live.py`, `dashboard.py` and
`watch_results.py` are gone. The lesson, which now applies to the rest of this thesis:
**commit new code the day it is written, before any clean-up.**

**Q: What was the bug you found?**
Our code counted thinking tokens by looking for a *start* marker in the model's answer. That
works for Gemma, which writes the marker itself. Qwen puts its `<think>` marker in the
**question** instead, so it is never in the answer. Our counter would have found nothing and
reported **0 thinking tokens on every single answer** — with no error and no crash.

**Q: Why does that matter so much?**
Thinking tokens are the one number this whole thesis tries to shrink. If they are all zero, every
result, every graph and every conclusion is wrong. And because nothing crashes, we could have run
for days before noticing.

**Q: How do you know it is fixed now?**
We wrote `scripts/test_prompts.py`. It downloads Qwen's **real** chat template and runs 13 checks:
the switch changes the prompt, thinking tokens are counted and are not zero, a switched-off answer
counts exactly zero, a cut-off answer counts as failed, and the old Gemma style still works. All
13 pass. It needs no GPU and takes about 10 seconds, so it runs before every session.

---

## 3. Hard questions

**Q: You chose this model before measuring it. Isn't that the same guessing you warned about?**
The *switch* and the *memory* are checked facts. The *speed* and the *accuracy* are not, and we
say so. That is why the choice is written down as **provisional**: notebook 12 runs a 30-problem
pilot and prints three numbers, and those numbers decide. We also wrote down in advance what each
result means, so we cannot talk ourselves into a convenient story afterwards.

**Q: You cut the test set from ~1,000 problems to 234. Is that cherry-picking?**
It would be, if we had chosen after seeing results. We chose before, and we wrote down the
arithmetic: 1,000 problems × 5 ways × 4 tries ≈ 20,000 answers ≈ 13+ GPU hours, which does not
finish on a free account in one week; 234 problems ≈ 3–4 hours, which does. The set is fixed and
named, not picked problem by problem. The honest cost is that fewer problems means wider error
bars, so only a bigger difference will be provable — and that must be in the thesis.

**Q: Your old Gemma numbers were 93% and 83%. Will you compare Qwen against them?**
No, and this is important. Those came from a Mac with 4-bit squeezing; the Qwen numbers will come
from a Colab GPU with 16-bit. Different machine, different precision — that is not a fair
head-to-head, and presenting it as one would be misleading. Instead we compare Qwen against the
**fixed thresholds** written in PLAN §7 (40% and 0.75). Those are absolute numbers, so they do
not care which machine produced them.

**Q: What if the room-to-shorten number fails? Doesn't your thesis collapse?**
Not immediately. The plan already says what to do: ask each problem 8 times instead of 4, because
more tries mean more chances that one of them is short (DECISIONS #27). If it still fails after
that, then it is a genuine result: *this model's correct answers are all about the same length,
so there is nothing for shortest-correct training to learn.* That is a finding, and we would
report it honestly rather than hide it.

---

## 4. What we checked, and what we only assume

| ✅ We checked this | ❌ We only assume this |
|---|---|
| Qwen3.5-2B has a real thinking switch (read its own chat template) | That it is fast enough on a free T4 |
| Thinking is OFF by default in that template | That it solves ≥40% of problems at least once |
| The markers are `<think>` and `</think>` | That its correct answers vary enough in length |
| The file is 4.58 GB and fits fully on a free T4 | That the full run finishes inside free Colab |
| The thinking counter is correct (13/13 checks pass) | That `transformers` on Colab loads it without trouble |
| The old Mac speed: 52 tok/s easy, 21 tok/s medium | |
| Qwen publishes **no** training cutoff date | |

---

## 5. Where this is written down

- **Decisions:** [DECISIONS.md](../DECISIONS.md) rows #52–#58 (and #8, #39, #47, #49 struck through)
- **Plan:** [PLAN.md](../PLAN.md) §6 (test set) and §7 (model, gates)
- **Roadmap:** [ROADMAP.md](../ROADMAP.md) "You are here" and "What to do next"
- **Notes:** [research/2026-09-20-qwen-small-models.md](../research/2026-09-20-qwen-small-models.md)
- **Code:** `scripts/models.py`, `scripts/prompts.py`, `scripts/gen_colab.py`,
  `scripts/check_gates.py`, `scripts/test_prompts.py`, `notebooks/12_qwen_colab.ipynb`
