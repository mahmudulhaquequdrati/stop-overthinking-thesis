"""Draw the pilot figure: tokens per problem, thinking ON vs OFF, and who passed.

1. What problem does this solve?  A table of 60 rows is hard to read. One picture shows
   the whole pilot: how much longer thinking ON is, and where each way of answering failed.
2. Why do we need it?  It is the first figure of the thesis, and it explains the result
   in one look.
3. What goes in?   results/<name>-graded.csv from scripts/grade_humaneval.py.
4. What comes out? results/figures/<name>.png (and .pdf for the thesis).
5. Why this way?   A "dumbbell": one line per problem, a dot for each way of answering.
   The gap between the dots IS the waste. Colors are a colorblind-safe pair, and pass/fail
   uses a different SHAPE as well, so the figure also works in black and white.
"""

import argparse, csv, os, statistics as st

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

OFF_COLOR, ON_COLOR = "#2a78d6", "#eb6834"   # validated pair (dataviz skill)
INK, MUTED, GRID = "#1a1a19", "#5c5b55", "#e3e2dd"


def load(path):
    rows = list(csv.DictReader(open(path)))
    by_task = {}
    for r in rows:
        r["total_new_tokens"] = int(r["total_new_tokens"])
        r["thinking_tokens"] = int(r["thinking_tokens"])
        r["passed"] = r["passed"] == "True"
        r["hit_limit"] = r["hit_limit"] == "True"
        by_task.setdefault(r["task_id"], {})[r["policy"]] = r
    return rows, by_task


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graded", default="results/2026-09-20-pilot-e2b-humanevalplus-graded.csv")
    ap.add_argument("--out", default="results/figures/2026-09-20-pilot-tokens")
    ap.add_argument("--title", default="Gemma-4-E2B on 30 HumanEval problems (pilot, 2026-09-20)")
    args = ap.parse_args()
    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    rows, by_task = load(args.graded)
    tasks = sorted(by_task, key=lambda t: by_task[t]["thinking_on"]["total_new_tokens"])

    fig, (ax, ax2) = plt.subplots(
        1, 2, figsize=(11, 8), gridspec_kw={"width_ratios": [3, 1], "wspace": 0.35})

    # ---- left: one line per problem, a dot for each way of answering -------------
    for i, t in enumerate(tasks):
        off, on = by_task[t]["thinking_off"], by_task[t]["thinking_on"]
        ax.plot([off["total_new_tokens"], on["total_new_tokens"]], [i, i],
                color=GRID, linewidth=2, zorder=1, solid_capstyle="round")
        for r, color in ((off, OFF_COLOR), (on, ON_COLOR)):
            ax.scatter(r["total_new_tokens"], i, s=70 if r["passed"] else 110,
                       marker="o" if r["passed"] else "X", color=color,
                       edgecolors="white", linewidths=1.2, zorder=2)

    ax.set_yticks(range(len(tasks)))
    ax.set_yticklabels([t.replace("HumanEval/", "#") for t in tasks], fontsize=8, color=MUTED)
    ax.set_ylim(-1, len(tasks))
    ax.set_xlabel("tokens the model wrote (thinking + answer)", fontsize=10, color=MUTED)
    ax.set_title(args.title, fontsize=12, color=INK, loc="left", pad=14)
    ax.axvline(2048, color=MUTED, linestyle=":", linewidth=1.2, zorder=0)
    ax.text(2048, len(tasks) - 0.5, " our token limit", fontsize=8, color=MUTED, va="top")
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=MUTED, length=0)

    ax.legend(handles=[
        Line2D([], [], marker="o", color=OFF_COLOR, linestyle="", markersize=8,
               markeredgecolor="white", label="thinking OFF — passed"),
        Line2D([], [], marker="o", color=ON_COLOR, linestyle="", markersize=8,
               markeredgecolor="white", label="thinking ON — passed"),
        Line2D([], [], marker="X", color=MUTED, linestyle="", markersize=9,
               markeredgecolor="white", label="failed the tests"),
    ], loc="lower right", frameon=False, fontsize=9, labelcolor=MUTED)

    # ---- right: the two summary numbers ----------------------------------------
    summary = {}
    for policy in ("thinking_off", "thinking_on"):
        rs = [r for r in rows if r["policy"] == policy]
        summary[policy] = (100 * sum(r["passed"] for r in rs) / len(rs),
                           st.median([r["total_new_tokens"] for r in rs]))

    bars = ax2.bar([0.8, 1.2], [summary["thinking_off"][0], summary["thinking_on"][0]],
                   width=0.32, color=[OFF_COLOR, ON_COLOR], zorder=2)
    for b, v in zip(bars, [summary["thinking_off"][0], summary["thinking_on"][0]]):
        ax2.text(b.get_x() + b.get_width() / 2, v + 2, f"{v:.0f}%", ha="center",
                 fontsize=10, color=INK)
    ax2.set_xticks([0.8, 1.2]); ax2.set_xticklabels(["OFF", "ON"], fontsize=9, color=MUTED)
    ax2.set_ylim(0, 112); ax2.set_xlim(0.55, 1.45)
    ax2.set_title("passed the tests", fontsize=10, color=INK, loc="left", pad=10)
    ax2.set_ylabel("% of 30 problems", fontsize=9, color=MUTED)
    ax2.grid(axis="y", color=GRID, linewidth=0.8); ax2.set_axisbelow(True)
    for side in ("top", "right"):
        ax2.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax2.spines[side].set_color(GRID)
    ax2.tick_params(colors=MUTED, length=0)

    ratio = summary["thinking_on"][1] / summary["thinking_off"][1]
    note = "\n".join([                       # short lines: the right column is narrow
        "middle number of tokens",
        f"   OFF {summary['thinking_off'][1]:.0f}  ·  ON {summary['thinking_on'][1]:.0f}",
        f"   → ON writes {ratio:.1f}× more",
        "",
        "4 ON answers and 1 OFF answer",
        "hit the token limit and were",
        "cut off, which is why some of",
        "them failed. The next run uses",
        "a higher limit for both.",
    ])
    fig.subplots_adjust(left=0.08, right=0.98, top=0.93, bottom=0.07)
    ax2.set_position([0.74, 0.46, 0.22, 0.44])          # keep the lower right free for the note
    fig.text(0.74, 0.36, note, fontsize=9, color=MUTED, va="top", ha="left", linespacing=1.7)
    for ext in ("png", "pdf"):
        fig.savefig(f"{args.out}.{ext}", dpi=200, facecolor="white")
    print("saved", args.out + ".png", "and .pdf")


if __name__ == "__main__":
    main()
