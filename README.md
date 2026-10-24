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
  shared/                  reusable Python functions (they only return values, no printing or plotting)
  explanation-notebooks/   simple and in-depth notebooks (+ images/ with the diagrams they show)
  pdf/                     PDF exports of the notebooks (code and hand calculations hidden)
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

Open a notebook in VS Code or JupyterLab and pick the `human-centric-ai-for-energy-labs` kernel. Notebooks add `../shared` to `sys.path`, so run them from their own folder.

On Windows, run commands that use the environment through `conda run -n human-centric-ai-for-energy-labs ...` (or activate it first). Starting the environment's `python.exe` directly skips the DLL paths and matplotlib crashes.

## Re-executing a notebook from the terminal

```
cd lab-3/explanation-notebooks
jupyter nbconvert --to notebook --execute --inplace lab-3-in-depth.ipynb
```

## Exporting a notebook to PDF

The PDFs are made with nbconvert and a Chromium-based browser (Chrome or Edge), so no LaTeX is needed:

```
jupyter nbconvert --to html --no-input --embed-images lab-3-in-depth.ipynb
chrome --headless --disable-gpu --no-pdf-header-footer --print-to-pdf=../pdf/lab-3-in-depth.pdf lab-3-in-depth.html
```

`--no-input` hides the code cells and `--embed-images` puts the SVG diagrams inside the HTML. Delete the temporary `.html` afterwards.
