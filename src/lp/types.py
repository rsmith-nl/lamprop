# file: types.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2023 R.F. Smith <rsmith@xs4all.nl>
# SPDX-License-Identifier: MIT
# Created: 2023-12-03T00:12:51+0100
# Last modified: 2023-12-03T00:45:40+0100

from collections import namedtuple

Fiber = namedtuple("Fiber", "E1 ν12 α1 ρ name")
Resin = namedtuple("Resin", "E ν α ρ name")
Lamina = namedtuple(
    "Lamina",
    "fiber resin fiber_weight angle vf thickness resin_weight E1 E2 E3 "
    "G12 G13 G23 ν12 ν13 ν23 αx αy αxy Q̅11 Q̅12 Q̅16 Q̅22 Q̅26 Q̅66 Q̅s44 Q̅s55 "
    "Q̅s45 ρ C"
)
Laminate = namedtuple(
    "Laminate",
    "name layers thickness fiber_weight ρ vf resin_weight ABD abd H h Ex Ey Ez "
    "Gxy Gyz Gxz νxy νyx αx αy wf C S tEx tEy tEz tGxy tGyz tGxz tνxy tνxz tνyz"
)
