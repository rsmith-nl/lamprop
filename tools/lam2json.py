#!/usr/bin/env python3
# file: lam2json.py
# vim:fileencoding=utf-8:ft=python
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2016-06-06 22:21:33 +0200
# Last modified: 2016-06-07 00:17:42 +0200

"""Script to convert a lamprop version 2 `lam` file to version 3 JSON
format."""

import argparse
import json
import os
import re
import sys
import logging

__version__ = '0.1.0'


def main(argv):
    """
    Entry point for lam2json.py.

    Arguments:
        argv: command line arguments
    """
    args = process_arguments(argv)
    sre = '.*{0}([^{0}]+)\.lam$'.format(os.sep)
    for path in args.files:
        if not path.endswith('.lam'):
            logging.error('{} is not a valid input file'.format(path))
            continue
        newpath = re.sub(sre, r'\1.json', path)
        logging.info('Converting {} to {}.'.format(path, newpath))
        data = process_file(path)
        with open(newpath, 'w') as outfile:
            outfile.write(data)


def process_arguments(argv):
    """Process the command line arguments."""
    opts = argparse.ArgumentParser(prog='lam2json', description=__doc__)
    opts.add_argument('-v', '--version', action='version',
                      version=__version__)
    opts.add_argument('--log', default='warning',
                      choices=['debug', 'info', 'warning', 'error'],
                      help="logging level (defaults to 'warning')")
    opts.add_argument("files", metavar='file', nargs='*',
                      help="one or more files to process")
    args = opts.parse_args(argv)
    logging.basicConfig(level=getattr(logging, args.log.upper(), None),
                        format='%(levelname)s: %(message)s')
    return args


def process_file(path):
    T, M, L = 1, 2, 3
    out = {}
    with open(path) as infile:
        lines = infile.readlines()
    # Only directives
    lines = [ln.strip() for ln in lines if len(ln) > 1 and ln[1] == ':' and
             ln[0] in 'frtmls']
    fl = [ln for ln in lines if ln[0] is 'f']
    out['fibers'] = []
    for ln in fl:
        _, E1, nu12, alpha1, density, name = ln.split(maxsplit=5)
        out['fibers'].append({"E1": float(E1), "nu12": float(nu12),
                              "alpha1": float(alpha1),
                              "density": float(density), "name": name})
    rl = [ln for ln in lines if ln[0] is 'r']
    out['resins'] = []
    for ln in rl:
        _, E, nu, alpha, density, name = ln.split(maxsplit=5)
        out['resins'].append({"E": float(E1), "nu": float(nu), "alpha":
                              float(alpha), "density": float(density),
                              "name": name})
    state = T
    out['laminates'] = []
    laminate = {}
    for ln in lines:
        if state == L and ln[0] == 't':
            out['laminates'].append(laminate)
            state = T
            # no continue!
        if state == T and ln[0] == 't':
            laminate = {}
            laminate['name'] = ln.split(maxsplit=1)[1]
            state = M
            continue
        if state == M and ln[0] == 'm':
            _, vf, rname = ln.split(maxsplit=2)
            laminate['vf'] = float(vf)
            laminate['matrix'] = rname
            laminate['lamina'] = []
            state = L
            continue
        if state == L and ln[0] == 'l':
            _, weight, angle, *rest = ln.split(maxsplit=4)
            lamina = {'weight': float(weight), 'angle': float(angle)}
            try:
                lamina['vf'] = float(rest[0])
                del rest[0]
            except ValueError:
                pass
            lamina['fiber'] = ' '.join(rest)
            laminate['lamina'].append(lamina)
            continue
        if state == L and ln[0] == 's':
            laminate['symmetric'] = True
            out['laminates'].append(laminate)
            state = T
    if 'lamina' in laminate:
        out['laminates'].append(laminate)
    return json.dumps(out, indent=2)


if __name__ == '__main__':
    main(sys.argv[1:])
