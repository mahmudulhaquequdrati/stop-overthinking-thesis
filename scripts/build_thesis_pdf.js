// Turn the thesis into a printable A4 PDF: thesis/Stop-Overthinking-Thesis.pdf
//
// 1. What problem does this solve?  The thesis is Markdown; a reader wants one file to download and print.
// 2. Why do we need it?  To hand in and print. On paper, links don't work, so the full problem lists
//    (FULL-RESULTS appendices A and B) are printed in the PDF as appendices E and F.
// 3. What goes in?   thesis/THESIS.md (rebuilt first) + results/full-results/FULL-RESULTS.md + the SVG charts.
// 4. What comes out? thesis/THESIS.html (print-styled) and thesis/Stop-Overthinking-Thesis.pdf.
// 5. Why this way?   This PC has no Python or pandoc. `marked` turns Markdown into HTML, and Microsoft Edge
//                    (already installed) prints HTML to PDF with page numbers — the same way the proposal PDF
//                    was made from proposal.html. Needs `marked`:  npm install --prefix <folder> marked@12
//                    then:  MARKED=<folder>/node_modules/marked node scripts/build_thesis_pdf.js
const fs = require("fs"), path = require("path"), { execFileSync } = require("child_process");
const { marked } = require(process.env.MARKED || "marked");
const EDGE = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe";
const DIR = "thesis", HTML = path.join(DIR, "THESIS.html"), PDF = path.join(DIR, "Stop-Overthinking-Thesis.pdf");

execFileSync(process.execPath, ["scripts/build_thesis.js"], { stdio: "inherit" });
let md = fs.readFileSync(path.join(DIR, "THESIS.md"), "utf8").replace(/<!--[\s\S]*?-->\s*/, "");

// On paper the problem lists must be inside the thesis, not behind a link.
const full = fs.readFileSync("results/full-results/FULL-RESULTS.md", "utf8");
const cut = (from, to) => full.slice(full.indexOf(from), full.indexOf(to));
md += "\n\n---\n\n# Printed appendices\n\n" +
  "*These two lists are copied from `results/full-results/FULL-RESULTS.md` so the printed thesis is complete.*\n\n" +
  cut("## Appendix A: every test problem", "## Appendix B").replace("## Appendix A: every test problem", "## Appendix E. Every test problem (234)") +
  cut("## Appendix B: every training problem", "## Appendix C").replace("## Appendix B: every training problem", "## Appendix F. Every training problem (280)");

let body = marked.parse(md, { gfm: true });

// Heading ids that match the GitHub-style links in the contents list.
const unesc = s => s.replace(/<[^>]+>/g, "").replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">");
const slug = s => unesc(s).toLowerCase().replace(/[^\w\s-]/g, "").trim().replace(/\s+/g, "-");
body = body.replace(/<h([1-3])>(.*?)<\/h\1>/g, (_, n, t) => `<h${n} id="${slug(t)}">${t}</h${n}>`);
// A table with an empty header row (| | |) would print a blank grey bar on every page it spans.
body = body.replace(/<thead>\s*<tr>(\s*<th[^>]*>\s*<\/th>)+\s*<\/tr>\s*<\/thead>/g, "");
// Tables with many rows (the appendices) get a smaller font.
body = body.replace(/<table>([\s\S]*?)<\/table>/g, (m, inner) => { const n = (inner.match(/<tr>/g) || []).length; return n > 60 ? `<table class="long">${inner}</table>` : n <= 25 ? `<table class="short">${inner}</table>` : m; });
// A rule right before a chapter would sit alone on a blank page; chapters already start on a new page.
body = body.replace(/<hr>\s*(<h1)/g, "$1");
// The cover: everything before the abstract.
const at = body.indexOf('<h2 id="abstract">');
body = `<section class="cover">${body.slice(0, at)}</section>\n${body.slice(at)}`;

const css = `
@page { size: A4; margin: 20mm 20mm 22mm 20mm;
  @bottom-center { content: counter(page); font: 9pt Georgia, serif; color: #555; } }
@page :first { @bottom-center { content: none; } }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: Georgia, "Times New Roman", serif; font-size: 10.5pt; line-height: 1.5; color: #111; background: #fff; margin: 0; }
.cover { height: 247mm; display: flex; flex-direction: column; justify-content: center; text-align: center; break-after: page; }
.cover h1 { font-size: 26pt; margin: 0 0 10pt; break-before: auto; border: none; }
.cover h2 { font-size: 14pt; font-weight: normal; font-style: italic; margin: 0 0 30pt; border: none; }
.cover p { font-size: 11pt; }
.cover hr { display: none; }
h1 { font-size: 20pt; margin: 0 0 12pt; padding-bottom: 6pt; border-bottom: 1.5pt solid #222; break-before: page; break-after: avoid; }
h2 { font-size: 13.5pt; margin: 18pt 0 6pt; break-after: avoid; }
h3 { font-size: 11.5pt; margin: 14pt 0 4pt; break-after: avoid; }
p, li { orphans: 3; widows: 3; }
a { color: #1c4f8f; text-decoration: none; }
hr { border: none; border-top: 0.6pt solid #bbb; margin: 14pt 0; }
blockquote { margin: 10pt 0; padding: 6pt 12pt; border-left: 3pt solid #1c4f8f; background: #f3f6fa; break-inside: avoid; }
blockquote p { margin: 3pt 0; }
table { width: 100%; border-collapse: collapse; margin: 6pt 0 12pt; font-size: 8.8pt; line-height: 1.35; }
th, td { border: 0.5pt solid #bbb; padding: 3pt 5pt; text-align: left; vertical-align: top; }
th { background: #eceae4; font-weight: bold; }
thead { display: table-header-group; }
tr { break-inside: avoid; }
table.long { font-size: 7.4pt; }
table.short { break-inside: avoid; }
table.long td, table.long th { padding: 1.2pt 3pt; }
code { font-family: Consolas, "Courier New", monospace; font-size: 8.8pt; background: #f1f0ec; padding: 0 2pt; border-radius: 2pt; }
pre { font-family: Consolas, "Courier New", monospace; font-size: 7.6pt; line-height: 1.3; background: #f6f5f1; border: 0.5pt solid #ddd;
      padding: 7pt 9pt; white-space: pre-wrap; word-break: break-word; break-inside: avoid; border-radius: 3pt; }
pre code { background: none; padding: 0; font-size: inherit; }
img { display: block; max-width: 100%; height: auto; margin: 8pt auto 2pt; break-inside: avoid; }
p:has(> img) { break-inside: avoid; break-after: avoid; margin: 0; }
ul, ol { padding-left: 18pt; }
#contents { break-before: page; font-size: 20pt; border-bottom: 1.5pt solid #222; padding-bottom: 6pt; }
#contents + ul { font-size: 9.5pt; line-height: 1.35; }
`;
fs.writeFileSync(HTML, `<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>Stop Overthinking, Keep Passing the Tests</title><style>${css}</style></head><body>${body}</body></html>`);

const url = "file:///" + path.resolve(HTML).replace(/\\/g, "/");
execFileSync(EDGE, ["--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--print-to-pdf-no-header",
  "--virtual-time-budget=15000", `--print-to-pdf=${path.resolve(PDF)}`, url], { stdio: "ignore" });
console.log(`${HTML} and ${PDF} (${(fs.statSync(PDF).size / 1024).toFixed(0)} KB)`);
