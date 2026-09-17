# Q&A 06: The method, the hypothesis, and what we compare against

⬅️ [All Q&A](README.md) · Hard word? See [GLOSSARY.md](../GLOSSARY.md)

---

## 1. The step in 2 sentences

The model answers each training problem 4 times. We keep its **shortest correct** answer,
train a small LoRA add-on on those answers, and compare it with 4 other ways of answering.

---

## 2. Questions a teacher may ask

**Q: Explain your method step by step.**

```text
1. The model answers each training problem 4 times (thinking ON)
          │
2. We run each answer against the problem's tests (in a sandbox)
          │
3. For each problem: keep the SHORTEST CORRECT answer
   (but not shorter than half the median correct length)
          │
4. Train ONE LoRA add-on on these short correct answers
          │
5. Test all 5 ways of answering on the same test problems,
   with the same limits and the same seeds
```

*Everyday example:* a student solves each homework question 4 times.
The teacher keeps the shortest solution that is still right, and the student studies those.

**Q: Why train on the model's *own* answers?**
They are in the model's own style, so they are easy for it to learn.
And they are already checked by real tests, so we know they are correct.

**Q: Why "not shorter than half the median"?**
A paper called S3-CoT (2602.01982) warns: training only on the very shortest answers hurts accuracy.
Very short answers may be lucky guesses. Our rule skips them.
It also stops the model from learning "always stop early".

**Q: What are the 5 ways of answering?**

| # | Way of answering | Cost |
|---|---|---|
| 1 | Thinking OFF | free |
| 2 | Thinking budget (stop thinking at a limit) | free |
| 3 | "Think briefly" prompt | free |
| 4 | Thinking ON (the normal way) | free |
| 5 | Thinking ON + our LoRA | needs training |

**Q: What is your hypothesis?**
Compared with thinking ON, the trained model:
1. uses **at least 25% fewer** thinking tokens,
2. loses **at most 3 points** of accuracy (on the same problems), and
3. is **more accurate** than thinking OFF, the thinking budget, and the "think briefly" prompt.

**Q: What do you change, and what do you measure?**
- **We change:** the way of answering (the 5 above).
- **We measure:**
  - accuracy: how often the first try passes the tests, averaged over 4 tries
  - thinking length in tokens
  - how often an answer hits the thinking limit

**Q: What result supports your hypothesis? What result proves it wrong?**
- **Supports:** all 3 parts are true on the code test set.
- **Proves it wrong:** a free option is as accurate as the trained model,
  **or** accuracy drops by more than 3 points.

---

## 3. Hard questions

**Q: Your model doesn't need to be more accurate than thinking ON?**
Right. We aim for a **better balance**: much shorter, almost as accurate,
and more accurate than the free options. That is useful in practice.

**Q: How do you know a difference is real and not luck?**
We compare the **same problems** before and after, with **error bars**.
We make the error bars by re-sampling the problems many times (a method called *bootstrap*).
We also use fixed seeds, so the run can be repeated.

**Q: Why 25% and 3 points? Aren't these numbers random?**
We set them **before** the experiment, so we can't move the goal later.
25% fewer tokens is a clear, useful saving. Earlier papers on the same method found
savings of that size (for example, SEER about 40%). 3 points is a small, acceptable accuracy loss.

**Q: Why not use reinforcement learning (like GRPO)? Many papers do.**
It needs much more GPU time. Simple training on example answers fits our free GPUs.
GRPO is future work.

---

## 4. Checked vs. assumed

| We checked | We assume |
|---|---|
| The same method cut tokens on math (Munkhbat et al.) and on 7B code (SEER) | That it also works on Gemma-4-E4B for code |
| S3-CoT's warning about shortest-only training | That half the median is the right cut-off |

---

## 5. Where it is written

- [DECISIONS.md](../DECISIONS.md) rows #14, #19, #25
- [PLAN.md](../PLAN.md) §5 (the 9 research questions), §8 (the method)
