# file: module.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2018 R.F. Smith <rsmith@xs4all.nl>
# Created: 2018-12-01T14:16:05+0100
# Last modified: 2020-10-03T12:26:18+0200
"""Using the lamprop module directly"""

import lp as la

t300 = la.Fiber(230000, 0.3, -0.41e-6, 1.76, 'T300')
epr04908 = la.Resin(2900, 0.36, 41.4e-6, 1.15, 'Epikote 04908')

l0 = la.Lamina(t300, epr04908, 100, 0, 0.50)
l90 = la.Lamina(t300, epr04908, 100, 90, 0.50)

cd0200 = la.Laminate('CD0200', (l0, l90, l90, l0))

print(la.text.engprop(cd0200))
