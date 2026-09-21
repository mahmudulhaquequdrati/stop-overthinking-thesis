"""The overlap check: no test problem may appear in the training data (CLAUDE.md §4).

1. What problem does this solve?  If a training problem is the same as, or very close to, a
   test problem, the LoRA would be tested on something it learned: an unfair, too-good result.
2. Why do we need it?  It is a hard rule of this thesis, and it must run before training.
3. What goes in?   The test problems (data/problems.json) and the training pools
   (data/mbpp.json, data/lcb_train.json).
4. What comes out? A printed report and data/overlap_exclude.json: the training task_ids to
   leave out. make_train_set.py --exclude reads it.
5. Why this way?   Two cheap, strict signals; a training problem is excluded if EITHER fires:
   - the same function name as a HumanEval+ problem (MBPP+ tests show the name), or
   - text overlap: the share of 5-word pieces the two questions have in common is >= 0.3.
   Strict on purpose: leaving out a few training problems costs almost nothing; one leaked
   test problem would damage the result.

Use:  python scripts/overlap_check.py
"""

import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from build_problem_set import load_all

OUT = "data/overlap_exclude.json"
SHINGLE, THRESHOLD = 5, 0.3


def shingles(text):
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {tuple(words[i:i + SHINGLE]) for i in range(max(1, len(words) - SHINGLE + 1))}


def called_names(text):
    return set(re.findall(r"assert\s+(?:\w+\()?\s*([A-Za-z_]\w*)\(", text))


def main():
    test = load_all("data/problems.json")
    train = [p for f in ("data/mbpp.json", "data/lcb_train.json") if os.path.exists(f)
             for p in load_all(f)]
    test_sh = [(t["task_id"], shingles(t["question"])) for t in test]
    test_names = {t["entry_point"]: t["task_id"] for t in test if t.get("entry_point")}
    test_ids = {t["task_id"] for t in test}

    flagged = {}
    for p in train:
        if p["task_id"] in test_ids:
            flagged[p["task_id"]] = f"same id as a test problem"
            continue
        for name in called_names(p["question"]):
            if name in test_names:
                flagged[p["task_id"]] = f"same function name as {test_names[name]} ({name})"
        sh = shingles(p["question"])
        for tid, tsh in test_sh:
            jac = len(sh & tsh) / max(1, len(sh | tsh))
            if jac >= THRESHOLD:
                flagged[p["task_id"]] = f"text overlap {jac:.2f} with {tid}"
                break

    with open(OUT, "w") as f:
        json.dump(sorted(flagged), f)
    print(f"checked {len(train)} training problems against {len(test)} test problems")
    print(f"excluded {len(flagged)} training problems -> {OUT}")
    for tid, why in sorted(flagged.items()):
        print(f"   {tid:<16} {why}")


if __name__ == "__main__":
    main()
