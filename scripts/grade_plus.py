"""Grade function-style answers (HumanEval+, MBPP+) with the benchmark's own "plus" tests.

1. What problem does this solve?  We must know which answers really work, judged by the
   benchmark's harder "plus" tests, never by eye.
2. Why do we need it?  The real thesis reports HumanEval+ (plus tests); the mini-thesis and the
   training data use MBPP+. One grader for both, so they are judged the same way.
3. What goes in?   A .jsonl of answers from scripts/gen_colab.py, and the problems file that
   holds each problem's test program (data/problems.json or data/mbpp.json).
4. What comes out? <answers>-graded.csv (policy, task_id, sample_index, passed, why_not,
   thinking_tokens, total_new_tokens, hit_limit), read by check_gates, make_train_set and
   the compare scripts.
5. Why this way?   Same safety rule as every grader (CLAUDE.md §4): the model's code runs in a
   separate process, in a temporary folder, with a time limit. The test program is the
   benchmark's own: `test_plus` for HumanEval+, `test` for MBPP+. If the test program defines
   check(candidate), we call it with the problem's function (HumanEval style).

Use:  python scripts/grade_plus.py --answers X.jsonl --problems data/problems.json
      python scripts/grade_plus.py --check-official 20 --problems data/problems.json --source humaneval
"""

import argparse, csv, json, os, statistics, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from build_problem_set import load_all
from grade_humaneval import extract_code

TIMEOUT_SECONDS = 30        # plus-test programs can be large (up to ~0.5 MB)


def test_program(problem):
    test = problem.get("test_plus") or problem["test"]
    if "def check(" in test and problem.get("entry_point"):
        test += f"\n\ncheck({problem['entry_point']})\n"
    return test


def run_one(code, problem, workdir):
    path = os.path.join(workdir, "candidate.py")
    with open(path, "w") as f:
        f.write(code + "\n\n" + test_program(problem) + "\n")
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
    ap.add_argument("--source", default=None, help="--check-official only: which problems")
    ap.add_argument("--check-official", type=int, default=0, metavar="N",
                    help="grade the official solutions of the first N problems instead")
    args = ap.parse_args()
    problems = {p["task_id"]: p for p in load_all(args.problems)}

    if args.check_official:
        chosen = [p for p in problems.values() if "canonical_solution" in p
                  and (args.source is None or p["source"] == args.source)][:args.check_official]
        with tempfile.TemporaryDirectory(prefix="grade-plus-") as wd:
            results = [(p["task_id"], run_one(p["canonical_solution"], p, wd)) for p in chosen]
        bad = [(t, why) for t, (ok, why) in results if not ok]
        print(f"grader sanity check: {len(chosen) - len(bad)}/{len(chosen)} official solutions pass "
              f"{'OK' if not bad else '<-- GRADER IS BROKEN, STOP'}")
        for t, why in bad[:5]:
            print("   ", t, why)
        if bad:
            raise SystemExit(1)
        return

    rows = [json.loads(l) for l in open(args.answers)]
    out_csv = args.answers.replace(".jsonl", "-graded.csv")
    graded = []
    with tempfile.TemporaryDirectory(prefix="grade-plus-") as wd, open(out_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["policy", "task_id", "sample_index", "difficulty", "passed", "why_not",
                    "thinking_tokens", "total_new_tokens", "hit_limit"])
        for r in rows:
            ok, why = run_one(extract_code(r["answer_text"]), problems[r["task_id"]], wd)
            w.writerow([r["policy"], r["task_id"], r.get("sample_index", 0),
                        problems[r["task_id"]]["difficulty"], ok, why,
                        r["thinking_tokens"], r["total_new_tokens"], r["hit_limit"]])
            graded.append((r, ok))

    passed = sum(ok for _, ok in graded)
    print(f"{os.path.basename(args.answers)}: passed {passed}/{len(graded)} "
          f"({100 * passed / max(len(graded), 1):.0f}%) | median thinking "
          f"{statistics.median(r['thinking_tokens'] for r, _ in graded):.0f} tokens | "
          f"hit the limit {sum(r['hit_limit'] for r, _ in graded)}")
    print("saved", out_csv)


if __name__ == "__main__":
    main()
