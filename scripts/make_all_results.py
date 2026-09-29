"""Join 2B + 0.8B + 4B summaries into results/ALL-RESULTS.md.

Use:  python scripts/make_all_results.py
"""

import csv, os

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


def status_line(label, folder_summary_rows, done_hint):
    real = any(len(parts) > 3 and "%" in str(parts[3]) for parts in folder_summary_rows.values())
    if real:
        return f"| **{label}** | ✅ has graded files | {done_hint} |"
    return f"| **{label}** | ⬜ not run yet | {done_hint} |"


def main():
    t2 = twob_from_csv()
    s08 = read_summary_table(os.path.join(ROOT, "results", "0.8b", "SUMMARY.md"))
    s4 = read_summary_table(os.path.join(ROOT, "results", "4b", "SUMMARY.md"))
    s2b512 = read_summary_table(os.path.join(ROOT, "results", "2b-limit512", "SUMMARY.md"))
    s2b2048 = read_summary_table(os.path.join(ROOT, "results", "2b-limit2048", "SUMMARY.md"))
    # Fill 2B extra limits from dedicated fill-in runs (not in main thesis summary.csv).
    t2 = dict(t2)
    for way, src in (("limit512", s2b512), ("limit2048", s2b2048)):
        if way in src and len(src[way]) > 3:
            acc_w = src[way][3]
            if isinstance(acc_w, str) and "%" in acc_w:
                t2[way] = {"accuracy": acc_w.replace("%", "").strip(), "way": way}

    def acc(way, src_2b_key=None):
        k = src_2b_key or way
        a = t2.get(k, {}).get("accuracy")
        a = f"{float(a):.1f}%" if a not in (None, "") else "—"
        b = s08.get(way, [None] * 7)
        c = s4.get(way, [None] * 7)
        b_acc = b[3] if len(b) > 3 else "—"
        c_acc = c[3] if len(c) > 3 else "—"
        if not (isinstance(b_acc, str) and "%" in b_acc):
            b_acc = "—"
        if not (isinstance(c_acc, str) and "%" in c_acc):
            c_acc = "—"
        return a, b_acc, c_acc

    rows_acc = [
        ("Thinking OFF", "off", "off"),
        ("Thinking ON", "on", "on"),
        ("Limit 512", "limit512", "limit512"),
        ("Limit 1,024", "limit", "limit1024"),
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
        status_line("Qwen3.5-0.8B", s08, "[0.8b/SUMMARY.md](0.8b/SUMMARY.md) · raw: `0.8b/raw/`"),
        status_line("Qwen3.5-4B", s4, "[4b/SUMMARY.md](4b/SUMMARY.md) · raw: `4b/raw/`"),
        "| **2B limit512 fill-in** | ✅ done (45.1%) | "
        "[2b-limit512/SUMMARY.md](2b-limit512/SUMMARY.md) · raw: `2b-limit512/raw/` |",
        "| **2B limit2048 fill-in** | ✅ done (46.6%, 1 try) | "
        "[2b-limit2048/SUMMARY.md](2b-limit2048/SUMMARY.md) · raw: `2b-limit2048/raw/` |",
        "",
        "**Tries (table captions):** 2B main and 4B = **2 tries**; lean 0.8B = **1 try**; "
        "2B limit512 fill-in = **2 tries**; 2B limit2048 fill-in = **1 try** (#83–#84).",
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
        # Annotate 1-try fill-in in the 2B cell for limit2048
        if knew == "limit2048" and a != "—" and "1 try" not in a:
            a = f"{a}*"
        lines.append(f"| {label} | {a} | {b} | {c} |")

    lines += [
        "",
        "\\* 2B limit2048 = **1 try** (lean fill-in). Other 2B main numbers = 2 tries.",
        "",
        "2B main numbers from `results/2026-09-24-thesis-run/summary.csv`. "
        "2B **limit512 = 45.1%** (`results/2b-limit512/`, #82). "
        "2B **limit2048 = 46.6%** (`results/2b-limit2048/`, #84). "
        "LoRA-2 is **not** re-run on 0.8B/4B (DECISIONS #72).",
        "",
        "**0.8B headline (checked, 1 try):** best free way = **OFF → 20.5%**. "
        "ON only 7.3% (78% cut off). limit512 17.5% · LoRA-1 17.9%. "
        "On this tiny model, **switching thinking OFF beats limits and LoRA**.",
        "",
        "**2B headline (checked):** best free way = **limit 1024 → 49.8%** (2 tries). "
        "Curve: limit512 45.1% → limit1024 **49.8%** → limit2048 46.6% (1 try). "
        "**Peaks at 1024** — longer budget did not help. LoRA did not beat limit 1024.",
        "",
        "**4B headline (checked, 2 tries):** best free way = **limit 2048 → 78.2%**. "
        "OFF 69.7% beats ON 64.3%. LoRA-1 69.9% does **not** beat the limits.",
        "",
        "**Join story:** [SIZE-COMPARISON.md](SIZE-COMPARISON.md).",
        "",
        "---",
        "",
        "## 2. Per-model summaries",
        "",
        "- [0.8b/SUMMARY.md](0.8b/SUMMARY.md) · [0.8b/RUN.md](0.8b/RUN.md)",
        "- [4b/SUMMARY.md](4b/SUMMARY.md)",
        "- [2B short](2026-09-24-thesis-run.md) · [2B full](full-results/FULL-RESULTS.md)",
        "- [2b-limit512/SUMMARY.md](2b-limit512/SUMMARY.md) · [2b-limit512/RUN.md](2b-limit512/RUN.md)",
        "- [2b-limit2048/SUMMARY.md](2b-limit2048/SUMMARY.md) · [2b-limit2048/RUN.md](2b-limit2048/RUN.md)",
        "- [SIZE-COMPARISON.md](SIZE-COMPARISON.md)",
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
        "- [15a 0.8B](../notebooks/15a_qwen35_0_8b.ipynb) — ✅ lean run done",
        "- [15b 4B](../notebooks/15b_qwen35_4b.ipynb) — ✅ done",
        "- [16 2B limit512](../notebooks/16_qwen35_2b_limit512.ipynb) — ✅ 45.1%",
        "- [17 2B limit2048 lean](../notebooks/17_qwen35_2b_limit2048.ipynb) — ✅ 46.6% (1 try)",
        "",
        "Rebuilt by `scripts/make_all_results.py`.",
        "",
    ]
    open(OUT, "w").write("\n".join(lines) + "\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
