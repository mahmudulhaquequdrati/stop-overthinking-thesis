# Teacher Q&A: what we did, and why

> **What is this folder?** One file for each step of the thesis.
> Each file has the questions a teacher may ask, with short, simple answers.
>
> **When do we write one?** At the end of every step. No step is finished without its Q&A file.
>
> Hard word? See [GLOSSARY.md](../GLOSSARY.md).

---

## 1. How to use it before a meeting

1. Open the files for the steps you will talk about.
2. Cover the answers. Read only the question.
3. Say your answer out loud, in your own words.
4. Then check the written answer.
5. Practice the **"Hard questions"** part most. Examiners like those.

---

## 2. Every file has the same parts

| Part | What it gives you |
|---|---|
| **The step in 2 sentences** | What we did, very short |
| **Questions a teacher may ask** | Simple answers: what, why, what else we could do, why not that |
| **Hard questions** | Tricky questions, with honest answers |
| **Checked vs. assumed** | What we really checked, and what we only believe for now |
| **Where it is written** | Links to DECISIONS, PLAN and research notes |

---

## 3. The steps so far

| # | Step | Date |
|---|---|---|
| [01](01-choosing-the-topic.md) | Choosing the topic | 2026-09-13 |
| [02](02-finding-the-gap.md) | Finding the gap (what nobody did yet) | 2026-09-13 |
| [03](03-code-only-easy-and-medium.md) | Code only, easy + medium problems only | 2026-09-13 |
| [04](04-choosing-the-model.md) | Choosing the model | 2026-09-13 |
| [05](05-data-and-test-size.md) | Choosing the data, and how many test problems | 2026-09-13 |
| [06](06-method-hypothesis-baselines.md) | The method, the hypothesis, and what we compare against | 2026-09-13 |
| [07](07-one-question-only.md) | Cutting the thesis to one question | 2026-09-13 |
| [08](08-safety-checks-before-training.md) | The two checks before the big runs | 2026-09-13 |
| [09](09-gpu-time-and-free-sessions.md) | GPU time, and working with free 12-hour sessions | 2026-09-17 |
| [10](10-proposal-and-title.md) | The proposal and the title | 2026-09-13 |
| [11](11-measuring-thinking-in-tokens.md) | Measuring thinking length in tokens (lesson 02) | 2026-09-17 |
| [12](12-how-our-training-works.md) | How our training works: fine-tuning (lesson 03) | 2026-09-17 |
| [13](13-thinking-and-the-switch.md) | Reasoning models, thinking, and the ON/OFF switch (lesson 04) | 2026-09-17 |
| [14](14-overthinking.md) | Overthinking: our problem, and how to measure it (lesson 05) | 2026-09-17 |
| [15](15-cutoff-dates-and-seen-tests.md) | Cutoff dates, and "has the model seen the test?" (lesson 06) | 2026-09-17 |
| [16](16-gpu-memory.md) | GPU memory: does the model fit? (lesson 07) | 2026-09-17 |
| [17](17-free-gpus-and-notebooks.md) | Free GPUs and notebooks: Colab, Kaggle, Python (lessons 08–09) | 2026-09-17 |
| [18](18-hugging-face-and-our-data.md) | Hugging Face, and checking our data (lesson 10) | 2026-09-17 |
| [19](19-first-model-call.md) | The first model call: thinking ON vs OFF (lesson 11) | 2026-09-17 |
| [20](20-first-model-load-out-of-memory.md) | The first model load ran out of memory, and the fix | 2026-09-19 |
| [21](21-first-real-numbers.md) | The first real numbers: thinking ON vs OFF, and the speed problem | 2026-09-20 |
| [22](22-pilot-on-the-mac.md) | The pilot on the Mac: 30 real problems, and what it changed | 2026-09-20 |
| [23](23-moving-to-colab-and-qwen.md) | Moving to Google Colab, and changing the model to Qwen3.5-2B | 2026-09-20 |
| [24](24-free-go-no-go-test.md) | The free "go / no-go" test, before any money is spent | 2026-09-21 |
| [25](25-mini-thesis-and-learning-curve.md) | The mini-thesis, and how we'll know if more training data helps | 2026-09-22 |
| [26](26-mini-thesis-results.md) | The mini-thesis results: training worked on easy problems | 2026-09-22 |
| [27](27-the-real-thesis-run.md) | The real thesis run (notebook 14): the rules, fixed before the run | 2026-09-22 |
| [28](28-thesis-run-results.md) | The real thesis run: the results, and what they mean | 2026-09-25 |

**What has been run:** notebooks 08 and 10 (no GPU needed). Notebook 11 ran out of memory on Colab ([qa/20](20-first-model-load-out-of-memory.md)), then **ran on Kaggle** (2026-09-19): it works, but it writes only ~4.4 tokens per second ([qa/21](21-first-real-numbers.md)). A pilot on the user's Mac then solved 30 real problems ([qa/22](22-pilot-on-the-mac.md)), but medium problems took 250 seconds each, so on 2026-09-20 everything moved to Google Colab with a smaller model ([qa/23](23-moving-to-colab-and-qwen.md)).
**Next:** notebook 14 ran on the A100 (2026-09-24). LoRA-2 did not think shorter; a plain thinking limit did best, because most long answers are loops ([qa/28](28-thesis-run-results.md)). Next: write the results and analysis chapter.
