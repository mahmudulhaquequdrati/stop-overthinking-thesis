"""Join 2B + 0.8B + 4B summaries into results/ALL-RESULTS.md.

Use:  python scripts/make_all_results.py
"""

import csv, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "ALL-RESULTS.md")


def read_summary_table(path):
    """Parse a SUMMARY.md pipe table into {way: row dict}."""
    if not os.path.exists(path):
        return {}
    rows = {}
    for line in open(path):
        if (not line.startswith("|") or "Way" in line
                or set(line.replace("|", "").replace("-", "").replace(" ", "")) == set()):
            continue
        parts = [p.strip() for p in line.strip().strip("|").split("|")]
        if len(parts) < 5 or parts[0] in ("—", "-"):
            continue
        way = parts[0]
        rows[way] = parts
    return rows


def twob_from_csv():
    path = os.path.join(ROOT, "results", "2026-09-24-thesis-run", "summary.csv")
    if not os.path.exists(path):
        return {}
    out = {}
    for r in csv.DictReader(open(path)):
        if r["group"] != "All":
            continue
        out[r["way"]] = r
    return out


def cell(v, default="—"):
    return v if v not in (None, "", "—") else default


def main():
    t2 = twob_from_csv()
    s08 = read_summary_table(os.path.join(ROOT, "results", "0.8b", "SUMMARY.md"))
    s4 = read_summary_table(os.path.join(ROOT, "results", "4b", "SUMMARY.md"))

    def acc(way, src_2b_key=None):
        k = src_2b_key or way
        a = t2.get(k, {}).get("accuracy")
        a = f"{float(a):.1f}%" if a not in (None, "") else "—"
        b = s08.get(way, [None] * 7)
        c = s4.get(way, [None] * 7)
        b_acc = b[3] if len(b) > 3 else "—"
        c_acc = c[3] if len(c) > 3 else "—"
        if b_acc in (None, "not run yet"):
            b_acc = "—"
        if c_acc in (None, "not run yet"):
            c_acc = "—"
        return a, b_acc, c_acc

    rows_acc = [
        ("Thinking OFF", "off", "off"),
        ("Thinking ON", "on", "on"),
        ("Limit 512", "limit512", "limit512"),
        ("Limit 1,024", "limit", "limit1024"),  # 2B used name "limit"
        ("Limit 2,048", "limit2048", "limit2048"),
        ("Limit 4,096", "limit4096", "limit4096"),
        ("LoRA-1", "lora1", "lora1"),
        ("LoRA-2 (2B only)", "lora2", "lora2"),
    ]

    hours_path = os.path.join(ROOT, "results", "shared", "hours_budget.json")
    hours_txt = open(hours_path).read() if os.path.exists(hours_path) else "{}"

    lines = [
        "# All results: 2B + 0.8B + 4B",
        "",
        "> **What this is:** one page that joins every main table from the three separate runs.",
        "> Each run’s raw files stay in their own folder. Rebuild with "
        "`python scripts/make_all_results.py`.",
        "",
        "| Model | Status | Separate folder |",
        "|---|---|---|",
        "| **Qwen3.5-2B** (main thesis) | ✅ done 2026-09-24 | "
        "[2026-09-24-thesis-run.md](2026-09-24-thesis-run.md) · "
        "[full-results/FULL-RESULTS.md](full-results/FULL-RESULTS.md) |",
        f"| **Qwen3.5-0.8B** | "
        f"{'✅ has graded files' if any(k for k in s08 if k not in ('—',)) else '⬜ not run yet'} | "
        "[0.8b/SUMMARY.md](0.8b/SUMMARY.md) · raw: `0.8b/raw/` |",
        f"| **Qwen3.5-4B** | "
        f"{'✅ has graded files' if any(k for k in s4 if k not in ('—',)) else '⬜ not run yet'} | "
        "[4b/SUMMARY.md](4b/SUMMARY.md) · raw: `4b/raw/` |",
        "",
        "**Shared hour pot:** ≤150 hours for 0.8B + 4B together. "
        "Ledger: [shared/hours_budget.json](shared/hours_budget.json).",
        "",
        "**Who this thesis is for:** people who run **small reasoning models for code** on a "
        "**limited GPU** (students, indie developers, one-GPU setups).",
        "",
        "---",
        "",
        "## 1. Accuracy (all problems)",
        "",
        "| Way | 2B (checked) | 0.8B | 4B |",
        "|---|---|---|---|",
    ]
    for label, k2, knew in rows_acc:
        a, b, c = acc(knew, src_2b_key=k2)
        if label.startswith("LoRA-2"):
            b, c = "n/a", "n/a"
        lines.append(f"| {label} | {a} | {b} | {c} |")

    lines += [
        "",
        "2B numbers from `results/2026-09-24-thesis-run/summary.csv`. "
        "LoRA-2 is **not** re-run on 0.8B/4B (DECISIONS #72).",
        "",
        "---",
        "",
        "## 2. Per-model summaries",
        "",
        "- [0.8b/SUMMARY.md](0.8b/SUMMARY.md)",
        "- [4b/SUMMARY.md](4b/SUMMARY.md)",
        "- [2B short](2026-09-24-thesis-run.md) · [2B full](full-results/FULL-RESULTS.md)",
        "",
        "---",
        "",
        "## 3. Shared hours ledger (raw JSON)",
        "",
        "```json",
        hours_txt.strip(),
        "```",
        "",
        "---",
        "",
        "## 4. Notebooks",
        "",
        "- [15a 0.8B](../notebooks/15a_qwen35_0_8b.ipynb) — run **second**",
        "- [15b 4B](../notebooks/15b_qwen35_4b.ipynb) — run **first**",
        "",
    ]
    open(OUT, "w").write("\n".join(lines) + "\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
