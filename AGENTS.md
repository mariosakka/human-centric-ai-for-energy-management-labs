# Instructions for this repo (AGENTS.md; CLAUDE.md imports it so Claude Code and other agents read the same rules)

Labs for *Human-Centric Artificial Intelligence for Energy Management*. Each lab is an assignment PDF (`lab-N/AI for Energy Lab N - ....pdf`) that gets solved and explained. Labs 3, 4, 5 and 6 are the reference examples: copy their structure and quality for any new lab. `README.md` has the layout and environment commands.

## Layout of every lab

```
lab-N/
  AI for Energy Lab N - <title>.pdf        the assignment (never edit)
  shared/                                   reusable Python, return values only (no print, no plots, no UI)
  explanation-notebooks/
    jupyter notebooks/                      <name>-simple.ipynb, <name>-in-depth.ipynb, images/ (SVG diagrams)
    visual explanations/<name>/             <name>.md + figures/ (committed), <name>.pdf (never committed)
```

Add the lab to the table in `README.md` and to `JOBS` in `tools/build_docs.py`.

## How to solve a lab

1. Read the assignment PDF as an image too (`pdftotext` garbles Greek letters and subscripts): render pages with PyMuPDF and look at them.
2. Put the sheet's data and the formulas in `lab-N/shared/<topic>.py` as functions that only return values, with an assert-based or pytest test next to it. Compute every number by running code, and check the key results independently.
   Every algorithm, formula, data table and sheet constant lives in `shared/`: notebooks import them and never define their own `def` or lambda for a computation (inline definitions are only allowed for drawing helpers such as annotations and plot styling). A new calculation a notebook needs goes into `shared/` first, with a test. Before finishing a lab, check each notebook's code cells for inline computation.
3. Write two executed notebooks that answer every sub-question, including the optional extension:
   - `*-simple`: plain words, analogies, minimal maths.
   - `*-in-depth`: precise definitions, formulas, assumptions, limits.
   Run them from their own folder; they add `../../shared` to `sys.path` with a relative path.
4. Draw every spatial or process idea as an SVG in `images/` (real images, never ASCII art), with an italic `*Figure: ...*` caption line below it. Check labels do not overlap.
5. Build the markdown companion and the PDF (see below), render a few PDF pages to PNG and look at them.

## Writing rules (from the `explanation-notebooks` skill, `general` plugin of my-agent-skills)

- Use that skill; read its `references/shared-rules.md` plus `simplified-rules.md` or `detailed-rules.md` before writing.
- Define every domain concept in the chapter where it is first used, in one blockquote box: `> **Term** (unit): definition.` No opening glossary; nothing defined before the chapter that needs it; expand acronyms at first use; explain what a device or quantity is before using it (e.g. a thermostat, irradiance, a fill factor).
- Every device, instrument, sensor or piece of equipment that is defined (a thermostat, a VAV box, a pyranometer, a PV cell) gets its own labelled SVG diagram right after its definition box (what it looks like, its parts, how it works), in both the simple and the in-depth version. Abstract concepts do not need one.
- Interpret values ("the collector turns 52 % of the sunlight into heat") instead of narrating how they were computed.
- No tables (use graphs or short bullet lists), no meta-comments about the document or the build, no hand calculations, UI widgets or code in the markdown and PDF.
- Check with `first_use.py NOTEBOOK "term1,term2"` that each term's first hit is its definition.

## Build and commit

```
conda run -n human-centric-ai-for-energy-labs python tools/build_docs.py lab-N
```

- Always run Python through `conda run -n human-centric-ai-for-energy-labs` (starting the env's `python.exe` directly crashes matplotlib on Windows). `conda run` cannot take multi-line `-c`: put scripts in files.
- Execute notebooks before building (`jupyter nbconvert --to notebook --execute --inplace`); the build does not run them.
- The PDF is rendered from the markdown by the `report-to-pdf` skill. If the installed copy is old, set `REPORT_TO_PDF_SCRIPT` to its `scripts/build_report_pdf.py`. A full build takes minutes (SVG rasterising): run it in the background.
- Commit the notebooks, `shared/`, `images/`, the `.md` and `figures/`. Never commit PDFs (the assignment PDFs and the built ones). Commit and push only when asked.
- Every git command prints a harmless `bad object refs/desktop.ini` / repack error (Google Drive); the commit and push still succeed.
- Labs are independent: parallel agents can solve different labs at the same time, as long as only one of them edits `tools/build_docs.py`, `README.md` and AGENTS.md.

## Moodle submissions

- Each lab's submission source is `lab-N/moodle-submission/lab-N-moodle-submission.md` plus `solve_lab_N.py` (a runner that imports `shared/` and prints the answers). Build with `python tools/build_submission.py <md> -o lab-N/moodle-submission/Lab-N-Moodle-Submission-<Topic>.pdf` (via `conda run`); the `.pdf` and `.docx` are never committed.
- Style of labs 2 to 4: Letter page, Calibri, no cover page. Written in the team's voice ("we"), plain: title and team line, Members, 1. Objective, 2. Input data (table), one numbered section per sub-question with the code snippet and its output, Conclusions, Annex with the full code. Maths in plain Unicode, never LaTeX.
- Syntax is documented at the top of `tools/build_submission.py`; look at the rendered pages before finishing.
