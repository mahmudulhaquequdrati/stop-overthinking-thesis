"""Print the three numbers that decide whether this model can carry the thesis.

1. What problem does this solve?  After a pilot we must decide: keep this model, or change
   it? We decide with numbers fixed IN ADVANCE, not with a feeling.
2. Why do we need it?  PLAN §7 sets two gates. This checks them, plus speed.
3. What goes in?   A graded .csv from grade_humaneval.py (needs several tries per problem).
4. What comes out? Three numbers, each with PASS or FAIL, and what to do next.
5. Why this way?   One script, run the same way every time, so the answer cannot drift.

THE THREE GATES

  1. Speed              tokens per second, and tokens per answer.
                        Question: can we finish inside free Colab?

  2. Solved at least    Of all problems, how many were solved by AT LEAST ONE of the tries?
     once >= 40%        If the model almost never solves a problem, there is no correct
     (PLAN §7)          short answer to learn from, and the thesis has nothing to teach.

  3. Room to shorten    For each problem: the SHORTEST correct answer divided by the
     <= 0.75            AVERAGE correct answer. 0.75 means the short one is 25% shorter.
     (PLAN §7)          THIS IS THE "will fine-tuning actually cut tokens?" NUMBER.
                        If it is close to 1.0, every correct answer is the same length,
                        so there is nothing to cut and fine-tuning cannot help.

Use:  python scripts/check_gates.py --graded results/...-graded.csv
"""

import argparse, collections, csv, statistics

SOLVED_AT_LEAST_ONCE_MIN = 0.40      # PLAN §7
ROOM_TO_SHORTEN_MAX = 0.75           # PLAN §7


def verdict(ok):
    return "PASS" if ok else "FAIL"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graded", required=True, help="the -graded.csv from grade_humaneval.py")
    ap.add_argument("--policy", default="thinking_on",
                    help="the gates are about the thinking answers we would learn from")
    args = ap.parse_args()

    rows = [r for r in csv.DictReader(open(args.graded)) if r["policy"] == args.policy]
    if not rows:
        raise SystemExit(f"no rows with policy={args.policy!r} in {args.graded}")

    by_problem = collections.defaultdict(list)
    for r in rows:
        by_problem[r["task_id"]].append(
            dict(passed=r["passed"] == "True",
                 total=int(r["total_new_tokens"]),
                 thinking=int(r["thinking_tokens"]),
                 hit_limit=r["hit_limit"] == "True"))

    tries = statistics.median(len(v) for v in by_problem.values())
    print(f"\n{len(rows)} answers · {len(by_problem)} problems · "
          f"{tries:.0f} tries each · policy = {args.policy}\n")

    # ---- gate 2: solved at least once -------------------------------------------------
    solved = [t for t, v in by_problem.items() if any(a["passed"] for a in v)]
    share = len(solved) / len(by_problem)
    gate2 = share >= SOLVED_AT_LEAST_ONCE_MIN
    print(f"GATE 2  solved at least once : {share:6.1%}  "
          f"(need >= {SOLVED_AT_LEAST_ONCE_MIN:.0%})  {verdict(gate2)}")
    print(f"        {len(solved)} of {len(by_problem)} problems were solved by at least one try")

    # ---- gate 3: room to shorten ------------------------------------------------------
    ratios = []
    for task_id in solved:
        lengths = [a["total"] for a in by_problem[task_id] if a["passed"]]
        if len(lengths) >= 2:                      # one correct answer tells us nothing
            ratios.append(min(lengths) / statistics.mean(lengths))
    if ratios:
        room = statistics.mean(ratios)
        gate3 = room <= ROOM_TO_SHORTEN_MAX
        print(f"\nGATE 3  room to shorten      : {room:6.3f}  "
              f"(need <= {ROOM_TO_SHORTEN_MAX})  {verdict(gate3)}")
        print(f"        measured on {len(ratios)} problems that were solved 2+ times")
        print(f"        meaning: the shortest correct answer is {(1 - room):.0%} shorter "
              f"than the average correct answer")
    else:
        gate3 = None
        print(f"\nGATE 3  room to shorten      :   n/a   "
              f"(no problem was solved more than once - run more tries)")

    # ---- gate 1: cost ------------------------------------------------------------------
    totals = [a["total"] for v in by_problem.values() for a in v]
    thinks = [a["thinking"] for v in by_problem.values() for a in v]
    cut = sum(a["hit_limit"] for v in by_problem.values() for a in v)
    print(f"\nGATE 1  cost per answer      : median {statistics.median(totals):.0f} tokens "
          f"({statistics.median(thinks):.0f} of them thinking)")
    print(f"        {cut} of {len(totals)} answers hit the token limit and were cut off")

    # ---- what to do next ---------------------------------------------------------------
    print("\nWHAT THIS MEANS")
    if not gate2:
        print("  The model is too weak. Step up to Qwen3.5-4B and run the pilot again.")
    elif gate3 is False:
        print("  Every correct answer is about the same length, so there is little to cut.")
        print("  Do NOT change model yet. Run 8 tries instead of 4 and check again")
        print("  (DECISIONS #27). If it still fails, that is a real finding: write it down.")
    elif gate3 is None:
        print("  Not enough repeated successes to judge. Run more tries per problem.")
    else:
        print("  Both gates pass. This model can carry the thesis.")
        print("  Write the DECISIONS rows and go on to the full run.")


if __name__ == "__main__":
    main()
