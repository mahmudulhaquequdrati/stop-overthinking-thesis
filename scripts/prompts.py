"""Build the prompt, and split a raw answer into "thinking" and "the answer".

1. What problem does this solve?  We must count thinking tokens the same way for every
   way of answering, and we must never grade code that the model wrote while still
   thinking.
2. Why do we need it?  Thinking tokens are the thing the whole thesis tries to shrink.
   If this file is wrong, every number in the thesis is wrong.
3. What goes in?   A tokenizer, a question, which way of answering, and the raw output.
4. What comes out? The prompt text; and (number of thinking tokens, the answer text).
5. Why this way?   Plain functions with no torch and no mlx, so they can be tested on any
   machine in a second, without a GPU.

The four ways of answering (PLAN §3):
    thinking_off   the switch is off
    thinking_on    the switch is on, normal thinking
    brief          the switch is on + the prompt asks for short thinking
    limit          the switch is on, but thinking is cut after k tokens
"""

POLICIES = ("thinking_off", "thinking_on", "brief", "limit")

BRIEF = ("\n\nThink briefly: keep your thinking to a few short sentences, "
         "then give the answer.")


def thinking_is_on(policy):
    """Only one way of answering has the switch off."""
    return policy != "thinking_off"


def make_prompt(tok, question, policy):
    """The text we actually send. Returns a string, not tokens, so the caller can pad a batch.

    Everything is identical between the ways of answering except the one thing being
    tested: the switch, and (for `brief`) one extra sentence. That is the fairness rule
    in CLAUDE.md §4.
    """
    if policy == "brief":
        question = question + BRIEF
    return tok.apply_chat_template(
        [{"role": "user", "content": question}],
        add_generation_prompt=True,
        tokenize=False,
        enable_thinking=thinking_is_on(policy),
    )


def split_thinking(tok, raw, policy, profile):
    """Return (number of thinking tokens, the answer text).

    Four cases:

      switch was OFF
          There is no thinking. Everything is the answer.

      thinking finished (the end marker is in the output)
          Thinking is everything before the end marker; the answer is everything after.
          For Gemma the start marker is also in the output, so we drop it. For Qwen the
          start marker was in the prompt, so there is nothing to drop.

      thinking started but NEVER finished (cut off by the token limit)
          ALL tokens count as thinking and there is NO answer. We must not grade code
          found inside the thinking: the model never delivered an answer, so this counts
          as a failure. The same rule applies to every way of answering, so it is fair.
    """
    if not thinking_is_on(policy):
        return 0, raw

    end, start = profile["think_end"], profile["think_start"]

    if end in raw:
        thinking, answer = raw.split(end, 1)
        if start in thinking:                 # Gemma-style: the start marker is in the output
            thinking = thinking.split(start, 1)[1]
        return n_tokens(tok, thinking), answer

    return n_tokens(tok, raw), ""             # never stopped thinking -> no answer -> fails


def n_tokens(tok, text):
    if not text:
        return 0
    return len(tok.encode(text, add_special_tokens=False))


def check_prompt_has_switch(tok, profile):
    """A safety check to run ONCE before a real run.

    Why: if the chat template ignores `enable_thinking`, both ways of answering get the
    same prompt, every number in the thesis becomes meaningless, and nothing crashes.
    So we look at the two prompts and demand that they differ.
    """
    on = make_prompt(tok, "hello", "thinking_on")
    off = make_prompt(tok, "hello", "thinking_off")
    if on == off:
        raise SystemExit(
            "STOP: the prompts for thinking ON and OFF are identical.\n"
            "The chat template is ignoring enable_thinking, so this model cannot be used.")
    if not profile["start_in_output"] and not on.rstrip().endswith(profile["think_start"]):
        print(f"WARNING: expected the prompt to end with {profile['think_start']!r}.\n"
              f"  thinking ON  ends with: {on[-60:]!r}\n"
              f"  thinking OFF ends with: {off[-60:]!r}")
    return on, off
