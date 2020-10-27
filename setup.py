#!/usr/bin/env python
# file: setup.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2020 R.F. Smith <rsmith@xs4all.nl>
# Created: 2020-10-25T12:18:04+0100
# Last modified: 2020-10-27T18:50:44+0100
"""Script to install scripts for the local user."""

import os
import py_compile
import shutil
import sys
import sysconfig
import tempfile
import zipfile as z


def main():
    """Entry point for the setup script."""
    # Building the archives
    nm1 = "lamprop"
    nm2 = "lamprop-gui"
    remove(nm1)
    remove(nm2)
    mkarchive(nm1, "lp", main="console.py")
    mkarchive(nm2, "lp", main="gui.py")
    scripts = [(nm1, ".pyz"), (nm2, ".pyw")]
    # Preparation
    if os.name == "posix":
        destdir = sysconfig.get_path("scripts", "posix_user")
        destdir2 = ""
    elif os.name == "nt":
        destdir = sysconfig.get_path("scripts", os.name)
        destdir2 = sysconfig.get_path("scripts", os.name + "_user")
    else:
        print(f"The system '{os.name}' is not recognized. Exiting")
        sys.exit(1)
    install = "install" in [a.lower() for a in sys.argv]
    if install:
        if not os.path.exists(destdir):
            os.mkdir(destdir)
    else:
        print("(Use the 'install' argument to actually install scripts.)")
    do_install(install, scripts, destdir, destdir2)


def do_install(install, scripts, destdir, destdir2):
    # Actual installation.
    for script, nt_ext in scripts:
        base = os.path.splitext(script)[0]
        if os.name == "posix":
            destname = destdir + os.sep + base
            destname2 = ""
        elif os.name == "nt":
            destname = destdir + os.sep + base + nt_ext
            destname2 = destdir2 + os.sep + base + nt_ext
        if install:
            for d in (destname, destname2):
                try:
                    shutil.copyfile(script, d)
                    print(f"* installed '{script}' as '{destname}'.")
                    os.chmod(d, 0o700)
                    break
                except (OSError, PermissionError, FileNotFoundError):
                    pass  # Can't write to destination
            else:
                print(f"! installation of '{script}' has failed.")
        else:
            print(f"* '{script}' would be installed as '{destname}'")
            if destname2:
                print(f"  or '{destname2}'")


def mkarchive(name, modules, main="__main__.py"):
    """
    Create a runnable archive.

    Arguments:
        name: Name of the archive.
        modules: Module name or iterable of module names to include.
        main: Name of the main file. Defaults to __main__.py
    """
    std = "__main__.py"
    shebang = b"#!/usr/bin/env python\n"
    if isinstance(modules, str):
        modules = [modules]
    if main != std:
        remove(std)
        os.link(main, std)
    # Optimization level for compile.
    lvl = 2
    # Forcibly compile __main__.py lest we use an old version!
    py_compile.compile(std, optimize=lvl)
    with tempfile.TemporaryFile() as tmpf:
        with z.PyZipFile(tmpf, mode="w", compression=z.ZIP_DEFLATED, optimize=lvl) as zf:
            zf.writepy(std)
            for m in modules:
                zf.writepy(m)
        if main != std:
            remove(std)
        tmpf.seek(0)
        archive_data = tmpf.read()
    with open(name, "wb") as archive:
        archive.write(shebang)
        archive.write(archive_data)
    os.chmod(name, 0o755)


def remove(path):
    """Remove a file, ignoring directories and nonexistant files."""
    try:
        os.remove(path)
    except (FileNotFoundError, PermissionError, IsADirectoryError, OSError):
        pass


if __name__ == "__main__":
    main()
