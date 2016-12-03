# file: parser.py
# vim:fileencoding=utf-8:ft=python
# Copyright © 2014-2016 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# Created: 2014-02-21 21:35:41 +0100
# Last modified: 2016-12-03 15:33:26 +0100
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
import re
from .types import Fiber, Resin, Lamina, Laminate

msg = logging.getLogger('parser')

_numre = r'([+-]?\d+(?:\.\d*)?(?:[eE][+-]?\d+)?)'
_spcre = r'\s+'


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
    fibers = find_components(directives, 'f:')
    msg.info("found {} fibers in '{}'".format(len(fibers), filename))
    fdict = {fiber.name: fiber for fiber in fibers}
    resins = find_components(directives, 'r:')
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
                laminates.append(Laminate(name, llist))
                state = T
                llist = None
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
                la = Lamina(fdict[fibername], matrix, weight, angle, vf)
                llist.append(la)
                continue
            if state == L and ln[0] == 's':
                llist = llist + list(reversed(llist))
                laminates.append(Laminate(name, llist))
                state = T
                llist = None
        except ValueError:
            logging.error('invalid line {} "{}" skipped'.format(num, ln))
        except KeyError:
            logging.error('line {} unknown "{}"'.format(num, ln))
    if llist:
        laminates.append(Laminate(name, llist))
    return laminates


def find_components(directives, what):
    """Finds fibers or resins.

    Arguments:
        directives: A sequence of strings containing directives.
            A directive is a line whose first non-space character is one of
            'f', 'r', 't', 'm', 'l' or 's', and whose second character is ':'.
        what: The key of the component to look for. 'f:' for fibers, 'r:' for
            resins.
    Returns:
        A list of Resin or Fiber objects.
    """
    choice = {'f:': Fiber, 'r:': Resin}
    rv = []
    names = []
    cre = _spcre.join([what, _numre, _numre, _numre, _numre, '(.*)$'])
    for num, ln in directives:
        match = re.fullmatch(cre, ln)
        if match:
            try:
                found = choice[what](*match.groups())
                if found.name in names:
                    s = "line {} is a duplicate {} '{}', will be ignored."
                    logging.warning(s.format(num, what, found.name))
                else:
                    rv.append(found)
            except ValueError as e:
                s = 'line {} is not a valid {}: {}'
                logging.error(s.format(num, type(what).__name__, e))
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
