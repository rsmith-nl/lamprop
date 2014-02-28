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
from lamprop.types import Fiber, Resin, Lamina, Laminate
from lamprop.utils import warn, error

__version__ = '$Revision$'[11:-2]


def parse(filename):
    """Parse a lamprop file

    :param filename: name of the file to parse
    :returns: a list of laminates
    """
    try:
        with open(filename, 'r') as df:
            data = df.readlines()
    except IOError:
        error("cannot read '{}'.".format(filename))
        return []
    data = [ln.strip() for ln in data]
    directives = [(num, ln) for num, ln in enumerate(data)
                  if len(ln) > 2 and ln[1] is ':']
    fibers = [_f(ln, num) for num, ln in directives if ln[0] is 'f']
    fdict = {fiber.name: fiber for fiber in fibers}
    _rmdup(fibers, 'fibers')
    resins = [_r(ln, num) for num, ln in directives if ln[0] is 'r']
    rdict = {resin.name: resin for resin in resins}
    _rmdup(resins, 'resins')
    directives = [(num, ln) for num, ln in directives if ln[0] in 'tml']
    tindices = [i for i, (_, ln) in enumerate(directives) if ln[0] is 't']
    if not tindices:
        error("no laminates found in '{}'".format(filename))
        return []
    tindices.append(len(directives))
    pairs = zip(tindices, tindices[1:])
    laminatedata = [directives[start:stop] for start, stop in pairs]
    laminates = []
    lamnames = []
    for lam in laminatedata:
        numt, t = lam[0]
        numm, m = lam[1]
        name = t[2:].strip()
        if name in lamnames:
            s = "laminate '{}' on line {} already exists. Skipping laminate."
            error(s.format(name, numt))
            continue
        lamnames.append(name)
        if m[0] is not 'm':
            error("no 'm:'-line after 't:'. Skipping laminate.")
            continue
        items = m.split(None, 2)
        try:
            vf = float(items[1])
            mname = items[2]
        except ValueError:
            vf = None
            mname = items[1]
        try:
            resin = rdict[mname]
        except KeyError:
            s = "unknown resin '{}' on line {}. Skipping laminate."
            error(s.format(mname, numm))
            continue
        layers = []
        for numl, l in lam[2:]:
            if l[0] is not 'l':
                s = "unexpected '{}:' on line {}. Skipping line."
                warn(s.format(l[0], numl))
                continue
            else:
                values = _l(l, numl, resin, vf)
            try:
                fiber = fdict[values[0]]
                values[0] = fiber
            except KeyError:
                s = "unknown fiber '{}' on line {}. Skipping line."
                error(s.format(values[0], numl))
                continue
            layers.append(Lamina(*values))
        if not layers:
            error('empty laminate. Skipping')
            continue
        laminates.append(Laminate(name, layers))
    return laminates


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

    f: <E1> <Poisson's ratio 1,2> <CTE1> <density> <name>

    :param line: text line to parse
    :param number: line number in the original file.
    :returns: a types.Fiber
    """
    test = line.split()
    if _num(test[5]):  # old format
        items = line.split(None, 8)
        indices = [1, 3, 5, 7, 8]
    else:
        items = line.split(None, 5)
        indices = [1, 2, 3, 4, 5]
    try:
        values = [float(items[j]) for j in indices[:4]]
        values.append(items[indices[4]])
        values.append(number)
    except ValueError as e:
        print('ERROR on line {}: ', number, e)
        return None
    return Fiber(*values)


def _r(line, number):
    """Parse a line describing a resin.

    r: <Ematrix> <Poisson's ratio> <CTE> <density> <name>

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
    return Resin(*values)


def _l(line, number, resin, vf):
    """Parse a lamina line;

    l: <weight> <angle> [<vf>] <fiber name>

    :param line: string to parse
    :param number: line number in the original file.
    :param resin: the resin type to use
    :param vf: global fiber volume fraction
    :returns: a tuple to initialize a Lamina
    """
    items = line.split(None, 4)
    try:
        vf = float(items[3])
    except ValueError:
        if vf is None:
            s = 'No vf in laminate line {}, and no global vf.'
            raise ValueError(s.format(line))
        items = line.split(None, 3)
    values = [items[-1], resin]
    values += [float(j) for j in items[1:3]]
    values.append(vf)
    return values


def _rmdup(lst, name):
    """Remove duplicate Fibers, Resins or Laminates.

    :param lst: List to search through.
    :param name: Name of the thing we're searching for
    :returns: @todo
    """
    names = []
    for n, i in enumerate(lst):
        if i.name not in names:
            names.append(i.name)
        else:
            s = "{} '{}' at line {} is a duplicate, will be ignored."
            warn(s.format(name, i.name, i.line))
            del(lst[n])
