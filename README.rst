=====================================================
Calculating elastic properties of composite laminates
=====================================================

The purpose of this program is to calculate some properties of
fiber-reinforced composite laminates. It calculates
- engineering properties like Ex, Ey, Gxy
- thermal properties CTE_x and CTE_y
- physical properties like density and laminate thickness
- stiffness and compliance matrices (ABD and abd)

Although these properties are not very difficult to calculate, (the relevant
equations and formulas can be readily found in the available composite
literature) the calculation is time-consuming and error-prone when done by
hand.

This program can _not_ calculate the strength of composite laminates;
because there are many different failure modes, strengths of composite
laminates cannot readily be calculated from the strengths of the separate
materials that form the laminate. These strengths have to be determined
from tests.

The program has options for producing LaTeX and HTML output in addition to
plain text output.

The program and its file format are documented by two manuals; lamprop.1 and
lamprop.5 respectively. If you install this program on UNIX-like systems with
'make install', these will be installed automatically. For users of other
systems, PDF versions are included in the distribution.


Requirements
------------

This program requires Python (version 3), and the numpy module (version 1.5 or
later). This version was developed and tested using Python 3.4.


Installation
------------

On UNIX-like platforms, run `make install` as root. This will install
the lamprop script itself in /usr/local/bin, and the manual pages in
/usr/local/man/man1 and /usr/local/man/man5. You can change these paths
by editing the Makefile and changing the definitions of PREFIX, MANDIR and
BINDIR.

On windows, copy the ‘lamprop’ script to a directory in your PATH (e.g.
the ‘Scripts’ subdirectory of your Python install) and rename it to
‘lamprop.py’.
