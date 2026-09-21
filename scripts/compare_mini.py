"""Compare every way of answering on the mini-thesis test set, and print the pre-set verdicts.

1. What problem does this solve?  After the mini-thesis we must answer 3 questions with
   numbers: does training cut thinking without losing accuracy? Does it beat the free
   options? Would MORE training data help?
2. Why do we need it?  These answers decide how to spend the rest of the week (DECISIONS #60).
3. What goes in?   Graded .csv files, one per way of answering (label=path), all on the SAME
   100 test problems; and the TARGET number printed by make_train_set.py.
4. What comes out? A table, error bars, the learning curve, and the verdicts.
5. Why this way?
   - Every comparison is PAIRED: the same problems, before and after. That removes the
     "some problems are just harder" noise.
   - Error bars come from resampling the problems 2,000 times with a fixed seed.
   - Cost = ALL new tokens (thinking + answer), so thinking OFF is measured fairly too.
   - The verdict rules below were written BEFORE any result existed. Do not change them
     after seeing numbers.

THE RULES (DECISIONS #60)
  R1 training works       LoRA-100% uses <= 0.75x the tokens of thinking ON,
                          and loses at most 3 accuracy points.
  R2 beats "think briefly" LoRA-100% within 3 points of brief's accuracy, with fewer tokens.
  R3 thinking OFF enough?  OFF within 3 points of LoRA-100%, with fewer tokens
                          -> on EASY problems thinking is not needed; the thesis needs medium.
  R4 more data helps?     from LoRA-50% to LoRA-100%: tokens fall by >= 0.10 more,
                          or accuracy rises >= 3 points -> still improving -> more data helps.
                          Both change by less than 0.05 / 3 points -> flat -> it won't.
  R5 room left            LoRA-100% token ratio vs TARGET (how short the training answers
                          were). Within 0.10 of TARGET -> the LoRA learned what its examples
                          show; to cut more we need SHORTER examples (8 tries), not more.
                          Far above TARGET -> more data or epochs can still help.

Use:  python scripts/compare_mini.py --target 0.70 \
          off=A-graded.csv on=B-graded.csv brief=C-graded.csv lora25=... lora50=... lora100=...
"""

import argparse, csv, random, statistics

REF = "on"
BOOT = 2000
SEED = 3407


def load(path):
    """task_id -> (share of tries that passed, mean total tokens, mean thinking tokens, cut)."""
    by = {}
    for r in csv.DictReader(open(path)):
        by.setdefault(r["task_id"], []).append(r)
    return {t: (statistics.mean(r["passed"] == "True" for r in rs),
                statistics.mean(int(r["total_new_tokens"]) for r in rs),
                statistics.mean(int(r["thinking_tokens"]) for r in rs),
                sum(r["hit_limit"] == "True" for r in rs)) for t, rs in by.items()}


def paired(a, b, rng):
    """Accuracy difference (points) and token ratio of a vs b, with 95% error bars."""
    tasks = sorted(set(a) & set(b))
    def stats(ts):
        acc = 100 * (statistics.mean(a[t][0] for t in ts) - statistics.mean(b[t][0] for t in ts))
        ratio = sum(a[t][1] for t in ts) / max(sum(b[t][1] for t in ts), 1)
        return acc, ratio
    point = stats(tasks)
    boots = [stats([rng.choice(tasks) for _ in tasks]) for _ in range(BOOT)]
    lo_hi = lambda xs: (sorted(xs)[int(0.025 * BOOT)], sorted(xs)[int(0.975 * BOOT)])
    return point, lo_hi([x for x, _ in boots]), lo_hi([y for _, y in boots]), len(tasks)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=float, required=True, help="TARGET from make_train_set.py")
    ap.add_argument("ways", nargs="+", help="label=path-graded.csv")
    args = ap.parse_args()
    ways = {w.split("=", 1)[0]: load(w.split("=", 1)[1]) for w in args.ways}
    if REF not in ways:
        raise SystemExit(f"need a way called {REF!r} (thinking ON) to compare against")
    rng = random.Random(SEED)

    print(f"\n{'way':<9}{'problems':>9}{'accuracy':>10}{'tokens':>8}{'thinking':>10}{'cut off':>9}"
          f"   vs thinking ON: accuracy (95%)          tokens ratio (95%)")
    res = {}
    for name, w in ways.items():
        acc = 100 * statistics.mean(v[0] for v in w.values())
        tok = statistics.mean(v[1] for v in w.values())
        think = statistics.mean(v[2] for v in w.values())
        cut = sum(v[3] for v in w.values())
        line = f"{name:<9}{len(w):>9}{acc:>9.1f}%{tok:>8.0f}{think:>10.0f}{cut:>9}"
        if name != REF:
            (d, r), (dlo, dhi), (rlo, rhi), n = paired(w, ways[REF], rng)
            line += f"   {d:+5.1f} pts [{dlo:+5.1f}, {dhi:+5.1f}]   x{r:.2f} [{rlo:.2f}, {rhi:.2f}]"
            res[name] = dict(acc=acc, tok=tok, d=d, r=r)
        else:
            res[name] = dict(acc=acc, tok=tok, d=0.0, r=1.0)
        print(line)

    print("\nLEARNING CURVE (LoRA trained on more and more of the same examples)")
    curve = [(k, res[k]) for k in ("lora25", "lora50", "lora100") if k in res]
    for k, v in curve:
        print(f"  {k:<8} accuracy {v['acc']:5.1f}%   tokens x{v['r']:.2f} of thinking ON")
    print(f"  TARGET   x{args.target:.2f}  (how short the training answers were)")

    print("\nVERDICTS (rules fixed before the run, DECISIONS #60)")
    L = res.get("lora100")
    if not L:
        raise SystemExit("  need lora100 for the verdicts")
    say = lambda tag, ok, text: print(f"  {tag} {'YES' if ok else 'NO ':<3} {text}")
    say("R1", L["r"] <= 0.75 and L["d"] >= -3,
        f"training works: tokens x{L['r']:.2f} (need <= 0.75), accuracy {L['d']:+.1f} pts (need >= -3)")
    if "brief" in res:
        B = res["brief"]
        say("R2", L["acc"] >= B["acc"] - 3 and L["tok"] < B["tok"],
            f"beats 'think briefly': {L['acc']:.1f}% vs {B['acc']:.1f}%, {L['tok']:.0f} vs {B['tok']:.0f} tokens")
    if "off" in res:
        O = res["off"]
        say("R3", O["acc"] >= L["acc"] - 3 and O["tok"] < L["tok"],
            f"thinking OFF is enough on easy problems: {O['acc']:.1f}% vs {L['acc']:.1f}% "
            f"(if YES: the thesis needs medium problems to show a difference)")
    if "lora50" in res:
        M = res["lora50"]
        more_cut, more_acc = M["r"] - L["r"], L["acc"] - M["acc"]
        if more_cut >= 0.10 or more_acc >= 3:
            v = "STILL IMPROVING -> more training data should help"
        elif abs(more_cut) < 0.05 and abs(more_acc) < 3:
            v = "FLAT -> more of the same data will probably not help"
        else:
            v = "UNCLEAR -> too small to tell; do not decide on data size from this"
        print(f"  R4     50% -> 100%: tokens {more_cut:+.2f} lower, accuracy {more_acc:+.1f} pts: {v}")
    gap = L["r"] - args.target
    print(f"  R5     LoRA x{L['r']:.2f} vs TARGET x{args.target:.2f} (gap {gap:+.2f}): " +
          ("reached what the examples show -> to cut more, make SHORTER examples (8 tries)"
           if gap <= 0.10 else "not there yet -> more data or more epochs can still help"))
    print("\n  Honest limit: 100 easy problems, 1 try each. Look at the error bars before "
          "believing any difference smaller than them.")


if __name__ == "__main__":
    main()
