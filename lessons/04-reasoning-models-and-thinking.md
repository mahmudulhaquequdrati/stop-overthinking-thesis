# Lesson 04: Reasoning models and "thinking"

⬅️ [Lesson 03](03-how-a-model-learns.md) · [ROADMAP](../ROADMAP.md) · ➡️ [Lesson 05: Overthinking](05-overthinking.md) · Hard word? See [GLOSSARY](../GLOSSARY.md)

---

## 1. In one sentence

**A reasoning model writes notes to itself (thinking) before its answer; many new models, like our Gemma, have a switch to turn this thinking ON or OFF.**

---

## 2. What is it?

### 2.1 Two kinds of answers

```text
Question: "Write a function that returns the largest number in a list."

THINKING OFF (answer directly)
  def largest(nums):
      return max(nums)

THINKING ON (notes first, then answer)
  [thinking]
  I need the largest number. Python has max(). What if the list is empty?
  max([]) gives an error. The task doesn't say what to do then, so I'll keep max().
  Let me check: largest([3, 9, 2]) → 9. Good.
  [/thinking]
  def largest(nums):
      return max(nums)
```

(Made-up example. Real Gemma thinking looks different. We see the real format in lesson 11.)

Same final code. But the second one wrote **many more tokens** first.

### 2.2 Everyday example: scrap paper in an exam

| | Without scrap paper | With scrap paper |
|---|---|---|
| Easy question ("2 + 2") | Fast, correct | Slower, same answer |
| Hard question (long division) | Often wrong | Slower, but more often correct |

Thinking is the model's scrap paper.

### 2.3 What is a reasoning model?

A **reasoning model** is an LLM that was **trained to write thinking** before answering.
(Lesson 03, stage 3: "reasoning training".)

A **thinking switch** means the same model can do both:
- **Thinking ON:** notes first, then the answer.
- **Thinking OFF:** the answer directly.

Our model, **Gemma-4-E4B**, has this switch. In code it is a setting like `enable_thinking=True` or `False`
(✅ checked on the Hugging Face model page, 2026-09-17; we will still test it ourselves in lesson 11).

---

## 3. Why do we need it? (in our thesis)

**The switch is the reason our thesis exists.**

- If thinking OFF is free and just as good → training is not worth it.
- If thinking ON is much more accurate but very long → there is room for something in between.

Our research question asks exactly this: **is training the model to think shorter better than just using the switch?**

All 5 ways of answering in our experiment are different ways of using thinking:

```text
                        thinking length
   0 ─────────────────────────────────────────────────▶ long

1. Thinking OFF          ●  (no thinking)
2. Thinking budget       ●━━━━━━━━━┫ stop at a limit
3. "Think briefly"       ●━━━━━━━━━━━━━?  (we ask in words; it may not listen)
4. Thinking ON           ●━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  (normal, often long)
5. ON + our LoRA         ●━━━━━━━━━━━━━?  (we hope: short, but still correct)
```

---

## 4. How does it work?

### 4.1 Thinking is just tokens, in a marked area

The model has no secret brain space. Thinking is **ordinary tokens**, written with the same loop (lessons 01–02).
The only difference: special marker tokens say **"thinking starts here"** and **"thinking ends here"**.

```text
[question] → <start thinking> t t t t t t t t t <end thinking> → answer tokens
                               └──── thinking tokens ────┘
                               this is what we count and want to shorten
```

For Gemma, the model page shows the real markers (✅ checked 2026-09-17):

```text
<|channel>thought
 ...thinking tokens...
<channel|>
 ...final answer...
```

- A chat website often **hides** or folds the thinking part.
- In our notebooks we **see and save all of it**, word for word (a project rule).

### 4.2 Why does thinking help?

The model can only "remember" what is **written in the text**.
Each new token is guessed by looking at **all the tokens before it**.

```text
Without thinking:  question ──────────────────────────────▶ answer
                   (must jump straight to the answer)

With thinking:     question → step 1 → step 2 → check → ▶ answer
                   (each step is written, so the next guess can use it)
```

*Everyday example:* multiplying 47 × 38 in your head vs. on paper.
On paper you write the in-between results, so each next step is easy.

### 4.3 Why can thinking be a waste?

Thinking helps on **hard** steps. On **easy** problems the model often still writes a lot:
repeating itself, checking the same thing again, "wait, let me reconsider…".
Every one of those tokens costs time. **That is overthinking** (next lesson).

### 4.4 How the switch works (the simple idea)

```text
Thinking ON:   the prompt lets the model open its thinking area → it writes notes → closes it → answers
Thinking OFF:  the prompt starts the answer directly → no thinking area
```

The exact format is set in the model's **chat template** (the rules that wrap our question in special tokens).

✅ **Gemma's model page says** (checked 2026-09-17):
- Thinking ON = the special token `<|think|>` is put at the start of the system prompt.
- Thinking OFF = that token is removed.
- In code, `enable_thinking=True` or `False` does this for us.

We still test it ourselves in lesson 11.

### 4.5 How a thinking budget works (our plan)

```text
1. Let the model think.
2. Count its thinking tokens.
3. At the limit (k tokens): stop it, close the thinking area ourselves.
4. Let it write the answer.
```

*Everyday example:* "Pens down on the scrap paper. Write your final answer now."
⚠️ How exactly we do this for Gemma is **not checked yet**. We set it up in the testing notebooks (Part 4).

### 4.6 What a paper found about OFF

The **NoThinking** paper (2504.09858, ✔ we checked the page) found:
skipping thinking can **beat** thinking with a small budget (under ~3,000 tokens), including on coding.
So thinking OFF is a **serious** rival, not an easy one to beat. That's why it is in our experiment.

---

## 5. Try it (free, 10 minutes)

1. Open a free chat site that has a **Thinking** button, for example **Qwen Chat**: https://chat.qwen.ai/
   (Qwen is the family of our backup model. You may need a free sign-in. Button names change over time.)
2. Turn thinking **OFF**. Ask: `Write a Python function that checks if a word is a palindrome.`
3. Turn thinking **ON**. Ask the same question in a **new** chat.
4. Compare:
   - How long did you wait?
   - How long is the thinking part?
   - Is the final code different?
5. Now ask with thinking ON: `What is 2 + 2?` → how much does it think for such an easy question?

**What you should notice:** thinking ON writes many more tokens, often for the same final code.
On the "2 + 2" question it may still think more than needed. That's overthinking.

---

## 6. ✅ Check yourself

**Q1.** What is a reasoning model?

<details><summary>Answer</summary>
An LLM trained to write thinking (notes to itself) before its final answer.
</details>

**Q2.** Is thinking a special hidden brain process?

<details><summary>Answer</summary>
No. Thinking is ordinary tokens written with the same loop, placed between special "start thinking" and "end thinking" markers.
</details>

**Q3.** Why can thinking make answers more correct?

<details><summary>Answer</summary>
Each new token is guessed by looking at all tokens written before. When the model writes in-between steps, later guesses can use them, like doing a hard sum on paper.
</details>

**Q4.** Why is the thinking switch so important for our thesis?

<details><summary>Answer</summary>
Because thinking OFF is a free way to be short. If OFF is as accurate as our trained model, training is not worth it. Testing that is our research question.
</details>

**Q5.** What is a thinking budget?

<details><summary>Answer</summary>
A limit on thinking tokens: at k tokens we stop the thinking and make the model write its answer.
</details>

---

## 7. You are here

```text
PART 1: What AI is → 01 ✅ → 02 ✅ → 03 ✅ → [04 ✅ Thinking] → 05 Overthinking → 06 Cutoffs
                                                  ↑ you just finished this
```

**Research chain:** you now understand the **EXPERIMENT** idea: 5 ways of using thinking on the same model.

**Explain-back test.** Lessons 02–06 are waiting for your explain-back. The full list of questions is at the end of [lesson 06](06-cutoff-dates.md#8-part-1-final-check-explain-it-back).
For this lesson:
Short answers are fine, one or two sentences each:
1. What is a token, and why do more tokens take more time?
2. How does a model learn, and what is fine-tuning?
3. What is "thinking" in a reasoning model, and why can it help?
4. What are our 5 ways of answering?

**Next:** [Lesson 05: Overthinking](05-overthinking.md).
