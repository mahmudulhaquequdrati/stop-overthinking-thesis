// Check the raw files of notebook 14 (the real thesis run) for the 4 warning signs.
//
// 1. What problem does this solve?  The last cell of notebook 14 prints averages only. Averages hide
//    WHY an answer failed (a loop? a cut-off? a bad training set?).
// 2. Why do we need it?  To tell a real result from a bug before we write the thesis.
// 3. What goes in?   The folder downloaded from Drive (results/thesis/), e.g.
//                    node scripts/check_thesis_run.js results/2026-09-24-thesis-run
// 4. What comes out? Printed tables: loops among cut-off answers, stage D (16k), the middle
//                    thinking length of finished answers, and how good the training data was.
// 5. Why this way?   Node, not Python, because the user's Windows PC has no Python. It only
//                    reads files; it never runs model-written code (CLAUDE.md §4).
const fs = require("fs"), path = require("path");
const dir = process.argv[2] || ".";
const P = f => path.join(dir, f);

function csv(f) {                       // the why_not column can hold commas and quotes
  const s = fs.readFileSync(P(f), "utf8"), rows = [];
  let row = [], cell = "", q = false;
  for (let i = 0; i < s.length; i++) {
    const c = s[i];
    if (q) { if (c == '"') { if (s[i + 1] == '"') { cell += '"'; i++ } else q = false } else cell += c }
    else if (c == '"') q = true;
    else if (c == ",") { row.push(cell); cell = "" }
    else if (c == "\n") { row.push(cell.replace(/\r$/, "")); rows.push(row); row = []; cell = "" }
    else cell += c;
  }
  if (cell || row.length) { row.push(cell); rows.push(row) }
  const [h, ...rs] = rows.filter(r => r.length > 1);
  return rs.map(v => Object.fromEntries(h.map((k, i) => [k, v[i]])));
}
const jsonl = f => fs.readFileSync(P(f), "utf8").split("\n").filter(Boolean).map(JSON.parse);
const median = a => { a = [...a].sort((x, y) => x - y); return a.length ? a[Math.floor(a.length / 2)] : "-" };

// A cut-off answer "loops" if a piece of its last 200 characters already appeared at least twice
// earlier. Rough on purpose: it misses loops with small changes, so it UNDER-counts.
function loops(t) {
  if (t.length < 400) return false;
  const probe = t.slice(-200, -80), body = t.slice(0, -200);
  let n = 0, i = -1;
  while ((i = body.indexOf(probe, i + 1)) !== -1) n++;
  return n >= 2;
}

console.log("1. Cut-off answers that are loops");
for (const f of fs.readdirSync(dir).filter(f => /^(test|x16k)-.*\.jsonl$/.test(f)).sort()) {
  const rs = jsonl(f), cut = rs.filter(r => r.hit_limit), lp = cut.filter(r => loops(r.raw_output));
  console.log(`   ${f.padEnd(24)} answers ${String(rs.length).padStart(4)}  cut off ${String(cut.length).padStart(4)}` +
              `  looping ${String(lp.length).padStart(4)} (${cut.length ? Math.round(100 * lp.length / cut.length) : 0}%)`);
}

console.log("\n2. Stage D: thinking ON, try 1, when the cut-off answers get 16,384 tokens");
for (const ds of ["he", "lcb"]) {
  const g = csv(`x16k-on16k-${ds}-graded.csv`), on1 = csv(`test-on-${ds}-graded.csv`).filter(r => r.sample_index === "0");
  const fin = g.filter(r => r.hit_limit === "False").length, ok = g.filter(r => r.passed === "True").length;
  const a = on1.filter(r => r.passed === "True").length;
  console.log(`   ${ds}: ON try 1 ${a}/${on1.length} (${(100 * a / on1.length).toFixed(1)}%). ${g.length} cut-off answers re-run: ` +
              `${fin} finished, ${ok} correct -> ${(100 * (a + ok) / on1.length).toFixed(1)}%`);
}

console.log("\n3. Middle (median) thinking of answers that FINISHED, both tries");
for (const w of ["on", "brief", "limit", "lora1", "lora2"]) {
  let s = `   ${w.padEnd(6)}`;
  for (const ds of ["he", "lcb"]) {
    const g = csv(`test-${w}-${ds}-graded.csv`), f = g.filter(r => r.hit_limit === "False");
    s += `  ${ds}: median ${String(median(f.map(r => +r.thinking_tokens))).padStart(5)}, finished ${f.length}/${g.length}`;
  }
  console.log(s);
}

console.log("\n4. LoRA-2 training data");
for (const f of ["train-mbpp-graded.csv", "train-lcb-graded.csv"]) {
  const g = csv(f), by = {};
  g.forEach(r => (by[r.task_id] = by[r.task_id] || []).push(r.passed === "True"));
  const n = Object.values(by);
  console.log(`   ${f}: problems ${n.length} | >=1 correct ${n.filter(a => a.some(Boolean)).length}` +
              ` | >=2 correct (a real choice) ${n.filter(a => a.filter(Boolean).length >= 2).length}` +
              ` | passed: ` + ["easy", "medium"].map(d => `${d} ${g.filter(r => r.difficulty === d && r.passed === "True").length}` +
              `/${g.filter(r => r.difficulty === d).length}`).join(", "));
}
for (const f of ["train-set-mbpp.jsonl", "train-set-lcb.jsonl"]) {
  const rs = jsonl(f);
  console.log(`   ${f}: ${rs.length} examples, median thinking ${median(rs.map(r => r.thinking_tokens))}`);
}
