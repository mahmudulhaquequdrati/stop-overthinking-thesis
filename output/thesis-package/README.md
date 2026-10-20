# Stop Overthinking thesis package

Prepared 20 October 2026 from the completed saved study. No new model training, inference, or generated-code execution was performed.

## Start here

- `thesis.docx`: editable Word thesis, ready to import into Google Docs.
- `thesis.pdf`: matching Word export, 60 pages in total. Preliminary pages are i–ix; Chapters 1–6 occupy Arabic pages 1–49; references and appendices continue to 51.
- `thesis-latex.pdf`: compiled LaTeX thesis, 58 pages in total. Preliminary pages are i–xi; Chapters 1–6 occupy Arabic pages 1–45; references and appendices continue to 47.
- `conference-paper.docx` and `conference-paper.pdf`: six-page conference-style paper, in two columns with full-width tables.
- `conference-paper-latex.pdf`: independently compiled six-page LaTeX paper.
- `latex/`: portable LaTeX sources, bibliography, and vector figures. The main file is `main.tex`; the short paper is `conference.tex`.
- `originality-review.md`: limited text-overlap and citation review, including its limitations.
- `qa/final-validation.json`: verified page counts, numbering, source agreement, and evidence checks.

The thesis contains 19 figures, 12 tables, and 13 verified primary-source references. Main body text is 11 point. The thesis is single column with 1.5 line spacing, US Letter pages, and one-inch margins. Both compiled formats use Times New Roman. Pagination differs because Word and LaTeX lay out paragraphs and figures differently.

## Before submission

Replace the marked author, ID, degree, department, university, supervisor, committee, contact, and submission-date fields. Add personal acknowledgments only where accurate. Signatures are intentionally blank. No names or approvals were copied from the example thesis.

This is a full thesis draft for author and supervisor review, not a claim that it has been approved by a university or conference. The short paper uses a generic conference layout because no venue was specified.

The Word contents, figure list, table list, page numbers, captions, and figure/table cross-references use genuine Word fields. Cached navigation has been populated and checked against the delivered PDF. After making edits in Word, update all fields. Google Docs import may alter pagination or field behavior, so recheck contents and section numbering after import. No live Google Doc was created.

The originality review is not a Turnitin or iThenticate certificate and does not establish a certified similarity percentage. It compares exact text against the supplied reference PDF and accessible primary-source abstracts or page descriptions. It cannot detect every form of unattributed reuse.

## Compile the LaTeX versions

Upload the complete `latex` folder to a TeX environment or open it locally. Compile `main.tex` for the thesis and `conference.tex` for the paper. Use XeLaTeX or Tectonic for Times New Roman where installed. If that font is unavailable, the sources fall back to TeX Gyre Termes; pdfLaTeX uses a Times-compatible font through mathptmx. Fonts are not redistributed in this package.

Compile at least twice so references, contents, and lists settle. Tectonic automatically repeats passes. Both supplied PDFs were successfully compiled and checked for unresolved references, unresolved citations, and overfull boxes. Remaining underfull-box notices concern loose line spacing in cells or bibliography entries.

The bibliography is embedded in each TeX document for simple standalone compilation. `references.bib` is also supplied for future BibTeX-based editing. Vector figures are in `latex/figures`; PNG versions for Word are in `figures`.

## Evidence and reproducibility

The study uses 464 unique problems: 164 HumanEval+, 166 LiveCodeBench easy, and 134 LiveCodeBench medium. Every completed LoRA combination has one answer per problem. Historical all-attempt equal-problem summaries and first-attempt comparisons are labeled separately.

`source/evidence` contains checked summaries, hashes, and the 464 test IDs. Full raw answers, grades, training material, and environment records remain in the original repository. The result-file manifest identifies those sources without inventing new measurements.

`source/build_package.py` generates prose-driven Word/LaTeX documents and plots from the repository. It requires the original repository layout, Python packages python-docx, reportlab, pypdf, and Pillow, and Poppler. It is not a standalone experimental runner. `source/populate_navigation.py` populates Word navigation from a rendered thesis PDF. `source/validate_package.py` checks final exports. The delivered manuscript prose and all six completed pass counts have been checked against the shared content and saved summaries.
