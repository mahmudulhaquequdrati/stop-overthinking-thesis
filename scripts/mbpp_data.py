"""MBPP+ problems for the mini-thesis: 100 to train on, 100 OTHER ones to test on.

1. What problem does this solve?  Before a week of GPU time, we want one small run of the
   WHOLE method (answer -> keep shortest correct -> train LoRA -> test) on a free T4.
   It needs easy problems with real tests that are NOT in our thesis test set.
2. Why do we need it?  HumanEval and LiveCodeBench are the final test set (DECISIONS #58).
   Training on them, or choosing anything from their results, would make the final test
   unfair (CLAUDE.md §4). MBPP+ was cut from the test set on 2026-09-20, so it is free to use.
3. What goes in?   The Hugging Face dataset `evalplus/mbppplus` (378 easy problems).
4. What comes out? data/mbpp.json: every problem with its question, its test program, the
   official solution, and its split: "train" (100), "test" (100) or "unused" (178).
5. Why this way?   The split is a fixed-seed shuffle, made before any answer is seen, so we
   cannot pick easy test problems by accident. The `test` field is MBPP+'s own complete
   test program (the harder "plus" tests), so we never write tests ourselves.

Use:  python scripts/mbpp_data.py
"""

import json, os, random, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import models

OUT = "data/mbpp.json"
N_TRAIN, N_TEST = 100, 100


def question_text(p):
    """What the model sees. One example test shows the function name and how it is called,
    which is how MBPP is normally asked."""
    return (f"{p['prompt'].strip()}\n\nYour code must pass this test:\n```python\n"
            f"{p['test_list'][0]}\n```\n\nAnswer with one Python code block only, "
            f"containing the complete function.")


def build():
    from datasets import load_dataset
    ds = load_dataset("evalplus/mbppplus")
    rows = list(ds[list(ds.keys())[0]])            # the dataset has one split

    ids = sorted(r["task_id"] for r in rows)
    random.Random(models.SEED).shuffle(ids)
    split = {t: "train" for t in ids[:N_TRAIN]}
    split.update({t: "test" for t in ids[N_TRAIN:N_TRAIN + N_TEST]})

    problems = []
    for r in rows:
        problems.append(dict(
            task_id=f"Mbpp/{r['task_id']}", source="mbpp", difficulty="easy",
            split=split.get(r["task_id"], "unused"), question=question_text(r),
            test="\n".join(r["test_imports"]) + "\n\n" + r["test"],
            canonical_solution=r["code"],
        ))
    return problems


def main():
    problems = build()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(dict(built="2026-09-22", seed=models.SEED, problems=problems), f)
    for s in ("train", "test", "unused"):
        print(f"  {s:<7} {sum(p['split'] == s for p in problems):>4} problems")
    overlap = ({p["task_id"] for p in problems if p["split"] == "train"} &
               {p["task_id"] for p in problems if p["split"] == "test"})
    print(f"train/test overlap: {len(overlap)} problems {'OK' if not overlap else '<-- STOP'}")
    print("saved", OUT)


if __name__ == "__main__":
    main()
