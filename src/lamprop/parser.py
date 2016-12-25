# file: parser.py
# vim:fileencoding=utf-8:ft=python
# Copyright © 2014-2016 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# Created: 2014-02-21 21:35:41 +0100
# Last modified: 2016-12-13 23:09:22 +0100
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
_numspcre = r'(?:([+-]?\d+(?:\.\d*)?(?:[eE][+-]?\d+)?\s+))'
_spcre = r'\s+'
_namere = r'(.*?)\s*$'


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
    fibers = _components(directives, 'f:')
    msg.info("found {} fibers in '{}'".format(len(fibers), filename))
    fdict = {fiber.name: fiber for fiber in fibers}
    resins = _components(directives, 'r:')
    msg.info("found {} resins in '{}'".format(len(resins), filename))
    rdict = {resin.name: resin for resin in resins}
    laminates = _laminates(directives, rdict, fdict)
    return laminates


def _components(directives, what):
    """Finds fibers or resins.

    Arguments:
        directives: A sequence of 2-tuples (int, string) containing a line
            number and a directive. A directive is a line whose first non-space
            character is one of 'f', 'r', 't', 'm', 'l' or 's', and whose
            second character is ':'.
        what: The key of the component to look for. 'f:' for fibers, 'r:' for
            resins.
    Returns:
        A list of Resin or Fiber objects.
    """
    choice = {'f:': Fiber, 'r:': Resin}
    rv = []
    names = []
    cre = ''.join([what, _spcre, _numspcre + r'{4}', _namere])
    for num, ln in (d for d in directives if d[1].startswith(what)):
        name = re.findall(_namere, ln)[0]
        numbers = re.findall(_numre, ln)[:4]

        match = re.fullmatch(cre, ln)
        if match:
            print('groups:', match.groups())
            try:
                found = choice[what](*match.groups())
                if found.name in names:
                    s = "line {} is a duplicate {} '{}', will be ignored."
                    msg.warning(s.format(num, what, found.name))
                else:
                    rv.append(found)
            except (ValueError, TypeError) as e:
                s = 'line {} is not a valid {}: {}'
                msg.error(s.format(num, type(choice[what]).__name__, e))
    return rv


def _laminates(directives, resin_dict, fiber_dict):
    laminate_directives = [(num, ln) for (num, ln) in directives if ln[0]
                           in 'tmls']
    laminate_keystring = ''.join(d[1][0] for d in laminate_directives)
    laminates = []
    for match in re.finditer('tml+s?', laminate_keystring):
        layers = []
        start, end = match.start(), match.end()
        try:
            laminate_name, global_vf, resin = \
                _parameters(laminate_directives, start, resin_dict)
        except ValueError as e:
            msg.warning(e)
            continue
        lastline = laminate_directives[end-1][1]
        if lastline.startswith('s'):
            end -= 1
        for k in range(start+2, end):
            try:
                layers.append(_lamina(laminate_directives[k][0],
                                      laminate_directives[k][1],
                                      global_vf, fiber_dict, resin))
            except ValueError as e:
                msg.warning(e)
        if lastline.startswith('s'):
            layers + list(reversed(layers))
    else:  # complete laminate
        if layers:
            laminates.append(Laminate(laminate_name, layers))
    return laminates


def _parameters(directives, start, resin_dict):
    s = 'illegal "{}" directive on line {}'
    # tre = r't:' + _spcre + _namere
    mre = _spcre.join([r'm:', _numre, _namere])
    try:
        laminate_name = directives[start][1].split(maxsplit=1)[1]
    except IndexError:
        raise ValueError(s.format('m:', directives[start][0]))
    try:
        global_vf, resin_name = \
            re.findall(mre, directives[start+1][1])[0]
    except (ValueError, IndexError):
        raise ValueError(s.format('t:', directives[start][0]))
    if resin_name not in resin_dict.keys():
        s = 'skipping laminate with unknown resin "{}" on line {}'
        raise ValueError(s.format(resin_name, directives[start][0]))
    return laminate_name, global_vf, resin_dict[resin_name]


def _lamina(num, line, vf, fiber_dict, resin):
    numbers = re.findall(_numre, line)
    if len(numbers) == 2:
        numbers = (numbers[0], numbers[1], vf)
    elif len(numbers) == 3:
        pass
    else:
        s = 'illegal "{}" directive on line {}'
        msg.warning(s.format('l:', num))
    fiber_name = re.findall(_namere, line)
    if fiber_name not in fiber_dict.keys():
        s = 'skipping lamina with unknown fiber "{}" on line {}'
        raise ValueError(s.format(fiber_name, line))
    numbers = [float(f) for f in numbers]
    return Lamina(fiber_dict[fiber_name], resin, *numbers)
