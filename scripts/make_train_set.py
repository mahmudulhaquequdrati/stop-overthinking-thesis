"""Make the training set: for each problem, keep the SHORTEST CORRECT answer (PLAN §8).

1. What problem does this solve?  The model answered each training problem 4 times. Some
   correct answers think much longer than others. We want to teach the short habit.
2. Why do we need it?  This file IS what the LoRA learns from. Wrong or cut-off answers in it
   would teach the model wrong code or unfinished thinking.
3. What goes in?   The answers .jsonl and its -graded.csv (thinking ON, several tries).
4. What comes out? A .jsonl: one line per kept problem, with the question and the chosen raw
   answer (thinking + code, word for word). Plus two printed numbers for the later analysis.
5. Why this way?   "Shortest" alone can pick a lucky, too-short answer; the S3-CoT paper warns
   that the very shortest answers hurt accuracy. So we keep the shortest correct answer that is
   at least HALF the median correct length for that problem (PLAN §7, selection rule).

THE "TARGET" NUMBER it prints matters later. It is how short our training answers are,
compared with a normal correct answer (e.g. 0.70 = 30% shorter). A LoRA cannot be expected to
cut more than its examples show it. compare_mini.py compares what the LoRA reached with this.

Use:  python scripts/make_train_set.py --answers A.jsonl --out train-set.jsonl
"""

import argparse, csv, json, os, statistics, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from build_problem_set import load_all


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--answers", required=True)
    ap.add_argument("--problems", default="data/mbpp.json")
    ap.add_argument("--splits", default="train",
                    help="which splits may be trained on (the real thesis uses all of MBPP+)")
    ap.add_argument("--exclude", default=None,
                    help="a .json list of task_ids to leave out (from scripts/overlap_check.py)")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    problems = {p["task_id"]: p for p in load_all(args.problems)}
    splits = set(args.splits.split(","))
    excluded = set(json.load(open(args.exclude))) if args.exclude else set()
    answers = {(r["task_id"], r["sample_index"]): r for r in map(json.loads, open(args.answers))}
    graded = csv.DictReader(open(args.answers.replace(".jsonl", "-graded.csv")))

    correct = {}                              # task_id -> the correct answers
    for g in graded:
        r = answers[(g["task_id"], int(g["sample_index"]))]
        if problems[g["task_id"]].get("split") not in splits:
            raise SystemExit(f"STOP: {g['task_id']} is not a training problem.")
        if g["task_id"] in excluded:                  # too close to a test problem
            continue
        if g["passed"] == "True" and not r["hit_limit"]:
            correct.setdefault(g["task_id"], []).append(r)

    kept, ratios = [], []
    for task_id, rs in sorted(correct.items()):
        lengths = [r["total_new_tokens"] for r in rs]
        floor = statistics.median(lengths) / 2
        best = min((r for r in rs if r["total_new_tokens"] >= floor), key=lambda r: r["total_new_tokens"])
        ratios.append(best["total_new_tokens"] / statistics.mean(lengths))
        kept.append(dict(task_id=task_id, question=problems[task_id]["question"],
                         completion=best["raw_output"], tokens=best["total_new_tokens"],
                         thinking_tokens=best["thinking_tokens"], n_correct=len(rs)))

    with open(args.out, "w") as f:
        for k in kept:
            f.write(json.dumps(k) + "\n")

    n_problems = len({t for t, _ in answers})
    target = statistics.mean(ratios)
    with open(args.out.replace(".jsonl", "-stats.json"), "w") as f:
        json.dump(dict(kept=len(kept), problems=n_problems, target=round(target, 3)), f)
    print(f"kept {len(kept)} of {n_problems} training problems (the others were never solved"
          f"{', or too close to a test problem' if excluded else ''})")
    print(f"median tokens of a kept answer: {statistics.median(k['tokens'] for k in kept):.0f}")
    print(f"TARGET = {target:.3f}  (kept answer / average correct answer; lower = more to learn)")
    print(f"         {sum(1 for k in kept if k['n_correct'] == 1)} problems had only one correct "
          f"answer, so for them there was nothing shorter to choose")
    print("saved", args.out)


if __name__ == "__main__":
    main()
