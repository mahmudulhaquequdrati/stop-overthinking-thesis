# Lesson 09: Colab and Kaggle (free computers with GPUs)

⬅️ [Lesson 08](08-python-basics.md) · [ROADMAP](../ROADMAP.md) · ➡️ [Lesson 10: Hugging Face](10-hugging-face.md) · Hard word? See [GLOSSARY](../GLOSSARY.md)

---

## 1. In one sentence

**Google Colab and Kaggle lend you a computer with a free T4 GPU through your browser, for a limited time; we run all our notebooks there, for $0.**

---

## 2. What is it?

*Everyday example:* a **free library computer room**.
- You don't own the computer. You borrow it.
- You get a time slot. When it ends, the computer is wiped.
- Take your work home (save it to your own storage), or it's gone.

| | Google Colab (free) | Kaggle |
|---|---|---|
| Owner | Google | Google (Kaggle) |
| GPU | 1 × T4 when available | 1 × P100 **or** 2 × T4 |
| Session length | "at most 12 hours", often less | ~12 hours |
| Weekly limit | none published | ~30 GPU-hours per week |
| Runs with browser closed? | **No** (idle tab disconnects, ~90 min) | **Yes** ("Save & Run All") |
| Our use | 2nd worker + fixing bugs | **Main worker** |

(From our research notes, 2026-09-13. Colab's weekly limit and Kaggle's session length come from secondary sources, so they are not fully checked.)

⚠️ **Kaggle's P100 is not usable for us:** current PyTorch needs a newer GPU type (compute capability ≥ 7.0; the P100 is 6.0). **Always choose 2 × T4 on Kaggle.**

---

## 3. Why do we need it? (in our thesis)

- **$0 rule.** We can't pay for a GPU. These are the free options.
- **Big work, small slots.** Our work needs tens of GPU-hours, but a session is ~12 hours and can die early.
  So every job saves as it goes and can continue later (PLAN.md §11, lesson 08 "append").
- **Two free workers.** Kaggle (2 × T4) + Colab can run in parallel.

---

## 4. How does it work?

### 4.1 A session, start to end

```text
open notebook → choose GPU → connect → (install libraries) → run cells → SAVE results to Drive
                                                                              │
                     session ends (time up, idle, or crash) → computer wiped ─┘
                     next time: start again, the notebook skips finished work
```

**Everything not saved outside the session is lost**: downloaded model, installed libraries, results.
Libraries and the model can be downloaded again (it takes minutes). **Results must be saved.**

### 4.2 Colab: turning on the GPU

```text
colab.research.google.com → File → Upload notebook (or New notebook)
Runtime → Change runtime type → Hardware accelerator: T4 GPU → Save
Press "Connect" (top right)
```

Check the GPU in a code cell:

```text
!nvidia-smi
```

You should see **Tesla T4** and about **15 GB** of memory.

**Save to Google Drive** (your own free storage), so results survive the session:

```python
from google.colab import drive
drive.mount("/content/drive")      # a window asks for permission
# then save files under /content/drive/MyDrive/...
```

### 4.3 Kaggle: turning on the GPU

```text
kaggle.com → sign up (free) → verify your phone number (needed for GPU and internet)
Create → New Notebook
Right panel "Session options": Accelerator → GPU T4 × 2 ; Internet → On
```

⚠️ The phone-verification step and menu names come from common knowledge, not our research notes. Menus change; look for "Accelerator".

**Kaggle's superpower: "Save Version → Save & Run All (Commit)".**
Kaggle runs the whole notebook **by itself**, even with your browser closed, and keeps the output files.
That's why Kaggle is our main worker for long jobs.

### 4.4 Watching the free limits

- **Kaggle:** the GPU hours left this week are shown in your profile / notebook settings.
- **Colab:** no published weekly number. If you use a lot, Colab may give you no GPU for a while.
- Save results every ~20 problems (project rule), so a sudden end loses at most a few minutes.

### 4.5 One open question you can answer yourself (a real research check)

PLAN.md §11 has an unchecked item: **does a Kaggle session with 2 × T4 use 1 or 2 hours of the weekly limit per real hour?**
If 1 → two GPUs are "free speed". If 2 → no gain in quota.
How to check (costs ~15 minutes of quota): note the hours left → run a 2 × T4 session for 15 minutes → note the hours left again.

---

## 5. Try it (free, 20 minutes)

### Part A: Colab (5 minutes)
1. Open Colab, upload [`notebooks/08_python_basics.ipynb`](../notebooks/08_python_basics.ipynb) (if you haven't yet).
2. Runtime → Change runtime type → **T4 GPU**.
3. Add a code cell with `!nvidia-smi` and run it. Write down: GPU name, total memory.
4. **Runtime → Disconnect and delete runtime** when done (gives the GPU back; good for your limit).

### Part B: Kaggle (15 minutes)
1. Make a free Kaggle account and verify your phone.
2. Create a new notebook, set **GPU T4 × 2** and **Internet On**.
3. Run `!nvidia-smi`. You should see **two** T4s.
4. **Optional research check (§4.5):** note the quota before and after 15 minutes. Tell me the result; it goes into DECISIONS.
5. Stop the session when done.

---

## 6. ✅ Check yourself

**Q1.** Why must results be saved to Google Drive (or Kaggle output) during the run?

<details><summary>Answer</summary>
When the free session ends, the computer is wiped. Anything not saved outside it, including results, is lost.
</details>

**Q2.** Why is Kaggle our main worker, not Colab?

<details><summary>Answer</summary>
Kaggle's "Save & Run All" runs the notebook with the browser closed, and it gives 2 × T4 GPUs. Colab needs the browser tab open and gives one T4.
</details>

**Q3.** On Kaggle, why do we pick 2 × T4 and never the P100?

<details><summary>Answer</summary>
Current PyTorch needs GPU compute capability ≥ 7.0; the P100 is 6.0, so it doesn't work for us.
</details>

**Q4.** Our job needs 30 GPU-hours but a session is 12 hours. How do we do it?

<details><summary>Answer</summary>
The job is resumable: it saves results often, and the next session skips finished problems and continues.
</details>

---

## 7. You are here

```text
PART 2: The tools → 07 ✅ → 08 ✅ → [09 ✅ Colab/Kaggle] → 10 Hugging Face → 11 First model call
                                          ↑ you just finished this
```

**Research chain:** tools for **DATA/CODE**.

**Next:** [Lesson 10: Hugging Face](10-hugging-face.md).
