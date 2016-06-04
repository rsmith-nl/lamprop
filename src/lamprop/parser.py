# file: parser.py
# vim:fileencoding=utf-8:ft=python
# Copyright © 2014-2016 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# Created: 2014-02-21 21:35:41 +0100
# Last modified: 2016-06-04 08:14:02 +0200
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

from collections import OrderedDict
import json
import logging
import re
from .types import mkfiber, mkresin, mklamina, mklaminate

msg = logging.getLogger('parser')


def fromjson(text, filename):
    """Parses a lamprop JSON file.

    Arguments:
        text: Text to parse.
        filename: Origin of the text.

    Returns:
        A dict of Fibers, a dict of Resins and a dict of Laminates, keyed by
        name.
    """
    data = _stripcomments(text, filename)
    fdict = _find('fibers', data, mkfiber, filename)
    rdict = _find('resins', data, mkresin, filename)
    ldict = OrderedDict()
    laminatedata = data['laminates']
    if not laminatedata:
        return fdict, rdict, ldict
    for lam in laminatedata:
        try:
            commonvf = lam['vf']
            mname = lam['matrix']
            r = rdict[mname]
            llist = []
            for la in lam['lamina']:
                fname = la['fiber']
                f = fdict[fname]
                vf = commonvf
                if 'vf' in la:
                    vf = la['vf']
                llist.append(mklamina(f, r, la['weight'], la['angle'], vf))
            if llist:
                if 'symmetric' in lam and lam['symmetric']:
                    llist = llist + list(reversed(llist))
                lname = lam['name']
                ldict[lname] = mklaminate(lname, llist)
        except KeyError as ke:
            msg.warning('{} not found, skipping laminate'.format(ke))
        except ValueError as ve:
            msg.warning(ve)
    return fdict, rdict, ldict


def _stripcomments(data, filename):
    """Read a JSON file, stripping out the '//' comments before parsing.

    Arguments:
        data: Contents of the file.
        filename: Name of the file.

    Returns:
        Dictionary containing the data
    """
    clean = re.sub('//.*$|/\*[^\*]*\*/', '\n', data, flags=re.MULTILINE)
    try:
        return json.loads(clean, object_pairs_hook=OrderedDict)
    except json.JSONDecodeError:
        msg.error("invalid json file '{}'.".format(filename))
        return {}


def _find(ident, data, totype, name):
    """Find Fibers or Resins in the data.

    Arguments:
        ident: String containing the key to look for
        data: A dictionary to look into
        totype: A function to create a type
        name: The name of the file from which data came.

    Returns:
        A dictionary keyed to the name of the Fiber or Resin.
    """
    m = "found {} {} in '{}'"
    found = OrderedDict()
    for f in data[ident]:
        try:
            v = totype(**f)
            if v.name not in found:
                found[v.name] = v
        except TypeError as te:
            miss = str(te).split(':')[1][1:]
            msg.warning('{} missing {}'.format(ident[:-1], miss))
        except ValueError as ve:
            msg.warning('in {}; {}'.format(ident[:-1], ve))
    msg.info(m.format(len(found), ident, name))
    return found
