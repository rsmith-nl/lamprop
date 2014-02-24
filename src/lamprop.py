#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# lamprop - main program.
# $Date$

from __future__ import print_function, division

__version__ = '$Revision$'[11:-2]

_lic = '''lamprop {}
Copyright © 2011-2014 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY AUTHOR AND CONTRIBUTORS ``AS IS'' AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED.  IN NO EVENT SHALL AUTHOR OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
SUCH DAMAGE.'''.format(__version__)

import argparse
import sys
from lamprop.parser import parse
import lamprop.text as text
import lamprop.latex as latex
import lamprop.html as html


class LicenseAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print(_lic)
        sys.exit()

desc = ('Calculate the elastic properties of a fibrous composite laminate.'
        ' See lamprop(1) for the manual of this program and lamprop(5) '
        'for the manual of the data file format.')

# Process the command-line arguments
opts = argparse.ArgumentParser(prog='lamprop', description=desc)
group = opts.add_mutually_exclusive_group()
group.add_argument('-l', '--latex', action='store_true', help="LaTeX output")
group.add_argument('-H', '--html', action='store_true', help="HTML output")
opts.add_argument('-e', '--eng', action='store_true',
                  help="produce only the layers and engineering properties")
opts.add_argument('-m', '--mat', action='store_true',
                  help="produce only the ABD and abd matrices")
group = opts.add_mutually_exclusive_group()
group.add_argument('-L', '--license', action=LicenseAction, nargs=0,
                   help="print the license")
group.add_argument('-v', '--version', action='version',
                   version=__version__)
opts.add_argument("files", metavar='file', nargs='*',
                  help="one or more files to process")
args = opts.parse_args()
del opts, group
if args.mat is False and args.eng is False:
    args.eng = True
    args.mat = True
elif args.mat and args.eng:
    pass
elif args.eng:
    args.mat = False
else:
    args.eng = False

# No files given to process.
if len(args.files) == 0:
    sys.exit(1)

# Set the output method.
out = text.out
if args.latex:
    out = latex.out
elif args.html:
    out = html.out
for f in args.files:
    # Process the files.
    laminates = parse(f)
    for curlam in laminates:
        out(curlam, args.eng, args.mat)
