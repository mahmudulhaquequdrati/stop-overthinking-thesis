"""A 10-second self-test for the thinking counter. No GPU needed.

1. What problem does this solve?  If split_thinking() is wrong, it reports 0 thinking
   tokens and NOTHING crashes. We would only notice days later, after wasting GPU hours.
2. Why do we need it?  Thinking tokens are the number the whole thesis is about.
3. What goes in?   Nothing. It downloads only the tokenizer (a few MB), not the model.
4. What comes out? PASS or FAIL for each check.
5. Why this way?   It uses the REAL chat template from Hugging Face, not a copy we typed
   out by hand, so it tests what will really happen on Colab.

Use:  ./.venv/bin/python scripts/test_prompts.py
"""

import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import models, prompts

FAILED = []


def check(name, got, want):
    ok = got == want
    print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    if not ok:
        print(f"        got:  {got!r}\n        want: {want!r}")
        FAILED.append(name)


def main():
    from transformers import AutoTokenizer

    profile = models.get("qwen35_2b")
    print(f"model profile: {profile['hf_id']}\n")
    tok = AutoTokenizer.from_pretrained(profile["hf_id"])

    print("1. Does the switch actually change the prompt?")
    on, off = prompts.check_prompt_has_switch(tok, profile)
    check("thinking ON prompt ends with <think>", on.rstrip().endswith("<think>"), True)
    check("thinking OFF prompt has an EMPTY think block",
          "<think>\n\n</think>" in off, True)
    print(f"        ON  tail: ...{on[-30:]!r}")
    print(f"        OFF tail: ...{off[-30:]!r}")

    print("\n2. THE TRAP: Qwen never writes <think> into its output.")
    # This is exactly what the model returns: thinking, then </think>, then the answer.
    qwen_out = "Let me think about this step by step.\n</think>\n\n```python\ndef f(): return 1\n```"
    n, answer = prompts.split_thinking(tok, qwen_out, "thinking_on", profile)
    check("thinking tokens are counted (NOT zero)", n > 0, True)
    check("the answer is the part after </think>", "def f(): return 1" in answer, True)
    check("the thinking text is NOT in the answer", "step by step" in answer, False)
    print(f"        counted {n} thinking tokens")

    print("\n3. Switch OFF: there is no thinking at all.")
    n, answer = prompts.split_thinking(tok, "```python\ndef f(): return 1\n```",
                                       "thinking_off", profile)
    check("0 thinking tokens", n, 0)
    check("everything is the answer", "def f()" in answer, True)

    print("\n4. Cut off while still thinking: no answer, so it fails.")
    cut = "I will start by writing a helper function\n```python\ndef f(): return 1\n```"
    n, answer = prompts.split_thinking(tok, cut, "thinking_on", profile)
    check("all tokens count as thinking", n > 0, True)
    check("the answer is EMPTY (we must not grade code from inside the thinking)", answer, "")

    print("\n5. The old Gemma style still works (start marker IS in the output).")
    gemma = dict(think_start="<|channel>", think_end="<channel|>", start_in_output=True)
    n, answer = prompts.split_thinking(
        tok, "<|channel>thought I am thinking<channel|>THE ANSWER", "thinking_on", gemma)
    check("thinking tokens counted", n > 0, True)
    check("answer is after the end marker", answer, "THE ANSWER")

    print("\n6. 'brief' adds one sentence; 'limit' does not change the prompt.")
    check("brief prompt is longer than thinking_on",
          len(prompts.make_prompt(tok, "q", "brief")) > len(prompts.make_prompt(tok, "q", "thinking_on")),
          True)
    check("limit prompt is identical to thinking_on",
          prompts.make_prompt(tok, "q", "limit") == prompts.make_prompt(tok, "q", "thinking_on"),
          True)

    print()
    if FAILED:
        print(f"{len(FAILED)} CHECK(S) FAILED: {', '.join(FAILED)}")
        print("Do NOT start a run until these pass.")
        sys.exit(1)
    print("All checks passed. The thinking counter is safe to use.")


if __name__ == "__main__":
    main()
