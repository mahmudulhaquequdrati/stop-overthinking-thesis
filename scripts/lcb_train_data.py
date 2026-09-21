"""Older LiveCodeBench problems to TRAIN on: medium-style problems that are not in the test set.

1. What problem does this solve?  MBPP+ has only easy, short function problems. Our test set
   also has medium LiveCodeBench problems (read input, print output). A LoRA that never saw
   that kind of problem may not learn to think short on it.
2. Why do we need it?  The real thesis wants improvement on medium problems too (DECISIONS #66).
3. What goes in?   LiveCodeBench release v1 (`test.jsonl`): problems from 2023-05 to 2024-03.
4. What comes out? data/lcb_train.json: 40 easy + 40 medium problems, split "train", with the
   same fields as the test problems (question, tests, run_as, func_name), so gen_colab.py,
   grade_lcb.py and make_train_set.py work on them unchanged.
5. Why this way?   Our LiveCodeBench test problems are all from after 2025-01-31 (lcb_data.py).
   These are all from before that date, so they cannot be the same problems; overlap_check.py
   also compares their text. The pick is a fixed-seed shuffle, made before any answer exists.

Use:  python scripts/lcb_train_data.py
"""

import json, os, random, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import models
from lcb_data import FRESH_AFTER, build_prompt, load_problems

OUT = "data/lcb_train.json"
N_EACH = 40


def main():
    old = [p for p in load_problems(files=("test.jsonl",), fresh_only=False)
           if p["contest_date"] <= FRESH_AFTER]
    rng = random.Random(models.SEED)
    chosen = []
    for diff in ("easy", "medium"):
        ps = sorted((p for p in old if p["difficulty"] == diff), key=lambda p: p["task_id"])
        rng.shuffle(ps)
        chosen += ps[:N_EACH]

    problems = [dict(task_id=p["task_id"], source="lcb", difficulty=p["difficulty"],
                     split="train", title=p["title"], run_as=p["run_as"],
                     question=build_prompt(p), func_name=p["func_name"], tests=p["tests"],
                     n_tests=len(p["tests"]), contest_date=p["contest_date"]) for p in chosen]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(dict(built="2026-09-22", seed=models.SEED, problems=problems), f)
    dates = sorted(p["contest_date"] for p in problems)
    print(f"saved {len(problems)} old LiveCodeBench training problems to {OUT} "
          f"({sum(p['difficulty'] == 'easy' for p in problems)} easy, "
          f"{sum(p['difficulty'] == 'medium' for p in problems)} medium; dates {dates[0]} to {dates[-1]})")


if __name__ == "__main__":
    main()
