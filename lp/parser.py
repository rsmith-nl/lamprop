# file: parser.py
# vim:fileencoding=utf-8:ft=python
# Copyright © 2014-2021 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause
# Created: 2014-02-21 21:35:41 +0100
# Last modified: 2022-01-27T21:16:14+0100
"""Parser for lamprop files."""

import copy
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
        msg.info(f'Reading file "{filename}".')
    except IOError:
        msg.warning(f'Cannot read "{filename}".')
        return []
    fdict = _get_components(fd, fiber)
    msg.info(f'Found {len(fdict)} fibers in "{filename}".')
    rdict = _get_components(rd, resin)
    msg.info(f'Found {len(rdict)} resins in "{filename}".')
    boundaries = [j for j in range(len(ld)) if ld[j][1][0] == "t"] + [len(ld)]
    bpairs = [(a, b) for a, b in zip(boundaries[:-1], boundaries[1:])]
    msg.info(f'Found {len(bpairs)} possible laminates in "{filename}".')
    laminates = []
    for a, b in bpairs:
        current = ld[a:b]
        lam = _laminate(current, rdict, fdict)
        if lam:
            laminates.append(lam)
    msg.info(f'Found {len(laminates)} laminates in "{filename}".')
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
        if len(ln) > 1 and ln[1] == ":" and ln[0] in "tmlscfr"
    ]
    msg.info(f'Found {len(directives)} directives in "{filename}".')
    rd = [(num, ln) for num, ln in directives if ln[0] == "r"]
    fd = [(num, ln) for num, ln in directives if ln[0] == "f"]
    ld = [(num, ln) for num, ln in directives if ln[0] in "tmlsc"]
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
    items = line.split()[1:]
    for j in items:
        try:
            numbers.append(float(j))
        except ValueError:
            break
    newitems = line.split(maxsplit=len(numbers) + 1)[1:]
    if len(newitems) > len(numbers):
        remain = newitems[-1]
    else:
        remain = ""
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
        if lname == "":
            msg.warning(f"No laminate name on line {ld[0][0]}.")
            return None
    else:
        msg.warning(f'No "t" directive on line {ld[0][0]}.')
        return None
    try:
        if not ld[1][1].startswith("m"):
            raise ValueError
        common_vf, rname = ld[1][1][2:].split(maxsplit=1)
        common_vf = float(common_vf)
        if rname not in resins:
            msg.warning(f'Unknown resin "{rname}" on line {ld[1][0]}.')
            raise ValueError
    except ValueError:
        msg.warning(f'No valid "m" directive on line {ld[1][0]}.')
        return None
    if ld[-1][1].startswith("s"):
        sym = True
        del ld[-1]
    llist = []
    for directive in ld[2:]:
        if directive[1].startswith("c"):  # Comment line.
            llist.append(directive[1][2:].strip())
            continue
        lamina = _get_lamina(directive, fibers, resins[rname], common_vf)
        if lamina:
            llist.append(lamina)
    if not llist:
        msg.warning(f'Empty laminate "{lname}".')
        return None
    if sym:
        msg.info(f'Laminate "{lname}" is symmetric.')
        llist = llist + _extended(llist)
    return laminate(lname, llist)


def _extended(original):
    """
    Create the extension to the `original` list to make the laminate symmetric.
    The position of the comments is taken into account.
    """
    if sum(1 for la in original if isinstance(la, str)) == 0:
        return original[::-1]
    layers = copy.deepcopy(original)
    if not isinstance(layers[-1], str):
        layers.append("__")
    if not isinstance(layers[0], str):
        layers.insert(0, "unknown")
    idx = [n for n, v in enumerate(layers) if isinstance(v, str)]
    pairs = list(zip(idx[:-1], idx[1:]))[::-1]
    extension = []
    for s, e in pairs:
        if layers[s] == "__":
            extension += layers[s + 1 : e][::-1]  # noqa
        else:
            extension += [layers[s]] + layers[s + 1 : e][::-1]  # noqa
    return extension


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
    for directive in directives:
        ln = directive[0]
        numbers, name = _get_numbers(directive)
        count = len(numbers)
        if count != 4:
            msg.warning(
                f"Expected 4 numbers for a {tname} on line {ln}, found {count}; skipping."
            )
            continue
        if len(name) == 0:
            msg.warning(f"Missing {tname} name on line {ln}; skipping.")
            continue
        if name in names:
            msg.warning(f'Duplicate {tname} "{name}" on line {ln} ignored.')
            continue
        E, ν, α, ρ = numbers
        if E < 0:
            msg.warning(f"Young's modulus must be >0 on line {ln}; skipping.")
            continue
        if ρ < 0:
            msg.warning(f"Density must be >0 on line {ln}; skipping.")
            continue
        if ν < 0 or ν >= 0.5:
            msg.warning(
                f"Poisson's ratio on line {ln} should be  >0 and <0.5; skipping."
            )
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
    ln, line = directive
    numbers, fname = _get_numbers(directive)
    if len(numbers) == 2:
        numbers = numbers + (vf,)
    elif len(numbers) != 3:
        msg.warning(f'Invalid lamina line {ln}, "{line}".')
        return None
    if fname not in fibers:
        msg.warning(f'Unknown fiber "{fname}" on line {ln}.')
        return None
    return lamina(fibers[fname], resin, *numbers)
