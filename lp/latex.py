# file: latex.py
# vim:fileencoding=utf-8:ft=python:fdm=marker
#
# Copyright © 2011-2019 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause
# Created: 2011-03-27 23:19:38 +0200
# Last modified: 2019-05-05T11:27:16+0200
"""LaTeX output routines for lamprop."""

from .version import __version__


def out(lam, eng, mat):
    """Output function for LaTeX format. Returns a list of lines."""
    texlname = lam.name.replace("_", r"\_")
    txt = "  \\caption{{\\label{{tab:{0}}}properties of {0}}}"
    lines = [
        "\\begin{table}[!htbp]",
        "  \\renewcommand{\\arraystretch}{1.2}",
        txt.format(texlname),
        "  \\centering\\footnotesize{\\rule{0pt}{10pt}",
        "  \\tiny calculated by lamprop {}\\\\[3pt]}}".format(__version__),
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
    lines = [
        "    \\begin{tabular}[t]{rcrrl}",
        "      \\multicolumn{4}{c}{\\small\\textbf{Laminate stacking}}\\\\[0.1em]",
        "      \\toprule %% \\usepackage{booktabs}",
        "      Layer & Weight & Angle & vf & Fiber type\\\\",
        "            & [g/m$^2$] & [$\\circ$] & [\\%]\\\\",
        "      \\midrule",
    ]
    for ln, la in enumerate(l.layers, start=1):
        s = "      {} & {:4.0f} & {:5.0f} & {:.3g} & {}\\\\"
        texfname = la.fiber.name.replace("_", r"\_")
        lines.append(s.format(ln, la.fiber_weight, la.angle, la.vf * 100, texfname))
    lines += [
        "      \\bottomrule",
        "    \\end{tabular}\\hspace{0.02\\textwidth}",
        "    \\begin{tabular}[t]{rrl}",
        "      \\multicolumn{3}{c}{\\small\\textbf{Engineering properties}}\\\\[0.1em]",
        "      \\toprule",
        "      Property & Value & Dimension\\\\",
        "      \\midrule",
        "      $\\mathrm{{v_f}}$ & {:.3g} &\\%\\\\".format(l.vf * 100),
        "      $\\mathrm{{w_f}}$ & {:.3g} &\\%\\\\".format(l.wf * 100),
        "      thickness & {:.3g} & mm\\\\".format(l.thickness),
        "      density & {:.3g} & g/cm$^3$\\\\".format(l.ρ),
        "      weight & {:.0f} & g/m$^2$\\\\".format(l.fiber_weight + l.resin_weight),
        "      resin & {:.0f} & g/m$^2$\\\\".format(l.resin_weight),
        "      \\midrule",
        "      $\\mathrm{{E_x}}$ & {:8.0f} & MPa\\\\".format(l.Ex),
        "      $\\mathrm{{E_y}}$ & {:8.0f} & MPa\\\\".format(l.Ey),
        "      $\\mathrm{{G_{{xy}}}}$ & {:8.0f} & MPa\\\\".format(l.Gxy),
        "      $\\mathrm{{\\nu_{{xy}}}}$ & {:g} &-\\\\".format(l.νxy),
        "      $\\mathrm{{\\nu_{{yx}}}}$ & {:g} &-\\\\".format(l.νyx),
        "      $\\mathrm{{\\alpha_x}}$ & {:g} & K$^{{-1}}$\\\\".format(l.αx),
        "      $\\mathrm{{\\alpha_y}}$ & {:g} & K$^{{-1}}$\\\\".format(l.αy),
        "      \\bottomrule",
        "    \\end{tabular}",
    ]
    return lines


def _matrices(l):
    """Return the ABD and abd matrices as LaTeX arrays in the form of
    a list of lines."""

    def pm(mat):
        """Return the contents of a matrix."""
        lines = []
        for t in range(6):
            numl = []
            for m in range(6):
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
        "  }",
    ]
    return lines
