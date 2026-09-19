"""Pilot: ask Gemma-4-E2B the first N HumanEval+ problems, thinking ON and OFF.

1. What problem does this solve?  We don't know if this small model solves enough code
   problems for us to shorten (PLAN §7 asks for ≥40% solved at least once).
2. Why do we need it?  If it solves too few, there is nothing to shorten, and we must
   use a bigger model on a paid GPU.
3. What goes in?   HumanEval+ problems, and the thinking switch (ON / OFF).
4. What comes out? One line per answer in results/<out>.jsonl: the raw answer word for
   word, the token counts, the seconds. Grading happens in a separate, safe step.
5. Why this way?   Answers are written in batches (faster, measured), saved one by one
   (a stop costs nothing), and the raw text is kept so re-grading never needs the model.

This script NEVER runs the code the model writes. Grading is done by evalplus in a
sandbox: see scripts/mac_pilot_grade.py.
"""

import argparse, json, os, time, pathlib, importlib, contextlib
import mlx.core as mx
from mlx_lm import batch_generate
from mlx_lm.utils import load_model, load_tokenizer
from mlx_lm.sample_utils import make_sampler
from huggingface_hub import snapshot_download
from evalplus.data import get_human_eval_plus

MODEL_ID = "unsloth/gemma-4-E2B-it-UD-MLX-4bit"
SEED = 3407
GEN = dict(temp=1.0, top_p=0.95, top_k=64)   # Gemma's recommended settings (DECISIONS #39)
THINK_START, THINK_END = "<|channel>", "<channel|>"

# mlx-lm 0.31.3 bug: its speed counter divides by a prompt time that can be 0.
_g = importlib.import_module("mlx_lm.generate")
@contextlib.contextmanager
def _stats(self, stats=None):
    stats = stats or _g.BatchStats()
    self._prompt_tokens_counter = self._prompt_time_counter = self._gen_tokens_counter = 0
    tic = time.perf_counter()
    try:
        yield stats
    finally:
        total = time.perf_counter() - tic
        stats.prompt_tokens += self._prompt_tokens_counter
        stats.prompt_time += self._prompt_time_counter
        stats.prompt_tps = stats.prompt_tokens / max(stats.prompt_time, 1e-9)
        stats.generation_tokens += self._gen_tokens_counter
        stats.generation_time += total - self._prompt_time_counter
        stats.generation_tps = stats.generation_tokens / max(stats.generation_time, 1e-9)
        stats.peak_memory = max(stats.peak_memory, mx.get_peak_memory() / 1e9)
_g.BatchGenerator.stats = _stats


def load_everything():
    # strict=False: in this model the last 20 of 35 layers share the memory of earlier
    # layers, so 140 saved numbers are never used (checked in mlx_lm/models/gemma4_text.py).
    p = pathlib.Path(snapshot_download(MODEL_ID))
    return load_model(p, strict=False)[0], load_tokenizer(p)


def ask_prompt(tok, problem_prompt, thinking):
    instruction = (
        "Complete this Python function. Answer with one Python code block only, "
        "containing the complete function.\n\n```python\n" + problem_prompt + "```"
    )
    return tok.apply_chat_template(
        [{"role": "user", "content": instruction}],
        add_generation_prompt=True, tokenize=True, enable_thinking=thinking,
    )


def split_thinking(raw):
    if THINK_START in raw and THINK_END in raw:
        return raw.split(THINK_START, 1)[1].split(THINK_END, 1)[0], raw.split(THINK_END, 1)[1]
    return "", raw


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=30, help="how many problems")
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--max-tokens", type=int, default=2048)
    ap.add_argument("--out", default="results/2026-09-20-pilot-e2b-humanevalplus.jsonl")
    args = ap.parse_args()

    problems = list(get_human_eval_plus().items())[: args.n]
    model, tok = load_everything()
    sampler = make_sampler(**GEN)

    done = set()
    if os.path.exists(args.out):                      # a stop costs nothing: skip finished work
        for line in open(args.out):
            r = json.loads(line)
            done.add((r["task_id"], r["policy"], r["sample_index"]))

    out = open(args.out, "a")
    for thinking in (True, False):
        policy = "thinking_on" if thinking else "thinking_off"
        todo = [(tid, p) for tid, p in problems if (tid, policy, 0) not in done]
        print(f"{policy}: {len(todo)} problems to do", flush=True)
        for start in range(0, len(todo), args.batch):
            chunk = todo[start : start + args.batch]
            prompts = [ask_prompt(tok, p["prompt"], thinking) for _, p in chunk]
            mx.random.seed(SEED)
            t0 = time.time()
            res = batch_generate(model, tok, prompts, max_tokens=args.max_tokens, sampler=sampler)
            secs = time.time() - t0
            for (tid, _), text in zip(chunk, res.texts):
                ids = tok.encode(text, add_special_tokens=False)
                thinking_text, answer_text = split_thinking(text)
                rec = dict(
                    task_id=tid, policy=policy, sample_index=0, seed=SEED, model_id=MODEL_ID,
                    thinking_tokens=len(tok.encode(thinking_text, add_special_tokens=False)) if thinking_text else 0,
                    total_new_tokens=len(ids), hit_limit=len(ids) >= args.max_tokens,
                    batch_size=len(chunk), batch_seconds=round(secs, 1),
                    raw_output=text, answer_text=answer_text,
                    timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
                )
                out.write(json.dumps(rec) + "\n")
            out.flush(); os.fsync(out.fileno())       # really saved to disk
            print(f"  {start + len(chunk)}/{len(todo)} | {round(secs,1)}s for this batch", flush=True)
    out.close()
    print("saved to", args.out)


if __name__ == "__main__":
    main()
