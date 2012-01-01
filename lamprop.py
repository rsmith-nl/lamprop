#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# lamprop - main program.
# Copyright © 2011,2012 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# Time-stamp: <>
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

import argparse
import sys
import lpfile
import lpver
import lpouttext
import lpoutlatex
import lpouthtml

class LicenseAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print lpver.lic
        sys.exit()

# Process the command-line arguments
opts = argparse.ArgumentParser(prog=lpver.name,
 description='Calculate the elastic properties of a fibrous composite laminate.'
             ' See lamprop(1) for the manual of this program and lamprop(5) '
             'for the manual of the data file format.')
group = opts.add_mutually_exclusive_group()
group.add_argument('-l', '--latex', action='store_true', help="LaTeX output")
group.add_argument('-H', '--html', action='store_true', help="HTML output")
opts.add_argument('-e', '--eng', action='store_true', 
                   help="produce the layers and engineering properties")
opts.add_argument('-m', '--mat', action='store_true', 
                   help="produce the ABD and abd matrices")
group = opts.add_mutually_exclusive_group()
group.add_argument('-L', '--license', action=LicenseAction, nargs=0,
                  help="print the license")
group.add_argument('-v', '--version', action='version', 
                   version='{0}'.format(lpver.version))
opts.add_argument("files", metavar='file', nargs='*', 
                  help="one or more files to process")
args = opts.parse_args()
del opts, group
if args.mat == False and args.eng == False:
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
out = lpouttext.out
if args.latex:
    out = lpoutlatex.out
elif args.html:
    out = lpouthtml.out
for f in args.files:
    # Process the files.
    fp = lpfile.LPparser()
    fibers, resins, laminates = fp.parse(f)
    # Print the results.
    for curlam in laminates:
        out(curlam, args.eng, args.mat)
