# file: html.py
# vim:fileencoding=utf-8:ft=python:fdm=indent
# Copyright © 2011-2015 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# Created: 2011-03-28 22:38:23 +0200
# Last modified: 2016-06-05 12:58:05 +0200
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

"HTML output routines for lamprop."

from .version import __version__

_header = """<!DOCTYPE html>
<html lang="en-US">
  <head>
    <meta charset="UTF-8">
    <meta name="description" contents="lamprop output">
  </head>
  <body>
    <!-- outer table -->
    <table cellpadding="10%">
      <caption><strong>Properties of {}</strong></caption>
      <tbody align="center">
        <tr>
          <td  align="center" colspan="2">created by {} {}.</td>
        </tr>"""

_footer = """      </tbody>
    </table>
    <hr />
  </body>
</html>"""

_epheader = """        <!-- first row; tables -->
        <tr>
          <td>
            <table border="1" frame="hsides"
              rules="groups" cellpadding="5%">
              <caption><strong>Laminate stacking</strong></caption>
              <thead align="right">
                <tr>
                  <td>Layer</td><td>weight</td>
                  <td>angle</td><td>vf</td><td align="left">fiber type</td>
                </tr>
                <tr>
                  <td></td><td>[g/m&sup2;]</td><td>[&deg;]</td><td></td>
                </tr>
              </thead>
              <tbody align="right">"""

_epfooter = """              </tbody>
            </table>
          </td>
          <td>
            <table border="1" frame="hsides" rules="groups" cellpadding="5%">
              <caption><strong>Engineering properties</strong></caption>
              <thead align="right">
                <tr>
                  <td>Property</td><td>Value</td>
                  <td align="left">Dimension</td>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>v<sub>f</sub></td><td>{:4.2f}</td><td align="left">-</td>
                </tr>
                <tr>
                  <td>w<sub>f</sub></td><td>{:4.2f}</td><td align="left">-</td>
                </tr>
                <tr>
                  <td>thickness</td><td>{:.2g}</td><td>mm</td>
                </tr>
                <tr>
                  <td>density</td><td>{:.3g}</td><td>g/cm&sup3;</td>
                </tr>
                <tr>
                  <td>weight</td><td>{:.0f}</td><td>g/m&sup2;</td>
                </tr>
                <tr>
                  <td>resin</td><td>{:.0f}</td><td>g/m&sup2;</td>
                </tr>
              </tbody>
                <tr>
                  <td>E<sub>x</sub></td><td>{:8.0f}</td><td>MPa</td>
                </tr>
                <tr>
                  <td>E<sub>y</sub></td><td>{:8.0f}</td><td>MPa</td>
                </tr>
                <tr>
                  <td>G<sub>xy</sub></td><td>{:8.0f}</td><td>MPa</td>
                </tr>
                <tr>
                  <td>&nu;<sub>xy</sub></td><td>{:g}</td><td>-</td>
                </tr>
                <tr>
                  <td>&nu;<sub>yx</sub></td><td>{:g}</td><td>-</td>
                </tr>
                <tr>
                  <td>&alpha;<sub>x</sub></td><td>{:g}</td>
                  <td>K<sup>-1</sup></td>
                </tr>
                <tr>
                  <td>&alpha;<sub>y</sub></td><td>{:g}</td>
                  <td>K<sup>-1</sup></td>
                </tr>
              </tbody>
            </table>
          </td>
        </tr>"""

_mat1 = """        <tr>
          <td colspan="2">
            <table border="1" frame="vsides" rules="groups" cellpadding="5%">
              <caption><strong>{}</strong></caption>
              <colgroup span="1"></colgroup>
              <colgroup span="1"></colgroup>
              <colgroup span="6"></colgroup>
              <colgroup span="1"></colgroup>
              <colgroup span="1"></colgroup>
              <tbody align="center">
                <tr>
                  <td>{}</td>
                  <td rowspan="6">=</td>"""

_mat2 = """                  <td rowspan="6">&times;</td>
                  <td>{}</td>
                </tr>"""

_mat3 = """                <tr>
                  <td>{}</td>"""

_mat4 = """                  <td>{}</td>
                </tr>"""

_mat5 = """              </tbody>
            </table>
          </td>
        </tr>"""


def out(lam, eng, mat):
    """HTML main output function."""
    print(_header.format(lam.name, 'lamprop', __version__))
    if eng:
        _engprop(lam)
    if mat:
        _matrices(lam)
    print(_footer)


def _engprop(l):
    '''Prints the engineering properties as a HTML table.'''
    print(_epheader)
    for ln, la in enumerate(l.layers, start=1):
        print('                <tr>')
        s = "                  <td>{}</td><td>{:4.0f}</td><td>{:5.0f}</td>"
        print(s.format(ln, la.fiber_weight, la.angle))
        s = '                  <td>{:4.2f}</td><td align="left">{}</td>'
        print(s.format(la.vf, la.fiber.name))
        print('                </tr>')
    print(_epfooter.format(l.vf, l.wf, l.thickness, l.density,
                           l.fiber_weight+l.resin_weight, l.resin_weight,
                           l.Ex, l.Ey, l.Gxy, l.nuxy, l.nuyx, l.alphax,
                           l.alphay))


def _matrices(l):
    '''Prints the ABD and abd matrices as HTML tables.'''
    def pr(mat, row):
        """Print a row from a matrix"""
        numl = []
        for m in range(6):
            num = mat[row, m]
            if num == 0.0:
                nums = '0'
            else:
                nums, exp = "{:> 10.4e}".format(num).split('e')
                exp = int(exp)
                if exp != 0:
                    nums += '&times;10<sup>{}</sup>'.format(exp)
            numl.append(nums)
        print('          <td>' + '</td><td>'.join(numl) + '</td>')
    fstr = ["N<sub>x</sub>", "N<sub>y</sub>", "N<sub>xy</sub>",
            "M<sub>x</sub>", "M<sub>y</sub>", "M<sub>xy</sub>"]
    dstr = ["&epsilon;<sub>x</sub>", "&epsilon;<sub>y</sub>",
            "&gamma;<sub>xy</sub>", "&kappa;<sub>x</sub>",
            "&kappa;<sub>y</sub>", "&kappa;<sub>xy</sub>"]
    print(_mat1.format('Stiffness (ABD) matrix', fstr[0]))
    pr(l.ABD, 0)
    print(_mat2.format(dstr[0]))
    for n in range(1, 6):
        print(_mat3.format(fstr[n]))
        pr(l.ABD, n)
        print(_mat4.format(dstr[n]))
    print(_mat5)
    print(_mat1.format('Compliance (abd) matrix', dstr[0]))
    pr(l.abd, 0)
    print(_mat2.format(fstr[0]))
    for n in range(1, 6):
        print(_mat3.format(dstr[n]))
        pr(l.abd, n)
        print(_mat4.format(fstr[n]))
    print(_mat5)
