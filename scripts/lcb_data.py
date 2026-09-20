"""Load LiveCodeBench problems (the "medium" part of our test set).

1. What problem does this solve?  HumanEval is too easy: thinking OFF already solves 93%
   (pilot, 2026-09-20). We need harder problems to see when thinking is worth its cost.
2. Why do we need it?  Our scope is easy + medium code problems (PLAN §3).
3. What goes in?   A LiveCodeBench file (test.jsonl … test6.jsonl), a difficulty, a date.
4. What comes out? A list of problems, each with: id, the question, the starter code, the
   test cases (input → expected output), and how it must be run ("stdin" or "functional").
5. Why this way?   The dataset ships a loading script that Hugging Face refuses to run
   (DECISIONS #40), so we download the .jsonl files ourselves. The hidden tests are packed
   (base64 → zlib → pickle → json); we unpack them the way the benchmark does.

A problem after `contest_date` 2025-01-31 used to be called "fresh": it appeared after Gemma's
training data was collected (cutoff January 2025, DECISIONS #36). Since 2026-09-20 we use Qwen,
which publishes NO cutoff date, so we can no longer prove any problem is new to the model
(DECISIONS #54). We keep the same date filter, but only to pick recent problems - it is NOT a
proof of freshness any more, and the thesis must not claim that it is.
"""

import base64, json, pickle, zlib

from huggingface_hub import hf_hub_download

REPO = "livecodebench/code_generation_lite"
FRESH_AFTER = "2025-01-31"          # picks recent problems; NOT a freshness proof (#54)


def _unpack(private_test_cases):
    """The hidden tests are packed: base64 → zlib → pickle → json."""
    try:
        return json.loads(private_test_cases)
    except json.JSONDecodeError:
        return json.loads(pickle.loads(zlib.decompress(base64.b64decode(private_test_cases.encode()))))


def load_problems(files=("test6.jsonl",), difficulties=("easy", "medium"), fresh_only=True,
                  max_tests=20):
    problems = []
    for name in files:
        path = hf_hub_download(REPO, name, repo_type="dataset")
        for line in open(path):
            row = json.loads(line)
            if row["difficulty"] not in difficulties:
                continue
            if fresh_only and row["contest_date"][:10] <= FRESH_AFTER:
                continue
            tests = json.loads(row["public_test_cases"]) + _unpack(row["private_test_cases"])
            problems.append(dict(
                task_id=f"lcb/{row['question_id']}",
                title=row["question_title"],
                question=row["question_content"],
                starter_code=row["starter_code"],
                difficulty=row["difficulty"],
                contest_date=row["contest_date"][:10],
                run_as=tests[0]["testtype"],                  # "stdin" or "functional"
                func_name=json.loads(row["metadata"] or "{}").get("func_name"),
                tests=[{"input": t["input"], "output": t["output"]} for t in tests[:max_tests]],
            ))
    return problems


def build_prompt(problem):
    """The question as we show it to the model. The same text for every way of answering."""
    if problem["run_as"] == "stdin":
        how = ("Write a complete Python program. It reads from standard input and prints the "
               "answer to standard output. Answer with one Python code block only.")
    else:
        how = ("Complete the given Python class/function. Answer with one Python code block "
               "only, containing the complete solution.")
    text = f"{problem['question']}\n\n{how}"
    if problem["starter_code"].strip():
        text += f"\n\nUse this starter code:\n```python\n{problem['starter_code']}```"
    return text


if __name__ == "__main__":       # a quick look at what we get
    from collections import Counter
    ps = load_problems()
    print(len(ps), "fresh easy+medium problems in test6.jsonl")
    print(Counter((p["difficulty"], p["run_as"]) for p in ps))
    print(Counter(p["contest_date"][:7] for p in ps))
    p = ps[0]
    print("\nexample:", p["task_id"], p["difficulty"], p["run_as"], "| tests:", len(p["tests"]))
    print(build_prompt(p)[:400])
