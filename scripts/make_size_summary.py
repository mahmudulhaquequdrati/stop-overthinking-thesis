"""Build SUMMARY.md for one size run (0.8b or 4b) from graded CSVs.

Use:
  python scripts/make_size_summary.py --dir results/4b/raw --run 4b --summary results/4b/SUMMARY.md
"""

import argparse, csv, glob, os, re, statistics


def load_dir(folder):
    """way -> list of per-try rows with passed, tokens, thinking, cut."""
    ways = {}
    for path in glob.glob(os.path.join(folder, "test-*-graded.csv")):
        m = re.match(r"test-(.+)-(he|lcb)-graded\.csv$", os.path.basename(path))
        if not m:
            continue
        way, ds = m.group(1), m.group(2)
        rows = list(csv.DictReader(open(path)))
        for r in rows:
            r["_ds"] = ds
            ways.setdefault(way, []).append(r)
    return ways


def stats(rows):
    if not rows:
        return None
    by = {}
    for r in rows:
        by.setdefault(r["task_id"], []).append(r)
    accs, thinks, toks, cuts = [], [], [], []
    for rs in by.values():
        accs.append(statistics.mean(1.0 if str(r["passed"]) == "True" else 0.0 for r in rs))
        thinks.append(statistics.mean(int(r["thinking_tokens"]) for r in rs))
        toks.append(statistics.mean(int(r["total_new_tokens"]) for r in rs))
        cuts.append(statistics.mean(
            1.0 if str(r.get("hit_limit")) in ("True", "true", "1") else 0.0 for r in rs))
    return dict(
        problems=len(by),
        tries=len(rows) // max(len(by), 1),
        accuracy=100 * statistics.mean(accs),
        thinking=statistics.mean(thinks),
        tokens=statistics.mean(toks),
        cut_off_pct=100 * statistics.mean(cuts),
    )


def order_ways(ways):
    pref = ["off", "on", "limit512", "limit1024", "limit2048", "limit4096", "lora1"]
    rest = sorted(w for w in ways if w not in pref)
    return [w for w in pref if w in ways] + rest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True, help="raw results folder for one size")
    ap.add_argument("--run", required=True, help="0.8b or 4b")
    ap.add_argument("--summary", required=True, help="SUMMARY.md path")
    args = ap.parse_args()

    ways = load_dir(args.dir)
    lines = [
        f"# {args.run} run — summary",
        "",
        f"Raw folder: `{args.dir}`",
        "",
        "| Way | Problems | Tries | Accuracy | Thinking | All tokens | Cut off % |",
        "|---|---|---|---|---|---|---|",
    ]
    if not ways:
        lines.append("| — | — | — | not run yet | — | — | — |")
    else:
        for w in order_ways(ways):
            s = stats(ways[w])
            if not s:
                continue
            lines.append(
                f"| {w} | {s['problems']} | {s['tries']} | {s['accuracy']:.1f}% | "
                f"{s['thinking']:.0f} | {s['tokens']:.0f} | {s['cut_off_pct']:.0f}% |"
            )
    lines += [
        "",
        "## Status",
        "",
        ("✅ Graded files found." if ways else "⬜ No graded `test-*-*.csv` files yet. "
         "Run the Colab notebook, then re-run this script."),
        "",
        f"Hours ledger (shared): `results/shared/hours_budget.json`",
    ]
    os.makedirs(os.path.dirname(os.path.abspath(args.summary)), exist_ok=True)
    open(args.summary, "w").write("\n".join(lines) + "\n")
    print("wrote", args.summary)
    for line in lines:
        print(line)


if __name__ == "__main__":
    main()
