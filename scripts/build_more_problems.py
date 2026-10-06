"""Append LiveCodeBench problems to the growing list. Never delete an id.

1. What problem does this solve?  We need more test problems, and a later batch
   must not throw away problems we already listed.
2. Why do we need it?  The extra-40 script stops if its id list would change.
   This list is allowed to grow. The 234, the extra 40, and the 80 train ids stay frozen.
3. What goes in?   LiveCodeBench files test2.jsonl–test5.jsonl, plus the frozen id files.
4. What comes out? results/more/ids.json (append only), more-lcb.json, and LISTS.md.
5. Why this way?   About half easy and half medium. If one side runs out, the other fills.
   Latest dates are taken first, the same rule as the extra 40. Lowering --n does not delete ids.

Use:  python scripts/build_more_problems.py --n 200
      python scripts/build_more_problems.py --self-check
"""

import argparse, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from build_extra_problems import (
    FRESH_AFTER, as_record, freeze_old_ids, shingles, train_questions,
)
from lcb_data import build_prompt, load_problems

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MORE = os.path.join(ROOT, "results", "more")
EXTRA = os.path.join(ROOT, "results", "extra")
FILES = ("test2.jsonl", "test3.jsonl", "test4.jsonl", "test5.jsonl")
SHINGLE_THRESHOLD = 0.3
# The extra 40 already graded a problem whose tests were 2.6 MB.
# A few older contest problems are 50–150 MB. Those would make the run fail.
MAX_TEST_CHARS = 2_700_000


def load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path) as f:
        return json.load(f)


def atomic_write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        f.write(text)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def take_more(easy, medium, have_ids, target):
    """New records to append. `have_ids` stays in its old order."""
    have = set(have_ids)
    need = target - len(have_ids)
    if need <= 0:
        return []

    def pool(rows):
        rows = [p for p in rows if p["task_id"] not in have]
        rows.sort(key=lambda p: (p["contest_date"], p["task_id"]))
        return rows

    easy_l, med_l = pool(easy), pool(medium)
    # Half and half. A short side is filled by the other side.
    n_easy = min(len(easy_l), (need + 1) // 2)
    n_med = min(len(med_l), need - n_easy)
    n_easy = min(len(easy_l), need - n_med)
    chosen = easy_l[-n_easy:] + med_l[-n_med:]
    chosen.sort(key=lambda p: p["task_id"])
    return chosen


def record(p):
    rec = as_record(p)
    rec["split"] = "more"
    rec["question"] = build_prompt(p)
    return rec


def clean_pool(blocked):
    """Easy and medium problems on or before the fresh-exam date, not in `blocked`."""
    pool = []
    for p in load_problems(files=FILES, fresh_only=False):
        if p["difficulty"] not in ("easy", "medium"):
            continue
        if p["contest_date"] > FRESH_AFTER:
            continue
        if p["task_id"] in blocked:
            continue
        pool.append(p)

    train_sh = [(tid, shingles(q)) for tid, q in train_questions()]
    easy, medium, dropped, dropped_size = [], [], [], []
    for p in pool:
        rec = record(p)
        if len(json.dumps(rec["tests"])) > MAX_TEST_CHARS:
            dropped_size.append(p["task_id"])
            continue
        sh = shingles(rec["question"])
        hit = None
        for tid, tsh in train_sh:
            jac = len(sh & tsh) / max(1, len(sh | tsh))
            if jac >= SHINGLE_THRESHOLD:
                hit = (tid, round(jac, 2))
                break
        if hit:
            dropped.append((p["task_id"], hit))
            continue
        (easy if p["difficulty"] == "easy" else medium).append(rec)
    return easy, medium, dropped, dropped_size


def write_lists(old_test, old_train, extra_ids, ids, problems, n_too_long):
    n_easy = sum(p["difficulty"] == "easy" for p in problems)
    n_med = sum(p["difficulty"] == "medium" for p in problems)
    dates = sorted(p["contest_date"] for p in problems)
    total = len(old_test) + len(extra_ids) + len(ids)
    lines = [
        "# Problem lists — the total you can show",
        "",
        "The old exam, the extra 40, and the training ids are frozen.",
        "The new list only grows. Lowering the target does not remove an id.",
        "The total below is a count of problems. It is not a new blended score.",
        "49.8% and 78.2% stay on the old exam of 234.",
        "",
        "| List | Count | File |",
        "|---|---|---|",
        f"| Old exam (HumanEval+ and LiveCodeBench) | {len(old_test)} | results/extra/old-test-ids.json |",
        f"| Extra 40 | {len(extra_ids)} | results/extra/ids.json |",
        f"| New list | {len(ids)} | results/more/ids.json |",
        f"| **Total** | **{total}** | the three files above |",
        "",
        f"New list mix: {n_easy} easy, {n_med} medium.",
        f"Left out because the tests are longer than 2.7 MB: {n_too_long}.",
        "The extra 40 already graded nothing bigger than 2.6 MB.",
        "This list is every remaining clean problem.",
        f"New list dates: {dates[0]} to {dates[-1]}." if dates else "New list dates: none yet.",
        "",
        "New ids:",
        "",
    ]
    by_id = {p["task_id"]: p for p in problems}
    for tid in ids:
        p = by_id[tid]
        lines.append(f"- `{p['task_id']}` · {p['difficulty']} · {p['contest_date']} · {p['title']}")
    lines.append("")
    atomic_write(os.path.join(MORE, "LISTS.md"), "\n".join(lines))
    return total, n_easy, n_med


def self_check():
    def rec(tid, diff, date):
        return dict(task_id=tid, difficulty=diff, contest_date=date, title=tid)

    easy = [rec(f"e{i:03d}", "easy", f"2024-06-{i%28+1:02d}") for i in range(10)]
    medium = [rec(f"m{i:03d}", "medium", f"2024-07-{i%28+1:02d}") for i in range(10)]
    got = take_more(easy, medium, [], 6)
    assert len(got) == 6, len(got)
    assert sum(p["difficulty"] == "easy" for p in got) == 3
    assert sum(p["difficulty"] == "medium" for p in got) == 3
    # Latest dates, not the earliest.
    assert "e009" in {p["task_id"] for p in got}
    assert "e000" not in {p["task_id"] for p in got}

    short_med = medium[:1]
    got2 = take_more(easy, short_med, [], 6)
    assert len(got2) == 6
    assert sum(p["difficulty"] == "medium" for p in got2) == 1
    assert sum(p["difficulty"] == "easy" for p in got2) == 5

    have = ["e009", "m009"]
    got3 = take_more(easy, medium, have, 6)
    assert len(got3) == 4
    assert "e009" not in {p["task_id"] for p in got3}
    assert take_more(easy, medium, have, 2) == []
    print("self-check OK")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=200, help="target size of the new list")
    ap.add_argument("--self-check", action="store_true")
    args = ap.parse_args()
    if args.self_check:
        self_check()
        return

    old_test, old_train = freeze_old_ids()
    extra_ids = load_json(os.path.join(EXTRA, "ids.json"), [])
    if len(extra_ids) != 40:
        raise SystemExit(f"STOP: expected 40 extra ids, got {len(extra_ids)}")
    have = load_json(os.path.join(MORE, "ids.json"), [])
    if not isinstance(have, list):
        raise SystemExit("STOP: results/more/ids.json is not a list")

    blocked = set(old_test) | set(old_train) | set(extra_ids) | set(have)
    if len(blocked) != len(old_test) + len(old_train) + len(extra_ids) + len(have):
        raise SystemExit("STOP: an id is in more than one frozen list")

    easy, medium, dropped, dropped_size = clean_pool(blocked)
    added = take_more(easy, medium, have, args.n)
    ids = list(have) + [p["task_id"] for p in added]
    if ids[:len(have)] != have:
        raise SystemExit("STOP: the old new-list order would change")
    if len(set(ids)) != len(ids):
        raise SystemExit("STOP: a repeated id")
    bad = set(ids) & (set(old_test) | set(old_train) | set(extra_ids))
    if bad:
        raise SystemExit(f"STOP: new id collides with a frozen list: {sorted(bad)[:5]}")

    by_new = {p["task_id"]: p for p in added}
    # Problems already on the list must still be in the saved file. We do not re-pick them.
    saved = load_json(os.path.join(MORE, "more-lcb.json"), {"problems": []})
    saved_by = {p["task_id"]: p for p in saved.get("problems", [])}
    problems = []
    for tid in ids:
        if tid in by_new:
            problems.append(by_new[tid])
        elif tid in saved_by:
            problems.append(saved_by[tid])
        else:
            raise SystemExit(f"STOP: {tid} is on the list but its question was not saved")

    os.makedirs(MORE, exist_ok=True)
    atomic_write(os.path.join(MORE, "ids.json"), json.dumps(ids, indent=2) + "\n")
    payload = dict(built="2026-10-06", source_files=list(FILES), problems=problems)
    atomic_write(os.path.join(MORE, "more-lcb.json"), json.dumps(payload) + "\n")
    total, n_easy, n_med = write_lists(
        old_test, old_train, extra_ids, ids, problems, len(dropped_size))

    print(f"old exam: {len(old_test)}")
    print(f"extra 40: {len(extra_ids)}")
    print(f"clean easy not already listed: {len(easy)}")
    print(f"clean medium not already listed: {len(medium)}")
    print(f"dropped because the tests are too long: {len(dropped_size)}")
    print(f"dropped for text overlap with training: {len(dropped)}")
    for tid, hit in dropped:
        print(f"   {tid} overlaps {hit[0]} ({hit[1]})")
    print(f"already on the new list: {len(have)}")
    print(f"appended now: {len(added)}")
    print(f"new list: {len(ids)} ({n_easy} easy, {n_med} medium)")
    print(f"total problems you can show: {total}")
    if len(ids) < args.n:
        print(f"NOTE: the clean pool ran out. Target was {args.n}. Kept every clean problem.")


if __name__ == "__main__":
    main()
