# -*- coding: utf-8 -*-
# Read and parse a lamprop file
#
# Copyright © 2011 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# Time-stamp: <2011-09-18 14:20:45 rsmith>
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

import lptypes

def _numeric(val):
   '''Tests if a value is a valid floating point number.'''
   try:
       float(val)
   except ValueError:
       return False
   return True

def parse(fname):
    '''Reads and parses the file fname. Returns a tuple containing dictionaries 
       of fibers, resins, and laminates.'''
    f = {} # dictionary of fibers
    r = {} # dictionary of resins
    l = [] # list of laminates
    curlam = None       # Current laminate
    curresin = None     # Current resin
    curvf = 0.0
    try:
        fl = open(fname)
    except IOError:
        print "Cannot open:", fname
        return None,None,None
    for line in fl:
        lst = line.split()
        if len(lst) == 0 or len(lst[0]) < 2 or lst[0][1] != ':':
            continue # comment line
        if lst[0][0] == 'f':
            if _numeric(lst[5]): # Old format
                finame = ' '.join(lst[8:])
                f[finame] = lptypes.Fiber(lst[1], lst[3], lst[5], lst[7], finame)
            else:               # New format; Name _must_ start with a non-mumber.
                finame = ' '.join(lst[5:])
                f[finame] = lptypes.Fiber(lst[1], lst[2], lst[3], lst[4], finame)
        elif lst[0][0] == 'r':
            rname = ' '.join(lst[5:])
            r[rname] = lptypes.Resin(lst[1], lst[2], lst[3], lst[4])
        elif lst[0][0] == 't':
            lname = ' '.join(lst[1:])
#            names = [x.name for x in l]
            if lname in [x.name for x in l]:
                print "Laminate '{0}' already exists! Skipping.".format(lname)
            else:
                if curlam != None:
                    curlam.finish()
                    curresin = None
                curlam = lptypes.Laminate(lname)
                l.append(curlam)
        elif lst[0][0] == 'm':
            if curlam == None:
                print "Found 'm:' line outside a laminate; Skipping."
                continue
            curvf = float(lst[1])
            mname = ' '.join(lst[2:])
            if mname in r:
                curresin = r[mname]
            else:
                curlam = None
                curresin = None
                print "Resin '{0}' unknown. Skipping".format(mname)
        elif lst[0][0] == 'l':
            if curlam == None:
                print "Found 'l:' line but no previous 't:' line! Skipping."
                continue
            if curresin == None:
                print "Found 'l:' line but no previous 'm:' line! Skipping."
                continue
            finame = ' '.join(lst[3:])
            if finame not in f:
                print "Unknown fiber in 'l:' line. Skipping."
                continue
            curlam.append(lptypes.Lamina(f[finame], curresin, 
                                         lst[1], lst[2], curvf))
    curlam.finish()
    fl.close()
    return f,r,l

