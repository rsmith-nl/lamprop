# file: latex.py
# vim:fileencoding=utf-8:ft=python:fdm=marker
#
# Copyright © 2011-2020 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause
# Created: 2011-03-27 23:19:38 +0200
# Last modified: 2021-05-24T01:52:59+0200
"""LaTeX output routines for lamprop."""

from .version import __version__
from lp.text import _fea as _fea_text


def out(lam, eng, mat, fea):  # {{{1
    """Output function for LaTeX format. Returns a list of lines."""
    texlname = lam.name.replace("_", r"\_")
    lines = [
        "\\begin{table}[!htbp]",
        "  \\renewcommand{\\arraystretch}{1.2}",
        f"  \\caption{{\\label{{tab:{texlname}}}properties of {texlname}}}",
        "  \\centering\\footnotesize{\\rule{0pt}{10pt}",
        f"  \\tiny calculated by lamprop {__version__}\\\\[3pt]}}",
        "    \\begin{tabular}[t]{rcrrl}",
        "      \\multicolumn{5}{c}{\\small\\textbf{Laminate stacking}}\\\\[0.1em]",
        "      \\toprule %% \\usepackage{booktabs}",
        "      Layer & Weight & Angle & vf & Fiber type\\\\",
        "            & [g/m$^2$] & [$\\circ$] & [\\%]\\\\",
        "      \\midrule",
    ]
    ln = 1
    for la in lam.layers:
        if isinstance(la, str):
            lines.append(r"\multicolumn{5}{l}{" + la + r"}\\")
            continue
        s = "      {} & {:4.0f} & {:5.0f} & {:.3g} & {}\\\\"
        texfname = la.fiber.name.replace("_", r"\_")
        lines.append(s.format(ln, la.fiber_weight, la.angle, la.vf * 100, texfname))
        ln += 1
    w = lam.fiber_weight + lam.resin_weight
    lines += [
        "      \\bottomrule",
        "    \\end{tabular}\\hspace{0.02\\textwidth}",
        "    \\begin{tabular}[t]{rrlrrl}",
        "      \\multicolumn{3}{c}{\\small\\textbf{Physical properties}}\\\\[0.1em]",
        "      \\toprule",
        "      Property & Value & Dimension\\\\",
        "      \\midrule",
        f"      $\\mathrm{{v_f}}$ & {lam.vf*100:.3g} &\\%\\\\",
        f"      $\\mathrm{{w_f}}$ & {lam.wf*100:.3g} &\\%\\\\",
        f"      thickness & {lam.thickness:.3g} & mm\\\\",
        f"      density & {lam.ρ:.3g} & g/cm$^3$\\\\",
        f"      weight & {w:.0f} & g/m$^2$\\\\",
        f"      resin & {lam.resin_weight:.0f} & g/m$^2$\\\\",
    ]

    if eng:
        lines += _engprop(lam)
    lines += [
        "      \\bottomrule",
        "    \\end{tabular}",
    ]
    if mat:
        lines += _matrices(lam)
    if fea:
        lines += _fea(lam)
    lines.append("\\end{table}")
    lines.append("")
    return lines


def _engprop(l):  # {{{1
    """Return the engineering properties as a LaTeX table in the form of
    a list of lines."""
    lines = [
        "      \\midrule",
        "      \\multicolumn{6}{c}{\\small\\textbf{Engineering properties}}\\\\[0.1em]",
        "      \\multicolumn{3}{c}{\\small\\textbf{In-plane}} & ",
        "\\multicolumn{3}{c}{\\small\\textbf{3D stiffness tensor}}\\\\[0.1em]",
        f"      $\\mathrm{{E_x}}$ & {l.Ex:8.0f} & MPa & $\\mathrm{{E_x}}$ & {l.tEx:8.0f} & MPa\\\\",
        f"      $\\mathrm{{E_y}}$ & {l.Ey:8.0f} & MPa & $\\mathrm{{E_y}}$ & {l.tEy:8.0f} & MPa\\\\",
        f"      $\\mathrm{{E_z}}$ & {l.Ez:8.0f} & MPa & $\\mathrm{{E_z}}$ & {l.tEz:8.0f} & MPa\\\\",
        f"      $\\mathrm{{G_{{xy}}}}$ & {l.Gxy:8.0f} & MPa &"
        f" $\\mathrm{{G_{{xy}}}}$ & {l.tGxy:8.0f} & MPa\\\\",
        f"      $\\mathrm{{G_{{xz}}}}$ & {l.Gxz:8.0f} & MPa &"
        f" $\\mathrm{{G_{{xz}}}}$ & {l.tGxz:8.0f} & MPa\\\\",
        f"      $\\mathrm{{G_{{yz}}}}$ & {l.Gyz:8.0f} & MPa & "
        f" $\\mathrm{{G_{{yz}}}}$ & {l.tGyz:8.0f} & MPa\\\\",
        f"      $\\mathrm{{\\nu_{{xy}}}}$ & {l.νxy:.4f} &- &"
        f"$\\mathrm{{\\nu_{{xy}}}}$ & {l.tνxy:.4f} &-\\\\",
        f"      $\\mathrm{{\\nu_{{yx}}}}$ & {l.νyx:.4f} &- & "
        f"$\\mathrm{{\\nu_{{xz}}}}$ & {l.tνxz:.4f} &-\\\\",
        f"      $\\mathrm{{\\alpha_x}}$ & {l.αx:.4g} & K$^{{-1}}$ &"
        f"$\\mathrm{{\\nu_{{yz}}}}$ & {l.tνyz:.4f} &-\\\\",
        f"      $\\mathrm{{\\alpha_y}}$ & {l.αy:.4g} & K$^{{-1}}$\\\\",
    ]
    return lines


def _matrices(l):  # {{{1
    """Return the matrices as LaTeX arrays in the form of
    a list of lines."""

    def pm(mat, r=6):
        """Return the contents of a matrix."""
        lines = []
        for t in range(r):
            numl = []
            for m in range(r):
                num = mat[t][m]
                if num == 0.0:
                    nums = "0"
                else:
                    nums, exp = "{:> 10.4e}".format(mat[t][m]).split("e")
                    exp = int(exp)
                    if exp != 0:
                        nums += "\\times 10^{{{}}}".format(exp)
                numl.append(nums)
            lines.append("          " + " & ".join(numl) + r"\\")
        return lines

    lines = [
        "  \\vbox{",
        "    \\vbox{\\small\\textbf{In-plane stiffness (ABD) matrix}\\\\[-3mm]",
        "      \\tiny\\[\\left\\{\\begin{array}{c}",
        "          N_x\\\\ N_y\\\\ N_{xy}\\\\ M_x\\\\ M_y\\\\ M_{xy}",
        "        \\end{array}\\right\\} = ",
        "      \\left|\\begin{array}{cccccc}",
    ]
    lines += pm(l.ABD)
    lines += [
        "          \\end{array}\\right| \\times",
        "        \\left\\{\\begin{array}{c}",
        "            \\epsilon_x\\\\[2pt] \\epsilon_y\\\\[2pt] \\gamma_{xy}\\\\[2pt]",
        "            \\kappa_x\\\\[2pt] \\kappa_y\\\\[2pt] \\kappa_{xy}",
        "          \\end{array}\\right\\}\\]",
        "    }",
        "    \\vbox{\\small\\textbf{Transverse stiffness (H) matrix}\\\\[-2mm]",
        "      \\tiny\\[\\left\\{\\begin{array}{c}",
        "          V_y\\\\ V_x",
        "        \\end{array}\\right\\} = ",
        "      \\left|\\begin{array}{cc}",
    ]
    lines += pm(l.H, r=2)
    lines += [
        "          \\end{array}\\right| \\times",
        "        \\left\\{\\begin{array}{c}",
        "            \\gamma_{yz}\\\\[2pt] \\gamma_{xz}",
        "          \\end{array}\\right\\}\\]",
        "    }",
    ]
    lines += [
        "    \\vbox{\\small\\textbf{3D stiffness tensor (C), contracted notation}\\\\[-3mm]",
        "      \\tiny\\[\\left\\{\\begin{array}{c}",
        "          \\sigma_{11}\\\\ \\sigma_{22}\\\\ \\sigma_{33}\\\\ \\sigma_{23}\\\\ \\sigma_{13}\\\\ \\sigma_{12}",
        "        \\end{array}\\right\\} = ",
        "      \\left|\\begin{array}{cccccc}",
    ]
    lines += pm(l.C)
    lines += [
        "          \\end{array}\\right| \\times",
        "        \\left\\{\\begin{array}{c}",
        "            \\epsilon_{11}\\\\[2pt] \\epsilon_{22}\\\\[2pt] \\epsilon_{33}\\\\[2pt]",
        "            2\\cdot\\epsilon_{23}\\\\[2pt] 2\\cdot\\epsilon_{13}\\\\[2pt] 2\\cdot\\epsilon_{12}",
        "          \\end{array}\\right\\}\\]",
        "    }",
        "  }",
    ]
    return lines


def _fea(l):  # {{{1
    lines = [
        "  \\vbox{",
        "  \\begin{verbatim}",
    ]
    lines += _fea_text(l)
    lines += [
        "  \\end{verbatim}",
        "  }",
    ]
    return lines
