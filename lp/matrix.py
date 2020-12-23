# file: matrix.py
# vim:fileencoding=utf-8:ft=python:fdm=marker
# Library for square matrices.
#
# Copyright © 2018,2019 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause
# Created: 2018-12-28T23:06:35+0100
# Last modified: 2020-12-23T20:32:16+0100

from copy import deepcopy

_LIMIT = 1e-7  # Numbers smaller than abs(_LIMIT) are set to 0.


def ident(num):
    """Create num×num identity matrix."""
    matrix = []
    for i in range(num):
        row = [1 if i == j else 0 for j in range(num)]
        matrix.append(row)
    return matrix


def zeros(num):
    """Create a num×num 0-filled matrix."""
    matrix = []
    for i in range(num):
        row = [0 for j in range(num)]
        matrix.append(row)
    return matrix


def copy(m):
    s = len(m)
    c = zeros(s)
    for i in range(s):
        for j in range(s):
            c[i][j] = m[i][j]
    return c


def det(m):
    """Calculate the determinant of a matrix."""
    tr, _ = _topright(m)
    d = _diag(tr)
    rv = 1
    for j in d:
        rv *= j
    return rv


def inv(m):
    """Calculate the inverse of a matrix"""
    size = _square_size(m)
    # Empty left-bottom triangle
    copy, rv = _topright(m)
    # Empty top-right triangle.
    for k in range(size - 1, -1, -1):
        for p in range(k - 1, -1, -1):
            fact = copy[p][k] / copy[k][k]
            for j in range(size):
                copy[p][j] -= fact * copy[k][j]
                if abs(copy[p][j]) < _LIMIT:
                    copy[p][j] = 0
                rv[p][j] -= fact * rv[k][j]
    # Divide by the diagonals.
    for r in range(size):
        for k in range(size):
            rv[r][k] /= copy[r][r]
    return rv


def add(a, b):
    """Return the sum of matrices a and b."""
    s, sb = _square_size(a), _square_size(b)
    if s != sb:
        raise ValueError("matrices cannot be multiplied")
    res = zeros(s)
    for i in range(s):
        for j in range(s):
            res[i][j] = a[i][j] + b[i][j]
    return res


def matmul(a, b):
    """Returns the matrix product of square matrices a and b."""
    s, sb = _square_size(a), _square_size(b)
    if s != sb:
        raise ValueError("matrices cannot be multiplied")
    res = zeros(s)
    for i in range(s):
        for j in range(s):
            for k in range(s):
                res[i][j] += a[i][k] * b[k][j]
    return res


def mul(m, s):
    """Multiply matrix m by scalar s."""
    s = _square_size(m)
    res = zeros(s)
    for i in range(s):
        for j in range(s):
            res[i][j] = m[i][j] * s
    return res


def transp(m):
    """Return the transpose of m."""
    s = len(m)
    r = zeros(s)
    for i in range(s):
        for j in range(s):
            r[i][j] = m[j][i]
    return r


def delete(m, r, k):
    """Delete row r and column r from matrix m."""
    size = _square_size(m)
    if r < 0 or r > size - 1:
        raise ValueError("invalid row")
    if k < 0 or k > size - 1:
        raise ValueError("invalid column")
    rv = deepcopy(m)
    rv.pop(r)
    for r in rv:
        r.pop(k)
    return rv


def _topright(m):
    """Return the top-right triangular matrix."""
    size = _square_size(m)
    copy = deepcopy(m)
    rv = ident(size)
    for k in range(size):
        for p in range(k + 1, size):
            fact = copy[p][k] / copy[k][k]
            for j in range(size):
                copy[p][j] -= fact * copy[k][j]
                if abs(copy[p][j]) < 1e-7:
                    copy[p][j] = 0
                rv[p][j] -= fact * rv[k][j]
    return copy, rv


def _diag(m):
    """Return the diagonal of a matrix."""
    return [m[j][j] for j in range(len(m))]


def _square_size(m):
    """
    Checks that a matrix is square and returns the size.
    Raises a ValueError when the matrix is not square.
    """
    size = len(m)
    for row in m:
        if len(row) != size:
            raise ValueError("invalid row length")
    return size
