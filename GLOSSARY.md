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

**Assert**
A line in a notebook that says "stop with an error if this is not true". We use it to check the thinking switch really worked.

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

**bf16, float16, float32** (number formats)
Ways to store one number in the computer. bf16 and float16 use 2 bytes; float32 uses 4 bytes.
The free T4 GPU **cannot compute in bf16**, so the loader converts some parts to float16.
Risk: float16 cannot hold very big numbers. If one "overflows", the model can write garbage
(like `!!!!!!`). float32 cannot overflow, but it needs twice the memory and is slower. Notebook 12
compares the two on 10 problems before trusting float16 (DECISIONS #59).
*Example:* the same price written as "€1.50" or "1 euro 50 cents": the same value, a different way to write it, a different amount of space.

---

## C

**Compute unit** (Colab)
What paid Colab time is counted in. The A100 costs **5.3 units per hour**, even when it sits idle.
We have 69 units for the whole thesis (DECISIONS #65).

**Cell**
One block in a notebook: a text cell (explanation) or a code cell (Python you can run with Shift+Enter).

**Chat template**
The rules that wrap our question in special tokens before the model reads it. It also decides if thinking is ON or OFF.

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
Gemma-4-E4B's published cutoff is January 2025 (for its pre-training data; checked on the model card).
See [lesson 06](lessons/06-cutoff-dates.md).

**CPU memory** (also: **RAM**)
The computer's normal memory, separate from the GPU's memory. Slower for the model's math, but often bigger.
Free Colab has about 12.7 GB; Kaggle about 29 GB (not checked yet).

---

## D

**Colab / Kaggle** → see **Colab** and **KV cache**
The notes the model keeps about every token written so far, so it doesn't redo work. It grows with the answer, and it uses GPU memory.

**Kaggle**.

**Dataset**
A collection of examples, such as code problems with their tests.

---

## E

**Drive (Google Drive)**
Your own free online storage. We save results there, so they survive when a free session ends.

**Epoch**
One full pass through all the training examples.
*Example:* reading your textbook once from start to end = 1 epoch.

**Error bar** (also: **confidence interval**)
A range that shows how sure we are about a number.
*Example:* "accuracy 80% ± 2" means the true value is probably between 78% and 82%.
Small error bar = we are sure. Big error bar = we are not sure.

**Error score** (also: **loss**)
During training: how wrong the model's guess was. Big = very wrong. Training tries to make it smaller.
See [lesson 03](lessons/03-how-a-model-learns.md).

---

## F

**Fast path**
The quick code for Qwen3.5's special layers. It needs two extra libraries (`flash-linear-attention`, `causal-conv1d`).
Without them the model still works, but runs slow backup code. Notebook 14 builds them once and keeps them on Drive.

**Fresh problem**
A test problem published **after** the model's cutoff date, so the model cannot have seen it.

**Fine-tuning**
Taking a model that is already trained and training it a little more, to teach it a new habit.
*Example:* a trained cook takes a short course in baking.

**FLOPs**
A count of the small math steps (additions, multiplications) a computer does.
We use it to **estimate** how fast training will be.

**Forgetting**
When fine-tuning damages skills the model had before. LoRA lowers this risk.

---

## G

**Gated (model or dataset)**
You must accept a form before downloading. Gemma-4-E4B and our datasets are **not** gated (checked).

**Gap (research gap)**
A question that nobody has answered yet. A thesis must fill a gap.

**Gate (check)**
A test we do **before** the big work. If the test fails, we change the plan first.
*Example:* checking the car has fuel before a long trip.
We have two: the **memory check** and the **room-to-shorten check** (PLAN.md §7).

**Go / no-go test**
A small, cheap test that decides whether to go on with a big, expensive plan.
*Example:* testing one dish on friends before you open a restaurant.
Ours is notebook 12: it runs free, and only if it passes do we spend money (DECISIONS #59).

**Gemma-4-E4B**
Our **old** main model, made by Google, released March 2026. It has a thinking ON/OFF switch.
We stopped using it on 2026-09-20 because it did not fit on a free Colab GPU (DECISIONS #53).

**Qwen3.5-2B**
Our main model since 2026-09-20. Made by Alibaba, released February 2026. It also has a
thinking ON/OFF switch. We chose it because it is small: about 4.5 GB, so the **whole model
fits on a free Colab GPU** and does not have to be split. Its weak point: Alibaba never said
when its training data stops, so we cannot prove it never saw our test problems.

**GPU**
A computer chip that does many math steps at the same time. AI models need it to run fast.
Ours is a free **Split**
A named part of a dataset, like `train` or `test`. HumanEval+ has one split: `test` (164 problems).

**T4** GPU with about 15 GB of memory.

**GPU-hour**
One GPU working for one hour.

**GRPO**
A type of **reinforcement learning** (see R). We do **not** use it. It is future work.

**GGUF**
A file format for models that the program **llama.cpp** reads. It squeezes the whole model, including big word tables.
Our Gemma-4-E4B as GGUF (Q4_K_M) is 4.98 GB; as bnb-4bit it is 10.95 GB.

---

## H

**Headroom** → we now say **room to shorten**. See **R**.

**Hugging Face** (HF)
A free website that stores AI models and datasets. We download everything from there.

**hf_hub_download**
A one-line way to download a single file from Hugging Face. We use it for LiveCodeBench.

**Hypothesis**
A guess we write down **before** testing. The data can prove it wrong.

**Hook**
A small piece of code that runs automatically just before or after one part of the model.
We use two hooks to move data between CPU memory and the GPU (notebook 11).

---

## K

**Kaggle**
A free website (like Colab) with free GPUs. It gives about 30 GPU-hours per week.
It can keep running when your browser is closed.

---

## L

**Learning curve**
Train the same way on more and more data (25%, 50%, 100%) and test each time.
If results still get better at the end, more data should help. If they stop changing, it won't.
*Example:* a runner timing themselves after 1, 2 and 4 weeks of practice. If 2→4 weeks still
helped a lot, keep practising; if not, practice more of the same won't help.
We use it in the mini-thesis (notebook 13, DECISIONS #60).

**Learning rate**
How big each nudge to the model's numbers is during training. Too big → it breaks. Too small → it learns very slowly.

**LLM** (Large Language Model)
A program that learned to guess the next piece of text from a huge amount of text.
See [lesson 01](lessons/01-what-is-an-llm.md).

**Loop (repetition loop)**
When the model writes the same lines again and again and never finishes.
*Example:* a student who keeps writing "wait, let me check again" until the exam time ends.
In our real run, most answers that hit the token limit were loops (results/2026-09-24-thesis-run.md).

**LoRA**
A cheap way to fine-tune. We don't change the whole model. We train a **small add-on**
that sits on top of it.
*Example:* instead of rewriting a whole book, you add sticky notes to some pages.
Good for us: it needs little GPU memory, and the original model stays unchanged.

**Loss** → see **Error score**.

**Loss curve**
A chart of the error score during training, step by step. Going down = the model is learning its
training examples. It does **not** tell you whether those examples teach the right thing.
*Example:* LoRA-2's loss went down, but its examples taught long thinking (FULL-RESULTS §13).

**llama.cpp**
A free program that makes a model write answers fast, also many at once. It runs on NVIDIA GPUs and reads GGUF files.
We plan to test it for writing answers (DECISIONS #47).

---

## M

**load_dataset**
A one-line way to download and open a dataset from Hugging Face.

**MBPP+**
378 easy Python problems, each with real tests (the "+" means extra, harder tests).
We cut it from our final test set, so we use it for the mini-thesis instead: 50 to train on,
50 other ones to test on (DECISIONS #60, #62).

**Mini-thesis**
The whole method, run once, small and free: answer, keep the shortest correct answer, train a
LoRA, test. It shows whether training works at all before we spend a week on it (notebook 13).

**Median**
The middle value when you sort numbers.
*Example:* lengths 100, 200, 900 → the median is 200.

**Memory (GPU memory, VRAM)**
The space on the GPU where the model and its work must fit.
A free T4 has about 15 GB. If it doesn't fit, the program crashes.

**Mixture of experts (MoE)**
A model built from many small "expert" parts, where only a few are used for each token.
*Example:* a hospital with 128 doctors, where each patient only sees 8. Gemma-4-26B-A4B works like this.

---

## O

**Notebook**
A page of cells you run step by step in the browser (Colab, Kaggle). Our experiments are notebooks.

**Overthinking**
Long thinking where short thinking would give the same answer. **This is our thesis problem.**
See [lesson 05](lessons/05-overthinking.md).

**Overlap check**
Making sure no test problem is also in the training data. If it is, we remove it from training.

**Offload**
Putting part of a model in CPU memory instead of on the GPU, to save GPU memory.
We offload Gemma's per-layer word table (DECISIONS #43).

**Out of memory** (also: **OOM**)
The error you get when something must be put on the GPU but there is no room left. The program stops.

---

## P

**Paired comparison**
We compare two ways of answering **on the same problems**.
*Example:* the same 100 students take a test before and after a course.
It is fairer than using different students, and we need fewer problems to see a small change.

**pip**
The free installer for Python libraries. In a notebook: `!pip install datasets`.

**Paper**
A written report of a research study.

**Parameters** (also: **weights**)
The numbers inside the model. Gemma-4-E4B has 8.0 billion. Learning = changing these numbers.
*Example:* 8 billion small knobs on a huge mixing desk.

**pass@1** (first-try pass rate)
How often the model's first answer passes all the tests.
We ask 4 times and take the average, so the number is more stable.

**Policy** → we now say **way of answering**. See **W**.

**Pre-training**
The first, giant stage of training: the model reads huge amounts of text and learns to guess the next token. Done by big companies, not by us.

**Python**
The programming language all our notebooks use. See [lesson 08](lessons/08-python-basics.md).

**Prompt**
The text we give the model: the question plus any instructions.

**Per-layer word table**
A special big table in Gemma's small "E" models. For every word, it holds a small piece of information for each of the 42 layers.
It is 5.25 GB and stays 16-bit even in the "4-bit" model. It caused our first out-of-memory crash (qa/20).

---

## Q

**Quantization (4-bit, 16-bit)**
Squeezing the model's numbers so they use less memory.
16-bit = 2 bytes per number. 4-bit = half a byte per number.
*Example:* saving a photo as a smaller JPEG. A little less detail, much smaller file.

**Qwen3.5-4B**
Our backup model (from Alibaba, February 2026). The bigger brother of Qwen3.5-2B. We use it
only if the 2B turns out to be too weak at code.

---

## R

**Reasoning model**
An LLM that writes **thinking** (notes to itself) before its answer.
See [lesson 04](lessons/04-reasoning-models-and-thinking.md).

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

**Smoke test**
A tiny first run that only checks that everything **works**, not how good the answers are.
*Example:* turning a new oven on for a minute before baking. Notebook 14 runs every way on 2 problems first.

**Special token**
A token with a job, not normal text. For example: "thinking starts here", "thinking ends here", "I'm done".

**safetensors**
The file format that stores a model's numbers on Hugging Face.

**Sampling (temperature, top_p, top_k)**
Settings that decide how random the model's writing is. Qwen's recommended values for code:
temperature 0.6, top_p 0.95, top_k 20. We use the same ones everywhere, for every way of
answering, so only the thing we are testing changes. *(Before 2026-09-20 we used Gemma's
values: 1.0 / 0.95 / 64. See DECISIONS #55.)*

**Thinking markers**
The little tags a model puts around its thinking, so a program can find where it starts and
stops. Every model uses different ones. Qwen uses `<think>` and `</think>`; our old model used
`<|channel>` and `<channel|>`. **This matters more than it looks.** Qwen writes its opening
`<think>` into the *question*, not into the answer, so a program that hunts for it in the answer
finds nothing and reports "0 thinking tokens" without any error. That would have made every
number in this thesis wrong (DECISIONS #56).

**Room to shorten**
The shortest correct answer divided by the average correct answer. If the model solves a problem
4 times and the answers are 400, 800, 900 and 1,100 tokens long, the room to shorten is
400 ÷ 800 = 0.5 — the short one is half the length, so there is a lot to cut. Our rule
(PLAN.md §7): it must be **0.75 or less**. *This is the number that answers "will training
really make the model write less?"* If every correct answer is the same length, there is nothing
to learn from.

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

**Training**
Teaching a model: it guesses the next token, sees the right one, and its numbers get a tiny nudge. Repeated for all examples.
See [lesson 03](lessons/03-how-a-model-learns.md).

**TARGET** (in the mini-thesis)
How short our training answers are, compared with a normal correct answer. 0.70 means 30% shorter.
A LoRA can't be expected to cut more than its examples show, so we compare the LoRA's result with it.
Printed by `scripts/make_train_set.py`.

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
We don't use it for the thesis runs yet (DECISIONS #57: a bug with LoRA add-ons). Notebook 12
only tests whether it runs, and how fast, before we decide anything (DECISIONS #59).

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
