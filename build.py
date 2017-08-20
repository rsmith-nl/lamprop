# file: build.py
# vim:fileencoding=utf-8:ft=python
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2016-04-24 17:06:48 +0200
# Last modified: 2017-08-20 16:00:32 +0200

"""Create runnable archives from program files and custom modules."""

# from subprocess import run, PIPE
import os
import sys
import py_compile
import tempfile
import zipfile as z


def mkarchive(name, modules, main='__main__.py'):
    """Create a runnable archive.

    It encodes the same (major) version of Python as used for the build in the
    call to ``env`` in the archive.

    Arguments:
        name: Name of the archive.
        modules: Module name or iterable of module names to include.
        main: Name of the main file. Defaults to __main__.py
    """
    std = '__main__.py'
    vi = sys.version_info
    shebang = '#!/usr/bin/env python{}\n'.format(vi.major).encode('ascii')
    if isinstance(modules, str):
        modules = [modules]
    if main != std:
        try:
            os.remove(std)
        except OSError:
            pass
        os.link(main, std)
    # Forcibly compile __main__.py lest we use an old version!
    py_compile.compile(std)
    tmpf = tempfile.TemporaryFile()
    with z.PyZipFile(tmpf, mode='w', compression=z.ZIP_DEFLATED) as zf:
        zf.writepy(std)
        for m in modules:
            zf.writepy(m)
    if main != std:
        os.remove(std)
    tmpf.seek(0)
    archive_data = tmpf.read()
    tmpf.close()
    with open(name, 'wb') as archive:
        archive.write(shebang)
        archive.write(archive_data)
    os.chmod(name, 0o755)


if __name__ == '__main__':
    from shutil import copy
    archname = 'lpbin'
    name = 'lamprop'
    os.chdir('src')
    mkarchive(archname, name)
    copy(archname, '../'+name)
    os.remove(archname)
