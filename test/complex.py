# file: complex.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2018 R.F. Smith <rsmith@xs4all.nl>
# Created: 2018-12-01T23:11:29+0100
# Last modified: 2020-10-03T12:25:59+0200

import lp as la

t300 = la.Fiber(230000, 0.3, -0.41e-6, 1.76, "T300-2")
epr04908 = la.Resin(2900, 0.36, 41.4e-6, 1.15, "Epikote 04908")

layers = [la.Lamina(t300, epr04908, 100, a, 0.50) for a in range(-90, 95, 15)]
layers += layers[::-1]

qi = la.Laminate("quasi-isotropic", layers)

print(la.latex.out(qi, eng=True, mat=False))
print(la.latex.out(qi, eng=False, mat=True))
