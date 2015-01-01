# vim:fileencoding=utf-8
# Copyright © 2011-2015 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# $Date$
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

"LaTeX output routines for lamprop."

__version__ = '$Revision$'[11:-2]


def out(lam, eng, mat):
    '''LaTeX main output function.'''
    print("\\begin{table}[!htbp]")
    print("  \\renewcommand{\\arraystretch}{1.2}")
    txt = "  \\caption{{\\label{{tab:{0}}}properties of {0}}}"
    print(txt.format(lam.name))
    print("  \\centering\\footnotesize{\\rule{0pt}{10pt}")
    print("  \\tiny calculated by lamprop {}\\\\[3pt]}}".format(__version__))
    if eng:
        _engprop(lam)
    if mat:
        _matrices(lam)
    print("\\end{table}\n")


def _engprop(l):
    '''Prints the engineering properties as a LaTeX table.'''
    print("  \\parbox{\\textwidth}{\\centering")
    print("    \\begin{tabular}[t]{rcrrl}")
    print("      \\multicolumn{4}{c}{\\small"
          "\\textbf{Laminate stacking}}\\\\[0.1em]")
    print("      \\toprule %% \\usepackage{booktabs}")
    print("      Layer & Weight & Angle & vf & Fiber type\\\\")
    print("            & [g/m$^2$] & [$\\circ$] & [-]\\\\")
    print("      \\midrule")
    for ln, la in enumerate(l.layers):
        s = "      {} & {:4.0f} & {:5.0f} & {:4.2f} & {}\\\\"
        print(s.format(ln, la.weight, la.angle, la.vf, la.fiber.name))
    print("      \\bottomrule")
    print("    \\end{tabular}\\hspace{0.02\\textwidth}")
    print("    \\begin{tabular}[t]{rrl}")
    print("      \\multicolumn{3}{c}{\\small\\textbf{Engineering"
          " properties}}\\\\[0.1em]")
    print("      \\toprule")
    print("      Property & Value & Dimension\\\\")
    print("      \\midrule")
    print("      $\\mathrm{{v_f}}$ & {:4.2f} &-\\\\".format(l.vf))
    print("      $\\mathrm{{w_f}}$ & {:4.2f} &-\\\\".format(l.wf))
    print("      thickness & {:.3g} & mm\\\\".format(l.thickness))
    print("      density & {:.3g} & g/cm$^3$\\\\".format(l.density))
    print("      weight & {:.0f} & g/m$^2$\\\\".format(l.weight+l.rc))
    print("      resin & {:.0f} & g/m$^2$\\\\".format(l.rc))
    print("      \\midrule")
    print("      $\\mathrm{{E_x}}$ & {:8.0f} & MPa\\\\".format(l.Ex))
    print("      $\\mathrm{{E_y}}$ & {:8.0f} & MPa\\\\".format(l.Ey))
    print("      $\\mathrm{{G_{{xy}}}}$ & {:8.0f} & MPa\\\\".format(l.Gxy))
    print("      $\\mathrm{{\\nu_{{xy}}}}$ & {:g} &-\\\\".format(l.Vxy))
    print("      $\\mathrm{{\\nu_{{yx}}}}$ & {:g} &-\\\\".format(l.Vyx))
    s = "      $\\mathrm{{\\alpha_x}}$ & {:g} & K$^{{-1}}$\\\\"
    print(s.format(l.cte_x))
    s = "      $\\mathrm{{\\alpha_y}}$ & {:g} & K$^{{-1}}$\\\\"
    print(s.format(l.cte_y))
    print("      \\bottomrule")
    print("    \\end{tabular}")
    print("  }\\vspace{5mm}")


def _matrices(l):
    '''Prints the ABD and abd matrices as LaTeX arrays.'''
    def pm(mat):
        """Print the contents of a matrix.
        """
        for t in range(6):
            numl = []
            for m in range(6):
                num = mat[t, m]
                if num == 0.0:
                    nums = '0'
                else:
                    nums, exp = "{:> 9.3e}".format(mat[t, m]).split('e')
                    exp = int(exp)
                    if exp != 0:
                        nums += '\\times 10^{{{}}}'.format(exp)
                numl.append(nums)
            print('          ' + ' & '.join(numl) + r'\\')
    print("  \\vbox{")
    print("    \\vbox{\\small\\textbf{Stiffness (ABD) matrix}\\\\")
    print("      \\tiny\\[\\left\\{\\begin{array}{c}")
    print("          N_x\\\\ N_y\\\\ N_{xy}\\\\ M_x\\\\ M_y\\\\ M_{xy}")
    print("        \\end{array}\\right\\} = ")
    print("      \\left|\\begin{array}{cccccc}")
    pm(l.ABD)
    print("          \\end{array}\\right| \\times")
    print("        \\left\\{\\begin{array}{c}")
    print("            \\epsilon_x\\\\[3pt] \\epsilon_y\\\\[3pt] "
          "\\gamma_{xy}\\\\[3pt]")
    print("            "
          "\\kappa_x\\\\[3pt] \\kappa_y\\\\[3pt] \\kappa_{xy}")
    print("          \\end{array}\\right\\}\\]")
    print("    }")
    print("    \\vbox{\\small\\textbf{Compliance (abd) matrix}\\\\")
    print("      \\tiny\\[\\left\\{\\begin{array}{c}")
    print("            \\epsilon_x\\\\[3pt] \\epsilon_y\\\\[3pt] "
          "\\gamma_{xy}\\\\[3pt]")
    print("            "
          "\\kappa_x\\\\[3pt] \\kappa_y\\\\[3pt] \\kappa_{xy}")
    print("          \\end{array}\\right\\} = \\left|\\begin{array}{cccccc}")
    pm(l.abd)
    print("          \\end{array}\\right|\\times")
    print("        \\left\\{\\begin{array}{c}")
    print("            N_x\\\\ N_y\\\\ N_{xy}\\\\ M_x\\\\ M_y\\\\ M_{xy}")
    print("          \\end{array}\\right\\}\\]\\\\")
    print("    }")
    print("  }")
