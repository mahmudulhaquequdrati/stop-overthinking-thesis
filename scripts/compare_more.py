"""Scores for the growing problem list only. Does not blend them into the old exam.

1. What problem does this solve?  After each graded way we need a score table, even if
   the Colab run stops early.
2. Why do we need it?  The old 49.8% and 78.2% must stay on the 234. This file is a
   separate table, with an easy row and a medium row.
3. What goes in?   results/more/<size>/test-*-lcb-graded.csv, plus the id lists.
4. What comes out? Printed tables, and with --write a SUMMARY.md inside results/more/.
5. Why this way?   Accuracy is the share of answers that passed. Easy and medium are
   counted apart so a near-zero medium score cannot hide the easy gap.

Use:  python scripts/compare_more.py --more-dir results/more --write results/more/SUMMARY.md
"""

import argparse, csv, glob, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MORE = os.path.join(ROOT, "results", "more")
EXTRA = os.path.join(ROOT, "results", "extra")


def rows(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def acc(rs):
    if not rs:
        return None
    passed = sum(r.get("passed") == "True" for r in rs)
    return 100.0 * passed / len(rs), passed, len(rs)


def load_folder(folder):
    out = {}
    if not os.path.isdir(folder):
        return out
    for path in glob.glob(os.path.join(folder, "test-*-graded.csv")):
        if "smoke" in path:
            continue
        m = re.match(r"test-(.+)-lcb-graded\.csv$", os.path.basename(path))
        if not m:
            continue
        out.setdefault(m.group(1), []).extend(rows(path))
    return out


def json_ids(path, fallback):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    if os.path.exists(fallback):
        with open(fallback) as f:
            return json.load(f)
    return []


def lines_for(title, rs_by_way):
    lines = [f"### {title}", ""]
    if not rs_by_way:
        lines += ["No graded files yet.", ""]
        return lines
    lines += ["| Way | Accuracy | Passed |", "|---|---|---|"]
    any_row = False
    for way in sorted(rs_by_way):
        got = acc(rs_by_way[way])
        if not got:
            continue
        pct, passed, n = got
        lines.append(f"| {way} | {pct:.1f}% | {passed}/{n} |")
        any_row = True
    if not any_row:
        lines.append("| — | — | — |")
    lines.append("")
    return lines


def by_diff(by_way, difficulty):
    out = {}
    for way, rs in by_way.items():
        kept = [r for r in rs if r.get("difficulty") == difficulty]
        if kept:
            out[way] = kept
    return out


def report(more_dir):
    old_ids = json_ids(os.path.join(EXTRA, "old-test-ids.json"), os.path.join(EXTRA, "old-test-ids.json"))
    extra_ids = json_ids(os.path.join(EXTRA, "ids.json"), os.path.join(EXTRA, "ids.json"))
    more_ids = json_ids(os.path.join(more_dir, "ids.json"), os.path.join(MORE, "ids.json"))
    overlap = set(more_ids) & (set(old_ids) | set(extra_ids))
    lines = [
        "# New-list scores (written by the run)",
        "",
        "The old exam files were not changed.",
        "This table is only the new list. It is not mixed into 49.8% or 78.2%.",
        "This file is rewritten after every graded way, so a stopped run still has its scores.",
        "",
        f"- Old exam: {len(old_ids)}",
        f"- Extra 40: {len(extra_ids)}",
        f"- New list: {len(more_ids)}",
        f"- Total problems: {len(old_ids) + len(extra_ids) + len(more_ids)}",
        f"- Overlap with the frozen lists: {len(overlap)}",
        "",
        "The total is a count of problems, not a blended accuracy.",
        "",
    ]
    for size in ("0.8b", "2b", "4b"):
        got = load_folder(os.path.join(more_dir, size))
        lines += lines_for(f"{size} — new list", got)
        lines += lines_for(f"{size} — easy", by_diff(got, "easy"))
        lines += lines_for(f"{size} — medium", by_diff(got, "medium"))
    return "\n".join(lines).rstrip() + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--more-dir", default=MORE)
    ap.add_argument("--write", default=None)
    args = ap.parse_args()
    text = report(args.more_dir)
    print(text)
    if args.write:
        parent = os.path.basename(os.path.dirname(os.path.abspath(args.write)))
        # "more" is the project folder. "more-out" is the Colab disk if Drive did not mount.
        if os.path.basename(args.write) != "SUMMARY.md" or parent not in ("more", "more-out"):
            raise SystemExit("STOP: --write must be more/SUMMARY.md")
        os.makedirs(os.path.dirname(os.path.abspath(args.write)), exist_ok=True)
        tmp = args.write + ".tmp"
        with open(tmp, "w") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, args.write)
        print("wrote", args.write)


if __name__ == "__main__":
    main()
