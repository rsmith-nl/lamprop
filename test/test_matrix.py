# file: test_matrix.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2019-01-01T01:59:28+0100
# Last modified: 2020-10-03T12:26:42+0200
"""Test of the matrix routines"""

import lp.matrix as mat

_rndm = [
    [0.21, 0.76, 0.07, 0.94, 0.33, 0.57],
    [0.76, 0.07, 0.94, 0.33, 0.57, 0.98],
    [0.07, 0.94, 0.33, 0.57, 0.98, 0.49],
    [0.94, 0.33, 0.57, 0.98, 0.49, 0.36],
    [0.33, 0.57, 0.98, 0.49, 0.36, 0.01],
    [0.57, 0.98, 0.49, 0.36, 0.01, 0.71]
]

# From https://www.mathsisfun.com/algebra/matrix-calculator.html,
# rounded to two decimals.
_invm = [
    [-1.52, -0.48, 0.34, 1.54, -0.88, 0.88],
    [-0.48, -0.66, 0.52, 0.04, 0.01, 0.93],
    [0.34, 0.52, -0.51, -0.71, 1.23, -0.29],
    [1.54, 0.04, -0.71, -0.01, 0.5, -0.8],
    [-0.88, 0.01, 1.23, 0.5, -0.45, -0.4],
    [0.88, 0.93, -0.29, -0.8, -0.4, 0.03]
]


def test_ident():  # {{{1
    m = mat.ident(6)
    for j in range(len(m)):
        for k in range(len(m[0])):
            if j == k:
                assert m[j][k] == 1
            else:
                assert m[j][k] == 0


def test_zeros():  # {{{1
    m = mat.zeros(6)
    for j in range(len(m)):
        for k in range(len(m[0])):
            assert m[j][k] == 0


def test_det_dia():
    m = [[1, 0, 0], [0, 2, 0], [0, 0, 3]]
    assert mat.det(m) == 6


def test_det_3():
    """From https://www.mathsisfun.com/algebra/matrix-determinant.html"""
    m = [[6, 1, 1], [4, -2, 5], [2, 8, 7]]
    assert mat.det(m) == -306


def test_det_6():
    """Using a random generated matrix and
    https://www.mathsisfun.com/algebra/matrix-calculator.html
    """
    assert round(mat.det(_rndm), 2) == -0.45


def test_inv_6():
    """Using a random generated matrix and
    https://www.mathsisfun.com/algebra/matrix-calculator.html
    """
    inv = [[round(n, 2) for n in row] for row in mat.inv(_rndm)]
    assert inv == _invm


def test_delete():
    smaller = [
        [0.21, 0.76, 0.07, 0.33, 0.57],
        [0.07, 0.94, 0.33, 0.98, 0.49],
        [0.94, 0.33, 0.57, 0.49, 0.36],
        [0.33, 0.57, 0.98, 0.36, 0.01],
        [0.57, 0.98, 0.49, 0.01, 0.71]
    ]
    assert mat.delete(_rndm, 1, 3) == smaller
