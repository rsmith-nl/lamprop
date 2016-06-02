# file: parser.py
# vim:fileencoding=utf-8:ft=python
# Copyright © 2014-2016 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# Created: 2014-02-21 21:35:41 +0100
# Last modified: 2016-06-02 11:05:29 +0200
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
from .types import Fiber, Resin, mklamina, mklaminate

msg = logging.getLogger('parser')


def fromjson(filename):
    """Parses a lamprop JSON file.

    Arguments:
        filename: The name of the file to parse.

    Returns:
        A dict of Fibers, a dict of Resins and a dict of Laminates, keyed by
        name.
    """
    try:
        with open(filename, encoding='utf-8') as df:
            data = json.load(df)
    except IOError:
        msg.error("cannot read '{}'.".format(filename))
        return {}, {}, {}
    fdict = _find('fibers', data, Fiber, filename)
    rdict = _find('resins', data, Resin, filename)
    ldict = {}
    laminatedata = data['laminates']
    if not laminatedata:
        return fdict, rdict, ldict
    for lam in laminatedata:
        if not _chklam(lam):
            continue
        commonvf = lam['vf']
        mname = lam['matrix']
        try:
            r = rdict[mname]
        except KeyError:
            msg.error('unknown resin {}, skipping laminate'.format(mname))
            continue
        llist = []
        for la in lam['lamina']:
            fname = la['fiber']
            try:
                f = fdict[fname]
            except KeyError:
                msg.error('unknown fiber {}, skipping lamina'.format(fname))
                continue
            vf = commonvf
            if 'vf' in la:
                vf = la['vf']
            llist.append(mklamina(f, r, la['weight'], la['angle'], vf))
        if llist:
            lname = lam['name']
            ldict[lname] = mklaminate(lname, llist)
    return fdict, rdict, ldict


def _chklam(ld):
    """Verify if the ld dict has the required keys

    Arguments:
        ld: laminate dictionary

    Returns:
        True or False
    """
    for j in ('matrix', 'name', 'vf', 'lamina'):
        if j not in ld:
            msg.error('no {} in laminate, skipping'.format(j))
            return False
    return True


def _find(ident, data, totype, name):
    """Find Fibers or Resins in the data.

    Arguments:
        ident: String containing the key to look for
        data: A dictionary to look into
        totype: A type to cast the data to
        name: The name of the file from which data came.

    Returns:
        A dictionary keyed to the name of the Fiber or Resin.
    """
    err = '{} missing {}'
    m = "found {} {} in '{}'"
    found = []
    for f in data[ident]:
        try:
            found.append(totype(**f))
        except TypeError as e:
            msg.warning(err.format(ident[:-1].capitalize(),
                                   str(e).split(':')[1]))
    _rmdup(found, ident)
    msg.info(m.format(len(found), ident, name))
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
