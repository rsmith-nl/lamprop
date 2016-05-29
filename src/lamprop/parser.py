# file: parser.py
# vim:fileencoding=utf-8:ft=python
# Copyright © 2014-2016 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# Created: 2014-02-21 21:35:41 +0100
# Last modified: 2016-05-29 20:21:32 +0200
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

"""Parser for lamprop files in JSON format"""

import json
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
            data = json.load(df)
    except IOError:
        msg.error("cannot read '{}'.".format(filename))
        return [], [], []
    fdict = _find('fibers', data, Fiber, filename)
    rdict = _find('resins', data, Resin, filename)
    ldict = {}
    laminatedata = data['laminates']
    if not laminatedata:
        return fdict, rdict, ldict
#    directives = [(num, ln) for num, ln in directives if ln[0] in 'tmls']
#    tindices = [i for i, (_, ln) in enumerate(directives) if ln[0] is 't']
#    if not tindices:
#        msg.error("no laminates found in '{}'".format(filename))
#        return []
#    else:
#        msg.info("found {} laminates in '{}'".format(len(tindices), filename))
#    tindices.append(len(directives))
#    pairs = zip(tindices, tindices[1:])
#    laminatedata = [directives[start:stop] for start, stop in pairs]
#    laminates = []
#    lamnames = []
#    for lam in laminatedata:
#        symmetric = False
#        numt, t = lam[0]
#        numm, m = lam[1]
#        name = t[2:].strip()
#        if name in lamnames:
#            s = "laminate '{}' on line {} already exists. Skipping laminate."
#            msg.warning(s.format(name, numt))
#            continue
#        lamnames.append(name)
#        if m[0] is not 'm':
#            s = "no 'm:' on line {}. Skipping laminate."
#            msg.warning(s.format(numt+1))
#            continue
#        items = m.split(None, 2)
#        try:
#            vf = float(items[1])
#            mname = items[2]
#        except ValueError:
#            vf = None
#            mname = items[1]
#        try:
#            resin = rdict[mname]
#        except KeyError:
#            s = "unknown resin '{}' on line {}. Skipping laminate."
#            msg.error(s.format(mname, numm))
#            continue
#        layers = []
#        if lam[-1][1].startswith('s'):
#            symmetric = True
#            msg.info("found symmetry directive in '{}'.".format(name))
#            del lam[-1]
#        try:
#            for numl, l in lam[2:]:
#                if l[0] is not 'l':
#                    s = "unexpected '{}:' on line {}. Skipping laminate."
#                    raise ValueError(s.format(l[0], numl))
#                else:
#                    values = _l(l, numl, resin, vf, msg)
#                try:
#                    fiber = fdict[values[0]]
#                    values[0] = fiber
#                except KeyError:
#                    s = "unknown fiber '{}' on line {}. Skipping laminate."
#                    raise ValueError(s.format(values[0], numl))
#                    continue
#                layers.append(lamina(*values))
#        except ValueError as e:
#            msg.error(e)
#            continue
#        if not layers:
#            msg.warning("empty laminate '{}'. Skipping".format(name))
#            continue
#        if symmetric:
#            extra = layers.copy()
#            extra.reverse()
#            layers += extra
#        laminates.append(laminate(name, layers))
#    return laminates


def _find(ident, data, totype, name):
    """Find Fibers or Resins in the data.
    Returns a dictionary keyed to the name of the Fiber or Resin.
    """
    err = '{} missing {}'
    m = "found {} {} in '{}'"
    found = []
    for f in data[ident]:
        try:
            found.append(totype(**f))
        except TypeError as e:
            msg.warning(err.fmt(ident[:-1].capitalize(), str(e).split(':')[1]))
    _rmdup(found, ident)
    msg.info(m.format(len(found), name))
    return {j.name: j for j in found}


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
            msg.warning(s.format(name, i.name, i.line))
            del(lst[n])
