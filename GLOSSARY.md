# GLOSSARY: hard words in simple English

> Found a word you don't know? Look here first.
> Each word has a short meaning. Many also have an everyday example.
> Words are in A–Z order.
> When we use a new hard word in any doc, we add it here too.

---

## A

**Accuracy**
How many problems the model gets right, as a percentage.
*Example:* 80 right out of 100 = 80% accuracy.

**Adapter** → see **LoRA**.

**Append-only file**
A results file where we only **add** new lines at the end. We never change old lines.
*Example:* a diary. You write new pages. You never erase old ones.
Why: if the computer stops suddenly, the old results are still safe.

**arXiv** (say "archive")
A free website where researchers post their papers.
Every paper has a number, like `2502.20122`.

---

## B

**Baseline**
The normal way, which we compare our idea against.
Without something to compare with, "better" means nothing.
*Example:* to show a new medicine works, you compare it to people who got no medicine.

**Batch**
A group of items processed together, at the same time.
*Example:* washing 10 plates at once instead of one by one.

**Benchmark**
A fixed set of test problems that everyone uses, so results can be compared.
*Example:* a standard school exam that all schools use.
Ours: HumanEval+, MBPP+, LiveCodeBench.

**Budget (thinking budget)**
A limit on how long the model may think. When it reaches the limit, we stop its thinking.
*Example:* "you have 5 minutes of scrap paper, then write your answer."

---

## C

**Checkpoint**
A saved copy of the training, taken while training is running.
If the computer stops, we continue from the last saved copy.
*Example:* a save point in a video game.

**Colab** (Google Colab)
A free website from Google where you run Python code on a GPU in your browser.

**Contamination** ("the model has seen the test")
The test problems were already in the model's training text.
Then a good score may be memory, not skill.
*Example:* a student who saw the exam questions the night before.

**Coverage** (share of problems solved at least once)
We ask the model each problem 4 times. Coverage = the share of problems where
**at least one** of the 4 answers is correct.

**Cutoff date (training cutoff)**
The date when the model's training text ends. The model knows nothing after it.
Gemma-4-E4B's published cutoff is January 2025.

---

## D

**Dataset**
A collection of examples, such as code problems with their tests.

---

## E

**Epoch**
One full pass through all the training examples.
*Example:* reading your textbook once from start to end = 1 epoch.

**Error bar** (also: **confidence interval**)
A range that shows how sure we are about a number.
*Example:* "accuracy 80% ± 2" means the true value is probably between 78% and 82%.
Small error bar = we are sure. Big error bar = we are not sure.

---

## F

**Fine-tuning**
Taking a model that is already trained and training it a little more, to teach it a new habit.
*Example:* a trained cook takes a short course in baking.

**FLOPs**
A count of the small math steps (additions, multiplications) a computer does.
We use it to **estimate** how fast training will be.

---

## G

**Gap (research gap)**
A question that nobody has answered yet. A thesis must fill a gap.

**Gate (check)**
A test we do **before** the big work. If the test fails, we change the plan first.
*Example:* checking the car has fuel before a long trip.
We have two: the **memory check** and the **room-to-shorten check** (PLAN.md §7).

**Gemma-4-E4B**
Our main model, made by Google, released March 2026. It has a thinking ON/OFF switch.

**GPU**
A computer chip that does many math steps at the same time. AI models need it to run fast.
Ours is a free **T4** GPU with about 15 GB of memory.

**GPU-hour**
One GPU working for one hour.

**GRPO**
A type of **reinforcement learning** (see R). We do **not** use it. It is future work.

---

## H

**Headroom** → we now say **room to shorten**. See **R**.

**Hugging Face** (HF)
A free website that stores AI models and datasets. We download everything from there.

**Hypothesis**
A guess we write down **before** testing. The data can prove it wrong.

---

## K

**Kaggle**
A free website (like Colab) with free GPUs. It gives about 30 GPU-hours per week.
It can keep running when your browser is closed.

---

## L

**LLM** (Large Language Model)
A program that learned to guess the next piece of text from a huge amount of text.
See [lesson 01](lessons/01-what-is-an-llm.md).

**LoRA**
A cheap way to fine-tune. We don't change the whole model. We train a **small add-on**
that sits on top of it.
*Example:* instead of rewriting a whole book, you add sticky notes to some pages.
Good for us: it needs little GPU memory, and the original model stays unchanged.

---

## M

**Median**
The middle value when you sort numbers.
*Example:* lengths 100, 200, 900 → the median is 200.

**Memory (GPU memory, VRAM)**
The space on the GPU where the model and its work must fit.
A free T4 has about 15 GB. If it doesn't fit, the program crashes.

---

## O

**Overthinking**
Long thinking where short thinking would give the same answer. **This is our thesis problem.**

**Overlap check**
Making sure no test problem is also in the training data. If it is, we remove it from training.

---

## P

**Paired comparison**
We compare two ways of answering **on the same problems**.
*Example:* the same 100 students take a test before and after a course.
It is fairer than using different students, and we need fewer problems to see a small change.

**Paper**
A written report of a research study.

**pass@1** (first-try pass rate)
How often the model's first answer passes all the tests.
We ask 4 times and take the average, so the number is more stable.

**Policy** → we now say **way of answering**. See **W**.

**Prompt**
The text we give the model: the question plus any instructions.

---

## Q

**Quantization (4-bit, 16-bit)**
Squeezing the model's numbers so they use less memory.
16-bit = 2 bytes per number. 4-bit = half a byte per number.
*Example:* saving a photo as a smaller JPEG. A little less detail, much smaller file.

**Qwen3.5-4B**
Our backup model (from Alibaba, February 2026). We use it only if Gemma doesn't fit in memory.

---

## R

**Reasoning model**
An LLM that writes **thinking** (notes to itself) before its answer.

**Reinforcement learning (RL)**
Training by rewards: the model tries, gets points for good answers, and changes to get more points.
We do **not** use it. We use simple training on example answers instead.

**Room to shorten** (old name: headroom)
How much shorter the shortest correct answer is, compared with a normal correct answer.
If the shortest is about as long as normal, there is nothing to learn.
Our rule: the shortest must be at least 25% shorter (ratio ≤ 0.75).

**Resumable job** (a job that can stop and continue)
A job that saves its progress often. If the free session dies, the next session
continues where it stopped, instead of starting again.

---

## S

**Sandbox**
A safe, closed box where we run code the model wrote. If the code is bad, it can't harm anything.

**Seed (fixed seed)**
A starting number for randomness. The same seed gives the same "random" choices every time.
So anyone can repeat our run and get the same result.

**Session (free session)**
One period of using a free GPU. Colab and Kaggle end a session after about 12 hours, sometimes sooner.

**Shortest correct answer**
Our method. The model answers each problem 4 times. We keep the shortest answer that
passes the tests, and train on those.

**SFT** (supervised fine-tuning)
Training on example answers: "for this question, write this answer".
This is the kind of training we do.

---

## T

**T4**
The free GPU on Colab and Kaggle. It is a 16 GB card, and Colab shows 14.56 GB usable.
In our docs we round this to "a 15 GB GPU".

**Test set**
Problems used **only** to measure the model, never to train it.

**Thinking (thinking tokens)**
The notes a reasoning model writes before its answer. We count their length in tokens.

**Thinking switch (ON/OFF)**
A setting in some new models. ON = the model thinks first. OFF = it answers directly.

**Token**
A small piece of text, about ¾ of a word. Models read and write text token by token.
*Example:* "overthinking" might be 2 tokens: "over" + "thinking".
See [lesson 02](lessons/02-tokens.md).

**Tokenizer**
The tool that cuts text into tokens and gives each token an ID number. Every model has its own.

**Training data**
Examples the model learns from. They must never include test problems.

---

## U

**Unsloth**
Free software that makes fine-tuning faster and use less memory. It has ready notebooks for free GPUs.

**Unverified**
We have not checked it ourselves yet. We only read it somewhere, or calculated it.

---

## V

**vLLM**
Free software that makes the model write answers fast, by doing many prompts at the same time.

---

## W

**Way of answering** (old name: policy)
One setting for how the model answers. We test 5 of them:

```text
1. Thinking OFF             → answer directly
2. Thinking budget          → think, but stop at a limit
3. "Think briefly" prompt   → we ask it in words to think short
4. Thinking ON              → normal thinking (the usual way)
5. Thinking ON + our LoRA   → normal thinking, after our training
```
