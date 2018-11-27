# file: test_types.py
# vim:fileencoding=utf-8:ft=python:fdm=marker
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2015-04-05 23:36:32 +0200
# Last modified: 2018-11-27T19:50:55+0100

"""Test for lamprop types"""

import sys

sys.path.insert(1, '.')

from lamprop.types import Fiber, Resin, Lamina, Laminate  # noqa

hf = Fiber(233000, 0.2, -0.54e-6, 1.76, "Hyer's carbon fiber")
hr = Resin(4620, 0.36, 41.4e-6, 1.1, "Hyer's resin")


def test_lamina():  # {{{1
    f = Fiber(230000, 0.30, -0.41e-6, 1.76, 'T300')
    r = Resin(2900, 0.36, 41.4e-6, 1.15, 'Epikote04908')
    la = Lamina(f, r, 100, 0, 0.5)
    assert ((la.E1, la.E2, la.G12, la.ν12, la.αx, la.αy, la.ρ) ==
            (116450.0, 5800, 2900.0, 0.3, 1.1060541004723054e-07, 4.14e-05,
             1.455))
    assert ((la.Q̅11, la.Q̅12, la.Q̅16, la.Q̅22, la.Q̅26, la.Q̅66) ==
            (116974.35045890552, 1747.8348630184253, 0.0, 5826.116210061417, 0.0, 2900.0))


def test_ud():  # {{{1
    la = Lamina(hf, hr, 100, 0, 0.5)
    ud = Laminate('ud', [la, la, la, la])
    assert 0.45 < ud.thickness < 0.46
    assert 1.42 < ud.ρ < 1.44
    assert ud.vf == 0.5
    assert 0.614 < ud.wf < 0.616
    assert 118800 < ud.Ex < 118820
    assert 9230 < ud.Ey < 9250
    assert 4610 < ud.Gxy < 4630
    assert 0.29 < ud.νxy < 0.31
    assert 0.022 < ud.νyx < 0.024
    assert 2.75e-7 < ud.αx < 2.76e-07
    assert 4.13e-5 < ud.αy < 4.15e-5


def test_plain_weave():  # {{{1
    A = Lamina(hf, hr, 100, 0, 0.5)
    B = Lamina(hf, hr, 100, 90, 0.5)
    pw = Laminate('pw', [A, B, B, A])
    assert 0.45 < pw.thickness < 0.46
    assert 1.42 < pw.ρ < 1.44
    assert pw.vf == 0.5
    assert 0.614 < pw.wf < 0.616
    assert 64345 < pw.Ex < 64365
    assert 64345 < pw.Ey < 64365
    assert 4610 < pw.Gxy < 4630
    assert 0.042 < pw.νxy < 0.044
    assert 0.042 < pw.νyx < 0.044
    assert 3.963e-06 < pw.αx < 3.983e-06
    assert 3.963e-06 < pw.αy < 3.983e-06


def test_pm45():  # {{{1
    A = Lamina(hf, hr, 100, 45, 0.5)
    B = Lamina(hf, hr, 100, -45, 0.5)
    pw = Laminate('pw', [A, B, B, A])
    assert 0.45 < pw.thickness < 0.46
    assert 1.42 < pw.ρ < 1.44
    assert pw.vf == 0.5
    assert 0.614 < pw.wf < 0.616
    assert 16238 < pw.Ex < 16258
    assert 16238 < pw.Ey < 16258
    assert 30832 < pw.Gxy < 30852
    assert 0.75836 < pw.νxy < 0.75866
    assert 0.75836 < pw.νyx < 0.75866
    assert 3.963e-06 < pw.αx < 3.983e-06
    assert 3.963e-06 < pw.αy < 3.983e-06


def test_qi():  # {{{1
    A = Lamina(hf, hr, 200, 0, 0.5)
    B = Lamina(hf, hr, 200, 90, 0.5)
    C = Lamina(hf, hr, 100, 45, 0.5)
    D = Lamina(hf, hr, 100, -45, 0.5)
    qi = Laminate('qi', [A, B, C, D, D, C, B, A])
    assert 1.35 < qi.thickness < 1.37
    assert 1.42 < qi.ρ < 1.44
    assert qi.vf == 0.5
    assert 0.614 < qi.wf < 0.616
    assert 53339 < qi.Ex < 53359
    assert 53339 < qi.Ey < 53359
    assert 13351 < qi.Gxy < 13371
    assert 0.20591 < qi.νxy < 0.20791
    assert 0.20591 < qi.νyx < 0.20791
    assert 3.963e-06 < qi.αx < 3.983e-06
    assert 3.963e-06 < qi.αy < 3.983e-06
