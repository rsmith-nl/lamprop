# file: test_parser.py
# vim:fileencoding=utf-8:ft=python:fdm=markers
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2016-06-08 22:10:46 +0200
# Last modified: 2016-06-08 22:59:41 +0200


"""Test for parser.py.

Run with: nosetests-3.5 -v test_types.py
"""

from shutil import rmtree
import sys

sys.path.insert(1, '../src')

from lamprop.parser import _f, _r  # noqa


def test_good_fibers():  # {{{1
    directives = [(1, 'f: 233000 0.2 -0.54e-6 1.76 new'),
                  (2, 'f: 230000 23000 0.20 8960 -0.41e-6 9e-6 1.76 old')]
    fibers = _f(directives)
    assert len(fibers) == 2
    assert fibers[0].name == 'new'
    assert -0.6e-6 < fibers[0].α1 < -0.5e-6  # noqa
    assert fibers[1].name == 'old'


def test_bad_fibers():  # {{{1
    directives = [(1, 'f: 233000 0.2 -0.54e-6 geen sg'),
                  (2, 'f: -230000 0.2 -0.41e-6 -1.76 Efout'),
                  (3, 'f: 230000 0.2 -0.41e-6 -1.76 sgfout')]
    fibers = _f(directives)
    assert len(fibers) == 0


def test_good_resins():  # {{{1
    directives = [(1, "r: 4620 0.36 41.4e-6 1.1 Hyer's resin")]
    resins = _r(directives)
    assert len(resins) == 1
    assert resins[0].E == 4620


def test_bad_resins():  # {{{1
    directives = [(1, "r: -4620 0.36 41.4e-6 1.1 Efout"),
                  (2, 'r: 4620 -2 41.4e-6 1.1 nufout'),
                  (3, 'r: 4620 0.7 41.4e-6 1.1 nufout'),
                  (4, 'r: 4620 0.2 41.4e-6 -0.1 sgfout')]
    resins = _r(directives)
    assert len(resins) == 0


def teardown():  # {{{1
    rmtree('__pycache__')
