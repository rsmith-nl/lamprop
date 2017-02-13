# file: parser.py
# vim:fileencoding=utf-8:ft=python
# Copyright © 2014-2016 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# Created: 2014-02-21 21:35:41 +0100
# Last modified: 2017-02-13 23:55:35 +0100
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

"""Parser for lamprop files"""

import logging
from .types import Fiber, Resin, Lamina, Laminate

msg = logging.getLogger('parser')


def parse(filename):
    """Parses a lamprop file.

    Arguments:
        filename: The name of the file to parse.

    Returns:
        A list of laminates.
    """
    try:
        rd, fd, ld = _directives(filename)
    except IOError:
        msg.error("cannot read '{}'.".format(filename))
    return []
    fibers = _f(fd)
    msg.info("found {} fibers in '{}'".format(len(fibers), filename))
    fdict = {fiber.name: fiber for fiber in fibers}
    resins = _r(rd)
    msg.info("found {} resins in '{}'".format(len(resins), filename))
    rdict = {resin.name: resin for resin in resins}
    boundaries = [j for j in range(len(ld)) if ld[j][1][0] == 't'] + [len(ld)]
    bpairs = [(a, b) for a, b in zip(boundaries[:-1], boundaries[1:])]
    laminates = []
    for a, b in bpairs:
        current = ld[a:b]
        lam = _laminate(current, rdict, fdict)
        if lam:
            laminates.append(lam)
    msg.info("found {} laminates in '{}'".format(len(laminates), filename))
    return laminates


def _directives(filename):
    """
    Read the directives from a lamprop file.

    Arguments:
        filename: The name of the file to parse.

    Returns:
        A 3-tuple (resin directives, fiber directives, laminate directives)
    """
    with open(filename, encoding='utf-8') as df:
        data = [ln.strip() for ln in df]
    # Filter out lines with directives.
    directives = [(num, ln) for num, ln in enumerate(data, start=1)
                  if len(ln) > 1 and ln[1] is ':' and ln[0] in 'tmlsfr']
    msg.info("found {} directives in '{}'".format(len(directives), filename))
    rd = [(num, ln) for num, ln in directives if ln[0] == 'r']
    fd = [(num, ln) for num, ln in directives if ln[0] == 'f']
    ld = [(num, ln) for num, ln in directives if ln[0] in 'tmls']
    return rd, fd, ld


def _laminate(ld, resins, fibers):
    sym = False
    if ld[0][1].startswith('t'):
        lname = ld[0][1][2:].strip()
    else:
        msg.error("No 't' directive on line {}".format(ld[0][0]))
        return None
    try:
        if not ld[1][1].startswith('m'):
            raise ValueError
        common_vf, rname = ld[1][1][2:].split(maxsplit=1)
        common_vf = float(common_vf)
        if rname not in resins:
            msg.error("Unknown resin '{}' on line {}".format(rname, ld[1][0]))
            raise ValueError
    except ValueError:
        msg.error("No valid 'm' directive on line {}".format(ld[1][0]))
        return None
    if ld[-1][1].startswith('s'):
        sym = True
        del(ld[-1])
    llist = []
    for num, ln in ld[2:]:
        items = ln.split(maxsplit=2)
        try:
            weight, angle = float(items[0]), float(items[1])
        except ValueError:
            fs = "Cannot find fiber weight or angle on line {}"
            msg.error(fs.format(num))
            continue
        try:
            foo = items[2].split(maxsplit=1)
            vf = float(foo[0])
            fname = foo[1]
        except ValueError:
            fname = items[2]
            vf = common_vf
        if fname not in fibers:
            fs = "Unknown fiber '{}' on line {}"
            msg.error(fs.format(fname, num))
            continue
        llist.append(Lamina(fibers[fname], resins[rname], weight, angle, vf))
    if sym:
        llist = llist + list(reversed(llist))
    return Laminate(lname, llist)


def _num(val):
    """Test if a string is a floating point number

    Arguments:
        val: The string to test.

    Returns:
        True if val is floating point a number, False otherwise.
    """
    try:
        float(val)
    except ValueError:
        return False
    return True


def _f(lines):
    """Parse fiber lines.

    Arguments:
        lines: A sequence of (number, line) tuples describing fibers.

    Returns:
        A list of types.Fiber
    """
    rv = []
    names = []
    for num, ln in lines:
        test = ln.split()
        try:
            if _num(test[5]):  # old format
                msg.info("old style fiber on line {}".format(num))
                items = ln.split(None, 8)
                indices = [1, 3, 5, 7, 8]
            else:
                items = ln.split(None, 5)
                indices = [1, 2, 3, 4, 5]
            E1, nu12, a1, rho = [float(items[j]) for j in indices[:4]]
            if E1 <= 0:
                raise ValueError('E1 must be >0')
            if rho <= 0:
                raise ValueError('fiber density must be >0')
            name = items[indices[4]]
        except (ValueError, IndexError) as e:
            msg.error('parsing a fiber on line {}; {}.'.format(num, e))
            continue
        if name not in names:
            rv.append(Fiber(E1, nu12, a1, rho, name))
            names.append(name)
        else:
            s = "fiber '{}' at line {} is a duplicate, will be ignored."
            msg.warning(s.format(name, num))
    return rv


def _r(lines):
    """Parse resin lines.

    Arguments:
        lines: A sequence of (line, number) tuples.

    Returns:
        A list of types.Resin
    """
    rl = [(num, ln) for num, ln in lines if ln[0] is 'r']
    rv = []
    names = []
    for num, ln in rl:
        items = ln.split(None, 5)
        try:
            E, nu, a, rho = [float(j) for j in items[1:5]]
            if E <= 0:
                raise ValueError('E must be >0')
            if nu <= -1 or nu >= 0.5:
                raise ValueError('resin Poisson constant <-1 or >0.5')
            if rho <= 0:
                raise ValueError('resin density must be >0')
            name = items[5]
        except ValueError as e:
            msg.error('parsing a resin on line {}; {}.'.format(num, e))
            continue
        if name not in names:
            rv.append(Resin(E, nu, a, rho, name))
            names.append(name)
        else:
            s = "resin '{}' at line {} is a duplicate, will be ignored."
            msg.warning(s.format(name, num))
    return rv


def _l(line, number, resin, vf):
    """Parse a lamina line;

    l: <weight> <angle> [<vf>] <fiber name>

    Arguments:
        line: String to parse.
        number: Line number in the original file.
        resin: The resin type to use.
        vf: Global fiber volume fraction.
        log: A Logger instance to report failures.

    Returns:
        A tuple to initialize a Lamina.
    """
    items = line.split(None, 4)
    try:
        vf = float(items[3])
    except ValueError:
        if vf is None:
            s = 'no vf in laminate line {}, and no global vf.'
            s = s.format(line)
            msg.error(s)
            raise ValueError(s)
        items = line.split(None, 3)
    values = [items[-1], resin]
    values += [float(j) for j in items[1:3]]
    values.append(vf)
    return values
