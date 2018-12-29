# file: core.py
# vim:fileencoding=utf-8:ft=python:fdm=marker
# Copyright © 2014-2018 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# Created: 2014-02-21 22:20:39 +0100
# Last modified: 2018-12-29T11:33:11+0100
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
"""
Core functions of lamprop.

The following references were used in coding this module:

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
  title =        {Basic Mechanics of Laminated Plates},
  institution =  {NASA},
  year =         {1994},
  number =       {Reference Publication 1351}
}
"""

from types import SimpleNamespace
import math
import lamprop.matrix as m


def fiber(E1, ν12, α1, ρ, name):
    """Create a fiber.

    The arguments with subscript "1" are in the length direction of the fiber.

    Arguments:
        E1 (float): Young's modulus in MPa. Must be > 0.
        ν12 (float): Poisson's constant.
        α1 (float): Coefficient of thermal expansion in K⁻¹.
        ρ (float): Fiber density in g/cm³. Must be > 0
        name (str): Name of the fiber. Must not be empty.
    """
    E1 = float(E1)
    ν12 = float(ν12)
    α1 = float(α1)
    ρ = float(ρ)
    # Validate parameters
    if E1 <= 0:
        raise ValueError('fiber E1 must be > 0')
    if ρ <= 0:
        raise ValueError('fiber ρ must be > 0')
    if not isinstance(name, str) and not len(name) > 0:
        raise ValueError('fiber name must be a non-empty string')
    return SimpleNamespace(E1=E1, ν12=ν12, α1=α1, ρ=ρ, name=name)


def resin(E, ν, α, ρ, name):
    """Create a resin.

    Arguments/properties of a Resin:
        E (float): Young's modulus in MPa. Must be >0.
        ν (float): Poisson's constant.
        α (float): CTE in K⁻¹
        ρ (float): Specific gravity of the resin in g/cm³. Must be >0.
        name (str): String containing the name of the resin. Must not be empty.
    """
    # Covert numbers to floats
    E = float(E)
    ν = float(ν)
    α = float(α)
    ρ = float(ρ)
    # Validate parameters
    if E <= 0:
        raise ValueError('E must be > 0')
    if ρ <= 0:
        raise ValueError('resin ρ must be > 0')
    if not isinstance(name, str) and not len(name) > 0:
        raise ValueError('resin name must be a non-empty string')
    return SimpleNamespace(E=E, ν=ν, α=α, ρ=ρ, name=name)


def lamina(fiber, resin, fiber_weight, angle, vf):
    """Create a lamina.

    Arguments:
        fiber: The Fiber used in the lamina
        resin: The Resin binding the lamina
        fiber_weight: The amount of Fibers in g/m². Must be >0.
        angle: Orientation of the layer in degrees counterclockwise from the
            x-axis.
        vf: Fiber volume fraction.

    Additional generated properties:
        thickness: Thickness of the lamina in mm.
        resin_weight: The amount of Resin in g/m².
        E1: Young's modulus of the lamina in the fiber direction in MPa.
        E2: Young's modulus of the lamina perpendicular to the fiber direction
            in MPa.
        G12: In-plane shear modulus in MPa.
        ν12: in-plane Poisson's constant.
        αx: CTE in x direction in K⁻¹.
        αy: CTE in y direction in K⁻¹.
        αxy: CTE in shear.
        Q̅11: Transformed lamina stiffness matrix component.
        Q̅12: Transformed lamina stiffness matrix component.
        Q̅16: Transformed lamina stiffness matrix component.
        Q̅22: Transformed lamina stiffness matrix component.
        Q̅26: Transformed lamina stiffness matrix component.
        Q̅66: Transformed lamina stiffness matrix component.
        ρ: Specific gravity of the lamina in g/cm³.
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
    fiber_thickness = fiber_weight/(fiber.ρ * 1000)
    thickness = fiber_thickness * (1 + vm / vf)
    resin_weight = thickness * vm * resin.ρ * 1000  # Resin [g/m²]
    E1 = vf * fiber.E1 + resin.E * vm  # Hyer:1998, p. 115, (3.32)
    # Originally a factor of 3 (conform Tsai:1992, p. 3-13) was used in
    # the following line. From practical experience this has been reduced
    # to 2.
    E2 = 2 * resin.E
    G12 = E2 / 2  # Tsai:1992, p. 3-13
    ν12 = 0.3  # Tsai:1992, p. 3-13
    ν21 = ν12 * E2 / E1  # Nettles:1994, p. 4
    a = math.radians(float(angle))
    m, n = math.cos(a), math.sin(a)
    # The powers of the sine and cosine are often used later.
    m2 = m * m
    m3, m4 = m2 * m, m2 * m2
    n2 = n * n
    n3, n4 = n2 * n, n2 * n2
    α1 = (fiber.α1 * fiber.E1 * vf + resin.α * resin.E * vm) / E1
    α2 = resin.α  # This is not 100% accurate, but simple.
    αx = α1 * m2 + α2 * n2
    αy = α1 * n2 + α2 * m2
    αxy = 2 * (α1 - α2) * m * n
    denum = (1 - ν12 * ν21)
    Q11, Q12 = E1 / denum, ν12 * E2 / denum
    Q22, Q66 = E2 / denum, G12
    # Q̅ according to Hyer:1997, p. 182
    Q̅11 = Q11 * m4 + 2 * (Q12 + 2 * Q66) * n2 * m2 + Q22 * n4
    QA = Q11 - Q12 - 2 * Q66
    QB = Q12 - Q22 + 2 * Q66
    Q̅12 = (Q11 + Q22 - 4 * Q66) * n2 * m2 + Q12 * (n4 + m4)
    Q̅16 = QA * n * m3 + QB * n3 * m
    Q̅22 = Q11 * n4 + 2 * (Q12 + 2 * Q66) * n2 * m2 + Q22 * m4
    Q̅26 = QA * n3 * m + QB * n * m3
    Q̅66 = (Q11 + Q22 - 2 * Q12 - 2 * Q66) * n2 * m2 + Q66 * (n4 + m4)
    ρ = fiber.ρ * vf + resin.ρ * vm

    return SimpleNamespace(fiber=fiber, resin=resin,
                           fiber_weight=fiber_weight, angle=angle,
                           vf=vf, thickness=thickness,
                           resin_weight=resin_weight, E1=E1, E2=E2, G12=G12,
                           ν12=ν12, αx=αx, αy=αy, αxy=αxy, Q̅11=Q̅11, Q̅12=Q̅12,
                           Q̅16=Q̅16, Q̅22=Q̅22, Q̅26=Q̅26, Q̅66=Q̅66, ρ=ρ)


def laminate(name, layers):
    """Create a laminate.

    Arguments/properties of a laminate:
        name: A non-empty string containing the name of the laminate
        layers: A non-empty sequence of lamina (will be converted into a tuple).

    Additional properties:
        thickness: Thickness of the laminate in mm.
        fiber_weight: Total area weight of fibers in g/m².
        ρ: Specific gravity of the laminate in g/cm³.
        vf: Average fiber volume fraction.
        resin_weight: Total area weight of resin in g/m².
        ABD: Stiffness matrix.
        abd: Compliance matrix.
        Ex: Young's modulus in the x-direction.
        Ey: Young's modulus in the y-direction.
        Gxy: In-plane shear modulus.
        νxy: Poisson constant.
        νyx: Poisson constant.
        αx: CTE in x-direction.
        αy: CTE in y-direction.
        wf: Fiber weight fraction.
    """
    if not layers:
        raise ValueError('no layers in the laminate')
    if not isinstance(name, str):
        raise ValueError('the name of a laminate must be a string')
    if len(name) == 0:
        raise ValueError('the length of the name of a laminate must be >0')
    layers = tuple(layers)
    thickness = sum(l.thickness for l in layers)
    fiber_weight = sum(l.fiber_weight for l in layers)
    ρ = sum(l.ρ * l.thickness for l in layers) / thickness
    vf = sum(l.vf * l.thickness for l in layers) / thickness
    resin_weight = sum(l.resin_weight for l in layers)
    wf = fiber_weight / (fiber_weight + resin_weight)
    # Set z-values for lamina.
    zs = -thickness/2
    lz2, lz3 = [], []
    for l in layers:
        ze = zs + l.thickness
        lz2.append((ze * ze - zs * zs) / 2)
        lz3.append((ze * ze * ze - zs * zs * zs) / 3)
        zs = ze
    Ntx, Nty, Ntxy = 0.0, 0.0, 0.0
    ABD = m.zeros(6)
    for l, z2, z3 in zip(layers, lz2, lz3):
        # first row
        ABD[0][0] += l.Q̅11 * l.thickness      # Hyer:1998, p. 290
        ABD[0][1] += l.Q̅12 * l.thickness
        ABD[0][2] += l.Q̅16 * l.thickness
        ABD[0][3] += l.Q̅11 * z2
        ABD[0][4] += l.Q̅12 * z2
        ABD[0][5] += l.Q̅16 * z2
        # second row
        ABD[1][0] += l.Q̅12 * l.thickness
        ABD[1][1] += l.Q̅22 * l.thickness
        ABD[1][2] += l.Q̅26 * l.thickness
        ABD[1][3] += l.Q̅12 * z2
        ABD[1][4] += l.Q̅22 * z2
        ABD[1][5] += l.Q̅26 * z2
        # third row
        ABD[2][0] += l.Q̅16 * l.thickness
        ABD[2][1] += l.Q̅26 * l.thickness
        ABD[2][2] += l.Q̅66 * l.thickness
        ABD[2][3] += l.Q̅16 * z2
        ABD[2][4] += l.Q̅26 * z2
        ABD[2][5] += l.Q̅66 * z2
        # fourth row
        ABD[3][0] += l.Q̅11 * z2
        ABD[3][1] += l.Q̅12 * z2
        ABD[3][2] += l.Q̅16 * z2
        ABD[3][3] += l.Q̅11 * z3
        ABD[3][4] += l.Q̅12 * z3
        ABD[3][5] += l.Q̅16 * z3
        # fifth row
        ABD[4][0] += l.Q̅12 * z2
        ABD[4][1] += l.Q̅22 * z2
        ABD[4][2] += l.Q̅26 * z2
        ABD[4][3] += l.Q̅12 * z3
        ABD[4][4] += l.Q̅22 * z3
        ABD[4][5] += l.Q̅26 * z3
        # sixth row
        ABD[5][0] += l.Q̅16 * z2
        ABD[5][1] += l.Q̅26 * z2
        ABD[5][2] += l.Q̅66 * z2
        ABD[5][3] += l.Q̅16 * z3
        ABD[5][4] += l.Q̅26 * z3
        ABD[5][5] += l.Q̅66 * z3
        # Calculate unit thermal stress resultants.
        # Hyer:1998, p. 445
        Ntx += (l.Q̅11 * l.αx + l.Q̅12 * l.αy +
                l.Q̅16 * l.αxy) * l.thickness
        Nty += (l.Q̅12 * l.αx + l.Q̅22 * l.αy +
                l.Q̅26 * l.αxy) * l.thickness
        Ntxy += (l.Q̅16 * l.αx + l.Q̅26 * l.αy +
                 l.Q̅66 * l.αxy) * l.thickness
    # Finish the matrices, discarding very small νmbers in ABD.
    for i in range(6):
        for j in range(6):
            if math.fabs(ABD[i][j]) < 1e-7:
                ABD[i][j] = 0.0
    abd = m.inv(ABD)
    # Calculate the engineering properties.
    # Nettles:1994, p. 34 e.v.
    dABD = m.det(ABD)
    dt1 = m.det(m.delete(ABD, 0, 0))
    Ex = (dABD / (dt1 * thickness))
    dt2 = m.det(m.delete(ABD, 1, 1))
    Ey = (dABD / (dt2 * thickness))
    dt3 = m.det(m.delete(ABD, 2, 2))
    Gxy = (dABD / (dt3 * thickness))
    dt4 = m.det(m.delete(ABD, 0, 1))
    dt5 = m.det(m.delete(ABD, 1, 0))
    νxy = dt4 / dt1
    νyx = dt5 / dt2
    # Calculate the coefficients of thermal expansion.
    # *Technically* only valid for a symmetric laminate!
    # Hyer:1998, p. 451, (11.86)
    αx = abd[0][0] * Ntx + abd[0][1] * Nty + abd[0][2] * Ntxy
    αy = abd[1][0] * Ntx + abd[1][1] * Nty + abd[1][2] * Ntxy
    return SimpleNamespace(name=name, layers=layers, thickness=thickness,
                           fiber_weight=fiber_weight, ρ=ρ, vf=vf,
                           resin_weight=resin_weight, ABD=ABD, abd=abd, Ex=Ex,
                           Ey=Ey, Gxy=Gxy, νxy=νxy, νyx=νyx, αx=αx, αy=αy, wf=wf)
