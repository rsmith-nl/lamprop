# file: test_parser.py
# vim:fileencoding=utf-8:ft=python:fdm=marker
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2016-06-09 19:44:58 +0200
# Last modified: 2016-06-09 21:29:24 +0200

"""Tests for the lamprop parser."""

import json
import logging
import sys

sys.path.insert(1, 'src')

from lamprop.types import mkresin, mkfiber  # noqa
from lamprop.parser import _find  # noqa


def setup():  # {{{1
    logging.basicConfig(level=logging.WARNING,
                        format='%(levelname)s: %(message)s')


def test_good_resins():  # {{{1
    data = '''{"resins": [{"E": 3500, "nu": 0.36, "alpha": 51.5e-6, "density":
              1.1, "name": "atlac 590"},
              {"E": 2900, "nu": 0.25, "alpha": 40e-6, "density": 1.15,
              "name": "EPR04908"}]}'''
    resins = _find('resins', json.loads(data), mkresin, 'data')
    assert len(resins) == 2
    assert resins['atlac 590'].E == 3500


def test_bad_resins():  # {{{1
    data = '''{"resins": [{"E": 3500, "alpha": 51.5e-6, "density":
              1.1, "name": "missing nu"},
              {"E": -2900, "nu": 0.25, "alpha": 40e-6, "density": 1.15,
              "name": "E<0"},
              {"E": 2900, "nu": 0.25, "alpha": 40e-6, "density": -1.15,
              "name": "rho<0"}]}'''
    read = json.loads(data)
    assert len(read['resins']) == 3
    resins = _find('resins', read, mkresin, 'data')
    assert len(resins) == 0


def test_good_fibers():  # {{{1
    data = '''{"fibers": [{"E1": 780000, "nu12": 0.27, "alpha1": -1.5e-6,
              "density": 2.17, "name": "granoc XN-80"},
              {"E1": 80000, "nu12": 0.33, "alpha1": 5e-6, "density": 2.62,
              "name": "advantex E-CR"},
              {"E1": 140000, "nu12": 0.33, "alpha1": 5e-6, "density": 0.975,
              "name": "dyneema"}]}'''
    read = json.loads(data)
    assert len(read['fibers']) == 3
    fibers = _find('fibers',  read, mkfiber, 'data')
    assert len(fibers) == 3
    assert fibers['dyneema'].E1 == 140000


def test_bad_fibers():  # {{{1
    data = '''{"fibers": [{"E1": 780000, "alpha1": -1.5e-6,
              "density": 2.17, "name": "nonu"},
              {"E1": -80000, "nu12": 0.33, "alpha1": 5e-6, "density": 2.62,
              "name": "E<0"},
              {"E1": 140000, "nu12": 0.33, "alpha1": 5e-6, "density": -0.975,
              "name": "rho<0"}]}'''
    read = json.loads(data)
    assert len(read['fibers']) == 3
    fibers = _find('fibers',  read, mkfiber, 'data')
    assert len(fibers) == 0
