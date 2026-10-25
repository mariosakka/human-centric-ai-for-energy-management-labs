"""Rebuild the PDF and the companion markdown folder of every notebook of a lab.

Run from the repo root inside the conda env:
    conda run -n human-centric-ai-for-energy-labs python tools/build_docs.py lab-2 lab-3 lab-4
    (no argument = all labs)

For each notebook this writes  <lab>/explanation-notebooks/visual explanations/<name>/<name>.md  (+ figures/)  and  <name>.pdf.
Code cells, tables-as-code, display equations (lab 2) and the hand-calculation sections are left out.
Notebooks are NOT executed here: run them first (jupyter nbconvert --to notebook --execute --inplace <nb>).
"""
import base64, os, re, shutil, subprocess, sys, tempfile
import nbformat as nbf
from nbconvert import MarkdownExporter

BROWSERS = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            "/usr/bin/google-chrome", "/usr/bin/chromium", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
CHROME = next((b for b in BROWSERS if os.path.exists(b)), None)

JN = "explanation-notebooks/jupyter notebooks"
TE = "explanation-notebooks/visual explanations"
L2A, L2B = f"lab-2/{JN}/lab-2-plus-lecture-challenge", f"lab-2/{JN}/only-lab-2"


BOX_CSS = ("<style>blockquote{border:1.5px solid #4a6fa5 !important;background:#eef3fa;border-radius:4px;"
           "padding:6px 14px !important;margin:10px 0;color:#1b2733;page-break-inside:avoid}"
           "blockquote p{margin:4px 0}</style>")


def starts(c, prefix):
    return c.cell_type == "markdown" and c.source.lstrip().startswith(prefix)


def strip_display_eq(c):
    if c.cell_type == "markdown":
        c.source = re.sub(r"\$\$.*?\$\$", "", c.source, flags=re.S)
    return c


keep_all = lambda c: True
no_step4 = lambda c: not starts(c, "## Step 4")
no_hand = lambda c: not starts(c, "## Hand calculation")
no_pmv_maths = lambda c: not starts(c, "## 0.7 How PMV and PPD are computed")

# notebook, which cells to keep, per-cell edit
JOBS = {
    "lab-2": [(f"{L2B}/lab-2.ipynb", no_step4, strip_display_eq),
              (f"{L2B}/lab-2-simple.ipynb", no_step4, strip_display_eq),
              (f"{L2A}/lab-2-in-depth.ipynb", no_step4, strip_display_eq),
              (f"{L2A}/lab-2-in-depth-simple.ipynb", no_step4, strip_display_eq)],
    "lab-3": [(f"lab-3/{JN}/lab-3-in-depth.ipynb", no_pmv_maths, lambda c: c),
              (f"lab-3/{JN}/lab-3-simple.ipynb", keep_all, lambda c: c)],
    "lab-4": [(f"lab-4/{JN}/lab-4-in-depth.ipynb", no_hand, lambda c: c),
              (f"lab-4/{JN}/lab-4-simple.ipynb", no_hand, lambda c: c)],
}


def build(nb_path, keep, edit):
    lab = nb_path.split("/")[0]
    name = os.path.splitext(os.path.basename(nb_path))[0]
    nb_dir = os.path.dirname(nb_path)
    out = os.path.join(lab, TE, name)
    shutil.rmtree(os.path.join(out, "figures"), ignore_errors=True)
    os.makedirs(os.path.join(out, "figures"), exist_ok=True)
    nb = nbf.read(nb_path, as_version=4)
    nb.cells = [edit(c) for c in nb.cells if keep(c)]

    # markdown companion: executed outputs become figures/output_*.png, diagrams are copied next to them
    exp = MarkdownExporter()
    exp.exclude_input = True
    body, res = exp.from_notebook_node(nb, resources={"output_files_dir": "figures"})
    for fname, data in res["outputs"].items():
        with open(os.path.join(out, fname), "wb") as f:
            f.write(data)

    def copy_svg(m):
        src = os.path.normpath(os.path.join(nb_dir, m.group(2)))
        shutil.copy(src, os.path.join(out, "figures", os.path.basename(src)))
        return f"![{m.group(1)}](figures/{os.path.basename(src)})"
    body = re.sub(r"!\[([^\]]*)\]\(([^)\s]+\.svg)\)", copy_svg, body)
    body = re.sub(r"\n{3,}", "\n\n", body).strip() + "\n"
    with open(os.path.join(out, name + ".md"), "w", encoding="utf8", newline="\n") as f:
        f.write(body)

    # PDF: temp notebook next to the original (relative image paths resolve), html with embedded images, browser print
    tmp = os.path.join(nb_dir, "tmp-" + name)
    nbf.write(nb, tmp + ".ipynb")
    subprocess.run([sys.executable, "-m", "jupyter", "nbconvert", "--to", "html", "--no-input", "--embed-images", tmp + ".ipynb"],
                   check=True, capture_output=True)
    html = open(tmp + ".html", encoding="utf8").read()

    def inline_svg(m):   # nbconvert --embed-images skips SVG: inline it so the browser finds it from the temp folder
        path = os.path.normpath(os.path.join(nb_dir, m.group(1)))
        return 'src="data:image/svg+xml;base64,' + base64.b64encode(open(path, "rb").read()).decode() + '"'
    html = re.sub(r'src="([^":]+\.svg)"', inline_svg, html)
    html = html.replace("</head>", BOX_CSS + "</head>", 1)    # definitions are markdown blockquotes: draw them as boxes
    open(tmp + ".html", "w", encoding="utf8").write(html)
    tdir = tempfile.mkdtemp()
    thtml, tpdf = os.path.join(tdir, "i.html"), os.path.join(tdir, "o.pdf")   # short paths: the browser fails on very long ones
    shutil.copy(tmp + ".html", thtml)
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=30000", f"--print-to-pdf={tpdf}",
                    "file:///" + thtml.replace("\\", "/")], capture_output=True)
    shutil.copy(tpdf, os.path.join(out, name + ".pdf"))
    for ext in (".ipynb", ".html"):
        os.remove(tmp + ext)
    shutil.rmtree(tdir, ignore_errors=True)
    print(name, "md", len(body), "chars; pdf", os.path.getsize(os.path.join(out, name + ".pdf")) // 1024, "KB")


if __name__ == "__main__":
    if CHROME is None:
        sys.exit("No Chrome/Edge found: edit BROWSERS in tools/build_docs.py")
    for lab in sys.argv[1:] or JOBS:
        for job in JOBS[lab]:
            build(*job)
