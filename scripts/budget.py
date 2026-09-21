"""Keep the thesis inside its Colab units (DECISIONS #65).

1. What problem does this solve?  69 units must finish the whole thesis. Running out halfway
   would leave no result at all.
2. Why do we need it?  So the notebook itself decides "run" or "skip" before each stage, with
   the rule fixed in advance, instead of someone guessing mid-run.
3. What goes in?   The units left when the session starts (typed once), the A100 price, and
   each stage's estimated cost.
4. What comes out? RUN / SKIP per stage, and a ledger on Drive (budget-ledger.jsonl) with the
   estimated units left after every stage.
5. Why this way?   Colab doesn't let a notebook read the unit balance, so we count time: every
   minute this session is connected costs RATE/60 units, idle or not. That is the honest
   (slightly pessimistic) count. Rule: start a stage only if units_left - cost >= FLOOR.
"""

import json, time

RATE = 5.3          # units per hour on the A100 (Colab, checked 2026-09-22)
FLOOR = 20          # always keep this much for fixing and re-running (DECISIONS #65)
_s = {}


def start(units_left, ledger):
    _s.update(t0=time.time(), units=float(units_left), ledger=ledger)
    _log("session start")
    print(f"[budget] {units_left:.1f} units left at start · A100 = {RATE}/hour · floor {FLOOR}")


def left():
    return _s["units"] - (time.time() - _s["t0"]) / 3600 * RATE


def gate(stage, cost):
    """True = run this stage. Never lets the estimate fall below FLOOR."""
    now = left()
    ok = now - cost >= FLOOR
    print(f"[budget] {stage}: costs ~{cost:.1f} · ~{now:.1f} left now · "
          + ("RUN" if ok else f"SKIP (would leave {now - cost:.1f} < {FLOOR})"))
    _log(f"{stage}: {'run' if ok else 'skip'}")
    return ok


def done(stage):
    _log(f"{stage}: done")
    print(f"[budget] {stage} done · ~{left():.1f} units left (check Colab's own number too)")


def _log(event):
    with open(_s["ledger"], "a") as f:
        f.write(json.dumps(dict(time=time.strftime("%Y-%m-%d %H:%M"), event=event,
                                units_left_est=round(left(), 2))) + "\n")
