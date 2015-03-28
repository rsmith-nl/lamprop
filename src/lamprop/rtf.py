# vim:fileencoding=utf-8
# Copyright © 2015 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
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

"""Rich Text Format output routines for lamprop."""

__version__ = '$Revision$'[11:-2]

import sys


def out(lam, eng, mat):
    """Rich Text Format main output function."""
    print(r'{\rtf1\ansi\deff0\uc4')  # RTF header
    if eng:
        _engprop(lam)
    if mat:
        _matrices(lam, not eng)
    print('}')  # Closing brace


def _engprop(l):
    """Prints the engineering properties in Rich Text Format."""
    print("Generated by lamprop {0}\\line".format(__version__))
    print("laminate: {0}\\line".format(l.name))
    s = "thickness: {0:.2f} mm, density: {1:4.2f} g/cm\\u01793\\line"
    print(s.format(l.thickness, l.ρ))
    s = "fiber volume fraction: {0:.1f}%, fiber weight fraction: {1:.1f}%\\line"
    print(s.format(l.vf*100, l.wf*100))
    s = "laminate weight: {0:.0f} g/m\\u01782, "
    "resin consumption: {1:.0f} g/m\\u01782\\line"
    print(s.format(l.fiber_weight+l.resin_weight, l.resin_weight))
    print("num weight angle   vf fiber\\line")
    for ln, la in enumerate(l.layers):
        s = "{0:3} {1:6g} {2:5g} {3:4g} {4}\\line"
        print(s.format(ln+1, la.fiber_weight, la.angle, la.vf, la.fiber.name))
    print("E_x  = {0:.0f} MPa\\line".format(l.Ex))
    print("E_y  = {0:.0f} MPa\\line".format(l.Ey))
    print("G_xy = {0:.0f} MPa\\line".format(l.Gxy))
    print("\\u0957v_xy = {0:7.5f}\\line".format(l.νxy))
    print("\\u0957v_yx = {0:7.5f}\\line".format(l.νyx))
    p = r"\u0945a_"
    u = r" {\upr{1/K}{\*\ud{K\u8315\u0185}}}, "
    s = (p + "x = {:9.4g}".format(l.αx) + u + p + "y = {:9.4g}".format(l.αy)
         + u[:-2] + "\\line")
    print(s)


def _matrices(l, printheader):
    """Prints the ABD and abd matrices Rich Text Format tables."""
    if printheader is True:
        print("Generated by lamprop {0}\\line".format(__version__))
        print("laminate: {0}\\line".format(l.name))
    print("Stiffness (ABD) matrix:\\line")
    matstr = "|{:> 10.4e} {:> 10.4e} {:> 10.4e} " \
             "{:> 10.4e} {:> 10.4e} {:> 10.4e}|\\line"
    for n in range(6):
        m = matstr.format(l.ABD[n, 0], l.ABD[n, 1], l.ABD[n, 2],
                          l.ABD[n, 3], l.ABD[n, 4], l.ABD[n, 5])
        print(m.replace('e+00', '    '))
    print("Compliance (abd) matrix:\\line")
    for n in range(6):
        m = matstr.format(l.abd[n, 0], l.abd[n, 1], l.abd[n, 2],
                          l.abd[n, 3], l.abd[n, 4], l.abd[n, 5])
        print(m.replace('e+00', '    '))
