# -*- coding: utf-8 -*-
# Classes for fiber, matrix and lamina properties.
#
# Copyright © 2011 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# Time-stamp: <2011-03-26 14:19:00 rsmith>
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

import math
import numpy

class Fiber:
    """A class for containing fiber properties. Direction 1 is in the length
    of the fiber, direction 2 is perpendicular to that."""
    def __init__(self, E1=0.0, E2=0.0, v12=0.0, G12=0.0, 
                 cte1=0.0, cte2=0.0, density=1.0):
        self.E1=E1      # Young's Modulus [MPa]
        self.E2=E2
        self.v12=v12    # Poisson's constant
        self.G12=G12    # Shear modulus [MPa]
        self.cte1=cte1  # Coefficient of thermal expansion [K⁻¹]
        self.cte2=cte2
        self.density=density    # [g/cm³]
    def fromline(self, line):
        lst = line.split()
        if lst[0] != 'f:':    # Ignore
            return False
        __init__(self, lst[1], lst[2], lst[3], lst[4], lst[5], lst[6], lst[7])
        return True

class Resin:
    """A class for containing resin properties."""
    def __init__(self, E=0.0, v=0.0, cte=0.0, density=1.0):
        self.E=E                # Young's Modulus [MPa]
        self.v=v                # Poisson's constant
        self.G=E/(2*(1+v))      # Shear modulus [MPa]
        self.cte=cte            # Coefficient of thermal expansion [K⁻¹]
        self.density = density  # [g/cm³]
    def fromline(self, line):
        lst = line.split()
        if lst[0] != 'r:':    # Ignore
            return False
        __init__(self, lst[1], lst[2], lst[3], lst[4])
        return True

class Lamina:
    """A class for unidirectional layer properties."""
    def __init__(self, fiber, resin, weight=0.0, angle=0.0, vf=0.5):
        self.fiber = fiber      # Fiber properties
        self.resin = resin      # Resin properties
        self.weight = weight    # Area weight if the fibers [g/m²]
        self.angle = angle      # Angle of the fibers [degrees]
        self.vf = vf            # Volume fraction of fibers in the lamina
        vm = (1-vf)             # Volume fraction of resin material
        self.thickness = weight/(fiber.density*1000.0)*(1+vm/vf)
        self.E1 = vf*fiber.E1+resin.E*vm
        self.E2 = 1/((vf/fiber.E2+0.5*vm/resin.E)/(vf+0.5*vm))
        self.G12 = 1/((vf/fiber.G12+0.6*vm/resin.G)/(vf+0.6*vm))
        self.v12 = fiber.v12*vf+resin.v*vm
        m = math.cos(math.radians(angle))
        n = math.sin(math.radians(angle))
        # The powers of the sine and cosine of the angle are often used later.
        m2 = m*m; m3 = m2*m; m4 = m3*m
        n2 = n*n; n3 = n2*n; n4 = n3*n
        cte1 = (fiber.cte1*fiber.E1+resin.cte*resin.E*vm)/self.E1
        cte2 = ((resin.cte+(fiber.cte2-resin.cte)*vf+
                 (fiber.E1*resin.v-resin.E*fiber.v12)/self.E1)*
                (resin.cte-fiber.cte1)*vm*vf)
        self.cte_x = cte1*m2+cte2*n2
        self.cte_y = cte1*n2+cte2*m2
        S11 = 1/self.E1; S12 = -self.v12/self.E1
        S22 = 1/self.E2; S66 = 1/self.G12; denum = S11*S22-S12*S12;
        Q11 = S22/denum; Q12 = -S12/denum; Q22 = S11/denum; Q66 = 1/S66
        self.Q_11 = Q11*m4+2*(Q12+2*Q66)*n2*m2+Q22*n4
        foo = Q11-Q12-2*Q66; bar = Q12-Q22+2*Q66
        self.Q_12 = (Q11+Q22-4*Q66)*n2*m2+Q12*(n4+m4)
        self.Q_16 = foo*n*m3+bar*n3*m
        self.Q_22 = Q11*n4+2*(Q12+2*Q66)*n2*m2+Q22*m4
        self.Q_26 = foo*n3*m+bar*n*m3
        self.Q_66 = (Q11+Q22-2*Q12-2*Q66)*n2*m2+Q66*(n4+m4)
        self.density = fiber.density*vf+resin.density*vm

class Laminate:
    def __init__(self, name):
        self.layers = []
        self.name = name
        self.thickness=0.0
        self.vf = 0.0
        self.wf = 0.0
        self.Ex = 0.0
        self.Ey = 0.0
        self.Gxy = 0.0
        self.Vxy = 0.0
        self.Vyx = 0.0
        self.finished=False
    def append(self, lamina): # Add a layer to the laminate.
        layers.append(lamina)
        self.finished = False
    def num_layers(self):
        return len(self.layers)
    def finish(self):
        for l in layers:
            if l == layers[0]:
                l.z0 = -l.thickness/2
                prev = layers[0]
            else:
                l.z0 = prev.z0 + prev.thickness
            zs = l.z0; ze = zs + l.thickness
            l.z2 = (ze*ze-zs*zs)/2
            l.z3 = (ze*ze*ze-zs*zs*zs)/3
            prev=l
        ABD = numpy.zeros((6,6))
        self.density=.0
        for l in layers:
                # first row
                ABD[0,0] += l.Q_11*l.t;      # [1], p. 290
                ABD[0,1] += l.Q_12*l.t;
                ABD[0,2] += l.Q_16*l.t;
                ABD[0,3] += l.Q_11*l.z2;
                ABD[0,4] += l.Q_12*l.z2;
                ABD[0,5] += l.Q_16*l.z2;
                # second row
                ABD[1,0] += l.Q_12*l.t;
                ABD[1,1] += l.Q_22*l.t;
                ABD[1,2] += l.Q_26*l.t;
                ABD[1,3] += l.Q_12*l.z2;
                ABD[1,4] += l.Q_22*l.z2;
                ABD[1,5] += l.Q_26*l.z2;
                # third row
                ABD[2,0] += l.Q_16*l.t;
                ABD[2,1] += l.Q_26*l.t;
                ABD[2,2] += l.Q_66*l.t;
                ABD[2,3] += l.Q_16*l.z2;
                ABD[2,4] += l.Q_26*l.z2;
                ABD[2,5] += l.Q_66*l.z2;
                # fourth row
                ABD[3,0] += l.Q_11*l.z2;
                ABD[3,1] += l.Q_12*l.z2;
                ABD[3,2] += l.Q_16*l.z2;
                ABD[3,3] += l.Q_11*l.z3;
                ABD[3,4] += l.Q_12*l.z3;
                ABD[3,5] += l.Q_16*l.z3;
                # fifth row
                ABD[4,0] += l.Q_12*l.z2;
                ABD[4,1] += l.Q_22*l.z2;
                ABD[4,2] += l.Q_26*l.z2;
                ABD[4,3] += l.Q_12*l.z3;
                ABD[4,4] += l.Q_22*l.z3;
                ABD[4,5] += l.Q_26*l.z3;
                # sixth row
                ABD[5,0] += l.Q_16*l.z2;
                ABD[5,1] += l.Q_26*l.z2;
                ABD[5,2] += l.Q_66*l.z2;
                ABD[5,3] += l.Q_16*l.z3;
                ABD[5,4] += l.Q_26*l.z3;
                ABD[5,5] += l.Q_66*l.z3;
                # Calculate unit thermal stress resultants
                self.Nt_x += (l.Q_11*l.cte_x+l.Q_12*l.cte_y+
                        l.Q_16*l.cte_xy)*l.t;  # [1], p. 445 
                self.Nt_y += (l.Q_12*l.cte_x+l.Q_22*l.cte_y+
                        l.Q_26*l.cte_xy)*l.t;
                self.Nt_xy += (l.Q_16*l.cte_x+l.Q_26*l.cte_y+
                        l.Q_66*l.cte_xy)*l.t;
                # denisty calculation
                self.density += l.density*l.t;
        self.ABD = ABD
        self.abd = numpy.linalg.inv(ABD)
        # FINISHME
        self.finished = True


