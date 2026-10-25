# human-centric-ai-for-energy-management-labs

Labs for *Human-Centric Artificial Intelligence for Energy Management*.

| Lab | Topic | Folder |
|---|---|---|
| 2 | Psychrometrics and thermal comfort (PMV / PPD) | `lab-2/` |
| 3 | HVAC setpoint optimization (App 2.3) | `lab-3/` |
| 4 | Steady-state heat loss of a house and a human-centred setpoint | `lab-4/` |

Each lab has the same layout:

```
lab-N/
  shared/                          reusable Python functions (they only return values, no printing or plotting)
  explanation-notebooks/
    jupyter notebooks/             simple and in-depth notebooks, with images/ (the diagrams they show)
    visual explanations/<name>/      PDF export of a notebook + <name>.md companion + figures/
```

## Environment

```
conda env create -f environment.yml
conda activate human-centric-ai-for-energy-labs
```

To update an existing environment after the file changed:

```
conda env update -n human-centric-ai-for-energy-labs -f environment.yml --prune
```

Open a notebook in VS Code or JupyterLab and pick the `human-centric-ai-for-energy-labs` kernel. Notebooks add the lab's `shared/` folder to `sys.path` with a relative path, so run them from their own folder.

On Windows, run commands that use the environment through `conda run -n human-centric-ai-for-energy-labs ...` (or activate it first). Starting the environment's `python.exe` directly skips the DLL paths and matplotlib crashes.

## Re-executing a notebook from the terminal

```
cd "lab-3/explanation-notebooks/jupyter notebooks"
jupyter nbconvert --to notebook --execute --inplace lab-3-in-depth.ipynb
```

## Building the PDFs and markdown companions

`tools/build_docs.py` rebuilds, for every notebook, the folder `lab-N/explanation-notebooks/visual explanations/<name>/` with `<name>.pdf`, `<name>.md` and `figures/`. Execute the notebooks first, then from the repo root:

```
conda run -n human-centric-ai-for-energy-labs python tools/build_docs.py lab-2 lab-3 lab-4
```

No argument builds all labs. The PDF is rendered from the markdown by the `report-to-pdf` skill (fpdf2; SVG diagrams, definition boxes, captions and maths), which `tools/build_docs.py` finds under `~/.claude/plugins` or through the `REPORT_TO_PDF_SCRIPT` environment variable (path of its `scripts/build_report_pdf.py`). It rasterises SVGs with headless Chrome or Edge, which takes a few minutes for all labs. Code cells, display equations (lab 2) and the hand-calculation sections are left out. The cell filters per notebook are at the top of the script.

The `.md` and `figures/` are committed; the `.pdf` files are not.
