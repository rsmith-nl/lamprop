# file: html.py
# vim:fileencoding=utf-8:ft=python:fdm=marker
#
# Copyright © 2011-2020 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause
# Created: 2011-03-28 22:38:23 +0200
# Last modified: 2021-05-24T01:52:30+0200
"""HTML output routines for lamprop."""

from .version import __version__
from lp.text import _fea as _fea_text


def out(lam, eng, mat, fea):  # {{{1
    """HTML main output function."""
    lines = [
        "<!DOCTYPE html>",
        '<html lang="en-US">',
        '<head><meta charset="UTF-8"><meta name="description" content="lamprop output">',
        "<title>lamprop output</title>",
        "</head>",
        "<body>",
        "<!-- outer table -->",
        '<table cellpadding="10%">',
        f"<caption><strong>Properties of {lam.name}</strong></caption>",
        '<tbody align="center">',
        f'<tr><td  align="center" colspan="2">created by lamprop {__version__}.</td></tr>',
    ]
    lines += [
        "<!-- first row; tables -->",
        "<tr><td>",
        '<table border="1" frame="hsides"',
        'rules="groups" cellpadding="5%">',
        "<caption><strong>Laminate stacking</strong></caption>",
        '<thead align="right">',
        "<tr><td>Layer</td><td>weight</td>",
        '<td>angle</td><td>vf</td><td align="left">fiber type</td></tr>',
        "<tr><td></td><td>[g/m&sup2;]</td><td>[&deg;]</td><td>[%]</td></tr>",
        "</thead>",
        '<tbody align="right">',
    ]
    ln = 1
    for la in lam.layers:
        if isinstance(la, str):
            lines += [
                "<tr>",
                f'<td colspan="5" align="left">{la}</td>',
                "</tr>",
            ]
            continue
        lines += [
            "<tr>",
            f"<td>{ln}</td><td>{la.fiber_weight:4.0f}</td><td>{la.angle:5.0f}</td>",
            f'<td>{la.vf*100:g}</td><td align="left">{la.fiber.name}</td>',
            "</tr>",
        ]
        ln += 1
    w = lam.fiber_weight + lam.resin_weight
    lines += [
        "</tbody>",
        "</table>",
        "</td>",
        "<td>",
        '<table border="1" frame="hsides" rules="groups" cellpadding="5%">',
        "<caption><strong>Physical properties</strong></caption>",
        '<thead align="right">',
        '<tr><td>Property</td><td>Value</td><td align="left">Dimension</td></tr>',
        "</thead>",
        '<tbody align="right">',
        f'<tr><td>v<sub>f</sub></td><td>{lam.vf*100:.3g}</td><td align="left">%</td></tr>',
        f'<tr><td>w<sub>f</sub></td><td>{lam.wf*100:.3g}</td><td align="left">%</td></tr>',
        f'<tr><td>thickness</td><td>{lam.thickness:.3g}</td><td align="left">mm</td></tr>',
        f'<tr><td>density</td><td>{lam.ρ:.3g}</td><td align="left">g/cm&sup3;</td></tr>',
        f'<tr><td>weight</td><td>{w:.0f}</td><td align="left">g/m&sup2;</td></tr>',
        f'<tr><td>resin</td><td>{lam.resin_weight:.0f}</td><td align="left">g/m&sup2;</td></tr>',
    ]
    if eng:
        lines += _engprop(lam)
    lines += [
        "</tbody>",
        "</table>",
        "</td>",
        "</tr>",
    ]
    if mat:
        lines += _matrices(lam)
    if fea:
        lines += _fea(lam)
    lines += [
        "</tbody>",
        "</table>",
        "<hr />",
        "</body>",
        "</html>",
    ]
    return lines


def _engprop(l):  # {{{1
    """Print the engineering properties as a HTML table."""
    lines = [
        "</tbody>",
        "<tbody>",
        '<tr><td colspan="6" align="center"><strong>Engineering properties</strong></td></tr>',
        '<tr><td colspan="3" align="center"><strong>In-plane</strong></td>',
        '<td colspan="3" align="center"><strong>3D stiffness tensor</strong></td></tr>',
        "<tr>",
        f'<td>E<sub>x</sub></td><td>{l.Ex:.0f}</td><td align="left">MPa</td>',
        f'<td>E<sub>x</sub></td><td>{l.tEx:.0f}</td><td align="left">MPa</td>',
        "</tr>",
        "<tr>",
        f'<td>E<sub>y</sub></td><td>{l.Ey:.0f}</td><td align="left">MPa</td>',
        f'<td>E<sub>y</sub></td><td>{l.tEy:.0f}</td><td align="left">MPa</td>',
        "</tr>",
        "<tr>",
        f'<td>E<sub>z</sub></td><td>{l.Ez:.0f}</td><td align="left">MPa</td>',
        f'<td>E<sub>z</sub></td><td>{l.tEz:.0f}</td><td align="left">MPa</td>',
        "</tr>",
        "<tr>",
        f'<td>G<sub>xy</sub></td><td>{l.Gxy:.0f}</td><td align="left">MPa</td>',
        f'<td>G<sub>xy</sub></td><td>{l.tGxy:.0f}</td><td align="left">MPa</td>',
        "</tr>",
        "<tr>",
        f'<td>G<sub>xz</sub></td><td>{l.Gxz:.0f}</td><td align="left">MPa</td>',
        f'<td>G<sub>xz</sub></td><td>{l.tGxz:.0f}</td><td align="left">MPa</td>',
        "</tr>",
        "<tr>",
        f'<td>G<sub>yz</sub></td><td>{l.Gyz:.0f}</td><td align="left">MPa</td>',
        f'<td>G<sub>yz</sub></td><td>{l.tGyz:.0f}</td><td align="left">MPa</td>',
        "</tr>",
        "<tr>",
        f'<td>&nu;<sub>xy</sub></td><td>{l.νxy:.3f}</td><td align="left">-</td>',
        f'<td>&nu;<sub>xy</sub></td><td>{l.tνxy:.3f}</td><td align="left">-</td>',
        "</tr>",
        "<tr>",
        f'<td>&nu;<sub>yx</sub></td><td>{l.νyx:.3f}</td><td align="left">-</td>',
        f'<td>&nu;<sub>xz</sub></td><td>{l.tνxz:.3f}</td><td align="left">-</td>',
        "</tr>",
        "<tr>",
        f'<td>&alpha;<sub>x</sub></td><td>{l.αx:.3f}</td><td align="left">K<sup>-1</sup></td>',
        f'<td>&nu;<sub>yz</sub></td><td>{l.tνyz:.3f}</td><td align="left">-</td>',
        "</tr>",
        "<tr>",
        f'<td>&alpha;<sub>y</sub></td><td>{l.αy:.3f}</td><td align="left">K<sup>-1</sup></td>',
        "</tr>",
    ]
    return lines


def _matrices(l):  # {{{1
    """Return the ABD and 3D stiffness matrices as HTML tables."""

    def pr(mat, row, r=6):
        """Return a row from a matrix."""
        numl = []
        for m in range(r):
            num = mat[row][m]
            if num == 0.0:
                nums = "0"
            else:
                nums, exp = f"{num:> 10.4e}".split("e")
                exp = int(exp)
                if exp != 0:
                    nums += f"&times;10<sup>{exp}</sup>"
            numl.append(nums)
        return "          <td>" + "</td><td>".join(numl) + "</td>"

    fstr = [
        "N<sub>x</sub>",
        "N<sub>y</sub>",
        "N<sub>xy</sub>",
        "M<sub>x</sub>",
        "M<sub>y</sub>",
        "M<sub>xy</sub>",
    ]
    hfstr = ["V<sub>y</sub>", "V<sub>x</sub>"]
    dstr = [
        "&epsilon;<sub>x</sub>",
        "&epsilon;<sub>y</sub>",
        "&gamma;<sub>xy</sub>",
        "&kappa;<sub>x</sub>",
        "&kappa;<sub>y</sub>",
        "&kappa;<sub>xy</sub>",
    ]
    hdstr = ["&gamma;<sub>yz</sub>", "&gamma;<sub>xz</sub>"]
    lines = [
        "<tr>",
        "<!-- second row, stiffness or ABD matrix -->",
        '<td colspan="2">',
        '<table border="1" frame="vsides" ' 'rules="groups" cellpadding="5%%">',
        "<caption><strong>In-plane stiffness (ABD) matrix</strong></caption>",
        '<colgroup span="1"></colgroup>',
        '<colgroup span="1"></colgroup>',
        '<colgroup span="6"></colgroup>',
        '<colgroup span="1"></colgroup>',
        '<colgroup span="1"></colgroup>',
        '<tbody align="center">',
        "<tr>",
        f"<td>{fstr[0]}</td>",
        '<td rowspan="6">=</td>',
        pr(l.ABD, 0),
        '<td rowspan="6">&times;</td>',
        f"<td>{dstr[0]}</td>",
        "</tr>",
    ]
    for n in range(1, 6):
        lines += [
            "<tr>",
            f"<td>{fstr[n]}</td>",
            pr(l.ABD, n),
            f"<td>{dstr[n]}</td>",
            "</tr>",
        ]
    lines += [
        "</tbody>",
        "</table>",
        "</td>",
        "</tr>",
        "<tr>",
        "<!-- third row, transverse stiffness or H matrix -->",
        '<td colspan="2">',
        '<table border="1" frame="vsides" ' 'rules="groups" cellpadding="5%%">',
        "<caption><strong>Transverse stiffness (H) matrix</strong>" "</caption>",
        '<colgroup span="1"></colgroup>',
        '<colgroup span="1"></colgroup>',
        '<colgroup span="2"></colgroup>',
        '<colgroup span="1"></colgroup>',
        '<colgroup span="1"></colgroup>',
        '<tbody align="center">',
        "<tr>",
        "<td>{}</td>".format(hfstr[0]),
        '<td rowspan="2">=</td>',
        pr(l.H, 0, r=2),
        '<td rowspan="2">&times;</td>',
        "<td>{}</td>".format(hdstr[0]),
        "</tr>",
        "<tr>",
        "<td>{}</td>".format(hfstr[1]),
        pr(l.H, 1, r=2),
        "<td>{}</td>".format(hdstr[1]),
        "</tr>",
        "</tbody>",
        "</table>",
        "</td>",
        "</tr>",
    ]
    fstr = [
        "&sigma;<sub>11</sub>",
        "&sigma;<sub>22</sub>",
        "&sigma;<sub>33</sub>",
        "&sigma;<sub>23</sub>",
        "&sigma;<sub>13</sub>",
        "&sigma;<sub>12</sub>",
    ]
    dstr = [
        "&epsilon;<sub>11</sub>",
        "&epsilon;<sub>22</sub>",
        "&epsilon;<sub>33</sub>",
        "2&epsilon;<sub>23</sub>",
        "2&epsilon;<sub>13</sub>",
        "2&epsilon;<sub>12</sub>",
    ]
    lines += [
        "<tr>",
        "<!-- next row, stiffness tensor -->",
        '<td colspan="2">',
        '<table border="1" frame="vsides" ' 'rules="groups" cellpadding="5%%">',
        "<caption><strong>3D stiffness (C) tensor, contracted notation</strong></caption>",
        '<colgroup span="1"></colgroup>',
        '<colgroup span="1"></colgroup>',
        '<colgroup span="6"></colgroup>',
        '<colgroup span="1"></colgroup>',
        '<colgroup span="1"></colgroup>',
        '<tbody align="center">',
        "<tr>",
        f"<td>{fstr[0]}</td>",
        '<td rowspan="6">=</td>',
        pr(l.C, 0),
        '<td rowspan="6">&times;</td>',
        f"<td>{dstr[0]}</td>",
        "</tr>",
    ]
    for n in range(1, 6):
        lines += [
            "<tr>",
            f"<td>{fstr[n]}</td>",
            pr(l.C, n),
            f"<td>{dstr[n]}</td>",
            "</tr>",
        ]
    lines += [
        "</tbody>",
        "</table>",
        "</td>",
        "</tr>",
        "<tr>",
    ]
    return lines


def _fea(l):  # {{{1
    lines = [
        "<tr>",
        "<!-- next row, stiffness tensor -->",
        '<td colspan="2" align="left">',
        "<pre>",
    ]
    lines += _fea_text(l)
    lines += [
        "</pre>",
        "</td>",
        "</tr>",
    ]
    return lines
