# file: parser.py
# vim:fileencoding=utf-8:ft=python
# Copyright © 2014-2016 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# Created: 2014-02-21 21:35:41 +0100
# Last modified: 2016-06-07 22:19:24 +0200
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
from .types import Fiber, Resin, lamina, laminate

msg = logging.getLogger('parser')


def parse(filename):
    """Parses a lamprop file.

    Arguments:
        filename: The name of the file to parse.

    Returns:
        A list of laminates.
    """
    try:
        with open(filename, encoding='utf-8') as df:
            data = [ln.strip() for ln in df]
    except IOError:
        msg.error("cannot read '{}'.".format(filename))
        return []
    # Filter out lines with directives.
    directives = [(num, ln) for num, ln in enumerate(data, start=1)
                  if len(ln) > 1 and ln[1] is ':' and ln[0] in 'tmlsfr']
    msg.info("found {} directives in '{}'".format(len(directives), filename))
    fibers = [_f(ln, num) for num, ln in directives if ln[0] is 'f']
    _rmdup(fibers, 'fibers')
    msg.info("found {} fibers in '{}'".format(len(fibers), filename))
    fdict = {fiber.name: fiber for fiber in fibers}
    resins = [_r(ln, num) for num, ln in directives if ln[0] is 'r']
    _rmdup(resins, 'resins')
    msg.info("found {} resins in '{}'".format(len(resins), filename))
    rdict = {resin.name: resin for resin in resins}
    directives = [(num, ln) for num, ln in directives if ln[0] in 'tmls']
    T, M, L = 1, 2, 3
    state = T
    name, vf, matrix, llist = None, None, None, []
    laminates = []
    for num, ln in directives:
        try:
            if state == L and ln[0] == 't':
                laminates.append(laminate(name, llist))
                state = T
                # no continue!
            if state == T and ln[0] == 't':
                vf, matrix = None, None
                name = ln.split(maxsplit=1)[1]
                state = M
                continue
            if state == M and ln[0] == 'm':
                _, vf, rname = ln.split(maxsplit=2)
                vf = float(vf)
                matrix = rdict[rname]
                llist = []
                state = L
                continue
            if state == L and ln[0] == 'l':
                _, weight, angle, *rest = ln.split(maxsplit=4)
                weight, angle = float(weight), float(angle)
                try:
                    vf = float(rest[0])
                    del rest[0]
                except ValueError:
                    pass
                fibername = ' '.join(rest)
                la = lamina(fdict[fibername], matrix, weight, angle, vf)
                llist.append(la)
                continue
            if state == L and ln[0] == 's':
                llist = llist + list(reversed(llist))
                laminates.append(laminate(name, llist))
                state = T
        except ValueError:
            logging.error('invalid line {} "{}" skipped'.format(num, ln))
        except KeyError:
            logging.error('line {} unknown "{}"'.format(num, ln))
    if len(llist):
        laminates.append(laminate(name, llist))
    return laminates


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


def _f(line, number):
    """Parse a line describing a fiber.

    f: <E1> <Poisson's ratio 1,2> <CTE1> <density> <name>

    Arguments:
        line: Text line to parse.
        number: Line number in the original file.
        log: Logger instance.

    Returns: A lptypes.Fiber object.
    """
    test = line.split()
    try:
        if _num(test[5]):  # old format
            msg.info("old style fiber on line {}".format(number))
            items = line.split(None, 8)
            indices = [1, 3, 5, 7, 8]
        else:
            items = line.split(None, 5)
            indices = [1, 2, 3, 4, 5]
        values = [float(items[j]) for j in indices[:4]]
        values.append(items[indices[4]])
        values.append(number)
    except (ValueError, IndexError) as e:
        msg.error('parsing a fiber on line {}; {}.'.format(number, e))
        return None
    return Fiber(*values)


def _r(line, number):
    """Parse a line describing a resin.

    r: <Ematrix> <Poisson's ratio> <CTE> <density> <name>

    Arguments:
        line: String to parse.
        number: Line number in the original file.
        log: Logger instance.

    Returns:
        A types.Resin object.
    """
    items = line.split(None, 5)
    try:
        values = [float(j) for j in items[1:5]]
        values.append(items[5])
        values.append(number)
    except ValueError as e:
        msg.error('parsing a resin on line {}; {}.'.format(number, e))
        return None
    return Resin(*values)


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


def _rmdup(lst, name):
    """Remove duplicate or empty Fibers or Resins from the supplied list.

    Arguments:
        lst: List to search through and modify.
        name: Name of the thing we're searching for.
    """
    names = []
    for n, i in enumerate(lst):
        if i is None:
            del(lst[n])
            continue
        if i.name not in names:
            names.append(i.name)
        else:
            s = "{} '{}' at line {} is a duplicate, will be ignored."
            mag.warning(s.format(name, i.name, i.line))
            del(lst[n])
