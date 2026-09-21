"""The thesis result: every way of answering on the 234 test problems, with error bars and the
three hypotheses of PLAN §5.

1. What problem does this solve?  Turns thousands of graded answers into the answer to the
   research question: is the trained model a better balance of accuracy and length than the
   free options?
2. Why do we need it?  This table IS the results chapter.
3. What goes in?   The -graded.csv files in one folder, named test-<way>-<he|lcb>-graded.csv.
4. What comes out? Printed tables (all 234 problems, HumanEval+, LiveCodeBench easy, LiveCodeBench
   medium), the three hypotheses with YES/NO, and summary.csv in the same folder.
5. Why this way?
   - PAIRED: every comparison uses the same problems. Tries are averaged per problem first, so
     the error bars are "clustered by problem" (PLAN §5).
   - Error bars: resample the problems 2,000 times, fixed seed 3407.
   - The main LoRA is fixed in advance (DECISIONS #66): lora2 if it exists, else lora1. We never
     pick the LoRA that happens to look best.

THE HYPOTHESES (PLAN §5), for the main LoRA vs thinking ON, on all 234 problems:
  H1  thinking tokens <= 0.75x thinking ON's                     (>= 25% shorter)
  H2  accuracy >= thinking ON's - 3 points
  H3  more accurate than thinking OFF, the thinking limit and "think briefly"

Use:  python scripts/compare_thesis.py --dir <results folder>
"""

import argparse, csv, glob, os, random, re, statistics

WAYS = ["off", "on", "brief", "limit", "lora1", "lora2"]
BOOT, SEED = 2000, 3407


def load(folder):
    """{way: {task_id: dict(acc, tokens, thinking, cut, group, tries)}}"""
    out = {}
    for path in glob.glob(os.path.join(folder, "test-*-graded.csv")):
        m = re.match(r"test-(\w+?)-(he|lcb)-graded\.csv$", os.path.basename(path))
        if not m or m.group(1) not in WAYS:
            continue
        way, ds = m.groups()
        by = {}
        for r in csv.DictReader(open(path)):
            by.setdefault(r["task_id"], []).append(r)
        for t, rs in by.items():
            group = "HumanEval+" if ds == "he" else f"LCB {rs[0]['difficulty']}"
            out.setdefault(way, {})[t] = dict(
                acc=statistics.mean(r["passed"] == "True" for r in rs),
                tokens=statistics.mean(int(r["total_new_tokens"]) for r in rs),
                thinking=statistics.mean(int(r["thinking_tokens"]) for r in rs),
                cut=statistics.mean(r["hit_limit"] == "True" for r in rs),
                group=group, tries=len(rs))
    return out


def paired(a, b, tasks, rng):
    """a vs b on the same tasks: accuracy difference (points) and thinking-token ratio, 95% bars."""
    def stats(ts):
        d = 100 * (statistics.mean(a[t]["acc"] for t in ts) - statistics.mean(b[t]["acc"] for t in ts))
        r = sum(a[t]["thinking"] for t in ts) / max(sum(b[t]["thinking"] for t in ts), 1e-9)
        return d, r
    point = stats(tasks)
    boots = [stats([rng.choice(tasks) for _ in tasks]) for _ in range(BOOT)]
    q = lambda xs: (sorted(xs)[int(0.025 * BOOT)], sorted(xs)[int(0.975 * BOOT)])
    return point, q([x for x, _ in boots]), q([y for _, y in boots])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    args = ap.parse_args()
    data = load(args.dir)
    if "on" not in data:
        raise SystemExit("need thinking ON results (test-on-he / test-on-lcb)")
    main_lora = "lora2" if "lora2" in data else "lora1" if "lora1" in data else None
    rng = random.Random(SEED)
    groups = ["All", "HumanEval+", "LCB easy", "LCB medium"]
    rows_out = []

    for g in groups:
        tasks_of = lambda w: {t for t, v in data[w].items() if g == "All" or v["group"] == g}
        common = set.intersection(*(tasks_of(w) for w in data))
        if not common:
            continue
        common = sorted(common)
        print(f"\n=== {g}: {len(common)} problems (only problems every way has answered) ===")
        print(f"{'way':<7}{'tries':>6}{'accuracy':>10}{'thinking':>10}{'tokens':>8}{'cut off':>9}"
              f"   vs ON: accuracy (95%)          thinking ratio (95%)")
        for w in [w for w in WAYS if w in data]:
            v = [data[w][t] for t in common]
            acc = 100 * statistics.mean(x["acc"] for x in v)
            think = statistics.mean(x["thinking"] for x in v)
            tok = statistics.mean(x["tokens"] for x in v)
            cut = 100 * statistics.mean(x["cut"] for x in v)
            tries = round(statistics.mean(x["tries"] for x in v), 1)
            line = f"{w:<7}{tries:>6}{acc:>9.1f}%{think:>10.0f}{tok:>8.0f}{cut:>8.0f}%"
            row = dict(group=g, way=w, problems=len(common), tries=tries, accuracy=round(acc, 1),
                       thinking=round(think), tokens=round(tok), cut_off_pct=round(cut))
            if w != "on":
                (d, r), (dlo, dhi), (rlo, rhi) = paired(data[w], data["on"], common, rng)
                line += f"   {d:+5.1f} [{dlo:+5.1f}, {dhi:+5.1f}]   x{r:.2f} [{rlo:.2f}, {rhi:.2f}]"
                row.update(d_vs_on=round(d, 1), d_lo=round(dlo, 1), d_hi=round(dhi, 1),
                           think_ratio=round(r, 2), r_lo=round(rlo, 2), r_hi=round(rhi, 2))
            print(line)
            rows_out.append(row)

        if main_lora and g == "All":
            L = data[main_lora]
            (d, r), (dlo, dhi), (rlo, rhi) = paired(L, data["on"], common, rng)
            print(f"\nHYPOTHESES for the main LoRA ({main_lora}, fixed in advance), all problems:")
            print(f"  H1 {'YES' if r <= 0.75 else 'NO '}  thinking x{r:.2f} of ON [{rlo:.2f}, {rhi:.2f}] (need <= 0.75)")
            print(f"  H2 {'YES' if d >= -3 else 'NO '}  accuracy {d:+.1f} pts vs ON [{dlo:+.1f}, {dhi:+.1f}] (need >= -3)")
            for free in ("off", "limit", "brief"):
                if free in data:
                    (d2, _), (lo2, hi2), _ = paired(L, data[free], common, rng)
                    sure = "clearly" if lo2 > 0 else "not clearly (error bar includes 0)" if d2 > 0 else ""
                    print(f"  H3 {'YES' if d2 > 0 else 'NO '}  vs {free:<5}: {d2:+.1f} pts [{lo2:+.1f}, {hi2:+.1f}] {sure}")

    with open(os.path.join(args.dir, "summary.csv"), "w", newline="") as f:
        keys = ["group", "way", "problems", "tries", "accuracy", "thinking", "tokens",
                "cut_off_pct", "d_vs_on", "d_lo", "d_hi", "think_ratio", "r_lo", "r_hi"]
        w = csv.DictWriter(f, fieldnames=keys, restval="")
        w.writeheader()
        w.writerows(rows_out)
    print(f"\nsaved {os.path.join(args.dir, 'summary.csv')}")
    print("Honest limits: 1-2 tries per problem; 234 problems; one model; one wording for 'brief'.")


if __name__ == "__main__":
    main()
