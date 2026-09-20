"""Download every problem ONCE and save them in one local file.

1. What problem does this solve?  Every run downloaded the benchmarks again and needed the
   internet. We want one file on this Mac with everything: the questions and their tests.
2. Why do we need it?  Faster starts, runs that work offline, and one place to look at or
   choose problems from.
3. What goes in?   HumanEval (easy, from evalplus) and LiveCodeBench (easy + medium, fresh).
4. What comes out? data/problems.json — one entry per problem, with the question we send to
   the model and everything the graders need.
5. Why this way?   The file is written once and only read afterwards, so a run can never
   change the problems under our feet. `data/` is not in git (the file is rebuildable).

Use:  ./.venv/bin/python scripts/build_problem_set.py
"""

import argparse, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

OUT = "data/problems.json"


def humaneval_problems():
    from evalplus.data import get_human_eval_plus
    out = []
    for task_id, p in get_human_eval_plus().items():
        out.append(dict(
            task_id=task_id, source="humaneval", difficulty="easy",
            title=p["entry_point"], run_as="function",
            question=("Complete this Python function. Answer with one Python code block only, "
                      "containing the complete function.\n\n```python\n" + p["prompt"] + "```"),
            entry_point=p["entry_point"], test=p["test"], n_tests=p["test"].count("assert"),
        ))
    return out


def lcb_problems():
    from lcb_data import load_problems, build_prompt
    out = []
    for p in load_problems():
        out.append(dict(
            task_id=p["task_id"], source="lcb", difficulty=p["difficulty"], title=p["title"],
            run_as=p["run_as"], question=build_prompt(p), func_name=p["func_name"],
            tests=p["tests"], n_tests=len(p["tests"]), contest_date=p["contest_date"],
        ))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=OUT)
    args = ap.parse_args()
    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    problems = humaneval_problems() + lcb_problems()
    with open(args.out, "w") as f:
        json.dump(dict(built="2026-09-20", problems=problems), f)

    size = os.path.getsize(args.out) / 1e6
    print(f"saved {len(problems)} problems to {args.out} ({size:.1f} MB)")
    for source in ("humaneval", "lcb"):
        rs = [p for p in problems if p["source"] == source]
        for diff in sorted({p["difficulty"] for p in rs}):
            n = sum(1 for p in rs if p["difficulty"] == diff)
            print(f"  {source:<10} {diff:<8} {n:>4} problems")


def load_all(path=OUT):
    """Read the saved problems. Used by the run scripts and the dashboard."""
    with open(path) as f:
        return json.load(f)["problems"]


if __name__ == "__main__":
    main()
