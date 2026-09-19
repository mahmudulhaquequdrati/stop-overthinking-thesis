# Q&A 19: The first model call (thinking ON vs OFF)

⬅️ [All Q&A](README.md) · Hard word? See [GLOSSARY.md](../GLOSSARY.md) · Lesson: [11 First model call](../lessons/11-first-model-call.md)

---

## 1. The step in 2 sentences

We wrote the first GPU notebook: load Gemma in 4-bit, ask one easy code question with thinking ON and OFF, count thinking tokens, save everything.
It is written but **not run yet**, because running it needs a free GPU session.

---

## 2. Questions a teacher may ask

**Q: What does this first run test?**
Four things: (1) the model loads and fits in memory, (2) the thinking switch really works, (3) we can count thinking tokens correctly, (4) how fast the free GPU really is.

**Q: How do you turn thinking on and off?**
`enable_thinking=True/False` in the chat template. Underneath, Gemma's template adds the special token `<|think|>` to the prompt when thinking is ON. Thinking is **OFF by default**, so we always set it on purpose.

**Q: How do you know the switch actually did something?**
The notebook prints both prompts and stops with an error if the ON prompt has no `<|think|>` token, or if the OFF prompt still has it. It also re-checks after the text is turned into tokens.

**Q: How do you count thinking tokens?**
Gemma writes the thinking between `<|channel>thought` and `<channel|>`. We count the model's own output tokens between those two markers. If the markers are missing, we count the thinking text again and say so.

**Q: Which settings did you use, and why the same for both?**
Gemma's recommended sampling: temperature 1.0, top_p 0.95, top_k 64; limit 4,096 new tokens; seeds fixed.
Everything is the same for ON and OFF, so the switch is the only difference. That is the rule for the real experiment too.

**Q: Why ask the same question more than once?**
The model is random, so lengths differ each time. Our real experiment asks 4 times and averages.

**Q: Why your own question, and not a HumanEval+ problem?**
So we don't shape our prompts or settings while looking at the test set. The test set stays untouched until the real experiment.

**Q: What do you save?**
One line per answer, appended to a file on Google Drive: ids, seed, settings, token counts, seconds, and the **raw answer word for word**. Re-counting later is then free; generating again would cost GPU hours.

---

## 3. Hard questions

**Q: Does this run measure accuracy?**
No. It does not grade anything, because grading means running the model's code, which may only happen in a sandbox (lesson 14). This run measures length, time and memory only.

**Q: You haven't run it. Isn't that weak?**
It is honest. The notebook is built from two checked sources: Gemma's model card and Unsloth's official notebook whose saved output shows a real free-T4 run.
If a cell fails, we write the error down and fix it. A failure is a finding, not a disaster.

**Q: One question, four answers. What can you conclude from that?**
Almost nothing about accuracy, and we don't claim anything. It is a working test of the setup (a "smoke test"), plus the first real speed and memory numbers.

**Q: What if the model writes 4,096 tokens and gets cut off?**
The record has `hit_limit: true`. In the real experiment we report how often each way of answering hits the limit, because a cut-off answer is usually a failed answer.

---

## 4. Checked vs. assumed

| We checked | We assume (until the run) |
|---|---|
| Gemma's card: `<\|think\|>` turns thinking on; thinking sits between `<\|channel>thought` and `<channel\|>` | That `enable_thinking` passes through Unsloth's chat template (the notebook checks it with an `assert`) |
| Gemma's recommended sampling settings | That the 4-bit model loads inside 15 GB in our own session |
| Unsloth's T4 run: 9.891 GB after loading | The writing speed (tokens per second) on a free T4 |
| The notebook's Python has no syntax errors | |

---

## 5. Where it is written

- [lessons/11-first-model-call.md](../lessons/11-first-model-call.md) · [notebooks/11_first_model_call.ipynb](../notebooks/11_first_model_call.ipynb)
- [research/2026-09-17-part2-tool-checks.md](../research/2026-09-17-part2-tool-checks.md)
- [DECISIONS.md](../DECISIONS.md) rows #37, #38, #39
