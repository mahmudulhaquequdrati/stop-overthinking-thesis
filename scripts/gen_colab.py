"""Ask the model a set of problems, one chosen way of answering, on a Colab GPU.

1. What problem does this solve?  We need answers from several ways of answering, on easy
   (HumanEval) and medium (LiveCodeBench) problems, saved safely.
2. Why do we need it?  These answers are the evidence of the whole thesis.
3. What goes in?   --policy, --samples, how many problems, the token limits.
4. What comes out? One line per answer in a .jsonl file: the raw answer word for word, the
   token counts, the seconds. Grading is a separate step, so we never re-generate.
5. Why this way?   Batches (a GPU is fast only when it answers many at once), saved one by
   one with fsync (a Colab disconnect costs nothing), a different fixed seed per sample,
   and ONE token limit shared by every way of answering so the comparison is fair.

Use on Colab:
  python scripts/gen_colab.py --policy thinking_on --n 30 --samples 4 \
      --out /content/drive/MyDrive/thesis/2026-09-21-qwen-pilot.jsonl
"""

import argparse, json, os, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import models, prompts
from build_problem_set import load_all


def load_model(profile, dtype=None):
    """Load the model onto the GPU. A T4 has no bfloat16, so we fall back to float16."""
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    if dtype is None:
        dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    tok = AutoTokenizer.from_pretrained(profile["hf_id"])
    tok.padding_side = "left"          # decoder models must be padded on the LEFT
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        profile["hf_id"], dtype=dtype, device_map="cuda:0")
    model.eval()

    used = torch.cuda.memory_allocated() / 1e9
    print(f"loaded {profile['hf_id']} as {dtype} | GPU memory used: {used:.2f} GB", flush=True)
    return model, tok


def add_adapter(model, adapter_dir):
    """Put our trained LoRA into the model, then merge it in, so it answers at the same speed,
    through the same code, as every other way of answering.

    The danger (DECISIONS #57): if the adapter's layer names do not match this model's, PEFT
    can create EMPTY LoRA layers, and the "trained" model silently answers like the base
    model. Trained LoRA layers have non-zero B matrices; empty ones are all zero. So we check.
    """
    from peft import PeftConfig, get_peft_model, get_peft_model_state_dict, set_peft_model_state_dict
    from safetensors.torch import load_file

    # Unsloth trains Qwen3.5 as a vision-language model, so it saves the LoRA under longer
    # names (seen on Colab 2026-09-22: PeftModel.from_pretrained found NONE of them). The
    # LoRA layers are the same; only the path in front of "layers.N." differs. So we match
    # each saved weight to this model's LoRA weight by the part from "layers." on.
    model = get_peft_model(model, PeftConfig.from_pretrained(adapter_dir))
    expected = {k[k.index("layers."):]: k for k in get_peft_model_state_dict(model)}
    saved = load_file(os.path.join(adapter_dir, "adapter_model.safetensors"))
    renamed = {expected[k[k.index("layers."):]]: v for k, v in saved.items()
               if "layers." in k and "visual" not in k and k[k.index("layers."):] in expected}
    if len(renamed) != len(expected):
        raise SystemExit(f"STOP: only {len(renamed)} of {len(expected)} LoRA weights matched. "
                         f"Saved names look like: {list(saved)[:3]}")
    set_peft_model_state_dict(model, renamed)
    b_sum = sum(p.detach().abs().sum().item() for n, p in model.named_parameters() if "lora_B" in n)
    n_layers = sum(1 for n, _ in model.named_parameters() if "lora_B" in n)
    if n_layers == 0 or b_sum == 0:
        raise SystemExit(f"STOP: the LoRA in {adapter_dir} did not load ({n_layers} layers, "
                         f"weight sum {b_sum}). The answers would silently be the base model's.")
    print(f"LoRA loaded: {n_layers} layers, weight sum {b_sum:.1f}", flush=True)
    return model.merge_and_unload()


def generate(model, tok, texts, max_new_tokens, profile, seed):
    """Answer a whole batch at once. Returns (the NEW text only, cut-off flag per answer).

    "Cut off" is read from the model's own tokens: the answer used every allowed token and did
    not end with a stop token. Counting the tokens again from the decoded text can be off by
    one (seen 2026-09-22: a looping answer counted 4,095 of 4,096 and was not marked cut off).
    """
    import torch
    from transformers import set_seed

    set_seed(seed)
    batch = tok(texts, return_tensors="pt", padding=True, add_special_tokens=False).to(model.device)
    with torch.no_grad():
        out = model.generate(**batch, max_new_tokens=max_new_tokens, do_sample=True,
                             pad_token_id=tok.pad_token_id, **profile["gen"])
    grown = out[:, batch["input_ids"].shape[1]:]          # drop the prompt part
    eos = model.generation_config.eos_token_id
    stop = {tok.pad_token_id, *(eos if isinstance(eos, list) else [eos])}
    cut = [grown.shape[1] >= max_new_tokens and t not in stop for t in grown[:, -1].tolist()]
    return tok.batch_decode(grown, skip_special_tokens=True), cut


def generate_safe(fn, texts, *args):
    """Run fn(texts, *args); if the GPU runs out of memory, do the batch in two halves.
    So a too-big batch size slows a run down instead of stopping it."""
    import torch
    try:
        return fn(texts, *args)
    except torch.cuda.OutOfMemoryError:
        if len(texts) == 1:
            raise
        torch.cuda.empty_cache()
        half = len(texts) // 2
        print(f"  out of GPU memory with {len(texts)} at once -> splitting in two", flush=True)
        a_txt, a_cut = generate_safe(fn, texts[:half], *args)
        b_txt, b_cut = generate_safe(fn, texts[half:], *args)
        return a_txt + b_txt, a_cut + b_cut


def generate_with_budget(model, tok, texts, budget, max_new_tokens, profile, seed):
    """The 'limit' way of answering: stop the thinking after `budget` tokens, then make the
    model answer now by adding the end-of-thinking marker ourselves.

    Done in two batched rounds, so it is as fast as the other ways of answering.
    """
    end = profile["think_end"]
    first, _ = generate(model, tok, texts, budget, profile, seed)

    seconds_texts, heads = [], []
    for prompt_text, head in zip(texts, first):
        if end in head:                       # it finished thinking on its own: keep only that part
            head = head.split(end, 1)[0] + end
        else:                                 # still thinking: cut it and force the answer
            head = head + end
        heads.append(head)
        seconds_texts.append(prompt_text + head)

    rest, cut = generate(model, tok, seconds_texts, max_new_tokens - budget, profile, seed)
    return [h + r for h, r in zip(heads, rest)], cut


def pick_problems(all_problems, source, n, difficulty="any", split="any"):
    ps = [p for p in all_problems if source == "all" or p["source"] == source]
    # Without this, the easy-first sort below means "--source lcb --n 20" gives only easy ones.
    ps = [p for p in ps if difficulty == "any" or p["difficulty"] == difficulty]
    ps = [p for p in ps if split == "any" or p.get("split") == split]
    ps.sort(key=lambda p: (p["difficulty"] != "easy", p["task_id"]))
    return ps[:n] if n else ps


def already_done(path):
    done = set()
    if os.path.exists(path):
        for line in open(path):
            if line.strip():
                r = json.loads(line)
                done.add((r["task_id"], r["policy"], r["sample_index"]))
    return done


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--policy", choices=prompts.POLICIES, required=True)
    ap.add_argument("--source", choices=["humaneval", "lcb", "mbpp", "all"], default="humaneval")
    ap.add_argument("--difficulty", choices=["any", "easy", "medium"], default="any")
    ap.add_argument("--split", choices=["any", "train", "test"], default="any",
                    help="MBPP only: the mini-thesis trains on 'train' and tests on 'test'")
    ap.add_argument("--only-ids", default=None, help="a .json list of task_ids to answer (and no others)")
    ap.add_argument("--adapter", default=None, help="a trained LoRA folder (the 5th way)")
    ap.add_argument("--label", default=None,
                    help="a name for this way of answering, e.g. lora50 (default: the policy)")
    ap.add_argument("--n", type=int, default=0, help="how many problems (0 = all)")
    ap.add_argument("--dtype", choices=["auto", "float16", "float32"], default="auto",
                    help="auto = bfloat16 if the GPU has it, else float16. A T4 has no bfloat16, "
                         "and float16 can overflow; float32 is the safe, slower check.")
    ap.add_argument("--samples", type=int, default=1, help="how many tries per problem")
    ap.add_argument("--batch", type=int, default=16)
    ap.add_argument("--max-tokens", type=int, default=4096,
                    help="the SAME safety limit for every way of answering")
    ap.add_argument("--think-budget", type=int, default=256, help="only for --policy limit")
    ap.add_argument("--model", default=models.DEFAULT)
    ap.add_argument("--problems", default="data/problems.json")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    profile = models.get(args.model)
    problems = pick_problems(load_all(args.problems), args.source, args.n, args.difficulty,
                             args.split)
    if args.only_ids:                                    # e.g. only the answers that were cut off
        keep = set(json.load(open(args.only_ids)))
        problems = [p for p in problems if p["task_id"] in keep]
    import torch
    dtype = None if args.dtype == "auto" else getattr(torch, args.dtype)
    model, tok = load_model(profile, dtype)
    if args.adapter:
        model = add_adapter(model, args.adapter)
    dtype_name = str(model.dtype).replace("torch.", "")
    prompts.check_prompt_has_switch(tok, profile)        # stop now if the switch does nothing

    done = already_done(args.out)
    todo = [(p, s) for s in range(args.samples) for p in problems
            if (p["task_id"], args.policy, s) not in done]
    print(f"{args.source} · {args.policy} · {args.samples} tries: "
          f"{len(todo)} of {len(problems) * args.samples} answers still to do", flush=True)

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    out = open(args.out, "a")
    for start in range(0, len(todo), args.batch):
        chunk = todo[start : start + args.batch]
        texts = [prompts.make_prompt(tok, p["question"], args.policy) for p, _ in chunk]
        # A different seed per try, otherwise all 4 tries would be the same answer.
        seed = models.SEED + chunk[0][1]

        t0 = time.time()
        if args.policy == "limit":
            answers, cut = generate_safe(
                lambda t: generate_with_budget(model, tok, t, args.think_budget,
                                               args.max_tokens, profile, seed), texts)
        else:
            answers, cut = generate_safe(
                lambda t: generate(model, tok, t, args.max_tokens, profile, seed), texts)
        secs = time.time() - t0

        new_tokens = 0
        for (p, sample_index), raw, was_cut in zip(chunk, answers, cut):
            n_all = prompts.n_tokens(tok, raw)
            new_tokens += n_all
            thinking_tokens, answer_text = prompts.split_thinking(tok, raw, args.policy, profile)
            out.write(json.dumps(dict(
                task_id=p["task_id"], policy=args.policy, way=args.label or args.policy,
                adapter=args.adapter, sample_index=sample_index,
                seed=seed, model_id=profile["hf_id"], model_profile=args.model,
                dataset=p["source"], difficulty=p["difficulty"], dtype=dtype_name,
                max_new_tokens=args.max_tokens,
                think_budget=args.think_budget if args.policy == "limit" else None,
                thinking_tokens=thinking_tokens, total_new_tokens=n_all,
                hit_limit=was_cut, batch_size=len(chunk),
                batch_seconds=round(secs, 1), raw_output=raw, answer_text=answer_text,
                timestamp=time.strftime("%Y-%m-%d %H:%M:%S"))) + "\n")
        out.flush(); os.fsync(out.fileno())        # really on disk, even if Colab dies now

        print(f"  {start + len(chunk)}/{len(todo)} | {secs:.0f}s | "
              f"{new_tokens / max(secs, 1e-9):.0f} tokens/s", flush=True)
    out.close()
    print("saved to", args.out)


if __name__ == "__main__":
    main()
