# file: types.py
# vim:fileencoding=utf-8:ft=python:fdm=indent
# Copyright © 2014-2015 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# Created: 2014-02-21 22:20:39 +0100
# Last modified: 2015-09-28 22:46:12 +0200
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

"""Core types of lamprop.

The following references used in coding this module:
@Book{Hyer:1998,
  author =       {Micheal W. Hyer},
  title =        {Stress analysis of fiber-reinforced composite materials},
  publisher =    {McGraw--Hill},
  year =         {1998},
  note =         {ISBN~0~07~115983~5}
}

@Book{Tsai:1992,
  author =       {Stephen W. Tsai},
  title =        {Theory of composites design},
  publisher =    {Think Composites},
  year =         {1992},
  note =         {ISBN~0~9618090~3~5}
}

@Article{1992WeiEn..52...29H,
   author = {Hart-Smith, L.~J.},
    title = "{The ten-percent rule for preliminary sizing of fibrous
                  composite structures}",
  journal = {Weight Engineering},
     year = 1992,
   volume = 52,
    pages = {29-45},
  adsnote = {Provided by the Smithsonian/NASA Astrophysics Data System}
}

@Book{Vinson:1987,
  author =       {J.R. Vinson},
  title =        {The behavior of structures composed of composite materials},
  publisher =    {Martinus Nijhoff Publishers},
  year =         {1987},
  note =         {ISBN~90~247~3125~90 (hardcover)}
}

@Techreport{Nettles:1994,
  author =       {A.T. Nettles},
  titls =        {Basic Mechanics of Laminated Plates},
  institution =  {NASA},
  year =         {1994},
  number =       {Reference Publication 1351}
}
"""

from collections import namedtuple
import numpy as np
import math


Fiber = namedtuple('Fiber', ['E1', 'ν12', 'α1', 'ρ', 'name', 'line'])
Resin = namedtuple('Resin', ['E', 'ν', 'α', 'ρ', 'name', 'line'])
Lamina = namedtuple('Lamina', ['fiber', 'resin', 'fiber_weight', 'angle',
                               'vf', 'thickness', 'resin_weight', 'E1', 'E2',
                               'G12', 'ν12', 'αx', 'αy', 'αxy', 'Q11', 'Q12',
                               'Q16', 'Q22', 'Q26', 'Q66', 'ρ'])
Laminate = namedtuple('Laminate', ['name', 'layers', 'thickness',
                                   'fiber_weight', 'ρ', 'vf', 'resin_weight',
                                   'ABD', 'abd', 'Ex', 'Ey', 'Gxy', 'νxy',
                                   'νyx', 'αx', 'αy', 'wf'])


def lamina(fiber, resin, fiber_weight, angle, vf):
    """Create a Lamina from the properties of the resin and fiber.

    :param fiber: the Fiber to be used in this lamina
    :param resin: the Resin to be used in this lamina
    :param fiber_weight: area weight of the fiber in g/m²
    :param angle: angle from the 0-axis in degrees counterclockwise
    :param vf: fiber volume fraction
    :returns: a Lamina
    """
    fiber_weight = float(fiber_weight)
    if fiber_weight < 0:
        raise ValueError('fiber_weight cannot be <0!')
    vf = float(vf)
    if 1.0 < vf <= 100.0:
        vf = vf/100.0
    elif not 0.0 <= vf <= 1.0:
        raise ValueError('vf must be in the ranges 0.0-1.0 or 1.0-100.0')
    vm = (1.0 - vf)  # Volume fraction of resin material
    # [gr/m²]/[gr/cm³] = [cm³/m²] = 1/10000 [cm³/cm²] = 1/1000 [mm]
    fiber_thickness = fiber_weight/(fiber.ρ*1000)
    thickness = fiber_thickness*(1+vm/vf)
    resin_weight = thickness*vm*resin.ρ*1000  # Resin [g/m²]
    E1 = vf*fiber.E1+resin.E*vm  # Hyer:1998, p. 115, (3.32)
    E2 = 3*resin.E  # Tsai:1992, p. 3-13
    G12 = E2/2  # Tsai:1992, p. 3-13
    ν12 = 0.3  # Tsai:1992, p. 3-13
    a = math.radians(angle)
    m, n = math.cos(a), math.sin(a)
    # The powers of the sine and cosine are often used later.
    m2 = m*m
    m3, m4 = m2*m, m2*m2
    n2 = n*n
    n3, n4 = n2*n, n2*n2
    α1 = (fiber.α1*fiber.E1*vf+resin.α*resin.E*vm)/E1
    α2 = resin.α  # This is not 100% accurate, but simple.
    αx = α1 * m2 + α2 * n2
    αy = α1 * n2 + α2 * m2
    αxy = 2 * (α1 - α2) * m * n
    S11, S12 = 1/E1, -ν12/E1
    S22, S66 = 1/E2, 1/G12
    denum = S11*S22-S12*S12
    Q11, Q12 = S22/denum, -S12/denum
    Q22, Q66 = S11/denum, 1/S66
    Q_11 = Q11*m4+2*(Q12+2*Q66)*n2*m2+Q22*n4
    QA = Q11-Q12-2*Q66
    QB = Q12-Q22+2*Q66
    Q_12 = (Q11+Q22-4*Q66)*n2*m2+Q12*(n4+m4)
    Q_16 = QA*n*m3+QB*n3*m
    Q_22 = Q11*n4+2*(Q12+2*Q66)*n2*m2+Q22*m4
    Q_26 = QA*n3*m+QB*n*m3
    Q_66 = (Q11+Q22-2*Q12-2*Q66)*n2*m2+Q66*(n4+m4)
    ρ = fiber.ρ*vf+resin.ρ*vm
    return Lamina(fiber, resin, fiber_weight, angle, vf, thickness,
                  resin_weight, E1, E2, G12, ν12, αx, αy, αxy, Q_11,
                  Q_12, Q_16, Q_22, Q_26, Q_66, ρ)


def laminate(name, layers):
    """Create a Laminate from a list of Lamina

    :param name: name of the laminate
    :param layers: list of Lamina
    :returns: a Laminate
    """
    if not layers:
        raise ValueError('No layers!')
    thickness = sum([l.thickness for l in layers])
    fw = sum([l.fiber_weight for l in layers])
    ρ = sum([l.ρ*l.thickness for l in layers])/thickness
    vf = sum([l.vf*l.thickness for l in layers])/thickness
    rw = sum([l.resin_weight for l in layers])
    wf = fw/(fw + rw)
    # Set z-values for lamina.
    zs = -thickness/2
    lz2, lz3 = [], []
    for l in layers:
        ze = zs + l.thickness
        lz2.append((ze*ze-zs*zs)/2)
        lz3.append((ze*ze*ze-zs*zs*zs)/3)
        zs = ze
    Ntx, Nty, Ntxy = 0.0, 0.0, 0.0
    ABD = np.zeros((6, 6))
    for l, z2, z3 in zip(layers, lz2, lz3):
        # first row
        ABD[0, 0] += l.Q11*l.thickness      # Hyer:1998, p. 290
        ABD[0, 1] += l.Q12*l.thickness
        ABD[0, 2] += l.Q16*l.thickness
        ABD[0, 3] += l.Q11*z2
        ABD[0, 4] += l.Q12*z2
        ABD[0, 5] += l.Q16*z2
        # second row
        ABD[1, 0] += l.Q12*l.thickness
        ABD[1, 1] += l.Q22*l.thickness
        ABD[1, 2] += l.Q26*l.thickness
        ABD[1, 3] += l.Q12*z2
        ABD[1, 4] += l.Q22*z2
        ABD[1, 5] += l.Q26*z2
        # third row
        ABD[2, 0] += l.Q16*l.thickness
        ABD[2, 1] += l.Q26*l.thickness
        ABD[2, 2] += l.Q66*l.thickness
        ABD[2, 3] += l.Q16*z2
        ABD[2, 4] += l.Q26*z2
        ABD[2, 5] += l.Q66*z2
        # fourth row
        ABD[3, 0] += l.Q11*z2
        ABD[3, 1] += l.Q12*z2
        ABD[3, 2] += l.Q16*z2
        ABD[3, 3] += l.Q11*z3
        ABD[3, 4] += l.Q12*z3
        ABD[3, 5] += l.Q16*z3
        # fifth row
        ABD[4, 0] += l.Q12*z2
        ABD[4, 1] += l.Q22*z2
        ABD[4, 2] += l.Q26*z2
        ABD[4, 3] += l.Q12*z3
        ABD[4, 4] += l.Q22*z3
        ABD[4, 5] += l.Q26*z3
        # sixth row
        ABD[5, 0] += l.Q16*z2
        ABD[5, 1] += l.Q26*z2
        ABD[5, 2] += l.Q66*z2
        ABD[5, 3] += l.Q16*z3
        ABD[5, 4] += l.Q26*z3
        ABD[5, 5] += l.Q66*z3
        # Calculate unit thermal stress resultants.
        # Hyer:1998, p. 445
        Ntx += (l.Q11*l.αx + l.Q12*l.αy + l.Q16*l.αxy)*l.thickness
        Nty += (l.Q12*l.αx + l.Q22*l.αy + l.Q26*l.αxy)*l.thickness
        Ntxy += (l.Q16*l.αx + l.Q26*l.αy + l.Q66*l.αxy)*l.thickness
    # Finish the matrices, discarding very small numbers in ABD.
    for i in range(6):
        for j in range(6):
            if math.fabs(ABD[i, j]) < 1e-7:
                ABD[i, j] = 0.0
    abd = np.linalg.inv(ABD)
    # Calculate the engineering properties.
    # Nettles:1994, p. 34 e.v.
    dABD = np.linalg.det(ABD)
    dt1 = np.linalg.det(ABD[1:6, 1:6])
    Ex = (dABD / (dt1 * thickness))
    dt2 = np.linalg.det(np.delete(np.delete(ABD, 1, 0), 1, 1))
    Ey = (dABD / (dt2 * thickness))
    dt3 = np.linalg.det(np.delete(np.delete(ABD, 2, 0), 2, 1))
    Gxy = (dABD / (dt3 * thickness))
    dt4 = np.linalg.det(np.delete(np.delete(ABD, 0, 0), 1, 1))
    dt5 = np.linalg.det(np.delete(np.delete(ABD, 1, 0), 0, 1))
    νxy = dt4 / dt1
    νyx = dt5 / dt2
    # non-symmetric laminates
    # Calculate the coefficients of thermal expansion.
    # Technically only valid for a symmetric laminate!
    # Hyer:1998, p. 451, (11.86)
    αx = abd[0, 0]*Ntx + abd[0, 1]*Nty + abd[0, 2]*Ntxy
    αy = abd[1, 0]*Ntx + abd[1, 1]*Nty + abd[1, 2]*Ntxy
    return Laminate(name, tuple(layers), thickness, fw, ρ, vf,
                    rw, ABD, abd, Ex, Ey, Gxy, νxy, νyx, αx, αy, wf)
