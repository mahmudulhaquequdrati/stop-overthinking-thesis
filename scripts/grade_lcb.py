"""Grade LiveCodeBench answers, each in its own short-lived process.

1. What problem does this solve?  These problems are not graded like HumanEval. Most of
   them are whole programs that read input and print an answer; the rest are one method
   of a class that is called with arguments.
2. Why do we need it?  They are the "medium" half of our test set (PLAN §3).
3. What goes in?   A .jsonl of answers (task_id + answer_text) and the problems.
4. What comes out? <answers>-graded.csv, one row per answer, plus a printed summary.
5. Why this way?   Same safety rule as scripts/grade_humaneval.py: the model's code runs in
   a separate process, in a temporary folder, with a time limit (CLAUDE.md §4). The tests
   come from the benchmark itself.

An answer passes only if it passes EVERY test of that problem, which is how LiveCodeBench
counts it.
"""

import argparse, csv, json, os, re, statistics as st, subprocess, sys, tempfile

from lcb_data import load_problems

FENCE = re.compile(r"```(?:python)?\s*\n(.*?)```", re.S)
TIMEOUT_SECONDS = 20        # these problems are bigger than HumanEval's


def extract_code(answer_text):
    blocks = FENCE.findall(answer_text)
    if blocks:
        return blocks[-1]
    if "```python" in answer_text:      # cut off by the token limit
        return answer_text.split("```python", 1)[1]
    return answer_text


def _driver_for_function(func_name):
    """A small program that reads the test arguments, calls the method, prints the result."""
    return f'''
import json, sys
_args = [json.loads(line) for line in sys.stdin.read().split("\\n") if line.strip()]
print(json.dumps(Solution().{func_name}(*_args)))
'''


def same_answer(got, expected, run_as):
    if run_as == "stdin":
        clean = lambda s: "\n".join(line.rstrip() for line in s.strip().split("\n"))
        return clean(got) == clean(expected)
    try:                                  # compare as data, so [1,2] == [1, 2]
        return json.loads(got) == json.loads(expected)
    except (json.JSONDecodeError, ValueError):
        return got.strip() == expected.strip()


def run_one(code, problem, workdir, show=False):
    """Returns (passed, why_not, details). `details` has one entry per test that was run,
    so a report can show the input, what was wanted, and what the code printed."""
    program = code if problem["run_as"] == "stdin" else code + _driver_for_function(problem["func_name"])
    path = os.path.join(workdir, "candidate.py")
    with open(path, "w") as f:
        f.write(program)
    details = []
    for i, test in enumerate(problem["tests"], 1):
        try:
            p = subprocess.run([sys.executable, "-I", path], cwd=workdir, input=test["input"],
                               capture_output=True, text=True, timeout=TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired:
            details.append(dict(n=i, ok=False, input=test["input"][:400],
                                want=test["output"][:200], got="(took too long)"))
            return False, f"timeout on test {i}", details
        ok = p.returncode == 0 and same_answer(p.stdout, test["output"], problem["run_as"])
        details.append(dict(n=i, ok=ok, input=test["input"][:400], want=test["output"][:200],
                            got=(p.stdout[:200] if p.returncode == 0 else
                                 "ERROR: " + (p.stderr.strip().split("\n")[-1][:200] or "crashed"))))
        if show:
            one = lambda s, n=70: " ".join(str(s).split())[:n]
            print(f"      test {i:>2} {'PASS' if ok else 'FAIL'} | in: {one(test['input'])} | "
                  f"want: {one(test['output'], 40)} | got: {one(p.stdout or p.stderr.strip().split(chr(10))[-1], 40)}")
        if p.returncode != 0:
            return False, (p.stderr.strip().split("\n")[-1][:150] or "crashed"), details
        if not ok:
            return False, f"wrong answer on test {i}", details
    return True, "", details


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--answers", required=True)
    ap.add_argument("--files", default="test6.jsonl")
    ap.add_argument("--show", action="store_true", help="print every test: input, wanted, got")
    args = ap.parse_args()

    problems = {p["task_id"]: p for p in load_problems(files=tuple(args.files.split(",")))}
    rows = [json.loads(l) for l in open(args.answers)]
    out_csv = args.answers.replace(".jsonl", "-graded.csv")

    graded = []
    with tempfile.TemporaryDirectory(prefix="grade-lcb-") as workdir, open(out_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["policy", "task_id", "difficulty", "passed", "why_not", "thinking_tokens",
                    "total_new_tokens", "hit_limit"])
        for i, r in enumerate(rows, 1):
            problem = problems[r["task_id"]]
            if args.show:
                print(f"\n--- {r['task_id']} ({problem['difficulty']}, {problem['run_as']}) · {r['policy']} · "
                      f"thinking {r['thinking_tokens']} tokens{' · CUT OFF' if r['hit_limit'] else ''}")
                print("    problem:", " ".join(problem["title"].split())[:90])
            ok, why, _tests = run_one(extract_code(r["answer_text"]), problem, workdir, show=args.show)
            w.writerow([r["policy"], r["task_id"], problem["difficulty"], ok, why,
                        r["thinking_tokens"], r["total_new_tokens"], r["hit_limit"]])
            graded.append((r, problem, ok))
            print(f"{i}/{len(rows)} {r['task_id']:<16}{problem['difficulty']:<8}{r['policy']:<13}"
                  f"{'PASS' if ok else 'fail: ' + why}", flush=True)

    print("\n=== SUMMARY (LiveCodeBench, all tests must pass) ===")
    for policy in sorted({r["policy"] for r in rows}):
        for diff in ("easy", "medium"):
            rs = [(r, ok) for r, p, ok in graded if r["policy"] == policy and p["difficulty"] == diff]
            if not rs:
                continue
            passed = sum(ok for _, ok in rs)
            think = [r["thinking_tokens"] for r, _ in rs]
            total = [r["total_new_tokens"] for r, _ in rs]
            cut = sum(r["hit_limit"] for r, _ in rs)
            print(f"{policy:<13}{diff:<8} passed {passed}/{len(rs)} ({100*passed/len(rs):.0f}%) | "
                  f"median thinking {st.median(think):.0f} | median all tokens {st.median(total):.0f} | "
                  f"hit the limit {cut}")
    print("\nsaved", out_csv)


if __name__ == "__main__":
    main()
