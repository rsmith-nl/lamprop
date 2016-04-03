#!/usr/bin/env python3
# file: build.py
# vim:fileencoding=utf-8:ft=python
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2016-03-31 11:59:23 +0200
# Last modified: 2016-04-03 12:16:32 +0200

"""Build an archive executable for the lamprop program."""

import os
import io
import zipfile as z


def buildarchive(name, srcdir, modules):
    """
    Build an executable archive for a program.

    Arguments:
        name: Name of the program without extension.
        srcdir: Directory to archive. This should contain __main__.py
        modules: module name or list of module names in srcdir.
    """
    if isinstance(modules, str):
        modules = [modules]
    origdir = os.getcwd()
    os.chdir(srcdir)
    tmpf = io.BytesIO()
    with z.PyZipFile(tmpf, mode='w', compression=z.ZIP_DEFLATED) as zf:
        zf.writepy('__main__.py')
        for m in modules:
            zf.writepy(m)
    os.chdir(origdir)
    with open(name, 'wb') as archive:
        archive.write(b'#!/usr/bin/env python3\n')
        archive.write(tmpf.getvalue())
    os.chmod(name, 0o755)


buildarchive('lamprop', 'src', 'lamprop')
