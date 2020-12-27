# file: latex.py
# vim:fileencoding=utf-8:ft=python:fdm=marker
#
# Copyright © 2011-2020 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause
# Created: 2011-03-27 23:19:38 +0200
# Last modified: 2020-12-27T01:16:21+0100
"""LaTeX output routines for lamprop."""

from .version import __version__


def out(lam, eng, mat, fea):
    """Output function for LaTeX format. Returns a list of lines."""
    texlname = lam.name.replace('_', r'\_')
    lines = [
        "\\begin{table}[!htbp]",
        "  \\renewcommand{\\arraystretch}{1.2}",
        f"  \\caption{{\\label{{tab:{texlname}}}properties of {texlname}}}",
        "  \\centering\\footnotesize{\\rule{0pt}{10pt}",
        f"  \\tiny calculated by lamprop {__version__}\\\\[3pt]}}",
        "    \\begin{tabular}[t]{rcrrl}",
        "      \\multicolumn{4}{c}{\\small\\textbf{Laminate stacking}}\\\\[0.1em]",
        "      \\toprule %% \\usepackage{booktabs}",
        "      Layer & Weight & Angle & vf & Fiber type\\\\",
        "            & [g/m$^2$] & [$\\circ$] & [\\%]\\\\",
        "      \\midrule",
    ]
    for ln, la in enumerate(lam.layers, start=1):
        s = "      {} & {:4.0f} & {:5.0f} & {:.3g} & {}\\\\"
        texfname = la.fiber.name.replace('_', r'\_')
        lines.append(s.format(ln, la.fiber_weight, la.angle, la.vf*100, texfname))
    lines += [
        "      \\bottomrule",
        "    \\end{tabular}\\hspace{0.02\\textwidth}",
    ]
    if eng:
        lines += _engprop(lam)
    if mat:
        lines += _matrices(lam)
    lines.append("\\end{table}")
    lines.append("")
    return lines


def _engprop(l):
    """Return the engineering properties as a LaTeX table in the form of
    a list of lines."""
    w = l.fiber_weight + l.resin_weight
    lines = [
        "    \\begin{tabular}[t]{rrl}",
        "      \\multicolumn{3}{c}{\\small\\textbf{Engineering properties}}\\\\[0.1em]",
        "      \\toprule",
        "      Property & Value & Dimension\\\\",
        "      \\midrule",
        f"      $\\mathrm{{v_f}}$ & {l.vf*100:.3g} &\\%\\\\",
        f"      $\\mathrm{{w_f}}$ & {l.wf*100:.3g} &\\%\\\\",
        f"      thickness & {l.thickness:.3g} & mm\\\\",
        "      density & {l.ρ:.3g} & g/cm$^3$\\\\",
        f"      weight & {w:.0f} & g/m$^2$\\\\",
        "      resin & {l.resin_weight:.0f} & g/m$^2$\\\\",
        "      \\midrule",
        "      \\multicolumn{3}{c}{\\small\\textbf{In-plane}}\\\\[0.1em]",
        f"      $\\mathrm{{E_x}}$ & {l.Ex:8.0f} & MPa\\\\",
        f"      $\\mathrm{{E_y}}$ & {l.Ey:8.0f} & MPa\\\\",
        f"      $\\mathrm{{E_z}}$ & {l.Ez:8.0f} & MPa\\\\",
        f"      $\\mathrm{{G_{{xy}}}}$ & {l.Gxy:8.0f} & MPa\\\\",
        f"      $\\mathrm{{G_{{xz}}}}$ & {l.Gxz:8.0f} & MPa\\\\",
        f"      $\\mathrm{{G_{{yz}}}}$ & {l.Gyz:8.0f} & MPa\\\\",
        f"      $\\mathrm{{\\nu_{{xy}}}}$ & {l.νxy:g} &-\\\\",
        f"      $\\mathrm{{\\nu_{{yx}}}}$ & {l.νyx:g} &-\\\\",
        f"      $\\mathrm{{\\alpha_x}}$ & {l.αx:g} & K$^{{-1}}$\\\\",
        f"      $\\mathrm{{\\alpha_y}}$ & {l.αy:g} & K$^{{-1}}$\\\\",
        "      \\midrule",
        "      \\multicolumn{3}{c}{\\small\\textbf{From 3D stiffness matrix}}\\\\[0.1em]",
        f"      $\\mathrm{{E_x}}$ & {l.tEx:8.0f} & MPa\\\\",
        f"      $\\mathrm{{E_y}}$ & {l.tEy:8.0f} & MPa\\\\",
        f"      $\\mathrm{{E_z}}$ & {l.tEz:8.0f} & MPa\\\\",
        f"      $\\mathrm{{G_{{xy}}}}$ & {l.Gxy:8.0f} & MPa\\\\",
        f"      $\\mathrm{{G_{{xz}}}}$ & {l.Gxz:8.0f} & MPa\\\\",
        f"      $\\mathrm{{G_{{yz}}}}$ & {l.Gyz:8.0f} & MPa\\\\",
        f"      $\\mathrm{{\\nu_{{xy}}}}$ & {l.tνxy:g} &-\\\\",
        f"      $\\mathrm{{\\nu_{{xz}}}}$ & {l.tνxz:g} &-\\\\",
        f"      $\\mathrm{{\\nu_{{yz}}}}$ & {l.tνyz:g} &-\\\\",
        "      \\bottomrule",
        "    \\end{tabular}",
    ]
    return lines


def _matrices(l):
    """Return the ABD and abd matrices as LaTeX arrays in the form of
    a list of lines."""
    def pm(mat, r=6):
        """Return the contents of a matrix."""
        lines = []
        for t in range(r):
            numl = []
            for m in range(r):
                num = mat[t][m]
                if num == 0.0:
                    nums = '0'
                else:
                    nums, exp = "{:> 10.4e}".format(mat[t][m]).split('e')
                    exp = int(exp)
                    if exp != 0:
                        nums += '\\times 10^{{{}}}'.format(exp)
                numl.append(nums)
            lines.append('          ' + ' & '.join(numl) + r'\\')
        return lines
    lines = [
        "  \\vbox{",
        "    \\vbox{\\small\\textbf{Stiffness (ABD) matrix}\\\\[-5mm]",
        "      \\tiny\\[\\left\\{\\begin{array}{c}",
        "          N_x\\\\ N_y\\\\ N_{xy}\\\\ M_x\\\\ M_y\\\\ M_{xy}",
        "        \\end{array}\\right\\} = ",
        "      \\left|\\begin{array}{cccccc}",
    ]
    lines += pm(l.ABD)
    lines += [
        "          \\end{array}\\right| \\times",
        "        \\left\\{\\begin{array}{c}",
        "            \\epsilon_x\\\\[3pt] \\epsilon_y\\\\[3pt] \\gamma_{xy}\\\\[3pt]",
        "            \\kappa_x\\\\[3pt] \\kappa_y\\\\[3pt] \\kappa_{xy}",
        "          \\end{array}\\right\\}\\]",
        "    }",
        "    \\vbox{\\small\\textbf{Transverse stiffness (H) matrix}\\\\[-2mm]",
        "      \\tiny\\[\\left\\{\\begin{array}{c}",
        "          V_y\\\\ V_x",
        "        \\end{array}\\right\\} = ",
        "      \\left|\\begin{array}{cc}"
    ]
    lines += pm(l.H, r=2)
    lines += [
        "          \\end{array}\\right| \\times",
        "        \\left\\{\\begin{array}{c}",
        "            \\gamma_{yz}\\\\[3pt] \\gamma_{xz}",
        "          \\end{array}\\right\\}\\]",
        "    }",
        "    \\vbox{\\small\\textbf{Compliance (abd) matrix}\\\\[-5mm]",
        "      \\tiny\\[\\left\\{\\begin{array}{c}",
        "            \\epsilon_x\\\\[3pt] \\epsilon_y\\\\[3pt] \\gamma_{xy}\\\\[3pt]",
        "            \\kappa_x\\\\[3pt] \\kappa_y\\\\[3pt] \\kappa_{xy}",
        "          \\end{array}\\right\\} = \\left|\\begin{array}{cccccc}",
    ]
    lines += pm(l.abd)
    lines += [
        "          \\end{array}\\right|\\times",
        "        \\left\\{\\begin{array}{c}",
        "            N_x\\\\ N_y\\\\ N_{xy}\\\\ M_x\\\\ M_y\\\\ M_{xy}",
        "          \\end{array}\\right\\}\\]\\\\",
        "    }",
        "    \\vbox{\\small\\textbf{Transverse compliance (h) matrix}\\\\[-2mm]",
        "      \\tiny\\[\\left\\{\\begin{array}{c}",
        "          \\gamma_{yz}\\\\[3pt] \\gamma_{xz}",
        "        \\end{array}\\right\\} = ",
        "      \\left|\\begin{array}{cc}"
    ]
    lines += pm(l.h, r=2)
    lines += [
        "          \\end{array}\\right| \\times",
        "        \\left\\{\\begin{array}{c}",
        "            V_y\\\\ V_x",
        "          \\end{array}\\right\\}\\]",
        "    }",
        "  }",
    ]
    return lines
