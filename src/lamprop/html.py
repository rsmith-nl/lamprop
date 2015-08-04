# file: html.py
# vim:fileencoding=utf-8:ft=python
# Copyright © 2011-2015 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# Created: 2011-03-28 22:38:23 +0200
# Last modified: 2015-05-16 16:59:27 +0200
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


def out(lam, eng, mat):
    '''HTML main output function.'''
    print('    <!-- outer table -->')
    print('    <table cellpadding="10%">')
    s = "      <caption><strong>Properties of {}</strong></caption>"
    print(s.format(lam.name))
    print('      <tbody align="center">')
    print('        <tr>')
    s = '          <td  align="center" colspan="2">created by {} {}.</td>'
    print(s.format('lamprop', __version__))
    print('        </tr>')
    if eng:
        _engprop(lam)
    if mat:
        _matrices(lam)
    print('      </tbody>')
    print('    </table>')
    print('    <hr />')


def _engprop(l):
    '''Prints the engineering properties as a HTML table.'''
    print('        <!-- first row; tables -->')
    print('        <tr>')
    print('          <td>')
    print('            <table border="1" frame="hsides"')
    print('              rules="groups" cellpadding="5%">')
    print('              '
          '<caption><strong>Laminate stacking</strong></caption>')
    print('              <thead align="right">')
    print('                <tr>')
    print('                  <td>Layer</td><td>weight</td>')
    print('                  <td>angle</td><td>vf</td>'
          '<td align="left">fiber type</td>')
    print('                </tr>')
    print('                <tr>')
    print('                  <td></td><td>[g/m&sup2;]</td>'
          '<td>[&deg;]</td><td>[%]</td>')
    print('                </tr>')
    print('              </thead>')
    print('              <tbody align="right">')
    for ln, la in enumerate(l.layers):
        print('                <tr>')
        s = "                  <td>{}</td><td>{:4.0f}</td><td>{:5.0f}</td>"
        print(s.format(ln, la.fiber_weight, la.angle))
        s = '                  <td>{:4.2f}</td><td align="left">{}</td>'
        print(s.format(la.vf, la.fiber.name))
        print('                </tr>')
    print('              </tbody>')
    print('            </table>')
    print('          </td>')
    print('          <td>')
    print('            <table border="1" frame="hsides"'
          ' rules="groups" cellpadding="5%">')
    print('              <caption><strong>Engineering properties '
          '</strong></caption>')
    print('              <thead align="right">')
    print('                <tr>')
    print('                  <td>Property</td><td>Value</td>')
    print('                  <td align="left">Dimension</td>')
    print('                </tr>')
    print('              </thead>')
    print('              <tbody align="right">')
    print('                <tr>')
    s = "                  <td>v<sub>f</sub></td>"\
        '<td>{:4.2f}</td><td align="left">-</td>'
    print(s.format(l.vf))
    print('                </tr>')
    print('                <tr>')
    s = "                  <td>w<sub>f</sub></td>"\
        '<td>{:4.2f}</td><td align="left">-</td>'
    print(s.format(l.wf))
    print('                </tr>')
    print('                <tr>')
    s = "                  <td>thickness</td><td>{:.3g}</td>"
    print(s.format(l.thickness))
    print('                  <td align="left">mm</td>')
    print('                </tr>')
    print('                <tr>')
    s = "                  <td>density</td><td>{:.3g}</td>"
    print(s.format(l.ρ))
    print('                  <td align="left">g/cm&sup3;</td>')
    print('                </tr>')
    print('                <tr>')
    s = "                  <td>weight</td><td>{:.0f}</td>"
    print(s.format(l.fiber_weight+l.resin_weight, l.resin_weight))
    print('                  <td align="left">g/m&sup2;</td>')
    print('                </tr>')
    print('                <tr>')
    s = "                  <td>resin</td><td>{:.0f}</td>"
    print(s.format(l.resin_weight))
    print('                  <td align="left">g/m&sup2;</td>')
    print('                </tr>')
    print('              </tbody>')
    print('                <tr>')
    s = "                  <td>E<sub>x</sub></td><td>{:8.0f}</td>"
    print(s.format(l.Ex))
    print('                  <td align="left">MPa</td>')
    print('                </tr>')
    print('                <tr>')
    s = "                  <td>E<sub>y</sub></td><td>{:8.0f}</td>"
    print(s.format(l.Ey))
    print('                  <td align="left">MPa</td>')
    print('                </tr>')
    print('                <tr>')
    s = "                  <td>G<sub>xy</sub></td><td>{:8.0f}</td>"
    print(s.format(l.Gxy))
    print('                  <td align="left">MPa</td>')
    print('                </tr>')
    print('                <tr>')
    s = "                  <td>&nu;<sub>xy</sub></td><td>{:g}</td>"
    print(s.format(l.νxy))
    print('                  <td align="left">-</td>')
    print('                </tr>')
    print('                <tr>')
    s = "                  <td>&nu;<sub>yx</sub></td><td>{:g}</td>"
    print(s.format(l.νyx))
    print('                  <td align="left">-</td>')
    print('                </tr>')
    print('                <tr>')
    s = "                  <td>&alpha;<sub>x</sub></td><td>{:g}</td>"
    print(s.format(l.αx))
    print('                  <td align="left">K<sup>-1</sup></td>')
    print('                </tr>')
    print('                <tr>')
    s = "                  <td>&alpha;<sub>y</sub></td><td>{:g}</td>"
    print(s.format(l.αy))
    print('                  <td align="left">K<sup>-1</sup></td>')
    print('                </tr>')
    print('              </tbody>')
    print('            </table>')
    print('          </td>')
    print('        </tr>')


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
    print('        <tr>')
    print('          <!-- second row, stiffness or ABD matrix -->')
    print('          <td colspan="2">')
    print('            <table border="1" frame="vsides" '
          'rules="groups" cellpadding="5%%">')
    print('              <caption><strong>Stiffness (ABD) matrix</strong>'
          '</caption>')
    print('              <colgroup span="1"></colgroup>')
    print('              <colgroup span="1"></colgroup>')
    print('              <colgroup span="6"></colgroup>')
    print('              <colgroup span="1"></colgroup>')
    print('              <colgroup span="1"></colgroup>')
    print('              <tbody align="center">')
    print('                <tr>')
    print('                  <td>{}</td>'.format(fstr[0]))
    print('                  <td rowspan="6">=</td>')
    pr(l.ABD, 0)
    print('                  <td rowspan="6">&times;</td>')
    print('                  <td>{}</td>'.format(dstr[0]))
    print('                </tr>')
    for n in range(1, 6):
        print('                <tr>')
        print('                  <td>{}</td>'.format(fstr[n]))
        pr(l.ABD, n)
        print('                  <td>{}</td>'.format(dstr[n]))
        print('                </tr>')
    print('              </tbody>')
    print('            </table>')
    print('          </td>')
    print('        </tr>')
    print('        <tr>')
    print('          <!-- third row, compliance or abd matrix -->')
    print('          <td colspan="2">')
    print('            <table border="1" frame="vsides" '
          'rules="groups" cellpadding="5%">')
    print('              <caption><strong>Compliance (abd) matrix</strong>'
          '</caption>')
    print('              <colgroup span="1"></colgroup>')
    print('              <colgroup span="1"></colgroup>')
    print('              <colgroup span="6"></colgroup>')
    print('              <colgroup span="1"></colgroup>')
    print('              <colgroup span="1"></colgroup>')
    print('              <tbody align="center">')
    print('                <tr>')
    print('                  <td>{}</td>'.format(dstr[0]))
    print('                  <td rowspan="6">=</td>')
    pr(l.abd, 0)
    print('                  <td rowspan="6">&times;</td>')
    print('                  <td>{}</td>'.format(fstr[0]))
    print('                </tr>')
    for n in range(1, 6):
        print('                <tr>')
        print('                  <td>{}</td>'.format(dstr[n]))
        pr(l.abd, n)
        print('                  <td>{}</td>'.format(fstr[n]))
        print('                </tr>')
    print('              </tbody>')
    print('            </table>')
    print('          </td>')
    print('        </tr>')
