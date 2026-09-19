"""Grade answers with HumanEval's own tests, each in its own short-lived process.

1. What problem does this solve?  We must know how many problems the model really solved,
   judged by the benchmark's tests, never by eye.
2. Why do we need it?  evalplus's own runner does not work on macOS: it sets a memory limit
   the way Linux does, macOS refuses it, and then every test process dies or hangs. We
   checked this: even the benchmark's OFFICIAL solutions scored 0 with it (2026-09-20).
3. What goes in?   A .jsonl of answers from scripts/mac_pilot_generate.py.
4. What comes out? <answers>-graded.csv (one row per answer) plus a printed summary.
5. Why this way?   Each answer runs in a separate Python process, in its own temporary
   folder, with a time limit (CLAUDE.md §4: never run model code inside our own program).
   The test code comes from the benchmark itself (evalplus ships HumanEval's `test` field),
   so we are not inventing our own tests.

Limit, to state in the thesis: these are HumanEval's ORIGINAL tests. The extra, harder
HumanEval+ tests need evalplus's runner, which we will run on Linux (Colab/Kaggle) later.
"""

import argparse, json, csv, os, re, statistics, subprocess, sys, tempfile

from evalplus.data import get_human_eval_plus

FENCE = re.compile(r"```(?:python)?\s*\n(.*?)```", re.S)
TIMEOUT_SECONDS = 15


def extract_code(answer_text):
    """Take the last complete ```python block; if there is none, take the raw text."""
    blocks = FENCE.findall(answer_text)
    if blocks:
        return blocks[-1]
    if "```python" in answer_text:      # an answer cut off by the token limit
        return answer_text.split("```python", 1)[1]
    return answer_text


def run_one(code, problem, workdir):
    """True if the code passes the benchmark's tests. Runs in its own process."""
    program = code + "\n\n" + problem["test"] + f"\n\ncheck({problem['entry_point']})\n"
    path = os.path.join(workdir, "candidate.py")
    with open(path, "w") as f:
        f.write(program)
    try:
        p = subprocess.run([sys.executable, "-I", path], cwd=workdir, timeout=TIMEOUT_SECONDS,
                           capture_output=True, text=True)
        return p.returncode == 0, ("" if p.returncode == 0 else p.stderr.strip().split("\n")[-1][:200])
    except subprocess.TimeoutExpired:
        return False, "timeout"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--answers", default="results/2026-09-20-pilot-e2b-humanevalplus.jsonl")
    args = ap.parse_args()

    problems = get_human_eval_plus()
    rows = [json.loads(l) for l in open(args.answers)]
    out_csv = args.answers.replace(".jsonl", "-graded.csv")

    with tempfile.TemporaryDirectory(prefix="grade-") as workdir, open(out_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["policy", "task_id", "passed", "why_not", "thinking_tokens",
                    "total_new_tokens", "hit_limit"])
        graded = []
        for i, r in enumerate(rows, 1):
            ok, why = run_one(extract_code(r["answer_text"]), problems[r["task_id"]], workdir)
            w.writerow([r["policy"], r["task_id"], ok, why, r["thinking_tokens"],
                        r["total_new_tokens"], r["hit_limit"]])
            graded.append((r, ok))
            print(f"{i}/{len(rows)} {r['task_id']:<14} {r['policy']:<13} {'PASS' if ok else 'fail: ' + why}", flush=True)

    print("\n=== SUMMARY (HumanEval original tests) ===")
    for policy in sorted({r["policy"] for r in rows}):
        rs = [(r, ok) for r, ok in graded if r["policy"] == policy]
        passed = sum(ok for _, ok in rs)
        think = [r["thinking_tokens"] for r, _ in rs]
        total = [r["total_new_tokens"] for r, _ in rs]
        cut = sum(r["hit_limit"] for r, _ in rs)
        print(f"{policy:<13} passed {passed}/{len(rs)} ({100 * passed / len(rs):.1f}%) | "
              f"median thinking tokens {statistics.median(think):.0f} | "
              f"median all tokens {statistics.median(total):.0f} | hit the token limit {cut}")
    print("\nsaved", out_csv)


if __name__ == "__main__":
    main()
