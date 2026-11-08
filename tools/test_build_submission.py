import os
import shutil
import sys

import pytest

sys.path.insert(0, os.path.dirname(__file__))
import build_submission as bs

SAMPLE = """# Laboratory 9 - Sample

**Team 4: Sample**

Members:

- Ada LOVELACE

## 1. Objective

We compute η = F_R(τα) − F_R·U_L · x with **bold**, *italic* and `code`.

| Quantity | Value |
|:--|--:|
| G_T | 600 W/m² |

> x = (T_i − T_a) / G_T

```python
x = (50 - 5) / 600
```

```text
x = 0.0750
```

---pagebreak---

## 2. Conclusions

- done
"""


@pytest.mark.skipif(not (os.path.exists(bs.SOFFICE) or shutil.which("soffice")), reason="LibreOffice not installed")
def test_sample_builds_docx_and_pdf(tmp_path):
    fitz = pytest.importorskip("pymupdf")
    md = tmp_path / "s.md"
    md.write_text(SAMPLE, encoding="utf8")
    out = tmp_path / "Sample.pdf"
    bs.build_docx(str(md), str(tmp_path / "Sample.docx"))
    bs.to_pdf(str(tmp_path / "Sample.docx"), str(out))
    assert (tmp_path / "Sample.docx").exists() and out.exists()
    doc = fitz.open(str(out))
    assert len(doc) >= 2                                    # the page break
    text = "".join(p.get_text() for p in doc)
    for key in ("Laboratory 9 - Sample", "Ada LOVELACE", "1. Objective", "600 W/m²", "x = 0.0750", "2. Conclusions"):
        assert key in text, key
    assert "**" not in text and "```" not in text


def test_long_code_lines_wrap_with_indentation():
    line = "    " + "word " * 40
    out = [p + line[a:b] for p, a, b in bs.wrap(line)]
    assert len(out) > 1 and all(len(x) <= 92 for x in out) and out[1].startswith("      ")
    assert "".join(line[a:b] for _, a, b in bs.wrap(line)).replace(" ", "") == line.replace(" ", "")


def test_python_highlighting_colours_keywords_strings_and_numbers():
    cols = bs.highlight(['def f(x):', '    return "a" + 1'])
    assert cols[0][0] != bs.CODE_INK                      # the keyword
    assert len({tuple(c) for c in cols[0] + cols[1]}) >= 3
