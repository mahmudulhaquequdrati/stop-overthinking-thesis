# Q&A 15: Cutoff dates, and "has the model seen the test?"

⬅️ [All Q&A](README.md) · Hard word? See [GLOSSARY.md](../GLOSSARY.md) · Lesson: [06 Cutoff dates](../lessons/06-cutoff-dates.md)

---

## 1. The step in 2 sentences

We learned that a model may have seen old test problems during its training, so a good score can be memory, not skill.
We checked Gemma's model page ourselves: its **pre-training** data has a cutoff of **January 2025**.

---

## 2. Questions a teacher may ask

**Q: What is a cutoff date?**
The day the model's training text ends. Anything published after that day is "fresh" for the model.

**Q: What is Gemma-4-E4B's cutoff?**
January 2025. We checked it on the Hugging Face model page on 2026-09-17. The page says:
"Our pre-training dataset … with a cutoff date of January 2025."

**Q: Which of your test problems are fresh?**
LiveCodeBench problems from February–April 2025. HumanEval+, MBPP+ and older LiveCodeBench problems
were published earlier, so the model may have seen them.

**Q: Why do you count January 2025 problems as "maybe seen"?**
To be safe. A problem from the cutoff month itself could have been in the training data.

**Q: Why did you choose a model with a published cutoff?**
So we can say which problems are fresh. Our backup, Qwen3.5-4B, has no published cutoff. That is its written downside.

---

## 3. Hard questions

**Q: Most of your test set may be memorized. Doesn't that ruin your results?**
Not the comparison. All 5 ways of answering use the **same** model on the **same** problems,
so memory helps all of them equally. We compare the ways of answering with each other,
not Gemma with other models. The absolute scores may be a bit too high, and we say so.

**Q: But maybe a memorized problem needs less thinking. Doesn't that change your token numbers?**
Possibly. That affects all 5 ways too, but maybe not equally. Testing fresh vs. seen problems separately
is future work (DECISIONS #25). We list it as a limitation.

**Q: Is "January 2025" a proof that the model never saw later problems?**
No. The date is for the **pre-training** data. The model page does not say when the data for later
training stages (chat and reasoning training) ends. So it is strong evidence, not proof.

**Q: How do you stop YOUR training data from containing test problems?**
That is a different risk, and one we control:
1. We drop DeepCoder's `lcbv5` part, because it overlaps with LiveCodeBench.
2. Before training, the overlap check removes every training problem that matches a test problem, exactly or nearly.
This matters most, because a test problem in our training data would help **only** our trained model.

---

## 4. Checked vs. assumed

| We checked | We assume |
|---|---|
| Gemma model page: pre-training cutoff January 2025 (2026-09-17) | The cutoff of Gemma's later training stages (not published) |
| LiveCodeBench lite `release_v6`: 1,055 problems, May 2023 – Apr 2025 (2026-09-13) | How many easy + medium problems are from Feb–Apr 2025 (count in the data notebook) |
| | That each LiveCodeBench problem has a usable date field (check in the data notebook) |

---

## 5. Where it is written

- [lessons/06-cutoff-dates.md](../lessons/06-cutoff-dates.md)
- [PLAN.md](../PLAN.md) §6 (data, overlap check), §7 (the model)
- [DECISIONS.md](../DECISIONS.md) rows #8, #9, #25, #36
- [research/datasets.md](../research/datasets.md) (fresh test sets)
- [Q&A 05](05-data-and-test-size.md) (data and test size)
