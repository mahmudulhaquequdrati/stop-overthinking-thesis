// Build the full results report of the real thesis run (notebook 14): text, tables, charts.
//
// 1. What problem does this solve?  The notebook prints only averages. To write the thesis we need
//    every number: which problems were used, what each way solved, how long it took, and charts.
// 2. Why do we need it?  One place to copy from when we write the paper, and every number in it
//    comes from the raw files, so nothing is typed by hand.
// 3. What goes in?   The Drive folder, downloaded:  results/2026-09-24-thesis-run/
//                    node scripts/make_full_results.js
// 4. What comes out? results/full-results/FULL-RESULTS.md, figures/*.svg (10 charts), tables/*.csv.
// 5. Why this way?   Node, because the user's PC has no Python. Charts are plain SVG files, so the
//                    .md file shows them in VS Code and on GitHub with no extra tools.
//                    It only reads files; it never runs model-written code (CLAUDE.md §4).
const fs = require("fs"), path = require("path");
const RUN = "results/2026-09-24-thesis-run", OUT = "results/full-results";
fs.mkdirSync(`${OUT}/figures`, { recursive: true }); fs.mkdirSync(`${OUT}/tables`, { recursive: true });

// ---------- reading ----------
function csv(f) {                       // why_not can hold commas and quotes
  const s = fs.readFileSync(path.join(RUN, f), "utf8"), rows = [];
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
const jsonl = f => fs.readFileSync(path.join(RUN, f), "utf8").split("\n").filter(Boolean).map(JSON.parse);
const mean = a => a.length ? a.reduce((x, y) => x + y, 0) / a.length : 0;
const median = a => { a = [...a].sort((x, y) => x - y); return a.length ? a[Math.floor(a.length / 2)] : 0 };
const pct = (a, b) => b ? 100 * a / b : 0;
const f1 = x => x.toFixed(1), n0 = x => Math.round(x).toLocaleString("en-US");
const idNum = id => { const m = id.match(/(\d+)/); return m ? +m[1] : 0 };

// A cut-off answer "loops" if a piece of its last 200 characters already appeared at least twice
// earlier. Rough on purpose: it misses loops with small changes, so it UNDER-counts.
function loops(t) {
  if (t.length < 400) return false;
  const probe = t.slice(-200, -80), body = t.slice(0, -200);
  let n = 0, i = -1;
  while ((i = body.indexOf(probe, i + 1)) !== -1) n++;
  return n >= 2;
}

// Colour follows the way in every chart. Order validated with the dataviz palette checker (light).
const WAYS = ["on", "off", "brief", "limit", "lora1", "lora2"];
const NAME = { on: "Thinking ON", off: "Thinking OFF", brief: "Think briefly", limit: "Limit 1,024",
               lora1: "LoRA-1", lora2: "LoRA-2 (main)" };
const COL = { on: "#2a78d6", off: "#eb6834", brief: "#1baf7a", limit: "#eda100", lora1: "#e87ba4", lora2: "#008300" };
const GROUPS = ["All", "HumanEval+", "LCB easy", "LCB medium"];
const DS = { he: "HumanEval+", lcb: "LiveCodeBench" };

// ---------- the test answers ----------
const A = [];                                            // one row per answer
for (const w of WAYS) for (const ds of ["he", "lcb"]) {
  const raw = new Map(jsonl(`test-${w}-${ds}.jsonl`).map(r => [`${r.task_id}|${r.sample_index}`, r]));
  for (const g of csv(`test-${w}-${ds}-graded.csv`)) {
    const r = raw.get(`${g.task_id}|${g.sample_index}`);
    const cut = g.hit_limit === "True";
    A.push({ way: w, ds, id: g.task_id, try: +g.sample_index, diff: g.difficulty,
             group: ds === "he" ? "HumanEval+" : g.difficulty === "easy" ? "LCB easy" : "LCB medium",
             pass: g.passed === "True", think: +g.thinking_tokens, total: +g.total_new_tokens, cut,
             loop: cut && r ? loops(r.raw_output) : false, why: g.why_not || "",
             sec: r ? r.batch_seconds / r.batch_size : 0, when: r ? r.timestamp : "" });
  }
}
const inGroup = (a, g) => g === "All" || a.group === g;
const S = {};                                            // stats per way per group
for (const w of WAYS) for (const g of GROUPS) {
  const xs = A.filter(a => a.way === w && inGroup(a, g)), fin = xs.filter(a => !a.cut);
  S[w + g] = { n: xs.length, pass: xs.filter(a => a.pass).length, acc: pct(xs.filter(a => a.pass).length, xs.length),
    think: mean(xs.map(a => a.think)), total: mean(xs.map(a => a.total)), ans: mean(xs.map(a => a.total - a.think)),
    medThink: median(xs.map(a => a.think)), medFinThink: median(fin.map(a => a.think)), fin: fin.length,
    cut: xs.filter(a => a.cut).length, loop: xs.filter(a => a.loop).length, problems: new Set(xs.map(a => a.id)).size };
}
// the notebook's own numbers, with the paired error bars
const SUM = {};
for (const r of csv("summary.csv")) SUM[r.way + r.group] = r;
const mismatch = [];
for (const w of WAYS) for (const g of GROUPS)
  if (Math.abs(S[w + g].acc - +SUM[w + g].accuracy) > 0.06) mismatch.push(`${w} ${g}: ${f1(S[w + g].acc)} vs ${SUM[w + g].accuracy}`);
if (mismatch.length) { console.error("MISMATCH with summary.csv:", mismatch); process.exit(1) }

// per problem: how many of the 2 tries each way solved
const P = new Map();
for (const a of A) {
  if (!P.has(a.id)) P.set(a.id, { id: a.id, ds: a.ds, diff: a.diff, group: a.group, s: {} });
  const p = P.get(a.id); p.s[a.way] = (p.s[a.way] || 0) + (a.pass ? 1 : 0);
}
const probs = [...P.values()].sort((x, y) => x.ds.localeCompare(y.ds) || idNum(x.id) - idNum(y.id) || x.id.localeCompare(y.id));

// stage D: try-1 thinking-ON answers that were cut off, re-run with 16,384 tokens
const D = {};
for (const ds of ["he", "lcb"]) {
  const g = csv(`x16k-on16k-${ds}-graded.csv`);
  const on1 = A.filter(a => a.way === "on" && a.ds === ds && a.try === 0);
  D[ds] = { rerun: g.length, fin: g.filter(r => r.hit_limit === "False").length, ok: g.filter(r => r.passed === "True").length,
            okIds: new Set(g.filter(r => r.passed === "True").map(r => r.task_id)), rerunIds: new Set(g.map(r => r.task_id)),
            n: on1.length, on1: on1.filter(a => a.pass).length,
            try1: Object.fromEntries(WAYS.map(w => [w, A.filter(a => a.way === w && a.ds === ds && a.try === 0 && a.pass).length])) };
  const rr = jsonl(`x16k-on16k-${ds}.jsonl`);
  D[ds].sec = rr.reduce((s, r) => s + r.batch_seconds / r.batch_size, 0);
  D[ds].loops = rr.filter(r => r.hit_limit && loops(r.raw_output)).length;
}

// ---------- the training data ----------
const TR = [];
for (const [pool, f, setf] of [["MBPP+", "train-mbpp-graded.csv", "train-set-mbpp.jsonl"], ["LiveCodeBench (older)", "train-lcb-graded.csv", "train-set-lcb.jsonl"]]) {
  const kept = new Map(jsonl(setf).map(r => [r.task_id, r]));
  const by = new Map();
  for (const r of csv(f)) {
    if (!by.has(r.task_id)) by.set(r.task_id, { id: r.task_id, pool, diff: r.difficulty, tries: 0, ok: 0, okThink: [] });
    const t = by.get(r.task_id); t.tries++;
    if (r.passed === "True") { t.ok++; t.okThink.push(+r.thinking_tokens) }
  }
  for (const t of by.values()) {
    const k = kept.get(t.id);
    t.kept = !!k; t.keptThink = k ? k.thinking_tokens : null;
    t.q = k ? k.question.replace(/\s+/g, " ").trim().slice(0, 70) : "";
    TR.push(t);
  }
}
TR.sort((x, y) => x.pool.localeCompare(y.pool) || idNum(x.id) - idNum(y.id) || x.id.localeCompare(y.id));
const trStats = pool => {
  const t = TR.filter(x => x.pool === pool);
  return { n: t.length, one: t.filter(x => x.ok >= 1).length, two: t.filter(x => x.ok >= 2).length,
           kept: t.filter(x => x.kept).length, answers: t.reduce((s, x) => s + x.tries, 0), okAns: t.reduce((s, x) => s + x.ok, 0),
           easy: t.filter(x => x.diff === "easy").length, medium: t.filter(x => x.diff === "medium").length,
           okEasy: t.filter(x => x.diff === "easy").reduce((s, x) => s + x.ok, 0), okMed: t.filter(x => x.diff === "medium").reduce((s, x) => s + x.ok, 0),
           medKept: median(t.filter(x => x.kept).map(x => x.keptThink)),
           medAllOk: median(t.flatMap(x => x.okThink)) };
};
const TM = trStats("MBPP+"), TL = trStats("LiveCodeBench (older)");
const excluded = TR.filter(x => x.ok >= 1 && !x.kept);
const TGT = { mbpp: JSON.parse(fs.readFileSync(`${RUN}/train-set-mbpp-stats.json`)), lcb: JSON.parse(fs.readFileSync(`${RUN}/train-set-lcb-stats.json`)) };
const LOSS = JSON.parse(fs.readFileSync(`${RUN}/lora/lora2/loss.json`));
const LEDGER = fs.readFileSync(`${RUN}/budget-ledger.jsonl`, "utf8").trim().split("\n").map(JSON.parse);
const trainSec = f => jsonl(f).reduce((s, r) => s + r.batch_seconds / r.batch_size, 0);
const TSEC = { mbpp: trainSec("train-mbpp.jsonl"), lcb: trainSec("train-lcb.jsonl") };

// ---------- timing ----------
const UNITS_PER_H = 5.3;                                 // Colab A100 price (DECISIONS #65)
const T = {};
for (const w of WAYS) for (const ds of ["he", "lcb"]) T[w + ds] = A.filter(a => a.way === w && a.ds === ds).reduce((s, a) => s + a.sec, 0);
const wayMin = w => (T[w + "he"] + T[w + "lcb"]) / 60;
const testMin = WAYS.reduce((s, w) => s + wayMin(w), 0);

// ---------- SVG charts ----------
const C = { bg: "#fcfcfb", ink: "#0b0b0b", ink2: "#52514e", mute: "#8a8984", grid: "#e6e5e0" };
const FONT = `font-family="system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"`;
const esc = s => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;");
const txt = (x, y, s, o = {}) => `<text x="${x}" y="${y}" font-size="${o.size || 12}" fill="${o.fill || C.ink2}" text-anchor="${o.anchor || "start"}"${o.weight ? ` font-weight="${o.weight}"` : ""}${o.rot ? ` transform="rotate(${o.rot} ${x} ${y})"` : ""}>${esc(s)}</text>`;
function svg(w, h, title, sub, body) {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" ${FONT}>
<title>${esc(title)}</title><rect width="${w}" height="${h}" fill="${C.bg}"/>
${txt(20, 28, title, { size: 16, fill: C.ink, weight: 600 })}${sub ? txt(20, 48, sub, { size: 12 }) : ""}
${body}</svg>`;
}
// a column that grows up from the baseline, 4px round top, square bottom
function col(x, base, w, h, fill, tip) {
  if (h <= 0) return "";
  const r = Math.min(4, h, w / 2), y = base - h;
  return `<path d="M${x},${base}V${y + r}Q${x},${y} ${x + r},${y}H${x + w - r}Q${x + w},${y} ${x + w},${y + r}V${base}Z" fill="${fill}"><title>${esc(tip)}</title></path>`;
}
// a bar that grows right from x0, 4px round end
function bar(x0, y, len, h, fill, tip, roundEnd = true) {
  if (len <= 0) return "";
  const r = roundEnd ? Math.min(4, len, h / 2) : 0, x = x0 + len;
  return `<path d="M${x0},${y}H${x - r}Q${x},${y} ${x},${y + r}V${y + h - r}Q${x},${y + h} ${x - r},${y + h}H${x0}Z" fill="${fill}"><title>${esc(tip)}</title></path>`;
}
function yAxis(x0, x1, base, top, max, step, fmt = v => v) {
  let s = "";
  for (let v = 0; v <= max + 1e-9; v += step) {
    const y = base - (v / max) * (base - top);
    s += `<line x1="${x0}" x2="${x1}" y1="${y}" y2="${y}" stroke="${C.grid}" stroke-width="1"/>` + txt(x0 - 8, y + 4, fmt(v), { anchor: "end", size: 11 });
  }
  return s;
}
function legend(x, y, items) {
  let s = "", cx = x;
  for (const [label, fill, kind] of items) {
    s += kind === "line" ? `<line x1="${cx}" x2="${cx + 16}" y1="${y - 4}" y2="${y - 4}" stroke="${fill}" stroke-width="2" stroke-linecap="round"/>`
                         : `<rect x="${cx}" y="${y - 10}" width="12" height="12" rx="3" fill="${fill}"/>`;
    s += txt(cx + (kind === "line" ? 22 : 18), y, label, { size: 12, fill: C.ink });
    cx += (kind === "line" ? 30 : 26) + label.length * 6.6;
  }
  return s;
}
const save = (name, s) => fs.writeFileSync(`${OUT}/figures/${name}`, s);

// Fig 1: accuracy by group, one column per way
{
  const W = 900, H = 420, L = 60, R = 20, top = 90, base = 360, gw = (W - L - R) / GROUPS.length, bw = 18, gap = 2;
  let b = yAxis(L, W - R, base, top, 70, 10, v => v + "%") + legend(L, 72, WAYS.map(w => [NAME[w], COL[w]]));
  GROUPS.forEach((g, gi) => {
    const x0 = L + gi * gw + (gw - WAYS.length * (bw + gap)) / 2;
    WAYS.forEach((w, wi) => {
      const v = S[w + g].acc;
      b += col(x0 + wi * (bw + gap), base, bw, (v / 70) * (base - top), COL[w], `${NAME[w]} · ${g}: ${f1(v)}% (${S[w + g].pass}/${S[w + g].n})`);
    });
    b += txt(L + gi * gw + gw / 2, base + 22, `${g} (${S["on" + g].problems})`, { anchor: "middle", fill: C.ink, size: 13 });
  });
  b += `<line x1="${L}" x2="${W - R}" y1="${base}" y2="${base}" stroke="${C.mute}" stroke-width="1"/>`;
  save("fig1-accuracy-by-group.svg", svg(W, H, "Accuracy of each way, by problem group", "Share of answers that pass the benchmark tests · 2 tries per problem · number of problems in brackets", b));
}

// Fig 2: accuracy vs tokens (all 234). One ink colour; the label names the way (6 series is too many hues for a scatter).
{
  const W = 900, H = 460, L = 70, R = 40, top = 70, base = 400, xmax = 6000, ymax = 60;
  const X = v => L + (v / xmax) * (W - L - R), Y = v => base - (v / ymax) * (base - top);
  let b = yAxis(L, W - R, base, top, ymax, 10, v => v + "%");
  for (let v = 0; v <= xmax; v += 1000) b += txt(X(v), base + 18, n0(v), { anchor: "middle", size: 11 });
  b += txt((L + W - R) / 2, base + 42, "average tokens written per answer (thinking + answer)", { anchor: "middle", size: 12 });
  b += txt(18, (top + base) / 2, "accuracy", { anchor: "middle", size: 12, rot: -90 });
  const off = { on: [10, 20], off: [10, 16], brief: [-10, -12, "end"], limit: [10, -10], lora1: [-10, 20, "end"], lora2: [10, -8] };
  for (const w of WAYS) {
    const s = S[w + "All"], x = X(s.total), y = Y(s.acc), [dx, dy, an] = off[w];
    b += `<circle cx="${x}" cy="${y}" r="6" fill="${C.ink}" stroke="${C.bg}" stroke-width="2"><title>${esc(`${NAME[w]}: ${f1(s.acc)}%, ${n0(s.total)} tokens`)}</title></circle>`;
    b += txt(x + dx, y + dy, `${NAME[w]} · ${f1(s.acc)}% · ${n0(s.total)}`, { size: 12, fill: C.ink, anchor: an || "start" });
  }
  save("fig2-accuracy-vs-tokens.svg", svg(W, H, "Accuracy against cost, all 234 problems", "Up = more correct · left = fewer tokens (cheaper, faster). Best is top-left.", b));
}

// Fig 3: what happened to each answer: finished / cut off in a loop / cut off, no loop
{
  const W = 900, H = 330, L = 130, R = 60, top = 90, bh = 22, rowH = 36, len = W - L - R;
  const seg = [["finished", "#b7d3f6"], ["cut off, not a loop", "#5598e7"], ["cut off in a loop", "#104281"]];
  let b = legend(L, 72, seg.map(([l, c]) => [l, c]));
  WAYS.forEach((w, i) => {
    const s = S[w + "All"], y = top + i * rowH, parts = [s.fin, s.cut - s.loop, s.loop];
    let x = L;
    parts.forEach((p, j) => {
      const l = (p / s.n) * len, last = j === 2 || parts.slice(j + 1).every(q => q === 0);
      b += bar(x, y, Math.max(0, l - (last ? 0 : 2)), bh, seg[j][1], `${NAME[w]}: ${seg[j][0]} ${p}/${s.n} (${f1(pct(p, s.n))}%)`, last);
      x += l;
    });
    b += txt(L - 10, y + 16, NAME[w], { anchor: "end", fill: C.ink, size: 13 });
    b += txt(W - R + 8, y + 16, `${f1(pct(s.cut, s.n))}% cut`, { size: 11 });
  });
  save("fig3-cutoffs-and-loops.svg", svg(W, H, "What happened to every answer (all 234 problems, 2 tries)", "Cut off = hit the token limit before finishing (counts as wrong). Loop = repeats the same lines.", b));
}

// Fig 4: how long the thinking was, HumanEval+ — share of answers whose thinking stopped within N tokens
{
  const W = 900, H = 450, L = 70, R = 150, top = 95, base = 390, xmax = 4096;
  const X = v => L + (v / xmax) * (W - L - R), Y = v => base - (v / 100) * (base - top);
  const ws = ["on", "limit", "lora1", "lora2"];
  let b = yAxis(L, W - R, base, top, 100, 20, v => v + "%") + legend(L, 74, ws.map(w => [NAME[w], COL[w], "line"]));
  for (let v = 0; v <= 4096; v += 1024) b += txt(X(v), base + 18, n0(v), { anchor: "middle", size: 11 });
  b += txt((L + W - R) / 2, base + 42, "thinking tokens", { anchor: "middle", size: 12 });
  for (const w of ws) {
    const xs = A.filter(a => a.way === w && a.ds === "he").map(a => a.cut ? Infinity : a.think).sort((p, q) => p - q);
    let d = "";
    for (let v = 0; v <= xmax; v += 32) {
      const share = pct(xs.filter(t => t <= v).length, xs.length);
      d += `${v ? "L" : "M"}${X(v).toFixed(1)},${Y(share).toFixed(1)}`;
    }
    const end = pct(xs.filter(t => t <= xmax).length, xs.length);
    b += `<path d="${d}" fill="none" stroke="${COL[w]}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"><title>${esc(NAME[w])}</title></path>`;
    b += `<circle cx="${X(xmax)}" cy="${Y(end)}" r="4" fill="${COL[w]}" stroke="${C.bg}" stroke-width="2"/>`;
  }
  // end labels with leader lines, sorted so they don't collide
  const ends = ws.map(w => { const xs = A.filter(a => a.way === w && a.ds === "he"); return [w, pct(xs.filter(a => !a.cut).length, xs.length)] }).sort((p, q) => q[1] - p[1]);
  ends.forEach(([w, e], i) => {
    const ly = top + 40 + i * 22;
    b += `<line x1="${X(xmax) + 6}" y1="${Y(e)}" x2="${W - R + 14}" y2="${ly - 4}" stroke="${C.mute}" stroke-width="1"/>`;
    b += txt(W - R + 18, ly, `${NAME[w]} ${f1(e)}%`, { size: 12, fill: C.ink });
  });
  save("fig4-thinking-length-humaneval.svg", svg(W, H, "How long the model thinks, HumanEval+ (164 problems × 2 tries)", "Share of answers that finished thinking within N tokens. The rest never finished (cut off at 4,096).", b));
}

// Fig 5: per problem, better or worse than thinking ON (diverging)
{
  const W = 900, H = 320, mid = 480, top = 90, bh = 22, rowH = 40;
  const ws = WAYS.filter(w => w !== "on");
  const wl = ws.map(w => { let win = 0, loss = 0; for (const p of probs) { if (p.s[w] > p.s.on) win++; else if (p.s[w] < p.s.on) loss++; } return [win, loss] });
  const scale = Math.min((mid - 190) / Math.max(...wl.map(x => x[1])), (W - mid - 60) / Math.max(...wl.map(x => x[0])));
  let b = legend(140, 72, [["worse than ON", "#e34948"], ["better than ON", "#2a78d6"]]);
  ws.forEach((w, i) => {
    const y = top + i * rowH;
    let win = 0, loss = 0;
    for (const p of probs) { if (p.s[w] > p.s.on) win++; else if (p.s[w] < p.s.on) loss++; }
    b += `<g transform="translate(${mid},0) scale(-1,1)">${bar(0, y, loss * scale, bh, "#e34948", `${NAME[w]}: worse on ${loss} problems`)}</g>`;
    b += bar(mid, y, win * scale, bh, "#2a78d6", `${NAME[w]}: better on ${win} problems`);
    b += txt(mid - loss * scale - 8, y + 16, String(loss), { anchor: "end", size: 12, fill: C.ink });
    b += txt(mid + win * scale + 8, y + 16, String(win), { size: 12, fill: C.ink });
    b += txt(20, y + 16, NAME[w], { fill: C.ink, size: 13 });
  });
  b += `<line x1="${mid}" x2="${mid}" y1="${top - 8}" y2="${top + ws.length * rowH - 12}" stroke="${C.mute}" stroke-width="1"/>`;
  save("fig5-better-worse-than-on.svg", svg(W, H, "Problem by problem: better or worse than thinking ON?", "Count of the 234 problems where the way solved MORE tries (right) or FEWER tries (left) than thinking ON", b));
}

// Fig 6: stage D, try 1
{
  const W = 900, H = 400, L = 60, R = 20, top = 90, base = 340, gw = (W - L - R) / 2, bw = 24, gap = 2;
  const series = [["ON, normal limit", COL.on, ds => D[ds].on1], ["ON, cut-offs get 16k", "#86b6ef", ds => D[ds].on1 + D[ds].ok],
                  ["Limit 1,024", COL.limit, ds => D[ds].try1.limit], ["Thinking OFF", COL.off, ds => D[ds].try1.off]];
  let b = yAxis(L, W - R, base, top, 70, 10, v => v + "%") + legend(L, 72, series.map(([l, c]) => [l, c]));
  ["he", "lcb"].forEach((ds, gi) => {
    const x0 = L + gi * gw + (gw - series.length * (bw + gap)) / 2;
    series.forEach(([l, c, fn], si) => {
      const v = pct(fn(ds), D[ds].n);
      b += col(x0 + si * (bw + gap), base, bw, (v / 70) * (base - top), c, `${l} · ${DS[ds]}: ${f1(v)}% (${fn(ds)}/${D[ds].n})`);
      b += txt(x0 + si * (bw + gap) + bw / 2, base - (v / 70) * (base - top) - 6, f1(v), { anchor: "middle", size: 10, fill: C.ink });
    });
    b += txt(L + gi * gw + gw / 2, base + 22, `${DS[ds]} (${D[ds].n} problems, try 1)`, { anchor: "middle", fill: C.ink, size: 13 });
  });
  b += `<line x1="${L}" x2="${W - R}" y1="${base}" y2="${base}" stroke="${C.mute}" stroke-width="1"/>`;
  save("fig6-stage-d-16k.svg", svg(W, H, "Stage D: does thinking ON catch up with 16,384 tokens?", "Only thinking ON's cut-off answers were re-run with 4× more room (try 1). The other ways are shown for comparison.", b));
}

// Fig 7: the training-data funnel
{
  const W = 900, H = 330, L = 230, R = 70, top = 90, bh = 18, len = W - L - R;
  const steps = [["problems", "n"], ["≥ 1 correct answer (of 4)", "one"], ["≥ 2 correct (a real choice)", "two"], ["kept for training", "kept"]];
  const pools = [["MBPP+ (200)", TM, "#4a3aa7"], ["LiveCodeBench older (80)", TL, "#8a8984"]];
  let b = legend(L, 72, pools.map(([l, , c]) => [l, c]));
  steps.forEach(([label, k], i) => {
    const y = top + i * 54;
    b += txt(L - 10, y + 24, label, { anchor: "end", fill: C.ink, size: 13 });
    pools.forEach(([pl, st, c], j) => {
      const l = (st[k] / 200) * len;
      b += bar(L, y + j * (bh + 2), l, bh, c, `${pl}: ${label} = ${st[k]}`);
      b += txt(L + l + 6, y + j * (bh + 2) + 14, String(st[k]), { size: 11, fill: C.ink });
    });
  });
  save("fig7-training-data-funnel.svg", svg(W, H, "LoRA-2 training data: from problems to kept examples", "Each problem got 4 thinking-ON tries. Only problems with a correct answer can give a training example.", b));
}

// Fig 8: LoRA-2 training loss
{
  const W = 900, H = 380, L = 70, R = 30, top = 70, base = 320, n = LOSS.losses.length, ymax = 0.4;
  const X = i => L + (i / (n - 1)) * (W - L - R), Y = v => base - (v / ymax) * (base - top);
  let b = yAxis(L, W - R, base, top, ymax, 0.1, v => v.toFixed(1));
  const perEpoch = n / LOSS.epochs;
  for (let e = 1; e < LOSS.epochs; e++) b += `<line x1="${X(e * perEpoch)}" x2="${X(e * perEpoch)}" y1="${top}" y2="${base}" stroke="${C.grid}" stroke-width="1"/>`;
  for (let e = 0; e < LOSS.epochs; e++) b += txt(X((e + 0.5) * perEpoch), base + 20, `epoch ${e + 1}`, { anchor: "middle", size: 11 });
  b += `<path d="${LOSS.losses.map((v, i) => `${i ? "L" : "M"}${X(i).toFixed(1)},${Y(v).toFixed(1)}`).join("")}" fill="none" stroke="${COL.lora2}" stroke-width="2" stroke-linejoin="round"/>`;
  save("fig8-lora2-training-loss.svg", svg(W, H, `LoRA-2 training loss (${LOSS.n_examples} examples, ${LOSS.epochs} epochs, ${n} steps)`, "Loss = how wrong the model's guesses for the next token are, on the training examples. Lower = learned them better.", b));
}

// Fig 9: LoRA-1 thinking vs ON, on the mini-thesis test and on the real test
{
  const MINI = { think: 0.59, acc: 15.0 };                // results/2026-09-22-mini-thesis-first-results.md
  const rows = [["MBPP+ test (mini-thesis)", MINI.think], ["HumanEval+", +SUM["lora1HumanEval+"].think_ratio],
                ["LCB easy", +SUM["lora1LCB easy"].think_ratio], ["LCB medium", +SUM["lora1LCB medium"].think_ratio],
                ["All 234 (real test)", +SUM["lora1All"].think_ratio]];
  const W = 900, H = 330, L = 200, R = 80, top = 80, bh = 22, rowH = 40, xmax = 1.2, len = W - L - R;
  const X = v => L + (v / xmax) * len;
  let b = "";
  for (const v of [0, 0.25, 0.5, 0.75, 1.0]) {
    b += `<line x1="${X(v)}" x2="${X(v)}" y1="${top - 6}" y2="${top + rows.length * rowH - 10}" stroke="${v === 0.75 || v === 1 ? C.mute : C.grid}" stroke-width="1"/>`;
    b += txt(X(v), top + rows.length * rowH + 8, v === 0.75 ? "0.75 = H1 goal" : v === 1 ? "1.0 = same as ON" : "x" + v, { anchor: "middle", size: 11 });
  }
  rows.forEach(([l, v], i) => {
    const y = top + i * rowH;
    b += bar(L, y, X(v) - L, bh, COL.lora1, `${l}: x${v.toFixed(2)}`);
    b += txt(L - 10, y + 16, l, { anchor: "end", fill: C.ink, size: 13 });
    b += txt(X(v) + 8, y + 16, "x" + v.toFixed(2), { size: 12, fill: C.ink });
  });
  save("fig9-lora1-transfer.svg", svg(W, H, "LoRA-1's thinking length, compared with thinking ON", "Shorter than ON on its own kind of problems (MBPP+), almost the same on new kinds of problems", b));
}

// Fig 10: GPU minutes per way (2 tries, both test sets)
{
  const W = 900, H = 330, L = 150, R = 150, top = 70, bh = 22, rowH = 38, len = W - L - R;
  const mx = Math.max(...WAYS.map(wayMin));
  let b = "";
  WAYS.forEach((w, i) => {
    const y = top + i * rowH, m = wayMin(w);
    b += bar(L, y, (m / mx) * len, bh, COL[w], `${NAME[w]}: ${f1(m)} GPU minutes`);
    b += txt(L - 10, y + 16, NAME[w], { anchor: "end", fill: C.ink, size: 13 });
    b += txt(L + (m / mx) * len + 8, y + 16, `${f1(m)} min · ${(m / 60 * UNITS_PER_H).toFixed(1)} units`, { size: 12, fill: C.ink });
  });
  save("fig10-gpu-time.svg", svg(W, H, "A100 time to answer all 234 problems twice, per way", "Estimated from each batch's time shared over its answers. A batch waits for its slowest answer.", b));
}

// ---------- CSV tables ----------
const toCsv = (head, rows) => [head.join(","), ...rows.map(r => r.map(v => /[",\n]/.test(String(v)) ? `"${String(v).replace(/"/g, '""')}"` : v).join(","))].join("\n") + "\n";
fs.writeFileSync(`${OUT}/tables/per-way-per-group.csv`, toCsv(
  ["group", "way", "problems", "answers", "passed", "accuracy_pct", "d_vs_on", "d_lo", "d_hi", "mean_thinking", "median_thinking", "median_thinking_finished", "mean_answer_tokens", "mean_total_tokens", "cut_off", "cut_off_loops", "think_ratio", "r_lo", "r_hi"],
  GROUPS.flatMap(g => WAYS.map(w => { const s = S[w + g], m = SUM[w + g];
    return [g, w, s.problems, s.n, s.pass, f1(s.acc), m.d_vs_on, m.d_lo, m.d_hi, Math.round(s.think), s.medThink, s.medFinThink, Math.round(s.ans), Math.round(s.total), s.cut, s.loop, m.think_ratio, m.r_lo, m.r_hi] }))));
fs.writeFileSync(`${OUT}/tables/per-problem.csv`, toCsv(
  ["task_id", "set", "difficulty", ...WAYS.map(w => w + "_solved_of_2"), "on16k_try1"],
  probs.map(p => [p.id, DS[p.ds], p.diff, ...WAYS.map(w => p.s[w] || 0), D[p.ds].rerunIds.has(p.id) ? (D[p.ds].okIds.has(p.id) ? "pass" : "fail") : ""])));
fs.writeFileSync(`${OUT}/tables/training-problems.csv`, toCsv(
  ["task_id", "pool", "difficulty", "tries", "correct", "kept", "kept_thinking_tokens", "question_start"],
  TR.map(t => [t.id, t.pool, t.diff, t.tries, t.ok, t.kept, t.keptThink ?? "", t.q])));
fs.writeFileSync(`${OUT}/tables/gpu-time.csv`, toCsv(["way", "he_minutes", "lcb_minutes", "total_minutes", "units"],
  WAYS.map(w => [w, f1(T[w + "he"] / 60), f1(T[w + "lcb"] / 60), f1(wayMin(w)), (wayMin(w) / 60 * UNITS_PER_H).toFixed(2)])));

// ---------- examples from the raw text ----------
const onHe = jsonl("test-on-he.jsonl"), briefHe = jsonl("test-brief-he.jsonl");
const loopEx = onHe.find(r => r.hit_limit && loops(r.raw_output) && r.raw_output.length > 3000);
const BRIEF_KEY = "Wait, if I output thinking text";
const briefEx = briefHe.find(r => r.raw_output.includes(BRIEF_KEY)) || briefHe[0];
const around = (t, key, n = 700) => { const i = Math.max(0, t.lastIndexOf(key) - 450); return t.slice(i, i + n) };
const clean = s => s.replace(/~~~/g, "~ ~ ~").trim();

// ---------- the report ----------
const md = [];
const line = s => md.push(s);
const tbl = (head, rows) => { line("| " + head.join(" | ") + " |"); line("|" + head.map(() => "---").join("|") + "|"); rows.forEach(r => line("| " + r.join(" | ") + " |")); line("") };
const ci = m => m.d_vs_on === "" ? "—" : `${+m.d_vs_on >= 0 ? "+" : ""}${m.d_vs_on} [${m.d_lo}, ${m.d_hi}]`;
const ratio = m => m.think_ratio === "" ? "—" : `x${(+m.think_ratio).toFixed(2)} [${(+m.r_lo).toFixed(2)}, ${(+m.r_hi).toFixed(2)}]`;
const sAll = w => S[w + "All"];
const wins = w => { let win = 0, loss = 0, same = 0; for (const p of probs) { if (p.s[w] > p.s.on) win++; else if (p.s[w] < p.s.on) loss++; else same++; } return { win, loss, same } };
const solvedOnce = (w, g = "All") => probs.filter(p => inGroup(p, g) && p.s[w] > 0).length;
const anyWay = probs.filter(p => WAYS.some(w => p.s[w] > 0)).length;
const noWay = probs.length - anyWay;
const only = w => probs.filter(p => p.s[w] > 0 && WAYS.every(v => v === w || !p.s[v])).length;
const firstSeen = LEDGER[0].time, lastSeen = LEDGER[LEDGER.length - 1].time;
const unitsUsed = LEDGER[0].units_left_est - LEDGER[LEDGER.length - 1].units_left_est;

line(`# Full results: the real thesis run (notebook 14)`);
line("");
line(`> **Made by** \`node scripts/make_full_results.js\` from the raw Drive files in [\`${RUN}/\`](../2026-09-24-thesis-run/).`);
line(`> Every number here is computed from those files, not typed by hand. Re-run the script to rebuild this page.`);
line(`> Short version: [../2026-09-24-thesis-run.md](../2026-09-24-thesis-run.md) · Teacher Q&A: [qa/28](../../qa/28-thesis-run-results.md).`);
line("");
line(`**Where we are:** \`PROBLEM ✅ → GAP ✅ → QUESTION ✅ → HYPOTHESIS ✅ → EXPERIMENT ✅ → DATA ✅ → RESULTS ✅ (this page) → ANALYSIS → CONCLUSION\``);
line("");
line(`## Contents`);
line("");
["0. Words used on this page", "1. The result in 5 lines", "2. What we tested (the 9 research questions)", "3. The set-up: model, GPU, settings",
 "4. The test problems (234)", "5. The training problems (280) and LoRA-2", "6. Main results: accuracy", "7. Main results: tokens (cost)",
 "8. The hypotheses", "9. Why: cut-offs and loops", "10. How long the model thinks", "11. Problem by problem", "12. Stage D: was the token limit unfair?",
 "13. Why LoRA-2 did not get shorter", "14. The mini-thesis vs the real test", "15. Time and money", "16. Examples from the raw answers",
 "17. Honest limits", "18. Claims for the paper", "Appendix A: every test problem", "Appendix B: every training problem", "Appendix C: files"].forEach(s => line(`- ${s}`));
line("");

line(`## 0. Words used on this page`);
line("");
tbl(["Word", "Meaning"], [
  ["token", "a small piece of text, about ¾ of a word. The model writes one token at a time."],
  ["thinking", "the text the model writes to itself before the answer. Costs tokens and time."],
  ["way (of answering)", "one set-up we test: thinking ON, OFF, \"think briefly\", a thinking limit, or ON + a trained LoRA"],
  ["accuracy", "the share of answers that pass the benchmark's own tests"],
  ["try", "one answer to one problem. Each way answered every problem **2 times** (different random seeds)."],
  ["cut off", "the answer hit the token limit before it finished. It has no final code, so it counts as **wrong**."],
  ["loop", "the model repeats the same lines again and again until the limit"],
  ["LoRA", "a small add-on trained on top of the model. LoRA-1 = from the mini-thesis, LoRA-2 = trained in this run."],
  ["error bar [a, b]", "the range the true difference probably lies in (95%). If it doesn't include 0, the difference is **proven** for this test."],
  ["median", "the middle value when you sort the numbers. Not pulled up by a few very long answers."],
  ["unit", "Colab's pay unit. An A100 costs about 5.3 units per hour."],
]);

line(`## 1. The result in 5 lines`);
line("");
line(`1. Our trained model (**LoRA-2**) did **not** think shorter: x${(+SUM.lora2All.think_ratio).toFixed(2)} of thinking ON's thinking. Accuracy ${f1(sAll("lora2").acc)}% vs ${f1(sAll("on").acc)}% for ON (+${SUM.lora2All.d_vs_on} points, not proven).`);
line(`2. The best way was the free **thinking limit** (stop thinking at 1,024 tokens): **${f1(sAll("limit").acc)}%**, +${SUM.limitAll.d_vs_on} points vs ON, proven [${SUM.limitAll.d_lo}, ${SUM.limitAll.d_hi}].`);
line(`3. **Thinking OFF** reached ${f1(sAll("off").acc)}%, almost the same as ON, with **${n0(sAll("off").total)}** tokens per answer instead of ${n0(sAll("on").total)} (4× fewer).`);
line(`4. **Why:** ${f1(pct(sAll("on").cut, sAll("on").n))}% of thinking-ON answers were cut off, and most cut-offs were **loops**. Finished answers were already short. Training does not stop loops; a limit does.`);
line(`5. "Think briefly" failed (${f1(sAll("brief").acc)}%) because the instruction clashed with our "one code block only" rule, and the model argued with itself until the limit.`);
line("");
line(`![Accuracy against cost](figures/fig2-accuracy-vs-tokens.svg)`);
line("");

line(`## 2. What we tested (the 9 research questions)`);
line("");
tbl(["Question", "Answer"], [
  ["What am I testing?", "Can training a small model on its own shortest correct answers make it think shorter on code problems, and is that better than free options?"],
  ["Hypothesis", "H1: ≥ 25% less thinking than ON · H2: accuracy ≥ ON − 3 points · H3: more accurate than OFF, the limit and \"think briefly\""],
  ["Independent variable (what we change)", "the way of answering: ON · OFF · think briefly · limit 1,024 · LoRA-1 · LoRA-2"],
  ["Dependent variables (what we measure)", "accuracy · thinking tokens · all tokens · cut-offs · GPU time"],
  ["What we compare against", "thinking ON (the model's normal way)"],
  ["Data", "234 test problems: HumanEval+ (164) + LiveCodeBench easy (31) + medium (39)"],
  ["Metric", "share of answers passing the benchmark's own tests; paired error bars (same problems, before vs after)"],
  ["What supports it", "LoRA-2: thinking ratio ≤ 0.75 AND accuracy ≥ ON − 3 AND better than every free way"],
  ["What contradicts it", "thinking not shorter, or a free way (OFF / limit / brief) as good or better"],
]);

line(`## 3. The set-up: model, GPU, settings`);
line("");
tbl(["Setting", "Value", "Why"], [
  ["Model", "`unsloth/Qwen3.5-2B` (2 billion parameters, has a thinking ON/OFF switch)", "small enough for one GPU; DECISIONS #52–53"],
  ["GPU", "Google Colab **A100** (40 GB), bfloat16, batch 128", "paid units, DECISIONS #48, #63"],
  ["Sampling", "temperature 0.6, top-p 0.95, top-k 20; a fixed seed per try (try 1 seed 3407)", "Qwen's own settings; fixed seeds (CLAUDE.md §4)"],
  ["Token limit", "**4,096** for HumanEval+, **8,192** for LiveCodeBench, the same for every way", "fairness, DECISIONS #66"],
  ["Limit way", "thinking cut at **1,024** tokens, then the model must answer", "about LoRA-1's thinking length in the mini-thesis"],
  ["Think briefly", "the question + \"Think briefly: keep your thinking to a few short sentences, then give the answer.\"", "the simplest prompt-only option"],
  ["Tries", "**2** per problem per way", "budget, DECISIONS #65"],
  ["Grading", "HumanEval+ plus-tests (evalplus) and LiveCodeBench's own tests, in a separate process with timeouts", "never by eye (CLAUDE.md §4)"],
  ["Error bars", "paired bootstrap over problems, 2,000 resamples, seed 3407", "`scripts/compare_thesis.py`"],
  ["LoRA training", "r 16, alpha 16, lr 2e-4, 3 epochs, batch 1 × 4, adamw_8bit, seed 3407", "`scripts/train_lora.py`, Unsloth's Qwen3.5 guide"],
  ["Main LoRA", "**LoRA-2**, named before the run", "no picking after results, DECISIONS #66"],
]);

line(`## 4. The test problems (234)`);
line("");
line("```text");
line("234 test problems");
line(" ├─ HumanEval+     164   all easy · write one Python function · HumanEval/0 … HumanEval/163");
line(" └─ LiveCodeBench   70   read input, print output · released from Feb 2025 on (after the model's data)");
line("      ├─ easy       31");
line("      └─ medium     39   (hard problems left out: a 2B model solves almost none, PLAN §3)");
line("```");
line("");
line(`The test set was fixed on 2026-09-20, before any result (DECISIONS #58). None of these problems was used for training (overlap check, DECISIONS #66).`);
line(`Every test problem, with what each way solved, is in **Appendix A** and in [tables/per-problem.csv](tables/per-problem.csv).`);
line("");
line(`**How many problems each way solved at least once (of 2 tries):**`);
line("");
tbl(["Way", ...GROUPS.map(g => `${g} (${S["on" + g].problems})`), "only this way solved it"],
  WAYS.map(w => [NAME[w], ...GROUPS.map(g => String(solvedOnce(w, g))), String(only(w))]));
line(`- Solved by **at least one** way: **${anyWay} of ${probs.length}** problems. Solved by **no** way: **${noWay}**.`);
line("");

line(`## 5. The training problems (280) and LoRA-2`);
line("");
line(`LoRA-2 learns from the model's own answers: 4 thinking-ON tries per problem, keep the **shortest correct** one, train on those.`);
line("");
line("```text");
line(`MBPP+ 200 problems (easy functions)          ─┐`);
line(`LiveCodeBench 80 older problems (before 2025) ─┤→ 4 tries each → grade → shortest correct → ${LOSS.n_examples} examples → LoRA-2`);
line(`   40 easy + 40 medium                         ─┘`);
line("```");
line("");
line(`![Training data funnel](figures/fig7-training-data-funnel.svg)`);
line("");
tbl(["", "MBPP+", "LiveCodeBench (older)"], [
  ["problems", TM.n, `${TL.n} (${TL.easy} easy, ${TL.medium} medium)`],
  ["answers (4 tries each)", TM.answers, TL.answers],
  ["correct answers", `${TM.okAns} (${f1(pct(TM.okAns, TM.answers))}%)`, `${TL.okAns} (${f1(pct(TL.okAns, TL.answers))}%): easy ${TL.okEasy}/${TL.easy * 4}, **medium ${TL.okMed}/${TL.medium * 4}**`],
  ["problems with ≥ 1 correct", TM.one, TL.one],
  ["problems with ≥ 2 correct (a real choice of \"shortest\")", TM.two, TL.two],
  ["kept as training examples", TM.kept, TL.kept],
  ["median thinking of kept examples", n0(TM.medKept), `**${n0(TL.medKept)}**`],
  ["TARGET (kept length ÷ average correct length; lower = more to learn)", TGT.mbpp.target, `**${TGT.lcb.target}** (almost nothing to learn)`],
]);
if (excluded.length) line(`Problems with a correct answer that were **not** kept (removed by the overlap check): ${excluded.map(x => "`" + x.id + "`").join(", ")}.`);
line(`LoRA-2 trained on **${LOSS.n_examples}** examples for ${LOSS.epochs} epochs (${LOSS.losses.length} steps). The mini-thesis answers for MBPP+ were reused, so they were not paid twice.`);
line(`Every training problem is in **Appendix B** and [tables/training-problems.csv](tables/training-problems.csv).`);
line("");
line(`![LoRA-2 training loss](figures/fig8-lora2-training-loss.svg)`);
line("");
line(`The loss goes from about ${mean(LOSS.losses.slice(0, 10)).toFixed(2)} (first 10 steps) to ${mean(LOSS.losses.slice(-10)).toFixed(2)} (last 10 steps). So LoRA-2 did learn its examples. The problem is **what** the examples teach (section 13).`);
line("");

line(`## 6. Main results: accuracy`);
line("");
line(`![Accuracy by group](figures/fig1-accuracy-by-group.svg)`);
line("");
for (const g of GROUPS) {
  line(`### ${g} — ${S["on" + g].problems} problems, ${S["on" + g].n} answers per way`);
  line("");
  tbl(["Way", "Passed", "Accuracy", "vs ON, points [95% error bar]"],
    WAYS.map(w => [NAME[w], `${S[w + g].pass} / ${S[w + g].n}`, `**${f1(S[w + g].acc)}%**`, ci(SUM[w + g])]));
}

line(`## 7. Main results: tokens (cost)`);
line("");
line(`Averages are pulled up by cut-off answers, so the **median** (middle) is also shown. "Finished" = answers that were not cut off.`);
line("");
for (const g of GROUPS) {
  line(`### ${g}`);
  line("");
  tbl(["Way", "Thinking (avg)", "Thinking (median)", "Thinking of finished answers (median)", "Answer part (avg)", "All tokens (avg)", "Thinking vs ON [95%]"],
    WAYS.map(w => { const s = S[w + g]; return [NAME[w], n0(s.think), n0(s.medThink), `${n0(s.medFinThink)} (n=${s.fin})`, n0(s.ans), `**${n0(s.total)}**`, ratio(SUM[w + g])] }));
}
line(`**Watch out:** the limit's thinking is short (x${(+SUM.limitAll.think_ratio).toFixed(2)}), but after the forced stop it keeps writing in the answer part (${n0(sAll("limit").ans)} tokens on average). Counting **all** tokens, the limit uses ${n0(sAll("limit").total)} vs ${n0(sAll("on").total)} for ON: **${f1(100 - pct(sAll("limit").total, sAll("on").total))}% fewer**, not 74% fewer.`);
line("");

line(`## 8. The hypotheses (for LoRA-2, fixed in advance)`);
line("");
tbl(["", "Test", "Needed", "Result", "Verdict"], [
  ["H1", "thinking vs ON", "≤ x0.75", ratio(SUM.lora2All), "❌ **NO**"],
  ["H2", "accuracy vs ON", "≥ −3 points", ci(SUM.lora2All), "✅ YES"],
  ["H3", "vs thinking OFF", "> 0", "+4.3 [−0.6, +9.2]", "⚠️ not proven (error bar includes 0)"],
  ["H3", "vs limit 1,024", "> 0", "−4.7 [−9.0, −0.2]", "❌ **NO**: the limit is better (proven)"],
  ["H3", "vs think briefly", "> 0", "+38.5 [+32.9, +44.2]", "✅ yes, but brief failed for its own reason (section 16)"],
]);
line(`(The H3 numbers are LoRA-2 minus the other way, printed by the notebook; see [the step 12 output](../2026-09-24-thesis-run-step12-output.txt).)`);
line("");
line(`**The answer to the research question: no.** On this model, training was not better than the free options. A free thinking limit was better.`);
line("");

line(`## 9. Why: cut-offs and loops`);
line("");
line(`![Cut-offs and loops](figures/fig3-cutoffs-and-loops.svg)`);
line("");
tbl(["Way", "Answers", "Finished", "Cut off", "Cut off in a loop", "Loops among cut-offs"],
  WAYS.map(w => { const s = sAll(w); return [NAME[w], s.n, s.fin, `${s.cut} (${f1(pct(s.cut, s.n))}%)`, s.loop, `${f1(pct(s.loop, s.cut))}%`] }));
tbl(["Way", ...GROUPS.slice(1).map(g => `${g}: cut off / loops`)],
  WAYS.map(w => [NAME[w], ...GROUPS.slice(1).map(g => `${S[w + g].cut}/${S[w + g].n} · ${S[w + g].loop}`)]));
line(`How the loop test works: a cut-off answer counts as a loop when a piece of its last 200 characters already appears at least twice earlier in the same answer. It misses loops with small changes, so the real numbers are probably **higher**.`);
line("");

line(`## 10. How long the model thinks`);
line("");
line(`![Thinking length on HumanEval+](figures/fig4-thinking-length-humaneval.svg)`);
line("");
line(`On HumanEval+, answers that **finish** think about the same amount with or without training (median of finished answers: ON ${n0(S["onHumanEval+"].medFinThink)}, LoRA-1 ${n0(S["lora1HumanEval+"].medFinThink)}, LoRA-2 ${n0(S["lora2HumanEval+"].medFinThink)}, limit ${n0(S["limitHumanEval+"].medFinThink)}). The big difference is how many **never** finish. So the waste is loops, not long careful thinking.`);
line("");

line(`## 11. Problem by problem`);
line("");
line(`![Better or worse than ON](figures/fig5-better-worse-than-on.svg)`);
line("");
tbl(["Way", "Better than ON (problems)", "Worse than ON", "Same"], WAYS.filter(w => w !== "on").map(w => { const x = wins(w); return [NAME[w], x.win, x.loss, x.same] }));
line(`"Better" = the way solved more of its 2 tries than ON on that problem.`);
line("");

line(`## 12. Stage D: was the token limit unfair to thinking ON?`);
line("");
line(`We re-ran only thinking ON's **cut-off** answers of try 1 with **16,384** tokens (4× more room).`);
line("");
line(`![Stage D](figures/fig6-stage-d-16k.svg)`);
line("");
tbl(["", "HumanEval+", "LiveCodeBench"], [
  ["cut-off ON answers re-run", D.he.rerun, D.lcb.rerun],
  ["finished within 16,384", D.he.fin, D.lcb.fin],
  ["correct", D.he.ok, D.lcb.ok],
  ["still cut off, in a loop", D.he.loops, D.lcb.loops],
  ["ON try 1, normal limit", `${D.he.on1}/${D.he.n} = ${f1(pct(D.he.on1, D.he.n))}%`, `${D.lcb.on1}/${D.lcb.n} = ${f1(pct(D.lcb.on1, D.lcb.n))}%`],
  ["ON try 1, with 16k", `**${D.he.on1 + D.he.ok}/${D.he.n} = ${f1(pct(D.he.on1 + D.he.ok, D.he.n))}%**`, `**${D.lcb.on1 + D.lcb.ok}/${D.lcb.n} = ${f1(pct(D.lcb.on1 + D.lcb.ok, D.lcb.n))}%**`],
  ["Limit 1,024, try 1", `${D.he.try1.limit}/${D.he.n} = ${f1(pct(D.he.try1.limit, D.he.n))}%`, `${D.lcb.try1.limit}/${D.lcb.n} = ${f1(pct(D.lcb.try1.limit, D.lcb.n))}%`],
  ["Thinking OFF, try 1", `${D.he.try1.off}/${D.he.n} = ${f1(pct(D.he.try1.off, D.he.n))}%`, `${D.lcb.try1.off}/${D.lcb.n} = ${f1(pct(D.lcb.try1.off, D.lcb.n))}%`],
  ["GPU time of the re-run", `${f1(D.he.sec / 60)} min`, `${f1(D.lcb.sec / 60)} min`],
]);
line(`- **HumanEval+:** with 16k, ON almost catches the limit way. So part of the limit's win on HumanEval+ comes from our 4,096 limit. **The thesis must say this.**`);
line(`- **LiveCodeBench:** more room helps little; most answers still loop. The limit and OFF stay clearly ahead.`);
line("");

line(`## 13. Why LoRA-2 did not get shorter`);
line("");
line(`1. **Medium training problems gave almost nothing to learn:** the model solved **${TL.okMed} of ${TL.medium * 4}** medium tries, so medium problems gave (almost) no examples.`);
line(`2. **The LiveCodeBench examples it did get were long:** median **${n0(TL.medKept)}** thinking tokens, and the shortest correct answer was barely shorter than the average correct one (TARGET ${TGT.lcb.target}). So LoRA-2 learned to think **long** on LiveCodeBench-style problems: on LiveCodeBench answers that finished, its median thinking is ${n0(median(A.filter(a => a.way === "lora2" && a.ds === "lcb" && !a.cut).map(a => a.think)))} tokens vs LoRA-1's ${n0(median(A.filter(a => a.way === "lora1" && a.ds === "lcb" && !a.cut).map(a => a.think)))}.`);
line(`3. **Training copies short correct answers, but the waste is loops** (section 9). Nothing in the examples teaches "stop when you are going round in circles".`);
line("");

line(`## 14. The mini-thesis vs the real test`);
line("");
line(`In the mini-thesis (100 MBPP+ test problems, 1 try), LoRA-1 cut tokens to **x0.59** and gained **+15 points** (DECISIONS #64). On the real test it did much less:`);
line("");
line(`![LoRA-1 transfer](figures/fig9-lora1-transfer.svg)`);
line("");
tbl(["Test", "LoRA-1 thinking vs ON", "LoRA-1 accuracy vs ON"], [
  ["MBPP+ (mini-thesis, same kind as training)", "x0.59 [0.46, 0.75]", "+15.0 [+6.0, +25.0]"],
  ...GROUPS.map(g => [g, ratio(SUM["lora1" + g]), ci(SUM["lora1" + g])])]);
line(`So the training works on problems **like its training data**, and mostly does **not** carry over to new kinds of problems. This is a finding in itself.`);
line("");

line(`## 15. Time and money`);
line("");
line(`![GPU time](figures/fig10-gpu-time.svg)`);
line("");
tbl(["Way", "HumanEval+ (min)", "LiveCodeBench (min)", "Total (min)", "≈ units"],
  WAYS.map(w => [NAME[w], f1(T[w + "he"] / 60), f1(T[w + "lcb"] / 60), `**${f1(wayMin(w))}**`, (wayMin(w) / 60 * UNITS_PER_H).toFixed(1)]));
line(`- Answering the test set, all ways, 2 tries: **${f1(testMin)} A100 minutes** (${f1(testMin / 60)} hours).`);
line(`- Making LoRA-2's training answers: MBPP+ ${f1(TSEC.mbpp / 60)} min (partly the mini-thesis's reused answers) + LiveCodeBench ${f1(TSEC.lcb / 60)} min. Training LoRA-2 itself: about 6 minutes (ledger 16:52 → 16:58).`);
line(`- Stage D (16k re-run): ${f1((D.he.sec + D.lcb.sec) / 60)} min.`);
line(`- **Whole budget:** the ledger went from ${LEDGER[0].units_left_est} units (${firstSeen}) to about ${LEDGER[LEDGER.length - 1].units_left_est} (${lastSeen}): about **${f1(unitsUsed)} units** used, including set-up and idle time. Colab's own number is the true one.`);
line(`- Time per answer is estimated: each batch's time shared equally over its answers.`);
line(`- **Why OFF is not 4× faster here:** answers run in batches of up to 128, and a batch waits for its **slowest** answer. OFF writes ${n0(sAll("off").total)} tokens on average, but a few of its LiveCodeBench answers ran to 8,192, so its batches still took long. Run one answer at a time (as a user would), time follows tokens. So **tokens are the fair measure of cost**, and GPU minutes here mostly show our batch set-up.`);
line("");
line(`**Ledger (units left, estimated):**`);
line("");
tbl(["Time", "Event", "Units left"], LEDGER.map(l => [l.time, l.event, l.units_left_est]));

line(`## 16. Examples from the raw answers`);
line("");
line(`### A loop (thinking ON, ${loopEx.task_id}, try ${loopEx.sample_index + 1}, cut off at ${n0(loopEx.total_new_tokens)} tokens) — the last part:`);
line("");
line("~~~text"); line(clean(loopEx.raw_output.slice(-900))); line("~~~");
line("");
line(`### "Think briefly" arguing with the rules (${briefEx.task_id}, try ${briefEx.sample_index + 1}):`);
line("");
line("~~~text"); line(clean(around(briefEx.raw_output, BRIEF_KEY))); line("~~~");
line("");
line(`Out of ${sAll("brief").n} "brief" answers, only ${sAll("brief").fin} finished. The prompt already says "Answer with one Python code block only", and "think briefly … then give the answer" adds a second rule. This is a result for **this wording**, not for asking to be brief in general.`);
line("");

line(`## 17. Honest limits`);
line("");
["One model only (Qwen3.5-2B). Bigger models may not loop as much.",
 "2 tries per problem and 234 problems: error bars are about ±4–6 points on all problems, and much wider on the small LiveCodeBench groups.",
 "One wording for \"think briefly\". Another wording may work better (not tested).",
 "The token limits (4,096 / 8,192) cut off some honest thinking on HumanEval+ (stage D: +5.5 points for ON).",
 "LiveCodeBench medium is at the floor (0–9% for every way), so it can't separate the ways.",
 "The loop test is rough and probably under-counts loops.",
 "GPU time per way is an estimate from batch times, not a separate measurement per answer."].forEach(s => line(`- ${s}`));
line("");

line(`## 18. Claims for the paper (each with its number)`);
line("");
[`Shortest-correct LoRA training did **not** shorten thinking on the test set (x${(+SUM.lora2All.think_ratio).toFixed(2)} [${SUM.lora2All.r_lo}, ${SUM.lora2All.r_hi}]).`,
 `A thinking limit of 1,024 tokens improved accuracy over thinking ON by **+${SUM.limitAll.d_vs_on} points [${SUM.limitAll.d_lo}, ${SUM.limitAll.d_hi}]**, and beat LoRA-2 by 4.7 points [0.2, 9.0].`,
 `Thinking OFF matched thinking ON (${SUM.offAll.d_vs_on} points [${SUM.offAll.d_lo}, ${SUM.offAll.d_hi}]) at **${n0(sAll("off").total)} vs ${n0(sAll("on").total)}** tokens per answer.`,
 `${f1(pct(sAll("on").loop, sAll("on").cut))}% of thinking ON's cut-off answers were loops; finished answers were already short (median ${n0(S["onHumanEval+"].medFinThink)} thinking tokens on HumanEval+).`,
 `LoRA training shortened thinking on problems like its training data (MBPP+: x0.59) but not on new problem types (HumanEval+ x${(+SUM["lora1HumanEval+"].think_ratio).toFixed(2)}).`,
 `A "think briefly" instruction that clashes with an output-format rule made the model think **longer** (x${(+SUM.briefAll.think_ratio).toFixed(2)}) and fail (${f1(sAll("brief").acc)}%).`,
 `Giving thinking ON 4× more room (16k) raised HumanEval+ try-1 accuracy from ${f1(pct(D.he.on1, D.he.n))}% to ${f1(pct(D.he.on1 + D.he.ok, D.he.n))}%, still not above the limit (${f1(pct(D.he.try1.limit, D.he.n))}%).`].forEach((s, i) => line(`${i + 1}. ${s}`));
line("");

line(`## Appendix A: every test problem`);
line("");
line(`Each cell = how many of the 2 tries passed. **ON 16k** = the try-1 re-run with 16,384 tokens (only for cut-off answers).`);
line("");
tbl(["#", "Problem", "Set", "Level", ...WAYS.map(w => NAME[w].replace(" (main)", "")), "ON 16k"],
  probs.map((p, i) => [i + 1, "`" + p.id + "`", p.ds === "he" ? "HE+" : "LCB", p.diff, ...WAYS.map(w => { const v = p.s[w] || 0; return v === 2 ? "**2**" : String(v) }),
    D[p.ds].rerunIds.has(p.id) ? (D[p.ds].okIds.has(p.id) ? "✔" : "✘") : ""]));

line(`## Appendix B: every training problem`);
line("");
line(`Correct = how many of the 4 tries passed. Kept = became a training example (the shortest correct answer).`);
line("");
tbl(["#", "Problem", "Pool", "Level", "Correct (of 4)", "Kept", "Kept thinking tokens", "Question starts with"],
  TR.map((t, i) => [i + 1, "`" + t.id + "`", t.pool.startsWith("MBPP") ? "MBPP+" : "LCB old", t.diff, t.ok, t.kept ? "✔" : "", t.keptThink ?? "", t.q.replace(/\|/g, "\\|")]));

line(`## Appendix C: files`);
line("");
tbl(["File", "What"], [
  ["[tables/per-way-per-group.csv](tables/per-way-per-group.csv)", "every number from sections 6–9, one row per way per group"],
  ["[tables/per-problem.csv](tables/per-problem.csv)", "Appendix A as a spreadsheet"],
  ["[tables/training-problems.csv](tables/training-problems.csv)", "Appendix B as a spreadsheet"],
  ["[tables/gpu-time.csv](tables/gpu-time.csv)", "section 15"],
  ["[figures/](figures/)", "the 10 charts as SVG (open in a browser; they scale for the paper)"],
  ["`../2026-09-24-thesis-run/`", "the raw files: every answer, word for word, and every grade"],
  ["`scripts/make_full_results.js`", "rebuilds this page: `node scripts/make_full_results.js`"],
]);

fs.writeFileSync(`${OUT}/FULL-RESULTS.md`, md.join("\n") + "\n");
console.log(`checked against summary.csv: all ${WAYS.length * GROUPS.length} accuracies match`);
console.log(`wrote ${OUT}/FULL-RESULTS.md (${md.length} lines), 10 figures, 4 tables`);
