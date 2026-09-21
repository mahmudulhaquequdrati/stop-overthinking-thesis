"""Grade MBPP+ answers with MBPP+'s own tests, each in its own short-lived process.

1. What problem does this solve?  We must know which answers really work, judged by the
   benchmark's tests, never by eye.
2. Why do we need it?  The mini-thesis keeps the SHORTEST CORRECT answer, so "correct" must
   be right, or we would train the model on wrong code.
3. What goes in?   A .jsonl of answers from scripts/gen_colab.py, and data/mbpp.json.
4. What comes out? <answers>-graded.csv, the same columns as grade_humaneval.py, so
   check_gates.py and compare_mini.py read it the same way.
5. Why this way?   The same safety rule as the other graders (CLAUDE.md §4): the model's code
   runs in a separate process, in a temporary folder, with a time limit. The test program is
   MBPP+'s own `test` field (the harder "plus" tests).

Use:  python scripts/grade_mbpp.py --answers X.jsonl
      python scripts/grade_mbpp.py --check-official      # the grader must pass its own answers
"""

import argparse, csv, json, os, statistics, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from build_problem_set import load_all
from grade_humaneval import extract_code

TIMEOUT_SECONDS = 20        # some MBPP+ test programs are large


def run_one(code, problem, workdir):
    program = code + "\n\n" + problem["test"] + "\n"
    path = os.path.join(workdir, "candidate.py")
    with open(path, "w") as f:
        f.write(program)
    try:
        p = subprocess.run([sys.executable, "-I", path], cwd=workdir, timeout=TIMEOUT_SECONDS,
                           capture_output=True, text=True)
    except subprocess.TimeoutExpired:
        return False, "timeout"
    return p.returncode == 0, ("" if p.returncode == 0 else
                               (p.stderr.strip().split("\n")[-1][:200] or "crashed"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--answers")
    ap.add_argument("--problems", default="data/mbpp.json")
    ap.add_argument("--check-official", type=int, default=0, metavar="N",
                    help="grade the official solutions of the first N train problems instead")
    args = ap.parse_args()
    problems = {p["task_id"]: p for p in load_all(args.problems)}

    if args.check_official:
        chosen = [p for p in problems.values() if p["split"] == "train"][:args.check_official]
        with tempfile.TemporaryDirectory(prefix="grade-mbpp-") as wd:
            passed = sum(run_one(p["canonical_solution"], p, wd)[0] for p in chosen)
        print(f"grader sanity check: {passed}/{len(chosen)} official solutions pass "
              f"{'OK' if passed == len(chosen) else '<-- GRADER IS BROKEN, STOP'}")
        return

    rows = [json.loads(l) for l in open(args.answers)]
    out_csv = args.answers.replace(".jsonl", "-graded.csv")
    graded = []
    with tempfile.TemporaryDirectory(prefix="grade-mbpp-") as wd, open(out_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["policy", "task_id", "sample_index", "passed", "why_not",
                    "thinking_tokens", "total_new_tokens", "hit_limit"])
        for r in rows:
            ok, why = run_one(extract_code(r["answer_text"]), problems[r["task_id"]], wd)
            w.writerow([r["policy"], r["task_id"], r.get("sample_index", 0), ok, why,
                        r["thinking_tokens"], r["total_new_tokens"], r["hit_limit"]])
            graded.append((r, ok))

    passed = sum(ok for _, ok in graded)
    print(f"{os.path.basename(args.answers)}: passed {passed}/{len(graded)} "
          f"({100 * passed / len(graded):.0f}%) | median thinking "
          f"{statistics.median(r['thinking_tokens'] for r, _ in graded):.0f} tokens | "
          f"hit the limit {sum(r['hit_limit'] for r, _ in graded)}")
    print("saved", out_csv)


if __name__ == "__main__":
    main()
