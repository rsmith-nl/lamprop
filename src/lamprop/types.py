# file: types.py
# vim:fileencoding=utf-8:ft=python:fdm=marker
# Copyright © 2014-2015 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# Created: 2014-02-21 22:20:39 +0100
# Last modified: 2016-06-04 08:04:16 +0200
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
import math
import numpy as np

Fiber = namedtuple('Fiber', 'E1 nu12 alpha1 density name')

Resin = namedtuple('Resin', 'E nu alpha density name')

Lamina = namedtuple('Lamina', ['fiber', 'resin', 'fiber_weight', 'angle', 'vf',
                               'thickness', 'resin_weight', 'E1', 'E2', 'G12',
                               'nu12', 'alphax', 'alphay', 'alphaxy', 'Q11',
                               'Q12', 'Q16', 'Q22', 'Q26', 'Q66', 'density'])

Laminate = namedtuple('Laminate', ['name', 'layers', 'thickness',
                                   'fiber_weight', 'density', 'vf',
                                   'resin_weight', 'ABD', 'abd', 'Ex', 'Ey',
                                   'Gxy', 'nuxy', 'nuyx', 'alphax', 'alphay',
                                   'wf'])


def mkfiber(E1, nu12, alpha1, density, name):
    E1 = float(E1)
    nu12 = float(nu12)
    alpha1 = float(alpha1)
    density = float(density)
    if E1 <= 0:
        raise ValueError('E1 must be > 0')
    if density <= 0:
        raise ValueError('fiber density must be > 0')
    return Fiber(E1, nu12, alpha1, density, name)


def mkresin(E, nu, alpha, density, name):
    E = float(E)
    nu = float(nu)
    alpha = float(alpha)
    density = float(density)
    if E <= 0:
        raise ValueError('E must be > 0')
    if density <= 0:
        raise ValueError('resin density must be > 0')
    return Resin(E, nu, alpha, density, name)


def mklamina(fiber, resin, fiber_weight, angle, vf):  # {{{1
    """Create a Lamina from the properties of the resin and fiber.

    Arguments:
        fiber: The Fiber to be used in this lamina.
        resin: The Resin to be used in this lamina.
        fiber_weight: Area weight of the fiber in g/m².
        angle: Angle from the 0-axis in degrees counterclockwise.
        vf: Fiber volume fraction.

    Returns:
        A Lamina object.
    """
    fiber_weight = float(fiber_weight)
    if fiber_weight <= 0:
        raise ValueError('fiber weight cannot be <=0!')
    vf = float(vf)
    if 1.0 < vf <= 100.0:
        vf = vf/100.0
    elif not 0.0 <= vf <= 1.0:
        raise ValueError('vf must be in the ranges 0.0-1.0 or 1.0-100.0')
    vm = (1.0 - vf)
    fiber_thickness = fiber_weight/(fiber.density*1000)
    thickness = fiber_thickness*(1+vm/vf)
    resin_weight = thickness*vm*resin.density*1000  # Resin [g/m²]
    E1 = vf*fiber.E1+resin.E*vm  # Hyer:1998, p. 115, (3.32)
    E2 = 3*resin.E  # Tsai:1992, p. 3-13
    G12 = E2/2  # Tsai:1992, p. 3-13
    nu12 = 0.3  # Tsai:1992, p. 3-13
    a = math.radians(float(angle))
    m, n = math.cos(a), math.sin(a)
    # The powers of the sine and cosine are often used later.
    m2 = m*m
    m3, m4 = m2*m, m2*m2
    n2 = n*n
    n3, n4 = n2*n, n2*n2
    alpha1 = (fiber.alpha1*fiber.E1*vf+resin.alpha*resin.E*vm)/E1
    alpha2 = resin.alpha  # This is not 100% accurate, but simple.
    alphax = alpha1 * m2 + alpha2 * n2
    alphay = alpha1 * n2 + alpha2 * m2
    alphaxy = 2 * (alpha1 - alpha2) * m * n
    S11, S12 = 1/E1, -nu12/E1
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
    density = fiber.density*vf+resin.density*vm
    return Lamina(fiber, resin, fiber_weight, angle, vf, thickness,
                  resin_weight, E1, E2, G12, nu12, alphax, alphay, alphaxy,
                  Q_11, Q_12, Q_16, Q_22, Q_26, Q_66, density)


def mklaminate(name, layers):  # {{{1
    """Create a Laminate from a list of Lamina

    Arguments:
        name: Name of the laminate.
        layers: List of Lamina.
    Returns:
        A Laminate object.
    """
    if not layers:
        raise ValueError('No layers!')
    thickness = sum([l.thickness for l in layers])
    fw = sum([l.fiber_weight for l in layers])
    density = sum([l.density*l.thickness for l in layers])/thickness
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
        Ntx += (l.Q11*l.alphax + l.Q12*l.alphay + l.Q16*l.alphaxy)*l.thickness
        Nty += (l.Q12*l.alphax + l.Q22*l.alphay + l.Q26*l.alphaxy)*l.thickness
        Ntxy += (l.Q16*l.alphax + l.Q26*l.alphay + l.Q66*l.alphaxy)*l.thickness
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
    nuxy = dt4 / dt1
    nuyx = dt5 / dt2
    # non-symmetric laminates
    # Calculate the coefficients of thermal expansion.
    # Technically only valid for a symmetric laminate!
    # Hyer:1998, p. 451, (11.86)
    alphax = abd[0, 0]*Ntx + abd[0, 1]*Nty + abd[0, 2]*Ntxy
    alphay = abd[1, 0]*Ntx + abd[1, 1]*Nty + abd[1, 2]*Ntxy
    return Laminate(name, tuple(layers), thickness, fw, density, vf,
                    rw, ABD, abd, Ex, Ey, Gxy, nuxy, nuyx, alphax, alphay, wf)
