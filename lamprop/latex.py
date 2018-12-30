# file: latex.py
# vim:fileencoding=utf-8:ft=python:fdm=marker
# Copyright © 2011-2018 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# Created: 2011-03-27 23:19:38 +0200
# Last modified: 2018-12-30T13:10:27+0100
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

"""LaTeX output routines for lamprop."""

from .version import __version__


def out(lam, eng, mat):  # {{{1
    """Output function for LaTeX format. Returns a list of lines."""
    texlname = lam.name.replace('_', '\_')
    txt = "  \\caption{{\\label{{tab:{0}}}properties of {0}}}"
    lines = [
        "\\begin{table}[!htbp]",
        "  \\renewcommand{\\arraystretch}{1.2}",
        txt.format(texlname),
        "  \\centering\\footnotesize{\\rule{0pt}{10pt}",
        "  \\tiny calculated by lamprop {}\\\\[3pt]}}".format(__version__)
    ]
    if eng:
        lines += _engprop(lam)
    if mat:
        lines += _matrices(lam)
    lines.append("\\end{table}")
    lines.append("")
    return lines  # 1}}}


def _engprop(l):  # {{{1
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
        texfname = la.fiber.name.replace('_', '\_')
        lines.append(s.format(ln, la.fiber_weight, la.angle, la.vf*100, texfname))
    lines += [
        "      \\bottomrule",
        "    \\end{tabular}\\hspace{0.02\\textwidth}",
        "    \\begin{tabular}[t]{rrl}",
        "      \\multicolumn{3}{c}{\\small\\textbf{Engineering properties}}\\\\[0.1em]",
        "      \\toprule",
        "      Property & Value & Dimension\\\\",
        "      \\midrule",
        "      $\\mathrm{{v_f}}$ & {:.3g} &\\%\\\\".format(l.vf*100),
        "      $\\mathrm{{w_f}}$ & {:.3g} &\\%\\\\".format(l.wf*100),
        "      thickness & {:.3g} & mm\\\\".format(l.thickness),
        "      density & {:.3g} & g/cm$^3$\\\\".format(l.ρ),
        "      weight & {:.0f} & g/m$^2$\\\\".format(l.fiber_weight+l.resin_weight),
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


def _matrices(l):  # {{{1
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
