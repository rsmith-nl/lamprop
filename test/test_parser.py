# file: test_parser.py
# vim:fileencoding=utf-8:ft=python:fdm=marker
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2016-06-08 22:10:46 +0200
# Last modified: 2017-02-14 22:34:19 +0100


"""Test for lamprop parser."""

import sys

sys.path.insert(1, 'src')

from lamprop.parser import _f, _r, Resin, Fiber, _l  # noqa


def test_good_fibers():  # {{{1
    directives = [(1, 'f: 233000 0.2 -0.54e-6 1.76 new'),
                  (2, 'f: 230000 23000 0.20 8960 -0.41e-6 9e-6 1.76 old')]
    fibers = _f(directives)
    assert len(fibers) == 2
    assert fibers['new'].name == 'new'
    assert -0.6e-6 < fibers['new'].α1 < -0.5e-6  # noqa
    assert fibers['old'].name == 'old'


def test_bad_fibers():  # {{{1
    directives = [(1, 'f: 233000 0.2 -0.54e-6 geen sg'),
                  (2, 'f: -230000 0.2 -0.41e-6 -1.76 Efout'),
                  (3, 'f: 230000 0.2 -0.41e-6 -1.76 sgfout')]
    fibers = _f(directives)
    assert len(fibers) == 0


def test_good_resins():  # {{{1
    directives = [(1, "r: 4620 0.36 41.4e-6 1.1 foo")]
    resins = _r(directives)
    assert len(resins) == 1
    assert resins['foo'].E == 4620


def test_bad_resins():  # {{{1
    directives = [(1, "r: -4620 0.36 41.4e-6 1.1 Efout"),
                  (2, 'r: 4620 -2 41.4e-6 1.1 nufout'),
                  (3, 'r: 4620 0.7 41.4e-6 1.1 nufout'),
                  (4, 'r: 4620 0.2 41.4e-6 -0.1 sgfout')]
    resins = _r(directives)
    assert len(resins) == 0


def test_good_lamina():
    directives = [(1, 'l: 200 0 carbon'),
                  (2, 'l: 302 -23.2 0.3 carbon'),
                  (3, 'l: 200 0 test 3'),
                  (4, 'l: 302 -23.2 0.3 test 3')]
    fdict = {'carbon': Fiber(240000, 0.2, -0.2e-6, 1.76, 'carbon'),
             'test 3': Fiber(240000, 0.2, -0.2e-6, 1.76, 'test 3')}
    r = Resin(3000, 0.3, 20e-6, 1.2, 'resin')
    lamina = []
    for num, ln in directives:
        lamina.append(_l(num, ln, fdict, r, 0.5))
    assert len(lamina) == 4
