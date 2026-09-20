"""Which model we use, and the few things that differ between models.

1. What problem does this solve?  The model name and its "thinking" markers were copied
   into four different files. When we changed model, they went out of step and the token
   counts quietly became wrong.
2. Why do we need it?  One place to change, so a model swap cannot half-happen.
3. What goes in?   A short profile name, e.g. "qwen35_2b".
4. What comes out? A dict with the Hugging Face name, the thinking markers, and the
   sampling settings.
5. Why this way?   A plain dict, not a class. This is a small research project
   (CLAUDE.md §5), and we only ever have two or three models.

THE IMPORTANT FIELD IS `start_in_output`.

  Gemma-4 writes the start marker itself:
      prompt ends: ...            output: <|channel>thought ... <channel|> ANSWER
  Qwen3.5 puts the start marker in the PROMPT:
      prompt ends: ... <think>    output: thinking ... </think> ANSWER

  So for Qwen the opening <think> is NEVER in the output. Code that looks for it finds
  nothing and reports 0 thinking tokens on every answer, without crashing. That would
  destroy the main measurement of this thesis. See scripts/prompts.py.
"""

PROFILES = {
    # Our model since 2026-09-20. 4.58 GB in 16-bit, fits fully on a free Colab T4.
    "qwen35_2b": dict(
        hf_id="unsloth/Qwen3.5-2B",
        think_start="<think>",
        think_end="</think>",
        start_in_output=False,
        # Qwen's own recommended settings for thinking + code, from the model card.
        # The SAME settings are used for every way of answering, so the comparison is fair.
        gen=dict(temperature=0.6, top_p=0.95, top_k=20),
    ),
    # The fallback, used only if 2B fails the "solved at least once >= 40%" gate (PLAN §7).
    "qwen35_4b": dict(
        hf_id="unsloth/Qwen3.5-4B",
        think_start="<think>",
        think_end="</think>",
        start_in_output=False,
        gen=dict(temperature=0.6, top_p=0.95, top_k=20),
    ),
}

DEFAULT = "qwen35_2b"
SEED = 3407                    # the same seed everywhere (CLAUDE.md §4)


def get(name=DEFAULT):
    if name not in PROFILES:
        raise SystemExit(f"unknown model profile {name!r}. Known: {', '.join(PROFILES)}")
    return PROFILES[name]
