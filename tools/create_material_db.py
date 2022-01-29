#! /usr/bin/env python3

import lp
import glob
import numpy as np
import os
import json
import argparse

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("lp_testdir", help="directory where the lamprop test files are")
    p.add_argument("--output", default="__matdb.json")
    args = p.parse_args()

    lp_testdir = args.lp_testdir

    lm = glob.glob(os.path.join(lp_testdir, "*lam"))

    fibers = {}
    resins = {}
    for i in lm:
        for j in open(i, "r").readlines():
            if j.startswith("f:") or j.startswith("r:"):
                try:
                    s = j.split()
                    sp = [float(j) for j in s[1:5]]
                    name = j.split(s[4])[-1].strip()
                    if j.startswith("f:"):
                        fb = lp.fiber(sp[0], sp[1], sp[2], sp[3], name)
                        fibers[name] = fb
                    elif j.startswith("r:"):
                        rs = lp.resin(sp[0], sp[1], sp[2], sp[3], name)
                        resins[name] = rs
                except:
                    print("fail to parse %s" % j)

    # check later if there should also be a loop over different ply thicknesses
    fiber_weight = 200.0
    angles = [90, -90, 45, -45, 30, -30, 15, -15, 10, -10, 0]
    vfs = np.arange(0.50, 0.85, 0.05)
    laminae = {}
    for angle in angles:
        for vf in vfs:
            for fb in fibers:
                for rs in resins:
                    key = (fb, rs, fiber_weight, angle, vf)
                    laminae[key] = lp.lamina(
                        fibers[fb], resins[rs], fiber_weight, angle, vf
                    )

    stacks = {
        "ud": [0, 0],
        "hoop": [90, 90],
        "biax090": [0, 90, 90, 0],
        "biax45": [45, -45, -45, 45],
        "triax45": [0, 45, 90, -45, 0],
        "triax30": [0, 30, 90, -30, 0],
        "biax15": [-15, 15, 15, -15],
    }

    def todict(lam):
        sub = vars(lam)
        sub["layers"] = [vars(i) for i in sub["layers"]]
        for i in range(len(sub["layers"])):
            if type(sub["layers"][i]["resin"]) != type({}):
                sub["layers"][i]["resin"] = vars(sub["layers"][i]["resin"])
            if type(sub["layers"][i]["fiber"]) != type({}):
                sub["layers"][i]["fiber"] = vars(sub["layers"][i]["fiber"])
        return sub

    all_laminates = {}

    for s in stacks:
        for vf in vfs:
            for fb in fibers:
                for rs in resins:
                    this_stack = [
                        laminae[(fb, rs, fiber_weight, ang, vf)] for ang in stacks[s]
                    ]
                    try:
                        lam = lp.laminate(
                            "%s_%s_%s_%i" % (s, fb, rs, 100 * vf), this_stack
                        )
                        all_laminates[lam.name] = todict(lam)
                    except:
                        pass

    json.dump(all_laminates, open(args.output, "w"), indent=4)
