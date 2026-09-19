# Lesson 05: Overthinking

⬅️ [Lesson 04](04-reasoning-models-and-thinking.md) · [ROADMAP](../ROADMAP.md) · ➡️ [Lesson 06: Cutoff dates](06-cutoff-dates.md) · Hard word? See [GLOSSARY](../GLOSSARY.md)

---

## 1. In one sentence

**Overthinking is when a model writes long thinking where much shorter thinking would give the same correct answer; it is the problem our thesis tries to fix.**

---

## 2. What is it?

### 2.1 Everyday examples

```text
A student writes 5 pages for "2 + 2 = ?"                  → correct, but a waste
A person locks the door, then checks it 10 more times     → still locked, time lost
```

### 2.2 What it looks like in a model

A made-up example of thinking for an **easy** problem ("return the sum of a list"):

```text
I need to add all numbers. Python has sum(). So: return sum(nums).          ← enough! (≈ 20 tokens)
Wait, let me double-check. What if the list is empty? sum([]) is 0. Good.
But let me reconsider. Maybe I should use a loop instead?
total = 0, for x in nums: total += x. That also works.
Hmm, which is better? sum() is simpler. Let me check again: sum([1,2,3]) = 6. Yes.
Wait, what about negative numbers? sum([-1, 2]) = 1. Fine.
Let me reconsider the loop version once more...                              ← (≈ 200+ tokens)
Final: return sum(nums)
```

The answer was ready after the **first line**. Everything after it gives the **same** final code.

### 2.3 Typical signs of overthinking

| Sign | Example |
|---|---|
| Checking the same thing again and again | "Let me check again…" ×5 |
| "Wait" / "let me reconsider" after the answer is already right | "Wait, maybe…" |
| Trying other solutions after one already works | "Maybe a loop instead?" |
| Repeating the question in other words | "So the task is to…" ×3 |

### 2.4 Not all long thinking is overthinking

```text
Hard problem, long thinking, needed to get it right   → GOOD thinking ✅
Easy problem, long thinking, same answer as short     → OVERTHINKING ❌
```

That's why we can't just cut all thinking: on harder steps it helps (lesson 04).

---

## 3. Why do we need it? (in our thesis)

**Overthinking is our PROBLEM box.**

```text
PROBLEM → GAP → QUESTION → HYPOTHESIS → EXPERIMENT → ...
   ↑
 this lesson
```

Why it matters:

1. **Time.** Every extra token is one more turn of the loop (lesson 02).
2. **Money and energy.** Companies pay for GPU time per token.
3. **Our own experiment.** Our test run is ~30 million tokens, about 10–30 GPU-hours (estimate, PLAN.md §10).
   Shorter thinking makes everything cheaper, for everyone who uses the model.

---

## 4. How does it work?

### 4.1 Why do models overthink? (a common explanation)

⚠️ This is the usual explanation in papers. We did not test it ourselves.

```text
Reasoning training (lesson 03, stage 3):
   the model gets rewarded for CORRECT answers
   long thinking often helps on HARD problems  → long thinking gets rewarded
   nothing punishes long thinking              → length is "free" for the model
                                  │
                                  ▼
   the habit "think long" is used EVERYWHERE, even on easy problems
```

*Everyday example:* a student learned that writing a lot got good marks on hard exams.
Now they write a lot on every question, even easy ones.

### 4.2 How we can SEE overthinking: ask the same problem 4 times

The model is a little random. Ask it the same problem 4 times and you get 4 different thinking lengths.

**Worked example** (made-up numbers):

| Try | Thinking tokens | Passes the tests? |
|---|---|---|
| 1 | 2,400 | ✅ |
| 2 | 1,200 | ✅ |
| 3 | 3,000 | ❌ |
| 4 | 1,800 | ✅ |

Only the **correct** tries count: 2,400 · 1,200 · 1,800.

```text
Average correct length   = (2,400 + 1,200 + 1,800) ÷ 3 = 1,800
Shortest correct length  = 1,200

Room to shorten = shortest ÷ average = 1,200 ÷ 1,800 = 0.67
```

**What 0.67 means:** the model **already can** solve this problem with 33% fewer tokens.
It just doesn't do it every time. That gap is overthinking we can **measure**.

Our rule (the room-to-shorten check, PLAN.md §7): the ratio must be **≤ 0.75** (at least 25% shorter). Here 0.67 ✅.

### 4.3 From measuring to fixing: which answer do we train on?

We keep the **shortest correct** answer, but **not shorter than half the median** correct length.

```text
Correct lengths sorted:  1,200 · 1,800 · 2,400
Median (middle value)  = 1,800
Half the median        = 900
Shortest correct       = 1,200   → 1,200 ≥ 900 → KEEP ✅ (this becomes a training example)
```

If the shortest had been 500 (below 900), we would **not** keep it: it might be a lucky, too-short answer
(the S3-CoT paper warns that training only on the very shortest answers hurts accuracy).

### 4.4 Four ways to fight overthinking

| Way | How | Cost | Risk |
|---|---|---|---|
| Thinking OFF | Don't think at all | free | Wrong answers where thinking was needed |
| Thinking budget | Stop at k tokens | free | Cut off in the middle of a needed step |
| "Think briefly" prompt | Ask in words | free | The model may not listen |
| **Training (ours)** | Learn from its own short correct answers | ~4 GPU-hours (estimate) + making data | May learn "always stop early" |

**Our question:** does the last row give a better balance than the three free rows?

### 4.5 What papers found (so it's not just a hope)

| Paper | Found | Mark |
|---|---|---|
| Self-Training Elicits Concise Reasoning (Munkhbat et al., 2502.20122) | Training on shortest correct answers: −12% tokens (plain), accuracy about the same (math) | ✔ |
| SEER (2509.14093) | Code tasks, 7B model: about 40% shorter | ✔ |
| Reasoning steps in thinking code LLMs (2511.05874) | Cutting 10–30% of steps keeps easy tasks, **hurts hard ones** | ✔ |
| Do NOT Think That Much for 2+3=? (2412.21187) | Describes overthinking in reasoning models | ⚠️ not opened |

✔ = we opened the paper page. ⚠️ = seen in search results only.

---

## 5. Try it (free, 10 minutes, paper and pen)

The model answered two problems 4 times each (made-up numbers).

**Problem A:** 1,000 ✅ · 1,100 ✅ · 900 ✅ · 1,000 ✅
**Problem B:** 3,000 ✅ · 600 ✅ · 2,000 ❌ · 2,400 ✅

For each problem, work out:
1. Average correct length
2. Shortest correct length
3. Room to shorten (shortest ÷ average). Is it ≤ 0.75?
4. Median correct length, and half of it
5. Do we keep the shortest correct answer as a training example?

<details><summary>Answers</summary>

**Problem A:** average = (1,000 + 1,100 + 900 + 1,000) ÷ 4 = 1,000. Shortest = 900. Ratio = 0.90 → **not ≤ 0.75**: little room to shorten, this model doesn't overthink much here.
Median = 1,000 (sorted 900, 1,000, 1,000, 1,100 → middle two are 1,000 and 1,000). Half = 500. 900 ≥ 500 → it *can* be kept, but it barely helps.

**Problem B:** correct ones are 3,000 · 600 · 2,400. Average = 6,000 ÷ 3 = 2,000. Shortest = 600. Ratio = 0.30 → lots of room to shorten.
Median = 2,400 (sorted 600, 2,400, 3,000). Half = 1,200. 600 < 1,200 → **don't keep** 600 (maybe a lucky, too-short answer).
Under our rule we take the shortest correct answer that is **not below** 1,200. That is 2,400.
</details>

Note: in the real check (PLAN.md §7) we average the ratio over 200 problems, not one.

---

## 6. ✅ Check yourself

**Q1.** What is overthinking, in one sentence?

<details><summary>Answer</summary>
Long thinking where much shorter thinking would give the same correct answer.
</details>

**Q2.** Is all long thinking bad?

<details><summary>Answer</summary>
No. On hard problems long thinking is often needed to be correct. It is only overthinking when shorter thinking would give the same correct answer.
</details>

**Q3.** How can we see overthinking with numbers?

<details><summary>Answer</summary>
Ask the same problem several times. If the shortest correct answer is much shorter than the average correct answer, the model can solve it shorter but usually doesn't.
</details>

**Q4.** Why don't we keep an extremely short correct answer (below half the median)?

<details><summary>Answer</summary>
It may be a lucky answer. Training on the very shortest answers can hurt accuracy (S3-CoT warning) and teach the model to stop too early.
</details>

**Q5.** Name the three free ways to fight overthinking.

<details><summary>Answer</summary>
Thinking OFF, a thinking budget, and a "think briefly" prompt.
</details>

---

## 7. You are here

```text
PART 1: What AI is → 01 ✅ → 02 ✅ → 03 ✅ → 04 ✅ → [05 ✅ Overthinking] → 06 Cutoffs
                                                          ↑ you just finished this
```

**Research chain:** you now understand our **PROBLEM** box, and the idea behind the **room-to-shorten check**.

**Next:** [Lesson 06: Cutoff dates](06-cutoff-dates.md), the last lesson of Part 1.
