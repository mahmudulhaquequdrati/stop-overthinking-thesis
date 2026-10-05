"""Join the frozen 234 scores with the extra-problem scores, when those exist.

1. What problem does this solve?  After each graded way, we need the score tables
   written down, even if the Colab run stops early.
2. Why do we need it?  The old headline files must stay. The extra folder can update.
3. What goes in?   The old graded csvs, plus results/extra/<size>/test-*-lcb-graded.csv.
4. What comes out? Printed tables, and with --write a SUMMARY.md inside the extra folder.
5. Why this way?   Accuracy is the share of answers that passed. Tries are counted as
   answers, the same way the thesis tables count them.

Use:  python scripts/compare_extra.py --extra-dir results/extra --write results/extra/SUMMARY.md
"""

import argparse, csv, glob, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTRA = os.path.join(ROOT, "results", "extra")

OLD = {
    "0.8b": "results/0.8b/raw",
    "2b": "results/2026-09-24-thesis-run",
    "4b": "results/4b/raw",
}
# These two 2B limits live in their own folders. The main 2B folder used the name "limit"
# for limit 1024.
EXTRA_2B = {
    "limit512": "results/2b-limit512/raw",
    "limit2048": "results/2b-limit2048/raw",
}


def rows(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def acc(rs):
    if not rs:
        return None
    passed = sum(r["passed"] == "True" for r in rs)
    return 100.0 * passed / len(rs), passed, len(rs)


def load_folder(folder, only_lcb=False):
    out = {}
    if not os.path.isdir(folder):
        return out
    for path in glob.glob(os.path.join(folder, "test-*-graded.csv")):
        name = os.path.basename(path)
        if "smoke" in path:
            continue
        m = re.match(r"test-(.+)-(he|lcb)-graded\.csv$", name)
        if not m:
            continue
        way, ds = m.group(1), m.group(2)
        if only_lcb and ds != "lcb":
            continue
        rs = rows(path)
        if way == "limit" and ds:
            way = "limit1024"
        out.setdefault(way, []).extend(rs)
    return out


def lines_for(title, by_way):
    lines = [f"### {title}", ""]
    if not by_way:
        lines.append("No graded files yet.")
        lines.append("")
        return lines
    lines.append("| Way | Accuracy | Passed |")
    lines.append("|---|---|---|")
    for way in sorted(by_way):
        got = acc(by_way[way])
        if not got:
            continue
        pct, passed, n = got
        lines.append(f"| {way} | {pct:.1f}% | {passed}/{n} |")
    lines.append("")
    return lines


def collect(extra_dir):
    blocks = []
    for size, rel in OLD.items():
        old = load_folder(os.path.join(ROOT, rel))
        if size == "2b":
            for way, rel2 in EXTRA_2B.items():
                more = load_folder(os.path.join(ROOT, rel2))
                if way in more:
                    old[way] = more[way]
        extra = load_folder(os.path.join(extra_dir, size), only_lcb=True)
        both = {way: old[way] + extra[way] for way in sorted(set(old) & set(extra))}
        blocks.append((size, old, extra, both))
    return blocks


def report(extra_dir):
    old_ids = json_ids(extra_dir, "old-test-ids.json")
    extra_ids = json_ids(extra_dir, "ids.json")
    lines = [
        "# Extra scores (written by the run)",
        "",
        "The old exam files were not changed.",
        "This file is rewritten after every graded way, so a stopped run still has its scores.",
        "",
        f"- Old exam ids: {len(old_ids)}",
        f"- Extra ids: {len(extra_ids)}",
        f"- Overlap: {len(set(old_ids) & set(extra_ids))}",
        f"- Total if added: {len(set(old_ids) | set(extra_ids))}",
        "",
    ]
    for size, old, extra, both in collect(extra_dir):
        lines += lines_for(f"{size} — old exam (frozen)", old)
        lines += lines_for(f"{size} — extra problems only", extra)
        lines += lines_for(f"{size} — old plus extra", both)
    return "\n".join(lines).rstrip() + "\n"


def json_ids(extra_dir, name):
    path = os.path.join(extra_dir, name)
    if not os.path.exists(path):
        path = os.path.join(ROOT, "results", "extra", name)
    if not os.path.exists(path):
        return []
    return json.load(open(path))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--extra-dir", default=EXTRA)
    ap.add_argument("--write", default=None, help="write SUMMARY.md here (inside the extra folder)")
    args = ap.parse_args()
    text = report(args.extra_dir)
    print(text)
    if args.write:
        if not args.write.endswith("SUMMARY.md") or "extra" not in args.write.replace("\\", "/"):
            raise SystemExit("STOP: --write must be an extra/SUMMARY.md path")
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
