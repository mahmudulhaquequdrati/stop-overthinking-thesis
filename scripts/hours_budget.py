"""Shared compute-hour pot for the 0.8B + 4B Colab runs (DECISIONS #72).

1. What problem does this solve?  Both new models share ≤150 hours. Without one ledger,
   two Colabs could burn the whole 200 and leave no buffer.
2. Why do we need it?  So each notebook can STOP before the combined total passes 150.
3. What goes in?   Path to hours_budget.json on Drive, this run's tag ("4b" or "0.8b"),
   and each stage's estimated hours.
4. What comes out? RUN / SKIP, and an updated JSON on Drive.
5. Why this way?   Colab cannot read the unit balance across sessions, so we count wall
   hours ourselves and keep a ≥50 hour buffer of the 200 unused by design.
"""

import json, os, time

CAP_HOURS = 150.0          # hard max for 0.8B + 4B combined
BUFFER_HINT = 50.0         # of the 200 bought; do not plan to spend this


def _load(path):
    if os.path.exists(path):
        return json.load(open(path))
    return dict(cap_hours=CAP_HOURS, used_hours=0.0, runs={}, note="shared pot")


def _save(path, data):
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    os.replace(tmp, path)


def left(path):
    d = _load(path)
    return float(d.get("cap_hours", CAP_HOURS)) - float(d.get("used_hours", 0.0))


def gate(path, run_tag, stage, cost_hours):
    """True = run this stage. Never lets combined used_hours + cost pass CAP_HOURS."""
    d = _load(path)
    used = float(d.get("used_hours", 0.0))
    rem = float(d.get("cap_hours", CAP_HOURS)) - used
    ok = rem - cost_hours >= 0
    print(f"[hours] {run_tag}/{stage}: costs ~{cost_hours:.1f}h · "
          f"~{rem:.1f}h left of {d.get('cap_hours', CAP_HOURS):.0f} · "
          + ("RUN" if ok else f"SKIP (would need {cost_hours - rem:.1f}h more)"))
    return ok


def start_stage(path, run_tag, stage):
    """Call when a stage actually begins. Stores wall-clock start on the ledger."""
    d = _load(path)
    runs = d.setdefault("runs", {})
    r = runs.setdefault(run_tag, dict(stages={}, hours=0.0))
    r["stages"][stage] = dict(t0=time.time(), hours=None)
    d["updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
    _save(path, d)
    print(f"[hours] {run_tag}/{stage} started · combined used {d['used_hours']:.2f}h")


def end_stage(path, run_tag, stage):
    """Call when a stage finishes. Adds wall hours to the shared pot."""
    d = _load(path)
    runs = d.setdefault("runs", {})
    r = runs.setdefault(run_tag, dict(stages={}, hours=0.0))
    info = r["stages"].get(stage) or {}
    t0 = info.get("t0", time.time())
    hours = (time.time() - t0) / 3600.0
    info["hours"] = round(hours, 3)
    info["ended"] = time.strftime("%Y-%m-%d %H:%M:%S")
    r["stages"][stage] = info
    r["hours"] = round(sum(s.get("hours") or 0 for s in r["stages"].values()), 3)
    d["used_hours"] = round(sum(v.get("hours") or 0 for v in runs.values()), 3)
    d["updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
    _save(path, d)
    rem = float(d["cap_hours"]) - float(d["used_hours"])
    print(f"[hours] {run_tag}/{stage} done in {hours:.2f}h · "
          f"run total {r['hours']:.2f}h · combined {d['used_hours']:.2f}h · "
          f"~{rem:.1f}h left of {d['cap_hours']:.0f}")
    return hours
