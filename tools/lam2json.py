#!/usr/bin/env python3
# file: lam2json.py
# vim:fileencoding=utf-8:ft=python
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2016-06-06 22:21:33 +0200
# Last modified: 2016-06-07 23:47:48 +0200

"""Script to convert a lamprop version 2 `lam` file to version 3 JSON
format."""

from collections import OrderedDict as Od
import argparse
import json
import logging
import os
import re
import sys

__version__ = '0.2.0'
es = 'invalid line {} "{}" skipped'


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
        if not args.nojoin:
            # Reformat the data
            data = re.sub(r'([^\}\]]),\s*\n\s*', r'\1, ', data,
                          flags=re.MULTILINE)
        if args.stdout:
            print(data)
        else:
            with open(newpath, 'w') as outfile:
                outfile.write(data)


def process_arguments(argv):
    """Process the command line arguments."""
    opts = argparse.ArgumentParser(prog='lam2json', description=__doc__)
    opts.add_argument('-v', '--version', action='version',
                      version=__version__)
    opts.add_argument('-s', '--stdout', action='store_true',
                      help='output to standard output (default: to file)')
    opts.add_argument('-j', '--nojoin', action='store_true',
                      help='print each value on a single line (default: join)')
    opts.add_argument('--log', default='warning',
                      choices=['debug', 'info', 'warning', 'error'],
                      help='logging level (defaults to "warning")')
    opts.add_argument("files", metavar='file', nargs='*',
                      help="one or more files to process")
    args = opts.parse_args(argv)
    logging.basicConfig(level=getattr(logging, args.log.upper(), None),
                        format='%(levelname)s: %(message)s')
    return args


def process_file(path):
    T, M, L = 1, 2, 3
    out = Od()
    with open(path) as infile:
        lines = infile.readlines()
    # Only directives
    lines = [(num, ln.strip()) for num, ln in enumerate(lines, start=1)
             if len(ln) > 1 and ln[1] == ':' and ln[0] in 'frtmls']
    out['fibers'] = findfibers(lines)
    out['resins'] = findresins(lines)
    state = T
    out['laminates'] = []
    laminate = Od()
    for num, ln in lines:
        comb = (state, ln[0])
        try:
            if comb == (L, 't'):
                out['laminates'].append(laminate)
                state = T
                # no continue!
            if comb == (T, 't'):
                laminate = Od()
                laminate['name'] = ln.split(maxsplit=1)[1]
                state = M
                continue
            if comb == (M, 'm'):
                _, vf, rname = ln.split(maxsplit=2)
                laminate['vf'] = float(vf)
                laminate['matrix'] = rname
                laminate['lamina'] = []
                state = L
                continue
            if comb == (L, 'l'):
                _, weight, angle, *rest = ln.split(maxsplit=4)
                lamina = Od()
                lamina['weight'] = float(weight)
                lamina['angle'] = float(angle)
                try:
                    lamina['vf'] = float(rest[0])
                    del rest[0]
                except ValueError:
                    pass
                lamina['fiber'] = ' '.join(rest)
                laminate['lamina'].append(lamina)
                continue
            if comb == (L, 's'):
                laminate['symmetric'] = True
                out['laminates'].append(laminate)
                state = T
                continue
            logging.error('unexpected line {} "{}"'.format(num, ln))
        except ValueError:
            logging.error(es.format(ln))
    if 'lamina' in laminate:
        out['laminates'].append(laminate)
    return json.dumps(out, indent=2)


def findfibers(lines):
    fl = [ln for ln in lines if ln[1][0] is 'f']
    rv = []
    for num, ln in fl:
        try:
            _, E1, nu12, alpha1, density, name = ln.split(maxsplit=5)
            newf = Od()
            newf["E1"] = float(E1)
            newf["nu12"] = float(nu12)
            newf["alpha1"] = float(alpha1)
            newf["density"] = float(density)
            newf["name"] = name
            rv.append(newf)
        except ValueError:
            logging.error(es.format(num, ln))
    return rv


def findresins(lines):
    rl = [ln for ln in lines if ln[1][0] is 'r']
    rv = []
    for num, ln in rl:
        try:
            _, E, nu, alpha, density, name = ln.split(maxsplit=5)
            newr = Od()
            newr["E"] = float(E)
            newr["nu"] = float(nu)
            newr["alpha"] = float(alpha)
            newr["density"] = float(density)
            newr["name"] = name
            rv.append(newr)
        except ValueError:
            logging.error(es.format(num, ln))
    return rv


if __name__ == '__main__':
    main(sys.argv[1:])
