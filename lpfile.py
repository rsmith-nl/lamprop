# -*- coding: utf-8 -*-
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

"Contains the LPparser class for parsing lamprop files."

import lptypes

def _numeric(val):
    '''Tests if a value is a valid floating point number.'''
    try:
        float(val)
    except ValueError:
        return False
    return True

class LPparser:
    def __init__(self):
        '''Initialize an empty parser object.'''
        self.f = {}
        self.r = {}
        self.l = []
        self.curlam = None
        self.curresin = None
        self.curvf = 0.0

    def _parse_f(self, lst):
        '''Parse a fiber line.'''
        if _numeric(lst[5]): # Old format
            finame = ' '.join(lst[8:])
            self.f[finame] = lptypes.Fiber(lst[1], lst[3], lst[5], lst[7], 
                                           finame)
        else:  # New format; Name _must_ start with a non-mumber.
            finame = ' '.join(lst[5:])
            self.f[finame] = lptypes.Fiber(lst[1], lst[2], lst[3], lst[4], 
                                           finame)

    def _parse_r(self, lst):
        '''Parse a resin line.'''
        rname = ' '.join(lst[5:])
        self.r[rname] = lptypes.Resin(lst[1], lst[2], lst[3], lst[4])

    def _parse_t(self, lst):
        '''Parse a laminate line.'''
        lname = ' '.join(lst[1:])
        if lname in [x.name for x in self.l]:
            print "Laminate '{0}' already exists! Skipping.".format(lname)
            return
        if self.curlam != None:
            self.curlam.finish()
            self.curresin = None
        self.curlam = lptypes.Laminate(lname)
        self.l.append(self.curlam)

    def _parse_m(self, lst):
        '''Parse a matrix line.'''
        if self.curlam == None:
            print "Found 'm:' line outside a laminate; Skipping."
            return
        self.curvf = float(lst[1])
        mname = ' '.join(lst[2:])
        if mname in self.r:
            self.curresin = self.r[mname]
        else:
            self.curlam = None
            self.curresin = None
            print "Resin '{0}' unknown. Skipping".format(mname)

    def _parse_l(self, lst):
        '''Parse a lamina line.'''
        if self.curlam == None:
            print "Found 'l:' line but no previous 't:' line! Skipping."
            return
        if self.curresin == None:
            print "Found 'l:' line but no previous 'm:' line! Skipping."
            return
        finame = ' '.join(lst[3:])
        if finame not in self.f:
            print "Unknown fiber in 'l:' line. Skipping."
            return
        self.curlam.append(lptypes.Lamina(self.f[finame], self.curresin, 
                                          lst[1], lst[2], self.curvf))

    def parse(self, fname):
        '''Reads and parses the file fname. Returns a tuple containing
        dictionaries of fibers, resins, and laminates.'''
        self.__init__()
        try:
            fl = open(fname)
        except IOError:
            print "Cannot open:", fname
            return None, None, None
        for line in fl:
            lst = line.split()
            if len(lst) == 0 or len(lst[0]) < 2 or lst[0][1] != ':':
                continue # comment line
            try:
                # Dispatch to the appropriate private method
                getattr(self, '_parse_'+lst[0][0])(lst)
            except AttributeError:
                print "Unknown line type '{}:'!".format(lst[0][0])
        self.curlam.finish()
        fl.close()
        return self.f, self.r, self.l

