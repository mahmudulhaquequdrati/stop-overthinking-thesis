// Join the thesis chapters into one file: thesis/THESIS.md.
//
// 1. What problem does this solve?  The thesis is written as one file per chapter (easy to edit),
//    but a reader or a teacher wants ONE document from top to bottom.
// 2. Why do we need it?  So there is always one complete, up-to-date copy to read, print or hand in.
// 3. What goes in?   thesis/00-*.md ... thesis/09-*.md, in file-name order.
// 4. What comes out? thesis/THESIS.md with a table of contents at the top.
// 5. Why this way?   Plain concatenation: the chapters already sit in thesis/, so the figure links
//                    (../results/...) still work from THESIS.md. Never edit THESIS.md by hand.
const fs = require("fs"), path = require("path");
const DIR = "thesis";
const files = fs.readdirSync(DIR).filter(f => /^\d\d-.*\.md$/.test(f)).sort();
const parts = files.map(f => fs.readFileSync(path.join(DIR, f), "utf8").trim());
const slug = s => s.toLowerCase().replace(/[^\w\s-]/g, "").trim().replace(/\s+/g, "-");
const toc = [];
for (const p of parts.slice(1)) for (const line of p.split("\n")) {   // the front matter comes before the contents
  const m = line.match(/^(#{1,2}) (.+)$/);
  if (m) toc.push(`${m[1] === "#" ? "" : "  "}- [${m[2]}](#${slug(m[2])})`);
}
const head = `<!-- Built by: node scripts/build_thesis.js — do not edit by hand; edit the chapter files in thesis/. -->\n\n`;
const [front, ...rest] = parts;
const out = head + front + "\n\n---\n\n## Contents\n\n" + toc.join("\n") + "\n\n---\n\n" + rest.join("\n\n---\n\n") + "\n";
fs.writeFileSync(path.join(DIR, "THESIS.md"), out);
console.log(`thesis/THESIS.md: ${files.length} chapters, ${out.split("\n").length} lines, ${out.split(/\s+/).length} words`);
