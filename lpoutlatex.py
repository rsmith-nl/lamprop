# -*- coding: utf-8 -*-
# LaTeX output routines for lamprop.
#
# Copyright © 2011 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# Time-stamp: <2011-11-13 18:29:51 rsmith>
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

import lpver

def out(lam, eng, mat):
    '''LaTeX main output function.'''
    print "\\begin{table}[!htbp]"
    print "  \\renewcommand{\\arraystretch}{1.2}"
    print "  \\caption{{\\label{{tab:{0}}}properties of {0}}}".format(lam.name)
    print "  \\centering\\footnotesize{\\rule{0pt}{10pt}"
    print "  \\tiny calculated by {0} {1}\\\\[3pt]}}".format(lpver.name,
                                                               lpver.version)
    if eng:
        _engprop(lam)
    if mat:
        _matrices(lam)
    print "\\end{table}\n"

def _engprop(l):
    '''Prints the engineering properties as a LaTeX table.'''
    print "  \\parbox{\\textwidth}{\\centering"
    print "    \\begin{tabular}[t]{rcrl}"
    print "      \\multicolumn{4}{c}{\\small"\
        "\\textbf{Laminate stacking}}\\\\[0.1em]"
    print "      \\toprule %% \\usepackage{booktabs}"
    print "      Layer & Weight & Angle & Fiber type\\\\"
    print "            & [gr/m$^2$] & [$\\circ$] & \\\\"
    print "      \\midrule"
    for ln, la in enumerate(l.layers):
        s = "      {} & {:4.0f} & {:5.0f} & {}\\\\"
        print s.format(ln, la.weight, la.angle, la.fiber.name)
    print "      \\bottomrule"
    print "    \\end{tabular}\\hspace{0.02\\textwidth}"
    print "    \\begin{tabular}[t]{rrl}"
    print "      \\multicolumn{3}{c}{\\small\\textbf{Engineering"\
        " properties}}\\\\[0.1em]"
    print "      \\toprule"
    print "      Property & Value & Dimension\\\\"
    print "      \\midrule"
    print "      $v_f$ & {:4.2f} &-\\\\".format(l.vf)
    print "      $w_f$ & {:4.2f} &-\\\\".format(l.wf)
    print "      thickness & {:.3g} & mm\\\\".format(l.thickness)
    print "      density & {:.3g} & gr/cm$^3$\\\\".format(l.density)
    print "      weight & {:.0f} & gr/m$^2$\\\\".format(l.weight+l.rc)
    print "      resin & {:.0f} & gr/m$^2$\\\\".format(l.rc)
    print "      \\midrule"
    print "      $E_x$ & {:8.0f} & MPa\\\\".format(l.Ex)
    print "      $E_y$ & {:8.0f} & MPa\\\\".format(l.Ey)
    print "      $G_{{xy}}$ & {:8.0f} & MPa\\\\".format(l.Gxy)
    print "      $\\nu_{{xy}}$ & {:g} &-\\\\".format(l.Vxy)
    print "      $\\nu_{{yx}}$ & {:g} &-\\\\".format(l.Vyx)
    print "      $\\alpha_x$ & {:g} & K$^{{-1}}$\\\\".format(l.cte_x)
    print "      $\\alpha_y$ & {:g} & K$^{{-1}}$\\\\".format(l.cte_y)
    print "      \\bottomrule"
    print "    \\end{tabular}"
    print "  }\\vspace{5mm}"


def _matrices(l):
    '''Prints the ABD and abd matrices as LaTeX arrays.'''
    print "  \\vbox{"
    print "    \\vbox{\\small\\textbf{Stiffness matrix}\\\\"
    print "      \\tiny\\[\\left\\{\\begin{array}{c}"
    print "          N_x\\\\ N_y\\\\ N_{xy}\\\\ M_x\\\\ M_y\\\\ M_{xy}"
    print "        \\end{array}\\right\\} = "
    print "      \\left|\\begin{array}{cccccc}"
    for t in range(6):
        s = "          {:6.0f} & {:6.0f} & {:6.0f} & {:6.0f}"\
        " & {:6.0f} & {:6.0f}\\\\"
        print s.format(l.ABD[t, 0], l.ABD[t, 1], l.ABD[t, 2], 
                       l.ABD[t, 3], l.ABD[t, 4], l.ABD[t, 5])
    print "          \\end{array}\\right| \\times"
    print "        \\left\\{\\begin{array}{c}"
    print "            \\epsilon^0_x\\\\[3pt] \\epsilon^0_y\\\\[3pt] "\
        "\\gamma^0_{xy}\\\\[3pt]"
    print "            \\kappa^0_x\\\\[3pt] \\kappa^0_y\\\\[3pt] \\kappa^0_{xy}"
    print "          \\end{array}\\right\\}\\]"
    print "    }"
    print "    \\vbox{\\small\\textbf{Compliance matrix}\\\\"
    print "      \\tiny\\[\\left\\{\\begin{array}{c}"
    print "            \\epsilon^0_x\\\\[3pt] \\epsilon^0_y\\\\[3pt] "\
        "\\gamma^0_{xy}\\\\[3pt]"
    print "            \\kappa^0_x\\\\[3pt] \\kappa^0_y\\\\[3pt] \\kappa^0_{xy}"
    print "          \\end{array}\\right\\} = \\left|\\begin{array}{cccccc}"
    for t in range(6):
        s = "          {:6.3g} & {:6.3g} & {:6.3g} & {:6.3g}"\
        " & {:6.3g} & {:6.3g}\\\\"
        print s.format(l.abd[t, 0]*1e6, l.abd[t, 1]*1e6, l.abd[t, 2]*1e6, 
                       l.abd[t, 3]*1e6, l.abd[t, 4]*1e6, l.abd[t, 5]*1e6)
    print "          \\end{array}\\right|\\times10^{-6}\\times"
    print "        \\left\\{\\begin{array}{c}"
    print "            N_x\\\\ N_y\\\\ N_{xy}\\\\ M_x\\\\ M_y\\\\ M_{xy}"
    print "          \\end{array}\\right\\}\\]\\\\"
    print "    }"
    print "  }"

