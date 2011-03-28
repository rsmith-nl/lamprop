# -*- coding: utf-8 -*-
# HTML output routines for lamprop.
#
# Copyright © 2011 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# Time-stamp: <2011-03-28 22:37:09 rsmith>
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

import lptypes
import lpver

def out(lam, name, eng, mat):
    '''HTML main output function.'''
    print "    <!-- outer table -->"
    print "    <table cellpadding=\"10%\">"
    s = "      <caption><strong>Properties of {}</strong></caption>"
    print s.format(name)
    print "      <tbody align=\"center\">"
    print "        <tr>"
    s = "          <td  align=\"center\" colspan=\"2\">created by {} {}.</td>"
    print s.format(lpver.name, lpver.version)
    print "        </tr>"
    if eng == True:
        engprop(lam, name)
    if mat == True:
        matrices(lam, name, not eng)
    print "      </tbody>"
    print "    </table>"
    print "    <hr />"

def engprop(l, nm):
    '''Prints the engineering properties as a HTML table.'''
    print "        <!-- first row; tables -->"
    print "        <tr>"
    print "          <td>"
    print "            <table border=\"1\" frame=\"hsides\""
    print "              rules=\"groups\" cellpadding=\"5%\">"
    print "              <caption><strong>Laminate stacking</strong></caption>"
    print "              <thead align=\"right\">"
    print "                <tr>"
    print "                  <td>Layer</td><td>Weight</td>"
    print "                  <td>Angle</td><td align=\"left\">Fiber type</td>"
    print "                </tr>"
    print "                <tr>"
    print "                  <td></td><td>[gr/m&sup2;]</td><td>[&deg;]</td>"
    print "                </tr>"
    print "              </thead>"
    print "              <tbody align=\"right\">"
    for ln,la in enumerate(l.layers):
        print "                <tr>"
        s = "                  <td>{}</td><td>{:4.0f}</td><td>{:5.0f}</td>"
        print s.format(ln, la.weight, la.angle)
        s = "                  <td align=\"left\">{}</td>"
        print s.format(la.fiber.name)
        print "                </tr>"
    print "              </tbody>"
    print "            </table>"
    print "          </td>"
    print "          <td>"
    print "            <table border=\"1\" frame=\"hsides\""\
	       " rules=\"groups\" cellpadding=\"5%\">"
    print "              <caption><strong>Engineering properties"\
	       "</strong></caption>"
    print "              <thead align=\"right\">"
    print "                <tr>"
    print "                  <td>Property</td><td>Value</td>"
    print "                  <td align=\"left\">Dimension</td>"
    print "                </tr>"
    print "              </thead>"
    print "              <tbody align=\"right\">"
    print "                <tr>"
    s = "                  <td>v<sub>f</sub></td>"\
        "<td>{:4.2f}</td><td align=\"left\">-</td>"
    print s.format(l.vf)
    print "                </tr>"
    print "                <tr>"
    s = "                  <td>w<sub>f</sub></td>"\
        "<td>{:4.2f}</td><td align=\"left\">-</td>"
    print s.format(l.wf)
    print "                </tr>"
    print "                <tr>"
    s = "                  <td>thickness</td><td>{:.3g}</td>"
    print s.format(l.thickness)
    print "                  <td align=\"left\">mm</td>"
    print "                </tr>"
    print "                <tr>"
    s = "                  <td>density</td><td>{:.3g}</td>"
    print s.format(l.density)
    print "                  <td align=\"left\">gr/cm&sup3;</td>"
    print "                </tr>"
    print "                <tr>"
    s = "                  <td>weight</td><td>{:.0f}</td>"
    print s.format(l.weight+l.rc)
    print "                  <td align=\"left\">gr/m&sup2;</td>"
    print "                </tr>"
    print "                <tr>"
    s = "                  <td>resin</td><td>{:.0f}</td>"
    print s.format(l.rc)
    print "                </tr>"
    print "              </tbody>"
    print "                <tr>"
    s = "                  <td>E<sub>x</sub></td><td>{:8.0f}</td>"
    print s.format(l.Ex)
    print "                  <td align=\"left\">MPa</td>"
    print "                </tr>"
    print "                <tr>"
    s =  "                  <td>G<sub>xy</sub></td><td>{:8.0f}</td>"
    print s.format(l.Gxy)
    print "                  <td align=\"left\">MPa</td>"
    print "                </tr>"
    print "                <tr>"
    s = "                  <td>&nu;<sub>xy</sub></td><td>{:g}</td>"
    print s.format(l.Vxy)
    print "                  <td align=\"left\">-</td>"
    print "                </tr>"
    print "                <tr>"
    s = "                  <td>&nu;<sub>yx</sub></td><td>{:g}</td>"
    print s.format(l.Vyx)
    print "                  <td align=\"left\">-</td>"
    print "                </tr>"
    print "                <tr>"
    s = "                  <td>&alpha;<sub>x</sub></td><td>{:g}</td>"
    print s.format(l.cte_x)
    print "                  <td align=\"left\">K<sup>-1</sup></td>"
    print "                </tr>"
    print "                <tr>"
    s = "                  <td>&alpha;<sub>y</sub></td><td>{:g}</td>"
    print s.format(l.cte_y)
    print "                  <td align=\"left\">K<sup>-1</sup></td>"
    print "                </tr>"
    print "              </tbody>"
    print "            </table>"
    print "          </td>"
    print "        </tr>"

def matrices(l, nm, printheader):
    '''Prints the ABD and abd matrices as HTML tables.'''
    fstr = ["N<sub>x</sub>", "N<sub>y</sub>", "N<sub>xy</sub>",
            "M<sub>x</sub>", "M<sub>y</sub>", "M<sub>xy</sub>"]
    dstr = ["&epsilon;<sub>x</sub>", "&epsilon;<sub>y</sub>",
            "&gamma;<sub>xy</sub>", "&kappa;<sub>x</sub>",
            "&kappa;<sub>y</sub>", "&kappa;<sub>xy</sub>"]
    print "        <tr>"
    print "          <!-- second row, stiffness matrix -->"
    print "          <td colspan=\"2\">"
    print "            <table border=\"1\" frame=\"vsides\" "\
	       "rules=\"groups\" cellpadding=\"5%%\">"
    print "              <caption><strong>Stiffness matrix</strong>"\
	       "</caption>"
    print "              <colgroup span=\"1\"></colgroup>"
    print "              <colgroup span=\"1\"></colgroup>"
    print "              <colgroup span=\"6\"></colgroup>"
    print "              <colgroup span=\"1\"></colgroup>"
    print "              <colgroup span=\"1\"></colgroup>"
    print "              <tbody align=\"center\">"
    print "                <tr>"
    print "                  <td>{}</td>".format(fstr[0])
    print "                  <td rowspan=\"6\">=</td>"
    s = "                  <td>{:6.0f}</td><td>{:6.0f}</td><td>{:6.0f}</td>"
    print s.format(l.ABD[0,0], l.ABD[0,1], l.ABD[0,2])
    s = "                  <td>{:6.0f}</td><td>{:6.0f}</td><td>{:6.0f}</td>"
    print s.format(l.ABD[0,3], l.ABD[0,4], l.ABD[0,5])
    print "                  <td rowspan=\"6\">&times;</td>"
    print "                  <td>{}</td>".format(dstr[0])
    print "                </tr>"
    for n in range(1,6):
        print "                <tr>"
        print "                  <td>{}</td>".format(fstr[n])
        s = "                  <td>{:6.0f}</td><td>{:6.0f}</td><td>{:6.0f}</td>"
        print s.format(l.ABD[n,0], l.ABD[n,1], l.ABD[n,2])
        s = "                  <td>{:6.0f}</td><td>{:6.0f}</td><td>{:6.0f}</td>"
        print s.format(l.ABD[n,3], l.ABD[n,4], l.ABD[n,5])
        print "                  <td>{}</td>".format(dstr[n])
        print "                </tr>"
    print "              </tbody>"
    print "            </table>"
    print "          </td>"
    print "        </tr>"
    print "        <tr>"
    print "          <!-- third row, compliance matrix -->"
    print "          <td colspan=\"2\">"
    print "            <table border=\"1\" frame=\"vsides\" "\
	       "rules=\"groups\" cellpadding=\"5%\">"
    print "              <caption><strong>Compliance matrix</strong>"\
	       "</caption>"
    print "              <colgroup span=\"1\"></colgroup>"
    print "              <colgroup span=\"1\"></colgroup>"
    print "              <colgroup span=\"6\"></colgroup>"
    print "              <colgroup span=\"1\"></colgroup>"
    print "              <colgroup span=\"1\"></colgroup>"
    print "              <tbody align=\"center\">"
    print "                <tr>"
    print "                  <td>{}</td>".format(fstr[0])
    print "                  <td rowspan=\"6\">=</td>"
    s = "                  <td>{:6.3g}</td><td>{:6.3g}</td><td>{:6.3g}</td>"
    print s.format(l.abd[0,0]*1e6, l.abd[0,1]*1e6, l.abd[0,2]*1e6)
    s = "                  <td>{:6.3g}</td><td>{:6.3g}</td><td>{:6.3g}</td>"
    print s.format(l.abd[0,3]*1e6, l.abd[0,4]*1e6, l.abd[0,5]*1e6)
    print "                  <td rowspan=\"6\">&times;10"\
        "<sup>-6</sup>&times;</td>"
    print "                </tr>"
    for n in range(1,6):
        print "                <tr>"
        print "                  <td>{}</td>".format(dstr[n])
        s = "                  <td>{:6.0f}</td><td>{:6.0f}</td><td>{:6.0f}</td>"
        print s.format(l.abd[n,0]*1e6, l.abd[n,1]*1e6, l.abd[n,2]*1e6)
        s = "                  <td>{:6.0f}</td><td>{:6.0f}</td><td>{:6.0f}</td>"
        print s.format(l.abd[n,3]*1e6, l.abd[n,4]*1e6, l.abd[n,5]*1e6)
        print "                  <td>{}</td>".format(fstr[n])
        print "                </tr>"
    print "              </tbody>"
    print "            </table>"
    print "          </td>"
    print "        </tr>"

