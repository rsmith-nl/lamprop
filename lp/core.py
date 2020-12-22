# file: core.py
# vim:fileencoding=utf-8:ft=python:fdm=marker
#
# Copyright © 2014-2020 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause
# Created: 2014-02-21 22:20:39 +0100
# Last modified: 2020-12-22T20:17:06+0100
"""
Core functions of lamprop.

The following references were used in coding this module:

@Book{Barbero:2018,
    author = {Ever J. Barbero},
    title = {Introduction to composite materials design},
    edition   = 3,
    publisher = {CRC Press},
    year = {2018},
    isbn = {9781138196803}
    note = {hardcover}
}

@Book{Hyer:1998,
  author =       {Micheal W. Hyer},
  title =        {Stress analysis of fiber-reinforced composite materials},
  publisher =    {McGraw--Hill},
  year =         {1998},
  isbn =         {0071159835}
}

@Book{Tsai:1992,
  author =       {Stephen W. Tsai},
  title =        {Theory of composites design},
  publisher =    {Think Composites},
  year =         {1992},
  isbn =         {0961809035}
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
  isbn =         {90247312590}
  note =         {hardcover}
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
import lp.matrix as m


def fiber(E1, ν12, α1, ρ, name):
    """Create a fiber as a SimpleNamespace.

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
        raise ValueError("fiber E1 must be > 0")
    if ρ <= 0:
        raise ValueError("fiber ρ must be > 0")
    if not isinstance(name, str) and not len(name) > 0:
        raise ValueError("fiber name must be a non-empty string")
    return SimpleNamespace(E1=E1, ν12=ν12, α1=α1, ρ=ρ, name=name)


def resin(E, ν, α, ρ, name):
    """Create a resin as a SimpleNamespace.

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
        raise ValueError("E must be > 0")
    if ρ <= 0:
        raise ValueError("resin ρ must be > 0")
    if not isinstance(name, str) and not len(name) > 0:
        raise ValueError("resin name must be a non-empty string")
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
        raise ValueError("fiber weight cannot be <=0!")
    vf = float(vf)
    if 1.0 < vf <= 100.0:
        vf = vf / 100.0
    elif not 0.0 <= vf <= 1.0:
        raise ValueError("vf must be in the ranges 0.0-1.0 or 1.0-100.0")
    vm = 1.0 - vf
    fiber_thickness = fiber_weight / (fiber.ρ * 1000)
    thickness = fiber_thickness * (1 + vm / vf)
    resin_weight = thickness * vm * resin.ρ * 1000  # Resin [g/m²]
    E1 = vf * fiber.E1 + resin.E * vm  # Hyer:1998, p. 115, (3.32)
    # As of version 2020-12-22, use the Halpin-Tsai formula for E2.
    ζ = 2  # Assume fibers with a round cross-section.
    η = (fiber.E1 / resin.E - 1) / (fiber.E1 / resin.E + ζ)
    E2 = resin.E * ((1 + ζ * η * vf) / (1 - η * vf))  # Barbero:2018, p. 117
    E3 = E2  # Assumed for UD layers.
    ν12 = fiber.ν12 * vf + resin.ν * vm  # Barbero:2018, p. 118
    # The matrix-dominated cylindrical assemblage model is used for G12.
    Gm = resin.E / (2 * (1 + resin.ν))
    G12 = Gm * (1 + vf) / (1 - vf)
    ν21 = ν12 * E2 / E1  # Nettles:1994, p. 4
    # Calculate G23
    Kf = fiber.E1 / (3 * (1 - 2 * fiber.ν12))
    Km = resin.E / (3 * (1 - 2 * resin.ν))
    K = 1 / (vf / Kf + vm / Km)
    ν23 = 1 - ν21 - E2 / (3 * K)
    G23 = E2 / (2 * (1 + ν23))
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
    denum = 1 - ν12 * ν21
    Q11, Q12 = E1 / denum, ν12 * E2 / denum
    Q22, Q66 = E2 / denum, G12
    Qs44 = G23
    Qs55 = G12
    # Q̅ according to Hyer:1997, p. 182
    Q̅11 = Q11 * m4 + 2 * (Q12 + 2 * Q66) * n2 * m2 + Q22 * n4
    QA = Q11 - Q12 - 2 * Q66
    QB = Q12 - Q22 + 2 * Q66
    Q̅12 = (Q11 + Q22 - 4 * Q66) * n2 * m2 + Q12 * (n4 + m4)
    Q̅16 = QA * n * m3 + QB * n3 * m
    Q̅22 = Q11 * n4 + 2 * (Q12 + 2 * Q66) * n2 * m2 + Q22 * m4
    Q̅26 = QA * n3 * m + QB * n * m3
    Q̅66 = (Q11 + Q22 - 2 * Q12 - 2 * Q66) * n2 * m2 + Q66 * (n4 + m4)
    # Qstar (Qs) according to Barbero:2018, p. 167
    Q̅s44 = Qs44 * m2 + Qs55 * n2
    Q̅s55 = Qs44 * n2 + Qs55 * m2
    Q̅s45 = (Q̅s55 - Q̅s44) * n * m
    # Calculate density
    ρ = fiber.ρ * vf + resin.ρ * vm
    return SimpleNamespace(
        fiber=fiber,
        resin=resin,
        fiber_weight=fiber_weight,
        angle=angle,
        vf=vf,
        thickness=thickness,
        resin_weight=resin_weight,
        E1=E1,
        E2=E2,
        E3=E3,
        G12=G12,
        ν12=ν12,
        αx=αx,
        αy=αy,
        αxy=αxy,
        Q̅11=Q̅11,
        Q̅12=Q̅12,
        Q̅16=Q̅16,
        Q̅22=Q̅22,
        Q̅26=Q̅26,
        Q̅66=Q̅66,
        Q̅s44=Q̅s44,
        Q̅s55=Q̅s55,
        Q̅s45=Q̅s45,
        ρ=ρ,
    )


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
        Ez: Young's modulus in the z-direction.
        Gxy: In-plane shear modulus.
        νxy: Poisson constant.
        νyx: Poisson constant.
        αx: CTE in x-direction.
        αy: CTE in y-direction.
        wf: Fiber weight fraction.
    """
    if not layers:
        raise ValueError("no layers in the laminate")
    if not isinstance(name, str):
        raise ValueError("the name of a laminate must be a string")
    if len(name) == 0:
        raise ValueError("the length of the name of a laminate must be >0")
    layers = tuple(layers)
    thickness = sum(l.thickness for l in layers)
    fiber_weight = sum(l.fiber_weight for l in layers)
    ρ = sum(l.ρ * l.thickness for l in layers) / thickness
    vf = sum(l.vf * l.thickness for l in layers) / thickness
    resin_weight = sum(l.resin_weight for l in layers)
    wf = fiber_weight / (fiber_weight + resin_weight)
    # Set z-values for lamina.
    zs = -thickness / 2
    lz2, lz3 = [], []
    for l in layers:
        ze = zs + l.thickness
        lz2.append((ze * ze - zs * zs) / 2)
        lz3.append((ze * ze * ze - zs * zs * zs) / 3)
        zs = ze
    Ntx, Nty, Ntxy = 0.0, 0.0, 0.0
    ABD = m.zeros(6)
    H = m.zeros(2)
    c3 = 0
    for l, z2, z3 in zip(layers, lz2, lz3):
        # first row
        ABD[0][0] += l.Q̅11 * l.thickness  # Hyer:1998, p. 290
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
        Ntx += (l.Q̅11 * l.αx + l.Q̅12 * l.αy + l.Q̅16 * l.αxy) * l.thickness
        Nty += (l.Q̅12 * l.αx + l.Q̅22 * l.αy + l.Q̅26 * l.αxy) * l.thickness
        Ntxy += (l.Q̅16 * l.αx + l.Q̅26 * l.αy + l.Q̅66 * l.αxy) * l.thickness
        # Calculate H matrix
        sb = 5 / 4 * (l.thickness - 4 * z3 / thickness ** 2)
        H[0][0] += l.Q̅s44 * sb
        H[0][1] += l.Q̅s45 * sb
        H[1][0] += l.Q̅s45 * sb
        H[1][1] += l.Q̅s55 * sb
        # Calculate E3
        c3 += l.thickness / l.E3
    # Finish the matrices, discarding very small numbers in ABD and H.
    for i in range(6):
        for j in range(6):
            if math.fabs(ABD[i][j]) < 1e-7:
                ABD[i][j] = 0.0
    for i in range(2):
        for j in range(2):
            if math.fabs(H[i][j]) < 1e-7:
                H[i][j] = 0.0
    abd = m.inv(ABD)
    h = m.inv(H)
    # Calculate the engineering properties.
    # Nettles:1994, p. 34 e.v.
    dABD = m.det(ABD)
    dt1 = m.det(m.delete(ABD, 0, 0))
    Ex = dABD / (dt1 * thickness)
    dt2 = m.det(m.delete(ABD, 1, 1))
    Ey = dABD / (dt2 * thickness)
    dt3 = m.det(m.delete(ABD, 2, 2))
    Gxy = dABD / (dt3 * thickness)
    dt4 = m.det(m.delete(ABD, 0, 1))
    dt5 = m.det(m.delete(ABD, 1, 0))
    νxy = dt4 / dt1
    νyx = dt5 / dt2
    # See Barbero:2018, p. 197
    Gyz = H[0][0] / thickness
    Gxz = H[1][1] / thickness
    # All layers experience the same force in Z-direction.
    Ez = thickness / c3
    # Calculate the coefficients of thermal expansion.
    # *Technically* only valid for a symmetric laminate!
    # Hyer:1998, p. 451, (11.86)
    αx = abd[0][0] * Ntx + abd[0][1] * Nty + abd[0][2] * Ntxy
    αy = abd[1][0] * Ntx + abd[1][1] * Nty + abd[1][2] * Ntxy
    return SimpleNamespace(
        name=name,
        layers=layers,
        thickness=thickness,
        fiber_weight=fiber_weight,
        ρ=ρ,
        vf=vf,
        resin_weight=resin_weight,
        ABD=ABD,
        abd=abd,
        H=H,
        h=h,
        Ex=Ex,
        Ey=Ey,
        Ez=Ez,
        Gxy=Gxy,
        Gyz=Gyz,
        Gxz=Gxz,
        νxy=νxy,
        νyx=νyx,
        αx=αx,
        αy=αy,
        wf=wf,
    )
