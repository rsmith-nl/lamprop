# -*- coding: utf-8 -*-
# Copyright © 2011-2013 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# $Date$
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
This module contains the classes necessary to calculate the properties of
continuous fiber reinforced laminates.

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

__version__ = '$Revision$'[11:-2]

import math
import numpy


class Fiber:
    """A class for containing fiber properties. Direction 1 is in the length
    of the fiber, direction 2 is perpendicular to that."""

    def __init__(self, E1, v12, cte1, density, name):
        """Create a fiber instance.

        E1: Young's modulus along the length of the fiber in MPa.
        v12: Poisson's constant of the fiber (dimensionless).
        cte1: Coefficient of thermal expansion in K⁻¹.
        density: In g/cm³.
        name: Identifier"""
        self.E1 = float(E1)
        self.v12 = float(v12)
        self.cte1 = float(cte1)
        self.density = float(density)
        self.name = name

    def __str__(self):
        s = "[name={}, density={}, E1={}, v12={}, cte1={}]"
        return s.format(self.name, self.density, self.E1, self.v12, 
                        self.cte1)

    def thickness(self, aw):
        """Return the theoretical thickness of a fiber layer in mm based on
        the area weight aw in gr/m²."""
        # [gr/m²]/[gr/cm³] = [cm³/m²] = 1/10000 [cm³/cm²] = 1/1000 [mm]
        return float(aw)/(self.density*1000)


class Resin:
    """A class for containing resin properties."""

    def __init__(self, E, v, cte, density):
        """Create a Resin instance.

        E: Young's Modulus of the resin in MPa.
        v: Poisson's constant of the resin (dimensionless).
        cte: Coefficient of thermal expansion of the resin in K⁻¹.
        density: in g/cm³.
        name: Identifier."""
        self.E = float(E)
        self.v = float(v)
        self.G = self.E/(2.0*(1.0+self.v))      # Shear modulus [MPa]
        self.cte = float(cte)
        self.density = float(density)

    def __str__(self):
        s = "[density={},E={}, v={}, G={}, cte={}]"
        return s.format(self.density, self.E, self.v, self.G, self.cte)


class Lamina:
    """A class for unidirectional layer properties."""

    def __init__(self, fiber, resin, weight, angle, vf):
        """Create a Lamina (layer) instance.

        fiber: Identifier of the Fiber used in this layer.
        resin: Identifier of the Resin used in this layer.
        weight: Area weight of the Fiber in g/m².
        angle: Angle of the fibers w.r.t. the 0-axis in degrees.
        vf: Volume fraction of fibers in the lamina 
        (dimensionless, between 0 and 1)."""
        self.fiber = fiber
        self.resin = resin
        self.weight = float(weight)
        self.angle = float(angle)
        self.vf = float(vf)
        vm = (1.0 - self.vf)            # Volume fraction of resin material
        self.thickness = fiber.thickness(weight)*(1+vm/vf)
        self.rc = self.thickness*vm*resin.density*1000.0  # Resin [g/m²]
        self.E1 = self.vf*fiber.E1+resin.E*vm   # Hyer:1998, p. 115, (3.32)
        self.E2 = 3*self.resin.E        # Tsai:1992, p. 3-13
        self.G12 = self.E2/2            # Tsai:1992, p. 3-13
        self.v12 = 0.3                  # Tsai:1992, p. 3-13
        m = math.cos(math.radians(self.angle))
        n = math.sin(math.radians(self.angle))
        # The powers of the sine and cosine are often used later.
        m2 = m*m
        m3 = m2*m
        m4 = m3*m
        n2 = n*n
        n3 = n2*n
        n4 = n3*n
        cte1 = (fiber.cte1*fiber.E1*self.vf+resin.cte*resin.E*vm)/self.E1
        cte2 = resin.cte # This is not 100% accurate, but simple.
        self.cte_x = cte1*m2+cte2*n2
        self.cte_y = cte1*n2+cte2*m2
        self.cte_xy = 2*(cte1-cte2)*m*n
        S11 = 1/self.E1  # Hyer:1998, p. 152, (4.5)
        S12 = -self.v12/self.E1
        S22 = 1/self.E2
        S66 = 1/self.G12
        denum = S11*S22-S12*S12
        Q11 = S22/denum
        Q12 = -S12/denum
        Q22 = S11/denum
        Q66 = 1/S66
        self.Q_11 = Q11*m4+2*(Q12+2*Q66)*n2*m2+Q22*n4
        QA = Q11-Q12-2*Q66
        QB = Q12-Q22+2*Q66
        self.Q_12 = (Q11+Q22-4*Q66)*n2*m2+Q12*(n4+m4)
        self.Q_16 = QA*n*m3+QB*n3*m
        self.Q_22 = Q11*n4+2*(Q12+2*Q66)*n2*m2+Q22*m4
        self.Q_26 = QA*n3*m+QB*n*m3
        self.Q_66 = (Q11+Q22-2*Q12-2*Q66)*n2*m2+Q66*(n4+m4)
        self.density = fiber.density*self.vf+resin.density*vm

    def __str__(self):
        s = "[fiber={}, resin={}, weight={}, angle={}, vf={}]"
        return s.format(self.fiber.name, self.resin.name, self.weight, 
                        self.angle, self.vf)


class Laminate:
    """A class for fibrous laminates."""

    def __init__(self, name):
        """Create a laminate instance.
        
        name: Identifier for the laminate."""
        self.name = name
        self.layers = []
        self.thickness = 0.0
        self.weight = 0.0       # Weight of the fibers only! [g/m²]
        self.rc = 0.0           # Weight of the resin [g/m²]
        self.finished = False
        self.vf = None
        self.wf = None
        self.Ex = None
        self.Ey = None
        self.Gxy = None
        self.Vxy = None
        self.Vyx = None
        self.density = None
        self.ABD = None
        self.abd = None
        self.cte_x = None
        self.cte_y = None

    def append(self, lamina):
        """Add a layer to the laminate."""
        self.layers.append(lamina)
        self.weight += lamina.weight
        self.rc += lamina.rc
        self.thickness += lamina.thickness
        self.finished = False

    def num_layers(self):
        """Return the number of layers in the laminate."""
        return len(self.layers)

    def finish(self):
        """Calculate the laminate properties."""
        if self.finished:
            return
        if len(self.layers) == 0:
            return
        self.density = 0.0
        self.vf = 0.0
        for l in self.layers:
            if l == self.layers[0]:
                zs = -self.thickness/2
                prev = self.layers[0]
            else:
                zs += prev.thickness
            ze = zs + l.thickness
            l.z2 = (ze*ze-zs*zs)/2
            l.z3 = (ze*ze*ze-zs*zs*zs)/3
            prev = l
        Nt_x = 0.0
        Nt_y = 0.0
        Nt_xy = 0.0
        ABD = numpy.zeros((6, 6))
        for l in self.layers:
            # first row
            ABD[0, 0] += l.Q_11*l.thickness      # Hyer:1998, p. 290
            ABD[0, 1] += l.Q_12*l.thickness
            ABD[0, 2] += l.Q_16*l.thickness
            ABD[0, 3] += l.Q_11*l.z2
            ABD[0, 4] += l.Q_12*l.z2
            ABD[0, 5] += l.Q_16*l.z2
            # second row
            ABD[1, 0] += l.Q_12*l.thickness
            ABD[1, 1] += l.Q_22*l.thickness
            ABD[1, 2] += l.Q_26*l.thickness
            ABD[1, 3] += l.Q_12*l.z2
            ABD[1, 4] += l.Q_22*l.z2
            ABD[1, 5] += l.Q_26*l.z2
            # third row
            ABD[2, 0] += l.Q_16*l.thickness
            ABD[2, 1] += l.Q_26*l.thickness
            ABD[2, 2] += l.Q_66*l.thickness
            ABD[2, 3] += l.Q_16*l.z2
            ABD[2, 4] += l.Q_26*l.z2
            ABD[2, 5] += l.Q_66*l.z2
            # fourth row
            ABD[3, 0] += l.Q_11*l.z2
            ABD[3, 1] += l.Q_12*l.z2
            ABD[3, 2] += l.Q_16*l.z2
            ABD[3, 3] += l.Q_11*l.z3
            ABD[3, 4] += l.Q_12*l.z3
            ABD[3, 5] += l.Q_16*l.z3
            # fifth row
            ABD[4, 0] += l.Q_12*l.z2
            ABD[4, 1] += l.Q_22*l.z2
            ABD[4, 2] += l.Q_26*l.z2
            ABD[4, 3] += l.Q_12*l.z3
            ABD[4, 4] += l.Q_22*l.z3
            ABD[4, 5] += l.Q_26*l.z3
            # sixth row
            ABD[5, 0] += l.Q_16*l.z2
            ABD[5, 1] += l.Q_26*l.z2
            ABD[5, 2] += l.Q_66*l.z2
            ABD[5, 3] += l.Q_16*l.z3
            ABD[5, 4] += l.Q_26*l.z3
            ABD[5, 5] += l.Q_66*l.z3
            # Calculate unit thermal stress resultants.
            Nt_x += (l.Q_11*l.cte_x + l.Q_12*l.cte_y + 
                     l.Q_16*l.cte_xy)*l.thickness  # Hyer:1998, p. 445
            Nt_y += (l.Q_12*l.cte_x + l.Q_22*l.cte_y + 
                     l.Q_26*l.cte_xy)*l.thickness 
            Nt_xy += (l.Q_16*l.cte_x + l.Q_26*l.cte_y + 
                      l.Q_66*l.cte_xy)*l.thickness
            # Overall density and fiber volume fraction calculation
            self.density += l.density*l.thickness
            self.vf += l.vf*l.thickness
        # Finish the density and vf calculations.
        self.density /= self.thickness
        self.vf /= self.thickness
        # Finish the matrices, discarding very small numbers in ABD.
        for i in range(6):
            for j in range(6):
                if math.fabs(ABD[i, j]) < 1e-7:
                    ABD[i, j] = 0.0
        self.ABD = ABD
        self.abd = numpy.linalg.inv(ABD)
        # Calculate the engineering properties.
        # Nettles:1994, p. 34 e.v.
        dABD = numpy.linalg.det(ABD)
        dt1 = numpy.linalg.det(ABD[1:6,1:6])
        self.Ex = (dABD / (dt1 * self.thickness))
        dt2 = numpy.linalg.det(numpy.delete(
                numpy.delete(ABD, 1, 0), 1, 1))
        self.Ey = (dABD / (dt2 * self.thickness))
        dt3 = numpy.linalg.det(numpy.delete(
                numpy.delete(ABD, 2, 0), 2, 1))
        self.Gxy = (dABD / (dt3 * self.thickness))
        dt4 = numpy.linalg.det(numpy.delete(
                numpy.delete(ABD, 0, 0), 1, 1))
        self.Vxy = dt4 / dt1
        self.Vyx = dt4 / dt2
        # non-symmetric laminates
        # Calculate the coefficients of thermal expansion.
        # Technically only valid for a symmetric laminate!
        self.cte_x = (self.abd[0, 0]*Nt_x + self.abd[0, 1]*Nt_y + 
                      self.abd[0, 2]*Nt_xy) # Hyer:1998, p. 451, (11.86)
        self.cte_y = (self.abd[1, 0]*Nt_x + self.abd[1, 1]*Nt_y + 
                      self.abd[1, 2]*Nt_xy)
        # Finish the weight fraction calculation.
        self.wf = self.weight/(self.weight+self.rc)
        self.finished = True
