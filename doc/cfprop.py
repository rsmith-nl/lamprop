#!/usr/bin/env python
# Encoding: utf-8

E1f = 233000.0
E2f = 23100.0
v12f = 0.2
v23f = 0.4
G12f = 8960
G23f = 8270
a1f = -0.54e-6
a2f = 10.1e-6

Em = 4620.0
vm = 0.36
am = 41.4e-6


def a1(vf):
    vm = 1 - vf
    rv = (a1f * E1f * vf + am * Em * vm) / (E1f * vf + Em * vm)
    print "vf = {}, α1 = {:.3g}".format(vf, rv)


def a2(vf):
    vm = 1 - vf
    E1 = E1f * vf + Em * vm
    p1 = am
    p2 = (a2f - am) * vf
    p3 = ((E1f * vm - Em * v12f) / E1) * (am - a1f) * vm * vf
    s = "α2(1) = {}, α2(2) = {}, α2(3) = {},\n α2(1-3) = {}, α2(1,3) = {}, {}"
    print s.format(p1, p2, p3, p1 + p2 + p3, p1 + p3, (p1 + p2 + p3) / (p1 + p3))


def a2alt(vf):
    vm = 1 - vf
    E1 = E1f * vf + Em * vm
    p1 = am * vm
    p3 = ((E1f * vm - Em * v12f) / E1) * (am - a1f) * vm * vf
    s = "alt α2(1) = {}, α2(3) = {},\n α2(1,3) = {}"
    print s.format(p1, p3, p1 + p3)


if __name__ == "__main__":
    for v in range(1, 6):
        v = v * 0.1
        a1(v)
        a2(v)
        a2alt(v)
