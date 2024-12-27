#!/usr/bin/env python
# file: install.py
# vim:fileencoding=utf-8:ft=python
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2024-12-27T17:33:41+0100
# Last modified: 2024-12-27T17:38:54+0100

import os
import shutil
import sys
import sysconfig


def install(script, nt_ext):
    if os.name == "posix":
        dest = [
            sysconfig.get_path("scripts", "posix_user") + os.sep + script
        ]
    elif os.name == "nt":
        dest = [
            sysconfig.get_path("scripts", os.name) + os.sep + script + nt_ext,
            sysconfig.get_path("scripts", os.name + "_user") + os.sep + script + nt_ext,
        ]
    else:
        print(f"The system '{os.name}' is not recognized. Exiting")
        sys.exit(1)
    for path in dest:
        try:
            shutil.copyfile(script, path)
            print(f"* installed '{script}' as '{path}'.")
            os.chmod(path, 0o700)
            break
        except (OSError, PermissionError, FileNotFoundError):
            pass  # Can't write to destination


install("lamprop", ".pyz")
install("lamprop-gui", ".pyw")
