"""Does vLLM run our model on this GPU, and how fast? A speed test only, no grading.

1. What problem does this solve?  Plain `transformers` may be too slow for a one-week
   thesis. vLLM is a tool built only for writing answers fast. We must know whether it
   works with Qwen3.5 BEFORE we spend money on a bigger GPU because of it.
2. Why do we need it?  Its tokens/s, next to the transformers tokens/s from the pilot,
   tells us whether switching tools (and maybe paying) is worth it (DECISIONS #59).
3. What goes in?   The first --n problems, thinking ON, the same settings and token limit
   as every other run.
4. What comes out? A printed "RUNS" or "FAILS", tokens/s, and a .jsonl with the raw answers
   (kept verbatim, CLAUDE.md §4, but NOT used as thesis results).
5. Why this way?   It runs in a fresh Colab runtime, because installing vLLM may replace the
   transformers version the pilot used. No LoRA here: the LoRA bug in DECISIONS #57 is
   about adapters, and this test is only about the base model's speed.

Use on Colab (after Runtime -> Restart):
  pip install vllm
  python scripts/try_vllm.py --out /content/drive/MyDrive/stop-overthinking/results/vllm-speed.jsonl
"""

import argparse, json, os, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import models, prompts
from build_problem_set import load_all
from gen_colab import pick_problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=16)
    ap.add_argument("--source", choices=["humaneval", "lcb", "all"], default="humaneval")
    ap.add_argument("--max-tokens", type=int, default=4096)
    ap.add_argument("--dtype", default="float16", help="a T4 has no bfloat16")
    ap.add_argument("--model", default=models.DEFAULT)
    ap.add_argument("--problems", default="data/problems.json")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    profile = models.get(args.model)
    problems = pick_problems(load_all(args.problems), args.source, args.n)

    try:
        from vllm import LLM, SamplingParams
        llm = LLM(model=profile["hf_id"], dtype=args.dtype, seed=models.SEED,
                  max_model_len=8192, gpu_memory_utilization=0.85)
    except Exception as e:                     # the answer "vLLM does not run here" is a result too
        print(f"\nvLLM FAILS on this GPU: {type(e).__name__}: {e}")
        return

    tok = llm.get_tokenizer()
    texts = [prompts.make_prompt(tok, p["question"], "thinking_on") for p in problems]
    params = SamplingParams(max_tokens=args.max_tokens, seed=models.SEED, **profile["gen"])

    t0 = time.time()
    outs = llm.generate(texts, params)
    secs = time.time() - t0

    total = 0
    with open(args.out, "w") as f:
        for p, o in zip(problems, outs):
            raw = o.outputs[0].text
            n_all = len(o.outputs[0].token_ids)
            total += n_all
            thinking_tokens, _ = prompts.split_thinking(tok, raw, "thinking_on", profile)
            f.write(json.dumps(dict(task_id=p["task_id"], policy="thinking_on", engine="vllm",
                                    dtype=args.dtype, thinking_tokens=thinking_tokens,
                                    total_new_tokens=n_all, hit_limit=n_all >= args.max_tokens,
                                    raw_output=raw)) + "\n")

    print(f"\nvLLM RUNS: {len(outs)} answers · {total} tokens · {secs:.0f} s · "
          f"{total / max(secs, 1e-9):.0f} tokens/s")
    print("Compare with the tokens/s the pilot printed for transformers.")
    print("saved", args.out)


if __name__ == "__main__":
    main()
