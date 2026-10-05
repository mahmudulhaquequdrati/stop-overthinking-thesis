"""Pick 40 extra LiveCodeBench problems that are not in the finished thesis.

1. What problem does this solve?  The thesis graded 234 problems. We want more exam
   questions without paying the GPU for those 234 again.
2. Why do we need it?  The old notebooks skip a file once it is full, so they cannot
   add problems. A separate list keeps the old run safe.
3. What goes in?   Graded csvs already in this repo (the old ids) and LiveCodeBench
   files test2.jsonl–test5.jsonl (April 2024–January 2025).
4. What comes out? results/extra/old-test-ids.json, old-train-ids.json, ids.json,
   LISTS.md, and data/extra-lcb.json (the questions, rebuilt each time).
5. Why this way?   The id list is fixed in git before any new score. The script
   stops if a rebuild would change that list.

Use:  python scripts/build_extra_problems.py
"""

import csv, glob, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lcb_data import FRESH_AFTER, build_prompt, load_problems

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTRA = os.path.join(ROOT, "results", "extra")
OUT_PROBLEMS = os.path.join(ROOT, "data", "extra-lcb.json")
N_KEEP = 40
SHINGLE, THRESHOLD = 5, 0.3
EXTRA_FILES = ("test2.jsonl", "test3.jsonl", "test4.jsonl", "test5.jsonl")


def read_ids(path):
    ids = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            ids.append(row["task_id"])
    return ids


def shingles(text):
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {tuple(words[i:i + SHINGLE]) for i in range(max(1, len(words) - SHINGLE + 1))}


def freeze_old_ids():
    """The exact exam and training ids already saved in the graded files."""
    test_he = read_ids(os.path.join(ROOT, "results/2026-09-24-thesis-run/test-on-he-graded.csv"))
    test_lcb = read_ids(os.path.join(ROOT, "results/2026-09-24-thesis-run/test-on-lcb-graded.csv"))
    train_lcb = read_ids(os.path.join(ROOT, "results/2026-09-24-thesis-run/train-lcb-graded.csv"))
    old_test = sorted(set(test_he) | set(test_lcb))
    old_train = sorted(set(train_lcb))
    overlap = set(old_test) & set(old_train)
    if overlap:
        raise SystemExit(f"STOP: train ids also in the exam: {sorted(overlap)[:5]}")
    if len(old_test) != 234:
        raise SystemExit(f"STOP: expected 234 old test ids, got {len(old_test)}")
    if len(old_train) != 80:
        raise SystemExit(f"STOP: expected 80 old train ids, got {len(old_train)}")
    return old_test, old_train


def train_questions():
    """Question text we already saved, so a new exam item cannot be a copy of homework."""
    texts = []
    for path in glob.glob(os.path.join(ROOT, "results/**/train-set*.jsonl"), recursive=True):
        for line in open(path):
            if line.strip():
                row = json.loads(line)
                if row.get("question"):
                    texts.append((row.get("task_id", os.path.basename(path)), row["question"]))
    return texts


def as_record(p):
    return dict(
        task_id=p["task_id"], source="lcb", difficulty=p["difficulty"], split="extra",
        title=p["title"], run_as=p["run_as"], question=build_prompt(p),
        func_name=p["func_name"], tests=p["tests"], n_tests=len(p["tests"]),
        contest_date=p["contest_date"],
    )


def choose(old_test, old_train):
    blocked = set(old_test) | set(old_train)
    pool = []
    for p in load_problems(files=EXTRA_FILES, fresh_only=False):
        if p["difficulty"] not in ("easy", "medium"):
            continue
        if p["contest_date"] > FRESH_AFTER:
            continue
        if p["task_id"] in blocked:
            continue
        pool.append(p)

    train_sh = [(tid, shingles(q)) for tid, q in train_questions()]
    clean, dropped = [], []
    for p in pool:
        rec = as_record(p)
        sh = shingles(rec["question"])
        hit = None
        for tid, tsh in train_sh:
            jac = len(sh & tsh) / max(1, len(sh | tsh))
            if jac >= THRESHOLD:
                hit = (tid, round(jac, 2))
                break
        if hit:
            dropped.append((p["task_id"], hit))
        else:
            clean.append(rec)

    # Latest dates sit closest to the real exam. task_id breaks ties. No hand picking.
    clean.sort(key=lambda p: (p["contest_date"], p["task_id"]))
    chosen = clean[-N_KEEP:] if len(clean) > N_KEEP else clean
    chosen.sort(key=lambda p: p["task_id"])
    return pool, dropped, chosen


def write_lists(old_test, old_train, chosen):
    os.makedirs(EXTRA, exist_ok=True)
    os.makedirs(os.path.dirname(OUT_PROBLEMS), exist_ok=True)

    def dump(name, rows):
        path = os.path.join(EXTRA, name)
        with open(path, "w") as f:
            json.dump(rows, f, indent=2)
            f.write("\n")

    ids = [p["task_id"] for p in chosen]
    frozen = os.path.join(EXTRA, "ids.json")
    if os.path.exists(frozen):
        previous = json.load(open(frozen))
        if previous != ids:
            raise SystemExit(
                "STOP: the extra id list would change. "
                f"Frozen {len(previous)} ids, rebuild wanted {len(ids)}. "
                "Do not overwrite results/extra/ids.json.")
    if set(ids) & set(old_test):
        raise SystemExit("STOP: an extra id is already in the old exam")
    if set(ids) & set(old_train):
        raise SystemExit("STOP: an extra id is already in training")

    dump("old-test-ids.json", old_test)
    dump("old-train-ids.json", old_train)
    dump("ids.json", ids)

    payload = dict(built="2026-10-05", source_files=list(EXTRA_FILES), problems=chosen)
    for path in (OUT_PROBLEMS, os.path.join(EXTRA, "extra-lcb.json")):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(payload, f)
            f.write("\n")

    n_easy = sum(p["difficulty"] == "easy" for p in chosen)
    n_med = sum(p["difficulty"] == "medium" for p in chosen)
    dates = sorted(p["contest_date"] for p in chosen)
    lines = [
        "# Problem lists for the extra check",
        "",
        "The old exam is frozen. The new notebook refuses those ids.",
        "It writes only under `results/extra/`. It does not write into the old result folders.",
        "",
        "| List | Count | File |",
        "|---|---|---|",
        f"| Old exam (HumanEval+ and LiveCodeBench) | {len(old_test)} | old-test-ids.json |",
        f"| Old LiveCodeBench training problems | {len(old_train)} | old-train-ids.json |",
        f"| New extra problems | {len(ids)} | ids.json |",
        f"| Total if we add them (exam + extra) | {len(old_test) + len(ids)} | the two files above |",
        "",
        f"Extra mix: {n_easy} easy, {n_med} medium.",
        f"Dates: {dates[0]} to {dates[-1]}." if dates else "Dates: none.",
        "",
        "New ids:",
        "",
    ]
    for p in chosen:
        lines.append(f"- `{p['task_id']}` · {p['difficulty']} · {p['contest_date']} · {p['title']}")
    lines.append("")
    with open(os.path.join(EXTRA, "LISTS.md"), "w") as f:
        f.write("\n".join(lines))
    return ids


def main():
    old_test, old_train = freeze_old_ids()
    pool, dropped, chosen = choose(old_test, old_train)
    ids = write_lists(old_test, old_train, chosen)
    print(f"old exam ids: {len(old_test)}")
    print(f"old train ids: {len(old_train)}")
    print(f"unused easy+medium in test2-test5 before overlap cut: {len(pool)}")
    print(f"dropped for text overlap with training: {len(dropped)}")
    for tid, hit in dropped:
        print(f"   {tid} overlaps {hit[0]} ({hit[1]})")
    print(f"extra problems kept: {len(ids)}")
    if len(ids) < 20:
        raise SystemExit("STOP: fewer than 20 extra problems. Do not run the notebook.")
    print("wrote results/extra/ and data/extra-lcb.json")


if __name__ == "__main__":
    main()
