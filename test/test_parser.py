# file: test_parser.py
# vim:fileencoding=utf-8:ft=python:fdm=marker
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2016-06-08 22:10:46 +0200
# Last modified: 2020-10-03T12:27:16+0200
"""Test for lamprop parser."""

import sys

sys.path.insert(1, '.')

from lp.parser import (_get_numbers, _get_components, _directives,
                            _get_lamina)  # noqa
from lp.core import (fiber, resin)  # noqa


def test_directives():  # {{{1
    r, f, la = _directives('test/twill245.lam')
    assert len(r) == 1
    assert len(f) == 1
    assert len(la) == 9


def test_numbers():  # {{{1
    directives = [(2, 'f:  238000  0.25    -0.1e-6     1.76    TenaxHTA'),
                  (3, 'f:  240000  0.25    -0.1e-6     1.77    TenaxHTS'),
                  (4, 'f:  240000  0.25    -0.12e-6    1.78    Tenax STS40'),
                  (5, 'f:  230000  0.27    -0.41e-6    1.76    Toracya T300'),
                  (6, 'f:  230000  0.27    -0.38e-6    1.80    Torayca T700SC'),
                  (7, 'f:  235000  0.25    -0.5e-6     1.79    pyrofil TR30S'),
                  (8, 'f:  640000  0.234   -1.47e-6    2.12    K 63712'),
                  (9, 'f:  790000  0.23    -1.2e-6     2.15    K 63A12'),
                  (10, 'f:  294000  0.27    -0.60e-6    1.76    T800S'),
                  (11, 'f:  900000  0.234   -1.47e-6    2.20    K 13C2U'),
                  (12, 'f:  339000  0.27    -0.73e-6    1.75    M35J'),
                  (13, 'f:  436000  0.234   -0.9e-6     1.84    M46J'),
                  (14, 'f:  242000  0.27    -0.6e-6     1.81    PX35UD'),
                  (15, ' f:  780000  0.27    -1.5e-6     2.17    XN-80'),
                  (19, ' f:  73000   0.33    5.3e-6      2.60    e-glas'),
                  (20, ' f:  80000   0.33    5e-6        2.62    advantex E-CR'),
                  (22, ' f: 270000   0.25    -6.0e-6     1.56    Zylon'),
                  (23, '\tf: 124000   0.3     -2e-6       1.44    aramide49')]
    for d in directives:
        numbers, rest = _get_numbers(d)
        assert len(numbers) == 4


def test_good_fibers():  # {{{1
    directives = [(2, 'f:  238000  0.25    -0.1e-6     1.76    TenaxHTA'),
                  (3, 'f:  240000  0.25    -0.1e-6     1.77    TenaxHTS'),
                  (4, 'f:  240000  0.25    -0.12e-6    1.78    Tenax STS40'),
                  (5, 'f:  230000  0.27    -0.41e-6    1.76    Toracya T300'),
                  (6, 'f:  230000  0.27    -0.38e-6    1.80    Torayca T700SC'),
                  (7, 'f:  235000  0.25    -0.5e-6     1.79    pyrofil TR30S'),
                  (8, 'f:  640000  0.234   -1.47e-6    2.12    K63712'),
                  (9, 'f:  790000  0.23    -1.2e-6     2.15    K63A12'),
                  (10, 'f:  294000  0.27    -0.60e-6    1.76    T800S'),
                  (11, 'f:  900000  0.234   -1.47e-6    2.20    K13C2U'),
                  (12, 'f:  339000  0.27    -0.73e-6    1.75    M35J'),
                  (13, 'f:  436000  0.234   -0.9e-6     1.84    M46J'),
                  (14, 'f:  242000  0.27    -0.6e-6     1.81    PX35UD'),
                  (15, ' f:  780000  0.27    -1.5e-6     2.17    XN-80'),
                  (19, ' f:  73000   0.33    5.3e-6      2.60    e-glas'),
                  (20, '  f:  80000   0.33    5e-6        2.62    advantex E-CR'),
                  (22, '  f: 270000   0.25    -6.0e-6     1.56    Zylon'),
                  (23, '\tf: 124000   0.3     -2e-6       1.44    aramide49')]
    fibers = _get_components(directives, fiber)
    assert len(fibers) == len(directives)
    assert fibers['Tenax STS40'].E1 == 240000
    assert fibers['Toracya T300'].ν12 == 0.27
    assert fibers['Torayca T700SC'].α1 == -0.38e-6
    assert fibers['K63712'].ρ == 2.12


def test_bad_fibers():  # {{{1
    directives = [(1, 'f: 233000 0.2 -0.54e-6 geen sg'),
                  (2, 'f: -230000 0.2 -0.41e-6 -1.76 Efout'),
                  (3, 'f: 230000 0.2 -0.41e-6 -1.76 sgfout')]
    fibers = _get_components(directives, fiber)
    assert len(fibers) == 0


def test_good_resins():  # {{{1
    directives = [(0, 'r:  2900    0.25    40e-6   1.15    EPR04908'),
                  (2, 'r:  4300    0.36    40e-6   1.19    palatal-P4-01'),
                  (3, 'r:  4000    0.36    40e-6   1.22    synolite-2155-N-1'),
                  (4, 'r:  4100    0.36    40e-6   1.2     distitron 3501LS1'),
                  (6, 'r:  3800    0.36    40e-6   1.165   synolite 1967-G-6'),
                  (8, 'r:  3600    0.36    55e-6   1.145   atlac 430'),
                  (9, 'r:  3500    0.36    51.5e-6   1.1   atlac 590')]
    resins = _get_components(directives, resin)
    assert len(resins) == len(directives)
    assert resins['EPR04908'].E == 2900
    for r in list(resins.values())[1:]:
        assert r.ν == 0.36


def test_bad_resins():  # {{{1
    directives = [(1, "r: -4620 0.36 41.4e-6 1.1 Efout"),
                  (2, 'r: 4620 -2 41.4e-6 1.1 nufout'),
                  (3, 'r: 4620 0.7 41.4e-6 1.1 nufout'),
                  (4, 'r: 4620 0.2 41.4e-6 -0.1 sgfout')]
    resins = _get_components(directives, resin)
    assert len(resins) == 0


def test_good_lamina():  # {{{1
    directives = [(1, 'l: 200 0 carbon'),
                  (2, 'l: 302 -23.2 0.3 carbon'),
                  (3, 'l: 200 0 test 3'),
                  (4, 'l: 302 -23.2 0.3 test 3')]
    fdict = {'carbon': fiber(240000, 0.2, -0.2e-6, 1.76, 'carbon'),
             'test 3': fiber(240000, 0.2, -0.2e-6, 1.76, 'test 3')}
    r = resin(3000, 0.3, 20e-6, 1.2, 'resin')
    lamina = []
    for d in directives:
        newlamina = _get_lamina(d, fdict, r, 0.5)
        if newlamina:
            lamina.append(newlamina)
    assert len(lamina) == 4
