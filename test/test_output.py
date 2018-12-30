# file: test_output.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2018 R.F. Smith <rsmith@xs4all.nl>
# Created: 2018-12-30T01:32:58+0100
# Last modified: 2018-12-30T02:38:12+0100
"""Compare output to reference output."""

from lamprop.parser import parse
import lamprop.text as text

laminates = parse('test/hyer.lam')


def test_text_output():
    # Read reference. Remove "Generated" lines.
    with open('test/reference/hyer-3.8.txt') as orig:
        origlines = orig.read().splitlines()
    origlines = [ln for ln in origlines if 'Generated' not in ln]
    # Produce text output
    outlist = []
    for curlam in laminates:
        outlist += text.engprop(curlam).splitlines()
        outlist += text.matrices(curlam).splitlines()
        outlist.append('')
    outlist = [ln for ln in outlist if 'Generated' not in ln]
    assert outlist == origlines
