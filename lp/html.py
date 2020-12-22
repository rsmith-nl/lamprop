# file: html.py
# vim:fileencoding=utf-8:ft=python:fdm=marker
#
# Copyright © 2011-2019 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause
# Created: 2011-03-28 22:38:23 +0200
# Last modified: 2019-05-05T19:42:52+0200
"""HTML output routines for lamprop."""

from .version import __version__


def out(lam, eng, mat):  # {{{1
    """HTML main output function."""
    lines = [
        '<!DOCTYPE html>',
        '<html lang="en-US">',
        '  <head>',
        '    <meta charset="UTF-8">',
        '    <meta name="description" contents="lamprop output">',
        '  </head>',
        '  <body>',
        '    <!-- outer table -->',
        '    <table cellpadding="10%">',
        "      <caption><strong>Properties of {}</strong></caption>".format(lam.name),
        '      <tbody align="center">',
        '        <tr>',
        '          <td  align="center" colspan="2">created by'
        ' {} {}.</td>'.format('lamprop', __version__),
        '        </tr>'
    ]
    if eng:
        lines += _engprop(lam)
    if mat:
        lines += _matrices(lam)
    lines += [
        '      </tbody>',
        '    </table>',
        '    <hr />',
        '  </body>',
        '</html>',
    ]
    return lines


def _engprop(l):  # {{{1
    """Print the engineering properties as a HTML table."""
    lines = [
        '        <!-- first row; tables -->',
        '        <tr>',
        '          <td>',
        '            <table border="1" frame="hsides"',
        '              rules="groups" cellpadding="5%">',
        '              <caption><strong>Laminate stacking</strong></caption>',
        '              <thead align="right">',
        '                <tr>',
        '                  <td>Layer</td><td>weight</td>',
        '                  <td>angle</td><td>vf</td><td align="left">fiber type</td>',
        '                </tr>',
        '                <tr>',
        '                  <td></td><td>[g/m&sup2;]</td><td>[&deg;]</td><td>[%]</td>',
        '                </tr>',
        '              </thead>',
        '              <tbody align="right">',
    ]
    for ln, la in enumerate(l.layers, start=1):
        lines += [
            '                <tr>',
            '                  <td>{}</td><td>{:4.0f}</td>'
            '<td>{:5.0f}</td>'.format(ln, la.fiber_weight, la.angle),
            '                  <td>{:g}</td><td align="left">'
            '{}</td>'.format(la.vf*100, la.fiber.name),
            '                </tr>'
        ]
    lines += [
        '              </tbody>',
        '            </table>',
        '          </td>',
        '          <td>',
        '            <table border="1" frame="hsides"'
        ' rules="groups" cellpadding="5%">',
        '              <caption><strong>Engineering properties </strong></caption>',
        '              <thead align="right">',
        '                <tr>',
        '                  <td>Property</td><td>Value</td>',
        '                  <td align="left">Dimension</td>',
        '                </tr>',
        '              </thead>',
        '              <tbody align="right">',
        '                <tr>',
        '                  <td>v<sub>f</sub></td><td>{:.3g}</td>'
        '<td align="left">%</td>'.format(l.vf*100),
        '                </tr>',
        '                <tr>',
        '                  <td>w<sub>f</sub></td><td>{:.3g}</td>'
        '<td align="left">%</td>'.format(l.wf*100),
        '                </tr>',
        '                <tr>',
        "                  <td>thickness</td><td>{:.3g}</td>".format(l.thickness),
        '                  <td align="left">mm</td>',
        '                </tr>',
        '                <tr>',
        '                  <td>density</td><td>{:.3g}</td>'.format(l.ρ),
        '                  <td align="left">g/cm&sup3;</td>',
        '                </tr>',
        '                <tr>',
        '                  <td>weight</td><td>{:.0f}</td>'.format(
            l.fiber_weight+l.resin_weight, l.resin_weight
        ),
        '                  <td align="left">g/m&sup2;</td>',
        '                </tr>',
        '                <tr>',
        '                  <td>resin</td><td>{:.0f}</td>'.format(l.resin_weight),
        '                  <td align="left">g/m&sup2;</td>',
        '                </tr>',
        '              </tbody>',
        '                <tr>',
        '                  <td>E<sub>x</sub></td><td>{:8.0f}</td>'.format(l.Ex),
        '                  <td align="left">MPa</td>',
        '                </tr>',
        '                <tr>',
        '                  <td>E<sub>y</sub></td><td>{:8.0f}</td>'.format(l.Ey),
        '                  <td align="left">MPa</td>',
        '                </tr>',
        '                <tr>',
        '                  <td>E<sub>z</sub></td><td>{:8.0f}</td>'.format(l.Ez),
        '                  <td align="left">MPa</td>',
        '                </tr>',
        '                <tr>',
        '                  <td>G<sub>xy</sub></td><td>{:8.0f}</td>'.format(l.Gxy),
        '                  <td align="left">MPa</td>',
        '                </tr>',
        '                <tr>',
        '                  <td>G<sub>xz</sub></td><td>{:8.0f}</td>'.format(l.Gxz),
        '                  <td align="left">MPa</td>',
        '                </tr>',
        '                <tr>',
        '                  <td>G<sub>yz</sub></td><td>{:8.0f}</td>'.format(l.Gyz),
        '                  <td align="left">MPa</td>',
        '                </tr>',
        '                <tr>',
        '                  <td>&nu;<sub>xy</sub></td><td>{:g}</td>'.format(l.νxy),
        '                  <td align="left">-</td>',
        '                </tr>',
        '                <tr>',
        '                  <td>&nu;<sub>yx</sub></td><td>{:g}</td>'.format(l.νyx),
        '                  <td align="left">-</td>',
        '                </tr>',
        '                <tr>',
        '                  <td>&alpha;<sub>x</sub></td><td>{:g}</td>'.format(l.αx),
        '                  <td align="left">K<sup>-1</sup></td>',
        '                </tr>',
        '                <tr>',
        '                  <td>&alpha;<sub>y</sub></td><td>{:g}</td>'.format(l.αy),
        '                  <td align="left">K<sup>-1</sup></td>',
        '                </tr>',
        '              </tbody>',
        '            </table>',
        '          </td>',
        '        </tr>',
    ]
    return lines


def _matrices(l):  # {{{1
    """Return the ABD and abd matrices as HTML tables."""
    def pr(mat, row, r=6):
        """Return a row from a matrix."""
        numl = []
        for m in range(r):
            num = mat[row][m]
            if num == 0.0:
                nums = '0'
            else:
                nums, exp = "{:> 10.4e}".format(num).split('e')
                exp = int(exp)
                if exp != 0:
                    nums += '&times;10<sup>{}</sup>'.format(exp)
            numl.append(nums)
        return '          <td>' + '</td><td>'.join(numl) + '</td>'

    fstr = ["N<sub>x</sub>", "N<sub>y</sub>", "N<sub>xy</sub>",
            "M<sub>x</sub>", "M<sub>y</sub>", "M<sub>xy</sub>"]
    hfstr = ["V<sub>y</sub>", "V<sub>x</sub>"]
    dstr = ["&epsilon;<sub>x</sub>", "&epsilon;<sub>y</sub>",
            "&gamma;<sub>xy</sub>", "&kappa;<sub>x</sub>",
            "&kappa;<sub>y</sub>", "&kappa;<sub>xy</sub>"]
    hdstr = ["&gamma;<sub>yz</sub>", "&gamma;<sub>xz</sub>"]
    lines = [
        '        <tr>',
        '          <!-- second row, stiffness or ABD matrix -->',
        '          <td colspan="2">',
        '            <table border="1" frame="vsides" '
        'rules="groups" cellpadding="5%%">',
        '              <caption><strong>Stiffness (ABD) matrix</strong>'
        '</caption>',
        '              <colgroup span="1"></colgroup>',
        '              <colgroup span="1"></colgroup>',
        '              <colgroup span="6"></colgroup>',
        '              <colgroup span="1"></colgroup>',
        '              <colgroup span="1"></colgroup>',
        '              <tbody align="center">',
        '                <tr>',
        '                  <td>{}</td>'.format(fstr[0]),
        '                  <td rowspan="6">=</td>',
        pr(l.ABD, 0),
        '                  <td rowspan="6">&times;</td>',
        '                  <td>{}</td>'.format(dstr[0]),
        '                </tr>'
    ]
    for n in range(1, 6):
        lines += [
            '                <tr>',
            '                  <td>{}</td>'.format(fstr[n]),
            pr(l.ABD, n),
            '                  <td>{}</td>'.format(dstr[n]),
            '                </tr>'
        ]
    lines += [
        '              </tbody>',
        '            </table>',
        '          </td>',
        '        </tr>',
        '        <tr>',
        '          <!-- third row, transverse stiffness or H matrix -->',
        '          <td colspan="2">',
        '            <table border="1" frame="vsides" '
        'rules="groups" cellpadding="5%%">',
        '              <caption><strong>Transverse stiffness (H) matrix</strong>'
        '</caption>',
        '              <colgroup span="1"></colgroup>',
        '              <colgroup span="1"></colgroup>',
        '              <colgroup span="2"></colgroup>',
        '              <colgroup span="1"></colgroup>',
        '              <colgroup span="1"></colgroup>',
        '              <tbody align="center">',
        '                <tr>',
        '                  <td>{}</td>'.format(hfstr[0]),
        '                  <td rowspan="2">=</td>',
        pr(l.H, 0, r=2),
        '                  <td rowspan="2">&times;</td>',
        '                  <td>{}</td>'.format(hdstr[0]),
        '                </tr>',
        '                <tr>',
        '                  <td>{}</td>'.format(hfstr[1]),
        pr(l.H, 1, r=2),
        '                  <td>{}</td>'.format(hdstr[1]),
        '                </tr>',
        '              </tbody>',
        '            </table>',
        '          </td>',
        '        </tr>',
        '        <tr>',
        '          <!-- fourth row, compliance or abd matrix -->',
        '          <td colspan="2">',
        '            <table border="1" frame="vsides" '
        'rules="groups" cellpadding="5%">',
        '              <caption><strong>Compliance (abd) matrix</strong>'
        '</caption>',
        '              <colgroup span="1"></colgroup>',
        '              <colgroup span="1"></colgroup>',
        '              <colgroup span="6"></colgroup>',
        '              <colgroup span="1"></colgroup>',
        '              <colgroup span="1"></colgroup>',
        '              <tbody align="center">',
        '                <tr>',
        '                  <td>{}</td>'.format(dstr[0]),
        '                  <td rowspan="6">=</td>',
        pr(l.abd, 0),
        '                  <td rowspan="6">&times;</td>',
        '                  <td>{}</td>'.format(fstr[0]),
        '                </tr>'
    ]
    for n in range(1, 6):
        lines += [
            '                <tr>',
            '                  <td>{}</td>'.format(dstr[n]),
            pr(l.abd, n),
            '                  <td>{}</td>'.format(fstr[n]),
            '                </tr>',
        ]
    lines += [
        '              </tbody>',
        '            </table>',
        '          </td>',
        '        </tr>',
        '        <tr>',
        '          <!-- fifth row, transverse compliance or h matrix -->',
        '          <td colspan="2">',
        '            <table border="1" frame="vsides" '
        'rules="groups" cellpadding="5%%">',
        '              <caption><strong>Transverse compliance (h) matrix</strong>'
        '</caption>',
        '              <colgroup span="1"></colgroup>',
        '              <colgroup span="1"></colgroup>',
        '              <colgroup span="2"></colgroup>',
        '              <colgroup span="1"></colgroup>',
        '              <colgroup span="1"></colgroup>',
        '              <tbody align="center">',
        '                <tr>',
        '                  <td>{}</td>'.format(hdstr[0]),
        '                  <td rowspan="2">=</td>',
        pr(l.h, 0, r=2),
        '                  <td rowspan="2">&times;</td>',
        '                  <td>{}</td>'.format(hfstr[0]),
        '                </tr>',
        '                <tr>',
        '                  <td>{}</td>'.format(hdstr[1]),
        pr(l.h, 1, r=2),
        '                  <td>{}</td>'.format(hfstr[1]),
        '                </tr>',
        '              </tbody>',
        '            </table>',
        '          </td>',
        '        </tr>',
    ]
    return lines
