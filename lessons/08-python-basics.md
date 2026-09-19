# Lesson 08: Python basics (just enough to read our notebooks)

⬅️ [Lesson 07](07-gpu-memory.md) · [ROADMAP](../ROADMAP.md) · ➡️ [Lesson 09: Colab and Kaggle](09-colab-and-kaggle.md) · Hard word? See [GLOSSARY](../GLOSSARY.md)

---

## 1. In one sentence

**Python is the programming language all our notebooks use; you don't need to be a programmer, you only need to read 8 simple building blocks.**

---

## 2. What is it?

**Python** is a language for giving a computer instructions, written in almost-English.
Almost all AI tools (Hugging Face, Unsloth, PyTorch) are used from Python.

*Everyday example:* a recipe. Each line is one instruction, done from top to bottom.

```python
eggs = 2                # take 2 eggs
print("Mix", eggs, "eggs")   # say what you do
```

Lines starting with `#` are **comments**: notes for humans. The computer ignores them.

---

## 3. Why do we need it? (in our thesis)

- Every step of the experiment is a **notebook** full of Python: load the model, ask questions, count tokens, save results.
- The project rule says: **learn before doing**. So you must be able to **read** what each cell does before running it.
- A teacher may point at code and ask "what does this line do?".

You will **not** write big programs. We write them together; you read and run them.

---

## 4. How does it work? The 8 building blocks

### Block 1: a value with a name (variable)

```python
model_name = "gemma-4-E4B"
max_tokens = 8000
print(model_name, max_tokens)     # shows: gemma-4-E4B 8000
```

A **variable** is a label on a box. `=` means "put this value in the box".

### Block 2: kinds of values

| Kind | Example | Used for |
|---|---|---|
| number | `3500`, `0.75` | limits, ratios |
| text (string) | `"thinking ON"` | questions, answers |
| True/False | `True` | switches, like `enable_thinking=True` |

### Block 3: a list (many values in order)

```python
lengths = [2400, 1200, 3000, 1800]   # thinking tokens of 4 tries
print(lengths[0])                     # first item → 2400  (counting starts at 0!)
print(len(lengths))                   # how many → 4
print(min(lengths))                   # smallest → 1200
```

### Block 4: a dictionary (values with names)

```python
result = {"problem_id": "HumanEval/0", "thinking_tokens": 1200, "passed": True}
print(result["thinking_tokens"])      # → 1200
```

*Everyday example:* a form with fields: name → value.
Our saved results are dictionaries like this, one per answer.

### Block 5: a loop (do it again for each item)

```python
for tries in lengths:
    print("this try used", tries, "tokens")
```

The **indented** lines (4 spaces) belong to the loop. Indentation matters in Python.

### Block 6: if (decide)

```python
ratio = 1200 / 1800
if ratio <= 0.75:
    print("room to shorten ✅")
else:
    print("little room to shorten")
```

### Block 7: a function (a named recipe you can reuse)

```python
def room_to_shorten(correct_lengths):
    return min(correct_lengths) / (sum(correct_lengths) / len(correct_lengths))

print(room_to_shorten([2400, 1200, 1800]))   # → 0.666...
```

- `def` = "define a recipe". What's in brackets goes **in**. `return` gives the result **out**.
- In our notebooks you'll see calls to functions from libraries, like `model.generate(...)`.

### Block 8: import and install (use other people's code)

```python
import json                  # use Python's built-in JSON tool
from datasets import load_dataset   # use a function from the "datasets" library
```

In a notebook, a line starting with `!` runs a command outside Python, for example installing a library:

```text
!pip install datasets
```

**pip** is the free app store for Python libraries.

### Bonus: how our results are saved (JSON lines)

```python
import json
with open("results.jsonl", "a") as f:        # "a" = append: only ADD to the end, never overwrite
    f.write(json.dumps(result) + "\n")        # one result = one line of text
```

This is the "results file we only add to" from PLAN.md §11.

### What is a notebook?

A **notebook** is a page with **cells**:
- **Text cells** explain (in our notebooks: the 5 code questions).
- **Code cells** run Python. Press ▶ (or Shift+Enter) to run one. The output appears under it.
- Cells run **in the order you press them**. Values stay in memory until the session ends.

---

## 5. Try it (free, 15 minutes)

1. Open https://colab.research.google.com (sign in with a Google account). No GPU needed for this.
2. **File → Upload notebook** → choose [`notebooks/08_python_basics.ipynb`](../notebooks/08_python_basics.ipynb) from this project.
3. Run each cell from top to bottom with **Shift+Enter**.
4. Change numbers and run again. Example: in the room-to-shorten cell, change the lengths and see if the result changes from ✅.
5. Break something on purpose: remove the 4 spaces before `print` inside the loop and run. Read the error. Put the spaces back.

**What you should notice:** each cell does one small thing, and you can read what it does. Errors are normal and tell you where the problem is.

---

## 6. ✅ Check yourself

**Q1.** What does this print?
```python
lengths = [900, 1500, 600]
print(lengths[1])
```
<details><summary>Answer</summary>
1500. Counting starts at 0, so index 1 is the second item.
</details>

**Q2.** What does `result["passed"]` give for `result = {"passed": False, "tokens": 700}`?
<details><summary>Answer</summary>
False.
</details>

**Q3.** Why do we open the results file with `"a"` and not `"w"`?
<details><summary>Answer</summary>
"a" (append) adds to the end and keeps old results. "w" (write) would erase the file first. If a free session dies, appending keeps everything saved so far.
</details>

**Q4.** What does `!pip install datasets` do?
<details><summary>Answer</summary>
It installs the free "datasets" library into the notebook's computer, so the code can use it.
</details>

---

## 7. You are here

```text
PART 2: The tools → 07 ✅ GPU memory → [08 ✅ Python] → 09 Colab/Kaggle → 10 Hugging Face → 11 First model call
                                            ↑ you just finished this
```

**Research chain:** tools for **DATA/CODE**.

**Next:** [Lesson 09: Colab and Kaggle](09-colab-and-kaggle.md).
