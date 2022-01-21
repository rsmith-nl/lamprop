# file: core.py
# vim:fileencoding=utf-8:ft=python:fdm=marker
#
# Copyright © 2014-2021 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause
# Created: 2014-02-21 22:20:39 +0100
# Last modified: 2022-01-21T15:35:24+0100
"""
Core functions of lamprop.

The following references were used in coding this module:

@Book{Barbero:2018,
    author = {Ever J. Barbero},
    title = {Introduction to composite materials design},
    edition   = 3,
    publisher = {CRC Press},
    year = {2018},
    isbn = {9781138196803},
    note = {hardcover}
}

@Book{Barbero:2008,
    author = {Ever J. Barbero},
    title = {Finite element analysis of composite materials},
    publisher = {CRC Press},
    year = {2008},
    isbn = {9781420054330},
    note = {hardcover}
}

@Book{Bower:2010,
    author = {Allan F. Bower},
    title = {Applied Mechanics of Solids},
    publisher = {CRC Press},
    year = {2010},
    isbn = {9781439802472a},
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
import lp.matrix as lpm


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
    rv = SimpleNamespace()
    rv.E1 = float(E1)
    assert rv.E1 > 0, "fiber E1 must be > 0"
    rv.ν12 = float(ν12)
    rv.α1 = float(α1)
    rv.ρ = float(ρ)
    assert rv.ρ > 0, "fiber ρ must be > 0"
    rv.name = name
    assert (
        isinstance(rv.name, str) and len(rv.name) > 0
    ), "fiber name must be a non-empty string"
    return rv


def resin(E, ν, α, ρ, name):
    """Create a resin as a SimpleNamespace.

    Arguments/properties of a Resin:
        E (float): Young's modulus in MPa. Must be >0.
        ν (float): Poisson's constant.
        α (float): CTE in K⁻¹
        ρ (float): Specific gravity of the resin in g/cm³. Must be >0.
        name (str): String containing the name of the resin. Must not be empty.
    """
    rv = SimpleNamespace()
    rv.E = float(E)
    assert rv.E > 0, "resin E must be > 0"
    rv.ν = float(ν)
    rv.α = float(α)
    rv.ρ = float(ρ)
    assert rv.ρ > 0, "resin ρ must be > 0"
    rv.name = name
    assert (
        isinstance(rv.name, str) and len(rv.name) > 0
    ), "resin name must be a non-empty string"
    return rv


def lamina(fiber, resin, fiber_weight, angle, vf):
    """Create a lamina of unidirectional fibers in resin.
    This can be considered as a transversely isotropic material.

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
        S: 3D stiffness matrix for the lamina in global coordinates.
    """
    fiber_weight = float(fiber_weight)
    assert fiber_weight > 0, "fiber weight cannot be <=0!"
    vf = float(vf)
    assert (
        1.0 < vf <= 100.0 or 0.0 <= vf <= 1.0
    ), "vf must be in the ranges 0.0-1.0 or 1.0-100.0"
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
    ν13 = ν12
    # The matrix-dominated cylindrical assemblage model is used for G12.
    Gm = resin.E / (2 * (1 + resin.ν))
    G12 = Gm * (1 + vf) / (1 - vf)
    G13 = G12
    ν21 = ν12 * E2 / E1  # Nettles:1994, p. 4
    # Calculate G23, necessary for Qs44.
    Kf = fiber.E1 / (3 * (1 - 2 * fiber.ν12))
    Km = resin.E / (3 * (1 - 2 * resin.ν))
    K = 1 / (vf / Kf + vm / Km)
    ν23 = 1 - ν21 - E2 / (3 * K)
    G23 = E2 / (2 * (1 + ν23))  # Barbero:2008, p. 23, Barbero:2018, p. 504
    a = math.radians(float(angle))
    m, n = math.cos(a), math.sin(a)
    # Calculate the 3D stiffness matrix for this lamina
    # Note about terminology: in the literature, the stiffness matrix is
    # generally named C, while its inverse the compliance matrix is called S.
    # This is confusing IMO, but I will follow convention here for the sake of
    # clarity.
    # First, the compliance matrix in lamina coordinates
    Sp = [
        [1 / E1, -ν12 / E1, -ν13 / E1, 0, 0, 0],
        [-ν12 / E1, 1 / E2, -ν23 / E2, 0, 0, 0],
        [-ν13 / E1, -ν23 / E2, 1 / E3, 0, 0, 0],
        [0, 0, 0, 1 / G23, 0, 0],
        [0, 0, 0, 0, 1 / G13, 0],
        [0, 0, 0, 0, 0, 1 / G12],
    ]
    # Invert it to the stiffness matrix in lamina coordinates
    Cp = lpm.inv(Sp)
    # Convert to global coordinates.
    Tbar = tbar(angle)
    C = lpm.matmul(lpm.matmul(lpm.transp(Tbar), Cp), Tbar)
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
    # Barbero:2018, p. 159
    denum = 1 - ν12 * ν21
    Q11, Q12 = E1 / denum, ν12 * E2 / denum
    Q22, Q66 = E2 / denum, G12
    Qs44 = G23
    Qs55 = G12  # Assuming transverse isotropy.
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
        G13=G12,
        G23=G23,
        ν12=ν12,
        ν13=ν13,
        ν23=ν23,
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
        C=C,
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
        C: 3D Stiffness matrix for the laminate in global coordinates.
    """
    assert layers, "no layers in the laminate"
    assert (
        isinstance(name, str) and len(name) > 0
    ), "laminate name must be a non-empty string"
    orig_layers = [la for la in layers]
    layers = tuple(la for la in layers if isinstance(la, SimpleNamespace))
    thickness = sum(la.thickness for la in layers)
    fiber_weight = sum(la.fiber_weight for la in layers)
    ρ = sum(la.ρ * la.thickness for la in layers) / thickness
    vf = sum(la.vf * la.thickness for la in layers) / thickness
    resin_weight = sum(la.resin_weight for la in layers)
    wf = fiber_weight / (fiber_weight + resin_weight)
    # Set z-values for lamina.
    zs = -thickness / 2
    lz2, lz3 = [], []
    C = lpm.zeros(6)
    for la in layers:
        ze = zs + la.thickness
        lz2.append((ze * ze - zs * zs) / 2)
        lz3.append((ze * ze * ze - zs * zs * zs) / 3)
        zs = ze
        C = lpm.add(C, lpm.mul(la.C, la.thickness / thickness))
    C = lpm.clean(C)
    S = lpm.inv(C)
    Ntx, Nty, Ntxy = 0.0, 0.0, 0.0
    ABD = lpm.zeros(6)
    H = lpm.zeros(2)
    c3 = 0
    for la, z2, z3 in zip(layers, lz2, lz3):
        # first row
        ABD[0][0] += la.Q̅11 * la.thickness  # Hyer:1998, p. 290
        ABD[0][1] += la.Q̅12 * la.thickness
        ABD[0][2] += la.Q̅16 * la.thickness
        ABD[0][3] += la.Q̅11 * z2
        ABD[0][4] += la.Q̅12 * z2
        ABD[0][5] += la.Q̅16 * z2
        # second row
        ABD[1][0] += la.Q̅12 * la.thickness
        ABD[1][1] += la.Q̅22 * la.thickness
        ABD[1][2] += la.Q̅26 * la.thickness
        ABD[1][3] += la.Q̅12 * z2
        ABD[1][4] += la.Q̅22 * z2
        ABD[1][5] += la.Q̅26 * z2
        # third row
        ABD[2][0] += la.Q̅16 * la.thickness
        ABD[2][1] += la.Q̅26 * la.thickness
        ABD[2][2] += la.Q̅66 * la.thickness
        ABD[2][3] += la.Q̅16 * z2
        ABD[2][4] += la.Q̅26 * z2
        ABD[2][5] += la.Q̅66 * z2
        # fourth row
        ABD[3][0] += la.Q̅11 * z2
        ABD[3][1] += la.Q̅12 * z2
        ABD[3][2] += la.Q̅16 * z2
        ABD[3][3] += la.Q̅11 * z3
        ABD[3][4] += la.Q̅12 * z3
        ABD[3][5] += la.Q̅16 * z3
        # fifth row
        ABD[4][0] += la.Q̅12 * z2
        ABD[4][1] += la.Q̅22 * z2
        ABD[4][2] += la.Q̅26 * z2
        ABD[4][3] += la.Q̅12 * z3
        ABD[4][4] += la.Q̅22 * z3
        ABD[4][5] += la.Q̅26 * z3
        # sixth row
        ABD[5][0] += la.Q̅16 * z2
        ABD[5][1] += la.Q̅26 * z2
        ABD[5][2] += la.Q̅66 * z2
        ABD[5][3] += la.Q̅16 * z3
        ABD[5][4] += la.Q̅26 * z3
        ABD[5][5] += la.Q̅66 * z3
        # Calculate unit thermal stress resultants.
        # Hyer:1998, p. 445
        Ntx += (la.Q̅11 * la.αx + la.Q̅12 * la.αy + la.Q̅16 * la.αxy) * la.thickness
        Nty += (la.Q̅12 * la.αx + la.Q̅22 * la.αy + la.Q̅26 * la.αxy) * la.thickness
        Ntxy += (la.Q̅16 * la.αx + la.Q̅26 * la.αy + la.Q̅66 * la.αxy) * la.thickness
        # Calculate H matrix (derived from Barbero:2018, p. 181)
        sb = 5 / 4 * (la.thickness - 4 * z3 / thickness ** 2)
        H[0][0] += la.Q̅s44 * sb
        H[0][1] += la.Q̅s45 * sb
        H[1][0] += la.Q̅s45 * sb
        H[1][1] += la.Q̅s55 * sb
        # Calculate E3
        c3 += la.thickness / la.E3
    # Finish the matrices, discarding very small numbers in ABD and H.
    ABD = lpm.clean(ABD)
    H = lpm.clean(H)
    abd = lpm.inv(ABD)
    h = lpm.inv(H)
    # Calculate the engineering properties.
    # Nettles:1994, p. 34 e.v.
    dABD = lpm.det(ABD)
    dt1 = lpm.det(lpm.delete(ABD, 0, 0))
    Ex = dABD / (dt1 * thickness)
    dt2 = lpm.det(lpm.delete(ABD, 1, 1))
    Ey = dABD / (dt2 * thickness)
    dt3 = lpm.det(lpm.delete(ABD, 2, 2))
    Gxy = dABD / (dt3 * thickness)
    dt4 = lpm.det(lpm.delete(ABD, 0, 1))
    dt5 = lpm.det(lpm.delete(ABD, 1, 0))
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
    # Calculate tensor engineering properties
    tEx, tEy, tEz = 1 / S[0][0], 1 / S[1][1], 1 / S[2][2]
    tGxy, tGxz, tGyz = 1 / S[5][5], 1 / S[4][4], 1 / S[3][3]
    tνxy, tνxz, tνyz = -S[1][0] / S[0][0], -S[2][0] / S[0][0], -S[2][1] / S[1][1]
    return SimpleNamespace(
        name=name,
        layers=orig_layers,
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
        C=C,
        S=S,
        tEx=tEx,
        tEy=tEy,
        tEz=tEz,
        tGxy=tGxy,
        tGyz=tGyz,
        tGxz=tGxz,
        tνxy=tνxy,
        tνxz=tνxz,
        tνyz=tνyz,
    )


def tbar(degrees):
    """Matrix for rotating lamina coordinates around the z-axis."""
    θ = math.radians(degrees)
    c, s = math.cos(θ), math.sin(θ)
    # Barbero:2008 p. 12 & 15
    Tbar = [
        [c * c, s * s, 0, 0, 0, c * s],
        [s * s, c * c, 0, 0, 0, -c * s],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, c, -s, 0],
        [0, 0, 0, s, c, 0],
        [-2 * c * s, 2 * c * s, 0, 0, 0, c * c - s * s],
    ]
    return Tbar


def isortho(C):
    """Determine if a stiffness matrix is orthotropic."""
    zero_indices = [
        (0, 3),
        (0, 4),
        (0, 5),
        (1, 3),
        (1, 4),
        (1, 5),
        (2, 3),
        (2, 4),
        (2, 5),
        (3, 0),
        (3, 1),
        (3, 2),
        (3, 4),
        (3, 5),
        (4, 0),
        (4, 1),
        (4, 2),
        (4, 3),
        (4, 5),
        (5, 0),
        (5, 1),
        (5, 2),
        (5, 3),
        (5, 4),
    ]
    count = 0
    for i, j in zero_indices:
        if math.isclose(C[i][j], 0.0):
            count += 1
    if count == len(zero_indices):
        return True
    return False


def isti(C):
    """Determine if the stiffness matrix C is transversely isotropic."""
    if not isortho(C):
        return False
    if math.isclose(C[4][4], C[5][5]) and math.isclose(
        C[3][3], 2 * (C[1][1] - C[1][2])
    ):
        return True
    return False


def toabaqusi(C):
    """Convert stiffness matrix to Abaqus format and SI units."""
    D = lpm.mul(C, 1e6)
    D[0][3] = C[0][5] * 1e6
    D[0][5] = C[0][3] * 1e6
    D[1][3] = C[1][5] * 1e6
    D[1][5] = C[1][3] * 1e6
    D[2][3] = C[2][5] * 1e6
    D[2][5] = C[2][3] * 1e6
    D[3][3] = C[5][5] * 1e6
    D[5][5] = C[3][3] * 1e6
    return D
