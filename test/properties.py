# Gegevens koolstofvezel
E1f=233000.0
E2f=23100.0
nu12f=0.2
nu23f=0.4
G12f=8960.0
G23f=8270
a1f=-0.54e-6
a2f=10.1e-6

# Gegevens hars
Em=4620
num=0.36
am=41.4e-6
Gm=Em/(2*(1+num))

def E1(vf):
    vm=1-vf
    return E1f*vf+vm*Em

def E2(vf):
    eta=0.55
    vm=1-vf
    E2inv=(vf/E2f+eta*vm/Em)/(vf+eta*vm)
    return 1/E2inv

def E2Hahn(vf):
    vm=1-vf
    Kt=E1f/(2*(1-vf))
    Km=Em/(2*(1-vm))
    eta4=(3-4*num+Gm/G23f)/(4*(1-num))
    G23=(vf+eta4*vm)/(vf/G23f+eta4*vm/Gm)
    nu12=nu12f*vf+num*vm
    m=1+4*Kt*nu12**2/E1(vf)
    return 4*Kt*G23/(Kt+m*G23)

def cte2(vf):
    #c1=(a1f*E1f*vf+am*Em*vm)/E1(vf)
    vm=1-vf
    c2 = am+(a2f-am)*vf+((E1f*num-Em*nu12f)/E1(vf))*(am-a1f)*vm*vf
    return c2

def cte2alt(vf):
    # Alleen goed geldig voor koolstofvezel!
    return am*((0.3-vf)*1.05+1)

# Test
if __name__ == '__main__':
    lv = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
    print "Carbon fiber"
    print "vf: ", lv
    print "E1: ", [E1(v) for v in lv]
    print "E2/Em: ", [E2(v)/Em for v in lv]
    print "E2Hahn/Em: ", [E2Hahn(v)/Em for v in lv]
    print "cte2/am: ", [cte2(v)/am for v in lv]
    print "cte2alt/am: ", [cte2alt(v)/am for v in lv]
    # Gegevens glasvezel
    E1f=70000.0
    E2f=80000.0
    nu12f=0.27
    nu23f=0.27
    G12f=E1f/(2*(1+nu12f))
    G23f=G12f
    a1f=9e-6
    a2f=9e-6
    print "Glass fiber"
    print "vf: ", lv
    print "E1: ", [E1(v) for v in lv]
    print "E2/Em: ", [E2(v)/Em for v in lv]
    print "E2Hahn/Em: ", [E2Hahn(v)/Em for v in lv]
    print "cte2/am: ", [cte2(v)/am for v in lv]
    print "cte2alt/am: ", [cte2alt(v)/am for v in lv]


