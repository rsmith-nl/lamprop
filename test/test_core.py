# file: test_types.py
# vim:fileencoding=utf-8:ft=python:fdm=marker
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2015-04-05 23:36:32 +0200
# Last modified: 2023-10-11T22:25:10+0200
"""Test for lamprop types"""

import sys
import math

# Inserting the path is needed to make sure that the module here is loaded,
# not an installed version!
sys.path.insert(1, ".")

from lp.core import fiber, resin, lamina, laminate  # noqa

hf = fiber(233000, 0.2, -0.54e-6, 1.76, "Hyer's carbon fiber")
hr = resin(4620, 0.36, 41.4e-6, 1.1, "Hyer's resin")


def areclose(a, b):
    for x, y in zip(a, b):
        assert math.isclose(x, y, rel_tol=0.01)


def test_lamina():  # {{{1
    f = fiber(230000, 0.30, -0.41e-6, 1.76, "T300")
    r = resin(2900, 0.36, 41.4e-6, 1.15, "Epikote04908")
    la = lamina(f, r, 100, 0, 0.5)
    areclose(
        (la.E1, la.E2, la.G12, la.ν12, la.αx, la.αy, la.ρ),
        (116450.0, 9714.87, 3198.53, 0.33, 1.106e-07, 2.07e-05, 1.455),
    )
    areclose(
        (la.Q̅11, la.Q̅12, la.Q̅16, la.Q̅22, la.Q̅26, la.Q̅66),
        (117517.65, 3235.30, 0.0, 9803.95, 0.0, 3198.53),
    )


def test_ud():  # {{{1
    la = lamina(hf, hr, 100, 0, 0.5)
    ud = laminate("ud", [la, la, la, la])
    assert math.isclose(ud.thickness, 0.4545, rel_tol=0.01)
    assert math.isclose(ud.ρ, 1.43, rel_tol=0.01)
    assert ud.vf == 0.5
    assert math.isclose(ud.wf, 0.615, rel_tol=0.01)
    assert math.isclose(ud.Ex, 118810, rel_tol=0.01)
    assert math.isclose(ud.Ey, 15109.06, rel_tol=0.01)
    assert math.isclose(ud.Ez, 15109.06, rel_tol=0.01)
    assert math.isclose(ud.Gxy, 5095.588, rel_tol=0.01)
    assert math.isclose(ud.Gxz, 4246.32, rel_tol=0.01)
    assert math.isclose(ud.Gyz, 4233.40, rel_tol=0.01)
    assert math.isclose(ud.νxy, 0.28, rel_tol=0.01)
    assert math.isclose(ud.νyx, 0.0356, rel_tol=0.01)
    assert math.isclose(ud.αx, 2.75e-07, rel_tol=0.01)
    assert math.isclose(ud.αy, 2.07e-05, rel_tol=0.01)
    assert math.isclose(ud.tEx, 118810.0, rel_tol=0.01)
    assert math.isclose(ud.tEy, 15109.06, rel_tol=0.01)
    assert math.isclose(ud.tEz, 15109.06, rel_tol=0.01)
    assert math.isclose(ud.tGxy, 5095.59, rel_tol=0.01)
    assert math.isclose(ud.tGyz, 5080.08, rel_tol=0.01)
    assert math.isclose(ud.tGxz, 5095.58, rel_tol=0.01)
    assert math.isclose(ud.tνxy, 0.2800, rel_tol=0.01)
    assert math.isclose(ud.tνxz, 0.2799, rel_tol=0.01)
    assert math.isclose(ud.tνyz, 0.4871, rel_tol=0.01)


def test_plain_weave():  # {{{1
    A = lamina(hf, hr, 100, 0, 0.5)
    B = lamina(hf, hr, 100, 90, 0.5)
    pw = laminate("pw", [A, B, B, A])
    assert math.isclose(pw.thickness, 0.4545, rel_tol=0.01)
    assert math.isclose(pw.ρ, 1.43, rel_tol=0.01)
    assert pw.vf == 0.5
    assert math.isclose(pw.wf, 0.615, rel_tol=0.01)
    assert math.isclose(pw.Ex, 67363.86, rel_tol=0.01)
    assert math.isclose(pw.Ey, 67363.86, rel_tol=0.01)
    assert math.isclose(pw.Ez, 15109.06, rel_tol=0.01)
    assert math.isclose(pw.Gxy, 5095.588, rel_tol=0.01)
    assert math.isclose(pw.Gxz, 4237.439, rel_tol=0.01)
    assert math.isclose(pw.Gyz, 4242.285, rel_tol=0.01)
    assert math.isclose(pw.νxy, 0.063, rel_tol=0.01)
    assert math.isclose(pw.νyx, 0.063, rel_tol=0.01)
    assert math.isclose(pw.αx, 3.0497e-06, rel_tol=0.01)
    assert math.isclose(pw.αy, 3.0497e-06, rel_tol=0.01)
    assert math.isclose(pw.tEx, 67402.13, rel_tol=0.01)
    assert math.isclose(pw.tEy, 67402.13, rel_tol=0.01)
    assert math.isclose(pw.tEz, 18205.69, rel_tol=0.01)
    assert math.isclose(pw.tGxy, 5095.588, rel_tol=0.01)
    assert math.isclose(pw.tGyz, 5087.835, rel_tol=0.01)
    assert math.isclose(pw.tGxz, 5087.835, rel_tol=0.01)
    assert math.isclose(pw.tνxy, 0.0626, rel_tol=0.01)
    assert math.isclose(pw.tνxz, 0.4324, rel_tol=0.01)
    assert math.isclose(pw.tνyz, 0.4324, rel_tol=0.01)


def test_pm45():  # {{{1
    A = lamina(hf, hr, 100, 45, 0.5)
    B = lamina(hf, hr, 100, -45, 0.5)
    pm45 = laminate("pm45", [A, B, B, A])
    assert math.isclose(pm45.thickness, 0.4545, rel_tol=0.01)
    assert math.isclose(pm45.ρ, 1.43, rel_tol=0.01)
    assert pm45.vf == 0.5
    assert math.isclose(pm45.wf, 0.615, rel_tol=0.01)
    assert math.isclose(pm45.Ex, 17899.5, rel_tol=0.01)
    assert math.isclose(pm45.Ey, 17899.5, rel_tol=0.01)
    assert math.isclose(pm45.Ez, 15109.06, rel_tol=0.01)
    assert math.isclose(pm45.Gxy, 31928.0, rel_tol=0.01)
    assert math.isclose(pm45.Gxz, 4239.86, rel_tol=0.01)
    assert math.isclose(pm45.Gyz, 4239.86, rel_tol=0.01)
    assert math.isclose(pm45.νxy, 0.756, rel_tol=0.01)
    assert math.isclose(pm45.νyx, 0.756, rel_tol=0.01)
    assert math.isclose(pm45.αx, 3.0497e-06, rel_tol=0.01)
    assert math.isclose(pm45.αy, 3.0497e-06, rel_tol=0.01)
    assert math.isclose(pm45.tEx, 17852.21, rel_tol=0.01)
    assert math.isclose(pm45.tEy, 17852.21, rel_tol=0.01)
    assert math.isclose(pm45.tEz, 18205.69, rel_tol=0.01)
    assert math.isclose(pm45.tGxy, 31714.22, rel_tol=0.01)
    assert math.isclose(pm45.tGyz, 5087.84, rel_tol=0.01)
    assert math.isclose(pm45.tGxz, 5087.84, rel_tol=0.01)
    assert math.isclose(pm45.tνxy, 0.7517, rel_tol=0.01)
    assert math.isclose(pm45.tνxz, 0.1145, rel_tol=0.01)
    assert math.isclose(pm45.tνyz, 0.1145, rel_tol=0.01)


def test_qi():  # {{{1
    A = lamina(hf, hr, 100, 0, 0.5)
    B = lamina(hf, hr, 100, 90, 0.5)
    C = lamina(hf, hr, 100, 45, 0.5)
    D = lamina(hf, hr, 100, -45, 0.5)
    qi = laminate("qi", [A, B, C, D, D, C, B, A])
    assert math.isclose(qi.thickness, 0.9090, rel_tol=0.01)
    assert math.isclose(qi.ρ, 1.43, rel_tol=0.01)
    assert qi.vf == 0.5
    assert math.isclose(qi.wf, 0.615, rel_tol=0.01)
    assert math.isclose(qi.Ex, 48663.52, rel_tol=0.01)
    assert math.isclose(qi.Ey, 48663.52, rel_tol=0.01)
    assert math.isclose(qi.Ez, 15109.06, rel_tol=0.01)
    assert math.isclose(qi.Gxy, 18387.97, rel_tol=0.01)
    assert math.isclose(qi.Gxz, 4238.95, rel_tol=0.01)
    assert math.isclose(qi.Gyz, 4240.77, rel_tol=0.01)
    assert math.isclose(qi.νxy, 0.32324, rel_tol=0.01)
    assert math.isclose(qi.νyx, 0.32324, rel_tol=0.01)
    assert math.isclose(qi.αx, 3.049e-06, rel_tol=0.01)
    assert math.isclose(qi.αy, 3.049e-06, rel_tol=0.01)
    assert math.isclose(qi.tEx, 48693.169, rel_tol=0.01)
    assert math.isclose(qi.tEy, 48693.169, rel_tol=0.01)
    assert math.isclose(qi.tEz, 18205.69, rel_tol=0.01)
    assert math.isclose(qi.tGxy, 18404.90, rel_tol=0.01)
    assert math.isclose(qi.tGyz, 5087.83, rel_tol=0.01)
    assert math.isclose(qi.tGxz, 5087.83, rel_tol=0.01)
    assert math.isclose(qi.tνxy, 0.32283, rel_tol=0.01)
    assert math.isclose(qi.tνxz, 0.31239, rel_tol=0.01)
    assert math.isclose(qi.tνyz, 0.31239, rel_tol=0.01)
