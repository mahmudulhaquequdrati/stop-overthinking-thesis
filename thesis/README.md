# The thesis

**Read the whole thesis in one file: [THESIS.md](THESIS.md)** (open it in VS Code and press **Ctrl+Shift+V** to see the charts).

**🖨️ To print or hand in: [Stop-Overthinking-Thesis.pdf](Stop-Overthinking-Thesis.pdf)** (A4, 56 pages, with page numbers).
It also contains the full lists of every test and training problem (printed appendices E and F).
Rebuild it after any change:

```text
npm install --prefix <any-folder> marked@12        (once)
MARKED=<any-folder>/node_modules/marked node scripts/build_thesis_pdf.js
```

| File | Chapter |
|---|---|
| [00-front-matter.md](00-front-matter.md) | Title, abstract, **the thesis in one page (for everyone)**, key facts |
| [01-introduction.md](01-introduction.md) | 1. The problem, the gap, the question, the hypotheses |
| [02-background.md](02-background.md) | 2. What LLMs, tokens, thinking, loops, LoRA and code test sets are; earlier work |
| [03-method.md](03-method.md) | 3. The six ways, the data, the training, the fairness rules, changes from the proposal |
| [04-how-we-measure.md](04-how-we-measure.md) | 4. **Where the evidence comes from:** pass rule, accuracy, points, error bars, tokens, loops |
| [05-results.md](05-results.md) | 5. All results, **starting with the thinking limit** |
| [06-analysis.md](06-analysis.md) | 6. Why it happened, earlier work, what could be wrong |
| [07-conclusion-and-future-work.md](07-conclusion-and-future-work.md) | 7. The answer, advice, **size results (0.8B/4B)**, bigger models still open |
| [08-references.md](08-references.md) | References |
| [09-appendices.md](09-appendices.md) | Every problem, how to repeat the work, project history, words |

**Size numbers for the paper:** [../results/RESULTS-INDEX.md](../results/RESULTS-INDEX.md) · §5.13 in the thesis.  
**All piles and charts:** [../easy-thesis/10-all-counts.md](../easy-thesis/10-all-counts.md). The same pictures are on the one page in this folder.

## Rules for editing

- Edit the **chapter files**, never THESIS.md. Then rebuild: `node scripts/build_thesis.js`.
- Every **2B** number comes from [results/full-results/FULL-RESULTS.md](../results/full-results/FULL-RESULTS.md).
  **0.8B / 4B** numbers come from [results/0.8b/SUMMARY.md](../results/0.8b/SUMMARY.md) and [results/4b/SUMMARY.md](../results/4b/SUMMARY.md).
- To fill in before handing in: your name, supervisor, university and department (top of `00-front-matter.md`).

