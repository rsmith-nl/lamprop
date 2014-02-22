# vim:fileencoding=utf-8
#
# Copyright © 2014 R.F. Smith. All rights reserved.
# Created: 2014-02-21 21:35:41 +0100
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

"""Parser for lamprop files"""

from __future__ import print_function, division
from lamprop.types import Fiber, Resin

__version__ = '$Revision$'[11:-2]


def parse(filename):
    """Parse a lamprop file

    :param filename: name of the file to parse
    :returns: @todo
    """
    with open(filename, 'r') as df:
        data = df.readlines()
    ds = 'DEBUG: {} contains {} {}'
    print(ds.format(filename, len(data), 'lines'))
    directives = [(num, ln.rstrip()) for num, ln in enumerate(data)
                  if len(ln) > 1 and ln[1] is ':']
    print(ds.format(filename, len(directives), 'directives'))
    fibers = [_f(ln, num) for num, ln in directives if ln[0] is 'f']
    print(ds.format(filename, len(fibers), 'fiber definitions'))
    resins = [_r(ln, num) for num, ln in directives if ln[0] is 'r']
    print(ds.format(filename, len(resins), 'resin definitions'))
    directives = [(num, ln) for num, ln in directives if ln[0] in 'tml']
    laminatelines = [dnum for dnum, (num, ln) in enumerate(directives)
                     if ln[0] is 't']
    print(ds.format(filename, len(laminatelines), 'laminate definitions'))
    print(laminatelines)


def _num(val):
    """Test if a value is a number

    :param val: string to test.
    :returns: True val is a number, false otherwise.
    """
    try:
        float(val)
    except ValueError:
        return False
    return True


def _f(line, number):
    """Parse a line describing a fiber.

    :param line: text line to parse
    :param number: line number in the original file.
    :returns: a types.Fiber
    """
    test = line.split()
    if _num(test[5]):  # old format
        print('DEBUG: old fiber format')
        items = line.split(None, 8)
        indices = [1, 3, 5, 7, 8]
    else:
        print('DEBUG: new fiber format')
        items = line.split(None, 5)
        indices = [1, 2, 3, 4, 5]
    try:
        values = [float(items[j]) for j in indices[:4]]
        values.append(items[indices[4]])
        values.append(number)
    except ValueError as e:
        print('ERROR on line {}: ', number, e)
        return None
    print('DEBUG: fiber', values)
    return Fiber(*values)


def _r(line, number):
    """Parse a line describing a resin.

    :param line: string to parse
    :param number: line number in the original file.
    :returns: a types.Resin
    """
    items = line.split(None, 5)
    try:
        values = [float(j) for j in items[1:5]]
        values.append(items[5])
        values.append(number)
    except ValueError as e:
        print('ERROR on line {}:', number, e)
        return None
    print('DEBUG: resin', values)
    return Resin(*values)
