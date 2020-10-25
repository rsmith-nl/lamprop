#!/usr/bin/env python
# file: setup.py
# vim:fileencoding=utf-8:ft=python
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2016-04-24 17:06:48 +0200
# Last modified: 2020-10-25T17:21:51+0100
"""Install script for lamprop."""

import os
import py_compile
import shutil
import sys
import sysconfig
import tempfile
import zipfile as z


def mkarchive(name, modules, main="__main__.py"):
    """
    Create a runnable archive.

    Arguments:
        name: Name of the archive.
        modules: Module name or iterable of module names to include.
        main: Name of the main file. Defaults to __main__.py
    """
    # print(f"Building {name}", end="... ")
    std = "__main__.py"
    shebang = b"#!/usr/bin/env python\n"
    if isinstance(modules, str):
        modules = [modules]
    if main != std:
        try:
            os.remove(std)
        except OSError:
            pass
        os.link(main, std)
    # Forcibly compile __main__.py lest we use an old version!
    # Use the same optimization level as for the PyZipFile!
    py_compile.compile(std, optimize=2)
    tmpf = tempfile.TemporaryFile()
    with z.PyZipFile(tmpf, mode="w", compression=z.ZIP_DEFLATED, optimize=2) as zf:
        zf.writepy(std)
        for m in modules:
            zf.writepy(m)
    if main != std:
        os.remove(std)
    tmpf.seek(0)
    archive_data = tmpf.read()
    tmpf.close()
    with open(name, "wb") as archive:
        archive.write(shebang)
        archive.write(archive_data)
    os.chmod(name, 0o755)
    # print("done.")


def remove(path):
    try:
        os.remove(path)
    except FileNotFoundError:
        pass


if __name__ == "__main__":
    nm1 = "lamprop"
    nm2 = "lamprop-gui"
    scripts = [nm1, nm2]
    if os.name == "nt":
        nm1 += ".pyz"
        nm2 += ".pyw"
    remove(nm1)
    remove(nm2)
    mkarchive(nm1, "lp", main="console.py")
    mkarchive(nm2, "lp", main="gui.py")
    # Installation
    scheme = os.name + "_user"
    destdir = sysconfig.get_path("scripts", scheme)
    extensions = (".pyw", ".pyz", "")  # Don't change the order!
    install = "install" in [a.lower() for a in sys.argv]
    if os.name not in ("nt", "posix"):
        print(f"The system '{os.name}' is not recognized. Exiting")
        sys.exit(1)
    if install:
        if not os.path.exists(destdir):
            os.mkdir(destdir)
    else:
        print("(Use the 'install' argument to actually install scripts.)")
    # Actual installation.
    for script in scripts:
        for ext in extensions:
            src = script + ext
            if os.path.exists(src):
                if os.name == "nt":
                    destname = destdir + os.sep + src
                elif os.name == "posix":
                    destname = destdir + os.sep + script
                if install:
                    shutil.copyfile(src, destname)
                    os.chmod(destname, 0o700)
                    print(f"* installed '{src}' as '{destname}'.")
                else:
                    print(f"* '{src}' would be installed as '{destname}'")
                # Only the first extension found will be installed.
                continue
