# file: test_output.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2018-12-30T01:32:58+0100
# Last modified: 2020-12-29T12:58:39+0100
"""Compare output to reference output."""

import zipfile
from lp.parser import parse
import lp.text as text
import lp.latex as latex
import lp.html as html

laminates = parse('test/hyer.lam')


def test_text_output():
    # Read reference. Remove "Generated" lines.
    with zipfile.ZipFile("test/reference/reference.zip") as refz:
        with refz.open("hyer-2020.12.28.txt") as orig:
            origlines = orig.read().decode().splitlines()
    origlines = [ln for ln in origlines if 'Generated' not in ln]
    # Produce text output
    outlist = []
    for curlam in laminates:
        outlist += text.out(curlam, True, True, True)
    outlist = [ln for ln in outlist if 'Generated' not in ln]
    assert outlist == origlines


def test_LaTeX_output():
    # Read reference. Remove "calculated by" lines.
    with zipfile.ZipFile("test/reference/reference.zip") as refz:
        with refz.open("hyer-2020.12.28.tex") as orig:
            origlines = orig.read().decode().splitlines()
    origlines = [ln for ln in origlines if 'calculated' not in ln]
    # Produce LaTeX output
    outlist = []
    for curlam in laminates:
        outlist += latex.out(curlam, True, True, True)
    outlist = [ln for ln in outlist if 'calculated' not in ln]
    assert outlist == origlines


def test_html_output():
    # Read reference. Remove "calculated by" lines.
    with zipfile.ZipFile("test/reference/reference.zip") as refz:
        with refz.open("hyer-2020.12.28.html") as orig:
            origlines = orig.read().decode().splitlines()
    origlines = [ln for ln in origlines if 'created by' not in ln]
    # Produce LaTeX output
    outlist = []
    for curlam in laminates:
        outlist += html.out(curlam, True, True, True)
    outlist = [ln for ln in outlist if 'created by' not in ln]
    assert outlist == origlines
