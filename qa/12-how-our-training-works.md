# Q&A 12: How our training works (fine-tuning)

⬅️ [All Q&A](README.md) · Hard word? See [GLOSSARY.md](../GLOSSARY.md) · Lesson: [03 How a model learns](../lessons/03-how-a-model-learns.md)

---

## 1. The step in 2 sentences

We learned how a model learns: guess the next token, compare with the right one, nudge its numbers a tiny bit.
Our thesis uses **fine-tuning**: a short extra training on the model's own short, correct answers, to teach it the habit of thinking shorter.

---

## 2. Questions a teacher may ask

**Q: What does "training a model" mean?**
The model guesses each next token of an example. We compare the guess with the real token and get an error score.
Then we nudge the model's numbers a tiny bit so the right token becomes more likely. We repeat this for all examples.

**Q: What is fine-tuning?**
Taking a model that is already trained and training it a little more on our own examples.
It doesn't learn everything again. It learns a new habit.

**Q: Which kind of fine-tuning do you use?**
**SFT** (supervised fine-tuning): we show example answers, and the model learns to write like them.
We do it with **LoRA**: a small add-on is trained, and the original numbers stay unchanged.
We do not use reinforcement learning (training with rewards). That is future work.

**Q: What does your training data look like?**
Each example is: **a code problem → the model's own shortest correct answer** (short thinking + code that passes the tests).
Plan: about 2,000 examples, 1 epoch (one pass). (Estimates; see PLAN.md §10.)

**Q: How does the model learn to think shorter if nobody tells it to?**
Every example it sees has short thinking. After many examples, the small nudges add up,
so finishing the thinking earlier becomes more likely.

**Q: Why not just tell the model "think briefly" in the prompt?**
That is exactly one of the free options we test. If the prompt works as well as training,
training is not worth it. That comparison is our research question.

**Q: Why 1 epoch?**
The closest paper (Munkhbat et al. 2025) trained on shortest correct answers for 1 epoch.
More epochs cost more GPU time and increase the risk of damaging other skills.

---

## 3. Hard questions

**Q: Does fine-tuning teach the model new knowledge?**
Not in our case. The answers come from the model itself, so it already "knows" them.
We change **how long it thinks**, not what it knows.

**Q: Could fine-tuning damage the model's other skills?**
Yes, that is a real risk (called *forgetting*). LoRA lowers it, because the original numbers stay unchanged.
We check it by measuring accuracy on the test set. If accuracy drops more than 3 points, the hypothesis fails.

**Q: The model might learn to always stop early. What then?**
Our selection rule skips answers shorter than half the median correct length.
We also record how often each way of answering hits the thinking limit.

**Q: Why can you answer with 8,000 tokens but only train on 3,500?**
Training needs much more GPU memory than answering, because it keeps in-between results to work out the nudges.
The memory check in week 3 tests if 3,500 fits.

**Q: When you train on an example, does the error score count the question tokens too?**
No, only the answer part (decided 2026-09-17, DECISIONS #42). We don't want the model to learn to write
questions; we want it to learn short correct answers. Unsloth's official Gemma-4 notebook does the same
(`train_on_responses_only`). We re-check it when we build the training notebook (lesson 20).

---

## 4. Checked vs. assumed

| We checked | We assume |
|---|---|
| Munkhbat et al. 2025 used 1 epoch (from our paper search) | That ~2,000 examples are enough to change the habit |
| The TensorFlow Playground page opens (2026-09-17) | Gemma-4's own training stages (the lesson shows a typical recipe, not checked for Gemma) |
| | The ~4 GPU-hour training time (estimate, measured in week 3) |

---

## 5. Where it is written

- [lessons/03-how-a-model-learns.md](../lessons/03-how-a-model-learns.md)
- [PLAN.md](../PLAN.md) §8 (the method), §10 (GPU time)
- [DECISIONS.md](../DECISIONS.md) rows #14, #25, #30
- [Q&A 06](06-method-hypothesis-baselines.md) (the method and hypothesis)
