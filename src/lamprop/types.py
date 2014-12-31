# vim:fileencoding=utf-8
#
# Copyright © 2014 R.F. Smith. All rights reserved.
# Created: 2014-02-21 22:20:39 +0100
# Modified: $Date$
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
# THIS SOFTWARE IS PROVIDED BY AUTHOR AND CONTRIBUTORS AS IS'' AND
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

__version__ = '$Revision$'[11:-2]


Fiber = namedtuple('Fiber', ['E1', 'v12', 'cte1', 'density', 'name', 'line'])


Resin = namedtuple('Resin', ['E', 'v', 'cte', 'density', 'name', 'line'])


class Lamina(object):
    """Unidirectional fiber/matrix composite layer properties"""

    __slots__ = ('_fiber', '_resin', '_weight', '_angle', '_vf', '_thickness',
                 '_rc', '_E1', '_E2', '_G12', '_v12', '_cte_x', '_cte_y',
                 '_cte_xy', '_Q_11', '_Q_12', '_Q_16', '_Q_22', '_Q_26',
                 '_Q_66', '_density', 'z2', 'z3')

    def __init__(self, fiber, resin, weight, angle, vf):
        """Initialize a Lamina object.

        :param fiber: the Fiber that forms the backbone of this layer
        :param resin: the Resin binder that is used
        :param weight: area weight of the fiber in g/m²
        :param angle: angle from the 0-axis in degrees counterclockwise
        :param vf: fiber volume fraction
        """
        if not isinstance(fiber, Fiber):
            raise ValueError('fiber must be a type Fiber')
        if not isinstance(resin, Resin):
            raise ValueError('resin must be a type Resin')
        weight = float(weight)
        if weight < 0:
            raise ValueError('weight cannot be <0!')
        vf = float(vf)
        if 1.0 < vf <= 100.0:
            vf = vf/100.0
        elif not 0.0 <= vf <= 1.0:
            raise ValueError('vf must be in the ranges 0.0-1.0 or 1.0-100.0')
        vm = (1.0 - vf)  # Volume fraction of resin material
        # [gr/m²]/[gr/cm³] = [cm³/m²] = 1/10000 [cm³/cm²] = 1/1000 [mm]
        fiber_thickness = weight/(fiber.density*1000)
        thickness = fiber_thickness*(1+vm/vf)
        rc = thickness*vm*resin.density*1000  # Resin [g/m²]
        E1 = vf*fiber.E1+resin.E*vm  # Hyer:1998, p. 115, (3.32)
        E2 = 3*resin.E  # Tsai:1992, p. 3-13
        G12 = E2/2  # Tsai:1992, p. 3-13
        v12 = 0.3  # Tsai:1992, p. 3-13
        a = math.radians(angle)
        m, n = math.cos(a), math.sin(a)
        # The powers of the sine and cosine are often used later.
        m2 = m*m
        m3, m4 = m2*m, m2*m2
        n2 = n*n
        n3, n4 = n2*n, n2*n2
        cte1 = (fiber.cte1*fiber.E1*vf+resin.cte*resin.E*vm)/E1
        cte2 = resin.cte  # This is not 100% accurate, but simple.
        cte_x = cte1*m2+cte2*n2
        cte_y = cte1*n2+cte2*m2
        cte_xy = 2*(cte1-cte2)*m*n
        S11, S12 = 1/E1, -v12/E1
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
        self._fiber, self._resin, self._weight = fiber, resin, weight
        self._angle, self._vf, self._rc = angle, vf, rc
        self._E1, self._E2, self._G12, self._v12 = E1, E2, G12, v12
        self._cte_x, self._cte_y, self._cte_xy = cte_x, cte_y, cte_xy
        self._Q_11, self._Q_12, self._Q_16 = Q_11, Q_12, Q_16
        self._Q_22, self._Q_26, self._Q_66 = Q_22, Q_26, Q_66
        self._density, self._thickness = density, thickness
        self.z2, self.z3 = None, None

    @property
    def fiber(self):
        return self._fiber

    @property
    def resin(self):
        return self._resin

    @property
    def weight(self):
        return self._weight

    @property
    def angle(self):
        return self._angle

    @property
    def vf(self):
        return self._vf

    @property
    def thickness(self):
        return self._thickness

    @property
    def rc(self):
        return self._rc

    @property
    def E1(self):
        return self._E1

    @property
    def E2(self):
        return self._E2

    @property
    def v12(self):
        return self._v12

    @property
    def cte_x(self):
        return self._cte_x

    @property
    def cte_y(self):
        return self._cte_y

    @property
    def cte_xy(self):
        return self._cte_xy

    @property
    def Q_11(self):
        return self._Q_11

    @property
    def Q_12(self):
        return self._Q_12

    @property
    def Q_16(self):
        return self._Q_16

    @property
    def Q_22(self):
        return self._Q_22

    @property
    def Q_26(self):
        return self._Q_26

    @property
    def Q_66(self):
        return self._Q_66

    @property
    def density(self):
        return self._density


class Laminate(object):
    """Laminate properties."""

    __slots__ = ('_name', '_layers', '_thickness', '_weight', '_density',
                 '_vf', '_rc', '_wf', '_ABD', '_abd', '_Ex', '_Ey', '_Gxy',
                 '_Vxy', '_Vyx', '_cte_x', '_cte_y')

    def __init__(self, name, layers):
        """Create a laminate from its name and constituent layers.

        :param name: name of the laminate
        :param lamina: a list of Lamina that make up the laminate
        """
        if not layers:
            raise ValueError('No layers!')
        self._name = name
        self._layers = layers
        self._thickness = sum([l.thickness for l in layers])
        self._weight = sum([l.weight for l in layers])  # fibers!
        self._density = sum([l.density*l.thickness
                             for l in layers])/self._thickness
        self._vf = sum([l.vf*l.thickness for l in layers])/self._thickness
        self._rc = sum([l.rc for l in layers])  # resin content
        self._wf = self._weight/(self._weight + self._rc)
        # Set z-values for lamina.
        zs = -self._thickness/2
        for l in self._layers:
            ze = zs + l.thickness
            l.z2 = (ze*ze-zs*zs)/2
            l.z3 = (ze*ze*ze-zs*zs*zs)/3
            zs = ze
        Nt_x, Nt_y, Nt_xy = 0.0, 0.0, 0.0
        ABD = np.zeros((6, 6))
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
        # Finish the matrices, discarding very small numbers in ABD.
        for i in range(6):
            for j in range(6):
                if math.fabs(ABD[i, j]) < 1e-7:
                    ABD[i, j] = 0.0
        self._ABD = ABD
        self._abd = np.linalg.inv(ABD)
        # Calculate the engineering properties.
        # Nettles:1994, p. 34 e.v.
        dABD = np.linalg.det(ABD)
        dt1 = np.linalg.det(ABD[1:6, 1:6])
        self._Ex = (dABD / (dt1 * self.thickness))
        dt2 = np.linalg.det(np.delete(np.delete(ABD, 1, 0), 1, 1))
        self._Ey = (dABD / (dt2 * self.thickness))
        dt3 = np.linalg.det(np.delete(np.delete(ABD, 2, 0), 2, 1))
        self._Gxy = (dABD / (dt3 * self.thickness))
        dt4 = np.linalg.det(np.delete(np.delete(ABD, 0, 0), 1, 1))
        dt5 = np.linalg.det(np.delete(np.delete(ABD, 1, 0), 0, 1))
        self._Vxy = dt4 / dt1
        self._Vyx = dt5 / dt2
        # non-symmetric laminates
        # Calculate the coefficients of thermal expansion.
        # Technically only valid for a symmetric laminate!
        self._cte_x = (self.abd[0, 0]*Nt_x + self.abd[0, 1]*Nt_y +
                       self.abd[0, 2]*Nt_xy)  # Hyer:1998, p. 451, (11.86)
        self._cte_y = (self.abd[1, 0]*Nt_x + self.abd[1, 1]*Nt_y +
                       self.abd[1, 2]*Nt_xy)

    @property
    def nlayers(self):
        return len(self._layers)

    @property
    def name(self):
        return self._name

    @property
    def layers(self):
        return self._layers

    @property
    def thickness(self):
        return self._thickness

    @property
    def weight(self):
        return self._weight

    @property
    def density(self):
        return self._density

    @property
    def vf(self):
        return self._vf

    @property
    def rc(self):
        return self._rc

    @property
    def wf(self):
        return self._wf

    @property
    def ABD(self):
        return self._ABD

    @property
    def abd(self):
        return self._abd

    @property
    def Ex(self):
        return self._Ex

    @property
    def Ey(self):
        return self._Ey

    @property
    def Gxy(self):
        return self._Gxy

    @property
    def Vxy(self):
        return self._Vxy

    @property
    def Vyx(self):
        return self._Vyx

    @property
    def cte_x(self):
        return self._cte_x

    @property
    def cte_y(self):
        return self._cte_y
