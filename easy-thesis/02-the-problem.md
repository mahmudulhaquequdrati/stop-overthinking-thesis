# The problem, the gap, and the question

We are in this box:

```text
PROBLEM → GAP → QUESTION → HYPOTHESIS → EXPERIMENT → … → CONCLUSION
   ▲         ▲        ▲           ▲
  here     here     here        here
```

## 1. The problem

New code models "think" before they answer.
Thinking means they write notes to themselves, then the code.
Thinking can help.
It also costs tokens and time.
A *token* is a small piece of text, about three quarters of a word.

On a small model, those notes are often far longer than the code.
People call that overthinking.
Our later results show a sharper name: **getting stuck in a loop.**

Everyday picture: the student writes five pages for "2 + 2", then copies the same paragraph until the bell rings.

## 2. Two ways to fix it

```text
Question
   │
   ├─ Free ways (no training)
   │     1. Thinking OFF
   │     2. Stop thinking at a fixed length
   │     3. Ask in words: "think briefly"
   │
   └─ Training
         Teach a small add-on (a LoRA) using the model's own shortest correct answers
```

A *LoRA* is a small add-on.
The rest of the model stays frozen.
Free ways need no training.
Training needs GPU time and careful data.

## 3. The gap

Other papers have trained models to think shorter.
Other papers have tried a thinking switch or a length cap.
We did not find a study that did **both** on one small code model that has a real ON/OFF switch.
That comparison is the gap.
If a free switch is as good as training, training is not worth it.

## 4. The question

**On a small model with a thinking switch, is training it to think shorter better than the free options?**

## 5. What we expected

We wrote this down **before** the main run.

| Part | We needed | Plain meaning |
|---|---|---|
| H1 | Thinking length ≤ 0.75× normal thinking | It should get clearly shorter |
| H2 | Accuracy loss ≤ 3 points | It should not get much worse |
| H3 | Better than each free way | Training should beat OFF, the limit, and "think briefly" |

What would support it: shorter thinking, accuracy held, and a win over the free ways.
What would reject it: thinking not shorter, or a free way that scores higher.

## 6. What we actually did, in one line

We used **Qwen3.5-2B** on **234** code problems.
We compared six ways.
Then we repeated the idea on **0.8B** and **4B**.

The full method is in [03-how-we-did-it.md](03-how-we-did-it.md).
The scores are in [05-results.md](05-results.md).
