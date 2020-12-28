# file: parser.py
# vim:fileencoding=utf-8:ft=python
# Copyright © 2014-2020 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause
# Created: 2014-02-21 21:35:41 +0100
# Last modified: 2020-12-28T17:32:15+0100
"""Parser for lamprop files."""

import logging
from .core import fiber, resin, lamina, laminate

msg = logging.getLogger("parser")


def parse(filename):
    """
    Parse a lamprop file.

    Arguments:
        filename: The name of the file to parse.

    Returns
        A list of types.laminate.
    """
    try:
        rd, fd, ld = _directives(filename)
    except IOError:
        msg.warning("cannot read '{}'.".format(filename))
        return []
    fdict = _get_components(fd, fiber)
    msg.info("found {} fibers in '{}'".format(len(fdict), filename))
    rdict = _get_components(rd, resin)
    msg.info("found {} resins in '{}'".format(len(rdict), filename))
    boundaries = [j for j in range(len(ld)) if ld[j][1][0] == "t"] + [len(ld)]
    bpairs = [(a, b) for a, b in zip(boundaries[:-1], boundaries[1:])]
    msg.info("found {} possible laminates in '{}'".format(len(bpairs), filename))
    laminates = []
    for a, b in bpairs:
        current = ld[a:b]
        lam = _laminate(current, rdict, fdict)
        if lam:
            laminates.append(lam)
    msg.info("found {} laminates in '{}'".format(len(laminates), filename))
    return laminates


def _directives(filename):
    """
    Read the directives from a lamprop file.

    Arguments:
        filename: The name of the file to parse.

    Returns:
        A 3-tuple (resin directives, fiber directives, laminate directives)
    """
    with open(filename, encoding="utf-8") as df:
        data = [ln.strip() for ln in df]
    # Filter out lines with directives.
    directives = [
        (num, ln)
        for num, ln in enumerate(data, start=1)
        if len(ln) > 1 and ln[1] == ":" and ln[0] in "tmlsfr"
    ]
    msg.info("found {} directives in '{}'".format(len(directives), filename))
    rd = [(num, ln) for num, ln in directives if ln[0] == "r"]
    fd = [(num, ln) for num, ln in directives if ln[0] == "f"]
    ld = [(num, ln) for num, ln in directives if ln[0] in "tmls"]
    return rd, fd, ld


def _get_numbers(directive):
    """
    Retrieve consecutive floating point numbers from a directive.

    Arguments:
        directive: A 2-tuple (int, str).

    Returns:
        A tuple of floating point numbers and the remainder of the string.
    """
    num, line = directive
    numbers = []
    for j in line.split()[1:]:
        if j[0] in "0123456789.+-":
            numbers.append(float(j))
        else:
            break
    remain = line.split(maxsplit=len(numbers) + 1)[-1]
    return tuple(numbers), remain


def _laminate(ld, resins, fibers):
    """
    Parse a laminate definition.

    This must be a t-directive, followed by an m-directive, followed by one or
    more l-directives and optionally finished by an s-directive.

    Arguments:
        ld: A sequence of (number, line) tuples describing a laminate.
        resins: A dictionary of resins, keyed by their names.
        fibers: A dictionary of fibers, keyed by their names.

    Returns:
        A laminate dictionary, or None.
    """
    sym = False
    if ld[0][1].startswith("t"):
        lname = ld[0][1][2:].strip()
    else:
        msg.warning("no 't' directive on line {}".format(ld[0][0]))
        return None
    try:
        if not ld[1][1].startswith("m"):
            raise ValueError
        common_vf, rname = ld[1][1][2:].split(maxsplit=1)
        common_vf = float(common_vf)
        if rname not in resins:
            msg.warning("unknown resin '{}' on line {}".format(rname, ld[1][0]))
            raise ValueError
    except ValueError:
        msg.warning("no valid 'm' directive on line {}".format(ld[1][0]))
        return None
    if ld[-1][1].startswith("s"):
        sym = True
        del ld[-1]
    llist = []
    for directive in ld[2:]:
        lamina = _get_lamina(directive, fibers, resins[rname], common_vf)
        if lamina:
            llist.append(lamina)
    if not llist:
        msg.warning("empty laminate '{}'".format(lname))
        return None
    if sym:
        msg.info("laminate '{}' is symmetric".format(lname))
        llist = llist + list(reversed(llist))
    return laminate(lname, llist)


def _get_components(directives, tp):
    """
    Parse fiber and resin lines.

    Arguments:
        directives: A sequence of (number, line) tuples describing fibers/resins.
        tp: The conversion function to use. Either core.fiber or core.resin

    Returns:
        A list of fiber dictionaries
    """
    rv = []
    names = []
    tname = tp.__name__
    w1 = "expected 4 numbers for a {} on line {}, found {}; skipping."
    w2 = 'duplicate {} "{}" on line {} ignored.'
    w3 = "{} must be >0 on line {}; skipping."
    w4 = "Poisson's ratio on line {} should be  >0 and <0.5; skipping."
    for directive in directives:
        ln = directive[0]
        numbers, name = _get_numbers(directive)
        count = len(numbers)
        if count != 4:
            msg.warning(w1.format(tname, ln, count))
            continue
        if name in names:
            msg.warning(w2.format(tname, name, ln))
            continue
        E, ν, α, ρ = numbers
        if E < 0:
            msg.warning(w3.format("Young's modulus", ln))
            continue
        if ρ < 0:
            msg.warning(w3.format("Density", ln))
            continue
        if ν < 0 or ν >= 0.5:
            msg.warning(w4.format(ln))
            continue
        rv.append(tp(*numbers, name))
    return {comp.name: comp for comp in rv}


def _get_lamina(directive, fibers, resin, vf):
    """
    Parse a lamina line.

    Arguments:
        directive: A 2-tuple (int, str) that contains the line number and
            a lamina line.
        resins: A dictionary of resins, keyed by their names.
        fibers: A dictionary of fibers, keyed by their names.
        vf: The global fiber volume fraction as a floating point number
            between 0 and 1.

    Returns:
        A lamina dictionary, or None.
    """
    w1 = "invalid lamina line {}, '{}'"
    w2 = "unknown fiber '{}' on line {}"
    ln, line = directive
    numbers, fname = _get_numbers(directive)
    if len(numbers) == 2:
        numbers = numbers + (vf,)
    elif len(numbers) != 3:
        msg.warning(w1.format(ln, line))
        return None
    if fname not in fibers:
        msg.warning(w2.format(fname, ln))
        return None
    return lamina(fibers[fname], resin, *numbers)
