# file: console.py
# vim:fileencoding=utf-8:ft=python
# lamprop - main program.
#
# Copyright © 2011-2021 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# Created: 2011-03-26 14:54:24 +0100
# Last modified: 2022-01-26T23:40:56+0100
#
# SPDX-License-Identifier: BSD-2-Clause

import argparse
import logging
import os
import sys
import lp


class LicenseAction(argparse.Action):
    """Action class to print the license."""

    def __call__(self, parser, namespace, values, option_string=None):
        print(lp.__license__)
        sys.exit()


def main():
    """Entry point for lamprop console application."""
    # Process the command-line arguments
    doc = (
        "Calculate the elastic properties of a fibrous composite laminate. "
        "See the manual (lamprop-manual.pdf) for more in-depth information."
    )
    opts = argparse.ArgumentParser(prog="lamprop", description=doc)
    group = opts.add_mutually_exclusive_group()
    group.add_argument(
        "-l",
        "--latex",
        action="store_true",
        help="generate LaTeX output (the default is plain text)",
    )
    group.add_argument("-H", "--html", action="store_true", help="generate HTML output")
    opts.add_argument(
        "-e",
        "--eng",
        action="store_true",
        help="output only the engineering properties",
    )
    opts.add_argument(
        "-m",
        "--mat",
        action="store_true",
        help="output only the ABD matrix and stiffness tensor",
    )
    opts.add_argument(
        "-f", "--fea", action="store_true", help="output only material data for FEA"
    )
    group = opts.add_mutually_exclusive_group()
    group.add_argument(
        "-L", "--license", action=LicenseAction, nargs=0, help="print the license"
    )
    group.add_argument("-v", "--version", action="version", version=lp.__version__)
    opts.add_argument(
        "--log",
        default="warning",
        choices=["debug", "info", "warning", "error"],
        help="logging level (defaults to 'warning')",
    )
    opts.add_argument(
        "files", metavar="file", nargs="*", help="one or more files to process"
    )
    args = opts.parse_args(sys.argv[1:])
    logging.basicConfig(
        level=getattr(logging, args.log.upper(), None),
        format="%(levelname)s: %(message)s",
    )
    del opts, group
    if args.mat is False and args.eng is False and args.fea is False:
        args.eng = True
        args.mat = True
        args.fea = True
    # No files given to process.
    if len(args.files) == 0:
        sys.exit(1)
    # Set the output method.
    out = lp.text_output
    if args.latex:
        out = lp.latex_output
    elif args.html:
        out = lp.html_output
    # Force utf-8 encoding for stdout on ms-windows.
    # Because redirected output uses cp1252 by default.
    if os.name == "nt":
        sys.stdout.reconfigure(encoding="utf-8")
    for f in args.files:
        logging.info("processing file '{}'".format(f))
        laminates = lp.parse(f)
        for curlam in laminates:
            print(*out(curlam, args.eng, args.mat, args.fea), sep="\n")


if __name__ == "__main__":
    main()
