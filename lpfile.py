# -*- coding: utf-8 -*-
# Read and parse a lamprop file
#
# Copyright © 2011 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# Time-stamp: <2011-03-26 21:55:26 rsmith>
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

import lamina

def parse(fname):
    '''Reads and parses the file fname. Returns a tuple containing dictionaries 
       of fibers, resins, and laminates.'''
    f = {} # dictionary of fibers
    r = {} # dictionary of resins
    l = {} # dictionary of laminates
    curlam = None       # Current laminate
    curresin = None     # Current resin
    try:
        fl = open(fname)
    except IOError:
        print "Cannot open:", fname
        return None,None,None
    for line in fl:
        lst = line.split()
        print "debug:", lst
        if len(lst) == 0 or len(lst[0]) < 2 or lst[0][1] != ':':
            print "debug: skipping line '{0}'".format(lst)
            continue # comment line
        if lst[0][0] == 'f':
            f[' '.join(lst[8:])] = lamina.Fiber(lst[1], lst[2], lst[3], lst[4], 
                                                lst[5], lst[6], lst[7])
            print "debug: found fiber"
        elif lst[0][0] == 'r':
            r[' '.join(lst[5:])] = lamina.Resin(lst[1], lst[2], lst[3], lst[4])
            print "debug: found resin"
        elif lst[0][0] == 't':
            lname = ' '.join(lst[3:])
            if lname in l:
                print "Laminate '{0}' already exists! Skipping.".format(lname)
            else:
                print "debug: Starting new laminate"
                if curlam != None:
                    curlam.finish()
                    curresin = None
                curlam = l[lname] = lamina.Laminate()
        elif lst[0][0] == 'm' and curlam != None:
            print "debug: Setting laminate resin."
            vf = float(lst[1])
            resinname = ' '.join(lst[2:])
            if resinname in r:
                curresin = r[resinname]
            else:
                curlam = None
                resinname = None
            #FINISHME
        elif lst[0][0] == 'l' and curlam != None:
            pass #FINISHME
    print f
    print r
    print l
    return f,r,l

