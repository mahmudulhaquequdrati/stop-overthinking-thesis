"""Grade the pilot answers with HumanEval+'s own tests, inside evalplus's sandbox.

1. What problem does this solve?  We need to know how many problems the model really
   solved, judged by the benchmark's tests, not by eye.
2. Why do we need it?  PLAN §7: the model must solve ≥40% of problems at least once,
   or there are no correct answers to shorten.
3. What goes in?   The raw answers from scripts/gen_colab.py (before 2026-09-20: the deleted
   scripts/mac_pilot_generate.py).
4. What comes out? results/<name>-graded.csv (one row per answer) and a printed summary:
   how often the first try passed the tests, and how long the thinking was.
5. Why this way?   evalplus runs the model's code in separate processes with time limits
   (CLAUDE.md §4). We never run model-written code ourselves.
"""

import argparse, json, csv, re, subprocess, sys, os, tempfile, statistics

from evalplus.data import get_human_eval_plus

FENCE = re.compile(r"```(?:python)?\s*\n(.*?)```", re.S)


def extract_code(answer_text):
    """Take the last complete ```python block; if there is none, take the raw text."""
    blocks = FENCE.findall(answer_text)
    if blocks:
        return blocks[-1]
    # an answer cut off by the token limit may have an opening fence only
    if "```python" in answer_text:
        return answer_text.split("```python", 1)[1]
    return answer_text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--answers", default="results/2026-09-20-pilot-e2b-humanevalplus.jsonl")
    ap.add_argument("--workdir", default=None, help="where the sandbox files go (default: a temp folder)")
    args = ap.parse_args()

    rows = [json.loads(l) for l in open(args.answers)]
    workdir = args.workdir or tempfile.mkdtemp(prefix="pilot-grade-")
    os.makedirs(workdir, exist_ok=True)

    results = {}
    for policy in sorted({r["policy"] for r in rows}):
        samples = os.path.join(workdir, f"{policy}.jsonl")
        ours = {r["task_id"]: extract_code(r["answer_text"]) for r in rows if r["policy"] == policy}
        # evalplus insists on every problem of the benchmark. The ones we did not ask get an
        # empty answer (it fails at once) and are left out of the summary below.
        with open(samples, "w") as f:
            for task_id in get_human_eval_plus():
                f.write(json.dumps({"task_id": task_id, "solution": ours.get(task_id, "")}) + "\n")

        # evalplus runs each solution in its own process, with a time limit
        cmd = [sys.executable, "-m", "evalplus.evaluate", "--dataset", "humaneval",
               "--samples", samples, "--i-just-wanna-run"]
        print("grading", policy, "...", flush=True)
        proc = subprocess.run(cmd, capture_output=True, text=True)
        print(proc.stdout[-1500:] or proc.stderr[-1500:], flush=True)

        eval_file = samples.replace(".jsonl", "_eval_results.json")
        if not os.path.exists(eval_file):
            print("!! no results file for", policy); continue
        data = json.load(open(eval_file))["eval"]
        for task_id, entries in data.items():
            e = entries[0] if isinstance(entries, list) else entries
            base_ok = e.get("base_status", e.get("base", [None])[0]) == "pass"
            plus_ok = e.get("plus_status", e.get("plus", [None])[0]) == "pass"
            results[(policy, task_id)] = (base_ok, plus_ok)

    out_csv = args.answers.replace(".jsonl", "-graded.csv")
    with open(out_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["policy", "task_id", "passed_base", "passed_plus", "thinking_tokens",
                    "total_new_tokens", "hit_limit"])
        for r in rows:
            base_ok, plus_ok = results.get((r["policy"], r["task_id"]), (None, None))
            w.writerow([r["policy"], r["task_id"], base_ok, plus_ok, r["thinking_tokens"],
                        r["total_new_tokens"], r["hit_limit"]])

    print("\n=== SUMMARY ===")
    for policy in sorted({r["policy"] for r in rows}):
        rs = [r for r in rows if r["policy"] == policy]
        got = [results.get((policy, r["task_id"]), (None, None)) for r in rs]
        base = [g[0] for g in got if g[0] is not None]
        plus = [g[1] for g in got if g[1] is not None]
        thinking = [r["thinking_tokens"] for r in rs]
        total = [r["total_new_tokens"] for r in rs]
        cut = sum(r["hit_limit"] for r in rs)
        print(f"{policy:<14} problems {len(rs):>3} | passed base tests "
              f"{sum(base)}/{len(base)} ({100*sum(base)/max(len(base),1):.1f}%) | passed the harder + tests "
              f"{sum(plus)}/{len(plus)} ({100*sum(plus)/max(len(plus),1):.1f}%) | median thinking tokens "
              f"{statistics.median(thinking):.0f} | median all tokens {statistics.median(total):.0f} | hit the limit {cut}")
    print("\nsaved", out_csv)


if __name__ == "__main__":
    main()
