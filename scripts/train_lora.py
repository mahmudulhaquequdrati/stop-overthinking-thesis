"""Train one LoRA add-on on the shortest correct answers, on a free T4.

1. What problem does this solve?  This is the "training" in our thesis: teach the model to
   think as briefly as its own best answers did, without changing the big model itself.
2. Why do we need it?  It makes the 5th way of answering (ON + LoRA), the one we test
   against the free options.
3. What goes in?   The train-set .jsonl from make_train_set.py, and --fraction: how much of
   it to use (0.25, 0.5 or 1.0 for the learning curve).
4. What comes out? A LoRA folder (a few MB) that gen_colab.py --adapter can load, plus the
   training loss per step in <out>/loss.json.
5. Why this way?
   - The prompt is built by the SAME function the answering code uses (prompts.make_prompt),
     and the answer is the model's own raw text. So training sees exactly the format that
     answering produces. No second chat format that could drift.
   - The model learns ONLY the answer: the question's tokens get label -100 (ignored).
   - 16-bit LoRA, not 4-bit: Unsloth's Qwen3.5 guide says 4-bit training hurts this model.
   - The learning curve uses NESTED subsets (the 25% is inside the 50%, which is inside the
     100%) and the SAME number of epochs, so only the amount of data changes.

Settings follow Unsloth's Qwen3.5 guide: r=16, alpha=16, q/k/v/o + MLP layers, lr 2e-4,
batch 1 x 4 accumulation, adamw_8bit, seed 3407.

Use:  python scripts/train_lora.py --train train-set.jsonl --fraction 0.5 --out lora50
"""

import argparse, json, os, random, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import models, prompts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", required=True)
    ap.add_argument("--fraction", type=float, default=1.0)
    ap.add_argument("--epochs", type=int, default=3)
    ap.add_argument("--model", default=models.DEFAULT)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    import unsloth                                   # must come before transformers
    from unsloth import FastLanguageModel
    import torch
    from transformers import AutoTokenizer, Trainer, TrainingArguments

    profile = models.get(args.model)
    examples = [json.loads(l) for l in open(args.train)]
    random.Random(models.SEED).shuffle(examples)     # nested: 25% is the start of 50%, etc.
    examples = examples[:max(1, round(len(examples) * args.fraction))]

    # The plain tokenizer, exactly as gen_colab.py uses it (Unsloth may hand back a processor).
    tok = AutoTokenizer.from_pretrained(profile["hf_id"])
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    rows = []
    for ex in examples:
        p_ids = tok(prompts.make_prompt(tok, ex["question"], "thinking_on"),
                    add_special_tokens=False)["input_ids"]
        c_ids = tok(ex["completion"] + tok.eos_token, add_special_tokens=False)["input_ids"]
        rows.append(dict(input_ids=p_ids + c_ids, labels=[-100] * len(p_ids) + c_ids))
    max_len = max(len(r["input_ids"]) for r in rows)
    print(f"{len(rows)} examples ({args.fraction:.0%}) · longest {max_len} tokens", flush=True)

    # Unsloth's guide shows FastLanguageModel for dense Qwen3.5 but also says Qwen3.5 is a
    # vision-language model loaded with FastModel. Not checked on a T4 yet, so try both.
    load = dict(model_name=profile["hf_id"], max_seq_length=max_len, load_in_4bit=False,
                load_in_16bit=True, full_finetuning=False)
    try:
        model, _ = FastLanguageModel.from_pretrained(**load)
    except Exception as e:
        print(f"FastLanguageModel failed ({type(e).__name__}: {e}); trying FastModel", flush=True)
        from unsloth import FastModel as FastLanguageModel
        model, _ = FastLanguageModel.from_pretrained(**load)
    model = FastLanguageModel.get_peft_model(
        model, r=16, lora_alpha=16, lora_dropout=0, bias="none",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj"],
        use_gradient_checkpointing="unsloth", random_state=models.SEED,
        max_seq_length=max_len)

    def collate(batch):
        n = max(len(b["input_ids"]) for b in batch)
        pad = lambda xs, v: xs + [v] * (n - len(xs))
        return dict(
            input_ids=torch.tensor([pad(b["input_ids"], tok.pad_token_id) for b in batch]),
            labels=torch.tensor([pad(b["labels"], -100) for b in batch]),
            attention_mask=torch.tensor([pad([1] * len(b["input_ids"]), 0) for b in batch]))

    bf16 = torch.cuda.is_bf16_supported()
    trainer = Trainer(
        model=model, train_dataset=rows, data_collator=collate,
        args=TrainingArguments(
            output_dir=os.path.join(args.out, "_work"), per_device_train_batch_size=1,
            gradient_accumulation_steps=4, num_train_epochs=args.epochs, learning_rate=2e-4,
            warmup_steps=3, lr_scheduler_type="linear", optim="adamw_8bit",
            bf16=bf16, fp16=not bf16, logging_steps=1, save_strategy="no",
            report_to="none", seed=models.SEED, remove_unused_columns=False))
    trainer.train()

    model.save_pretrained(args.out)
    losses = [h["loss"] for h in trainer.state.log_history if "loss" in h]
    with open(os.path.join(args.out, "loss.json"), "w") as f:
        json.dump(dict(fraction=args.fraction, n_examples=len(rows), epochs=args.epochs,
                       losses=losses), f)
    print(f"loss: first {losses[0]:.3f} -> last {losses[-1]:.3f} · saved LoRA to {args.out}")


if __name__ == "__main__":
    main()
