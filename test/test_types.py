# file: test_types.py
# vim:fileencoding=utf-8:ft=python:fdm=indent
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2015-04-05 23:36:32 +0200
# Last modified: 2016-06-02 11:25:20 +0200

"""Test for lptypes.py.

Run with: nosetests-3.5 -v test_types.py
"""

from shutil import rmtree
import os
import sys

sys.path.insert(1, '../src')

from lamprop.types import Fiber, Resin, mklamina, mklaminate

hf = Fiber(233000, 0.2, -0.54e-6, 1.76, "Hyer's carbon fiber")
hr = Resin(4620, 0.36, 41.4e-6, 1.1, "Hyer's resin")


def test_lamina():
    f = Fiber(230000, 0.30, -0.41e-6, 1.76, 'T300')
    r = Resin(2900, 0.36, 41.4e-6, 1.15, 'Epikote04908')
    l = mklamina(f, r, 100, 0, 0.5)
    assert ((l.E1, l.E2, l.G12, l.nu12, l.alphax, l.alphay, l.density) ==
            (116450.0, 8700, 4350.0, 0.3, 1.1060541004723054e-07, 4.14e-05,
             1.455))
    assert ((l.Q11, l.Q12, l.Q16, l.Q22, l.Q26, l.Q66) ==
            (117238.3004659929, 2627.6682199763113, 0.0, 8758.894066587705,
             0.0, 4350.0))


def test_ud():
    l = mklamina(hf, hr, 100, 0, 0.5)
    ud = mklaminate('ud', [l, l, l, l])
    assert 0.45 < ud.thickness < 0.46
    assert 1.42 < ud.density < 1.44
    assert ud.vf == 0.5
    assert 0.614 < ud.wf < 0.616
    assert 118800 < ud.Ex < 118820
    assert 13850 < ud.Ey < 13870
    assert 6920 < ud.Gxy < 6940
    assert 0.29 < ud.nuxy < 0.31
    assert 0.034 < ud.nuyx < 0.036
    assert 2.75e-7 < ud.alphax < 2.76e-07
    assert 4.13e-5 < ud.alphay < 4.15e-5


def test_plain_weave():
    A = mklamina(hf, hr, 100, 0, 0.5)
    B = mklamina(hf, hr, 100, 90, 0.5)
    pw = mklaminate('pw', [A, B, B, A])
    assert 0.45 < pw.thickness < 0.46
    assert 1.42 < pw.density < 1.44
    assert pw.vf == 0.5
    assert 0.614 < pw.wf < 0.616
    assert 66765 < pw.Ex < 66785
    assert 66765 < pw.Ey < 66785
    assert 6920 < pw.Gxy < 6940
    assert 0.06258 < pw.nuxy < 0.06278
    assert 0.06258 < pw.nuyx < 0.06278
    assert 5.521e-06 < pw.alphax < 5.541e-06
    assert 5.521e-06 < pw.alphay < 5.541e-06


def test_pm45():
    A = mklamina(hf, hr, 100, 45, 0.5)
    B = mklamina(hf, hr, 100, -45, 0.5)
    pw = mklaminate('pw', [A, B, B, A])
    assert 0.45 < pw.thickness < 0.46
    assert 1.42 < pw.density < 1.44
    assert pw.vf == 0.5
    assert 0.614 < pw.wf < 0.616
    assert 23195 < pw.Ex < 23215
    assert 23195 < pw.Ey < 23215
    assert 31408 < pw.Gxy < 31428
    assert 0.67417 < pw.nuxy < 0.67437
    assert 0.67417 < pw.nuyx < 0.67437
    assert 5.521e-06 < pw.alphax < 5.541e-06
    assert 5.521e-06 < pw.alphay < 5.541e-06


def test_qi():
    A = mklamina(hf, hr, 200, 0, 0.5)
    B = mklamina(hf, hr, 200, 90, 0.5)
    C = mklamina(hf, hr, 100, 45, 0.5)
    D = mklamina(hf, hr, 100, -45, 0.5)
    pw = mklaminate('pw', [A, B, C, D, D, C, B, A])
    assert 1.35 < pw.thickness < 1.37
    assert 1.42 < pw.density < 1.44
    assert pw.vf == 0.5
    assert 0.614 < pw.wf < 0.616
    assert 56269 < pw.Ex < 56289
    assert 56269 < pw.Ey < 56289
    assert 15083 < pw.Gxy < 15103
    assert 0.20992 < pw.nuxy < 0.21012
    assert 0.20992 < pw.nuyx < 0.21012
    assert 5.521e-06 < pw.alphax < 5.541e-06
    assert 5.521e-06 < pw.alphay < 5.541e-06


def teardown():
    rmtree('__pycache__')