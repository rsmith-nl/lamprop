#!/usr/bin/env python
# file: build.py
# vim:fileencoding=utf-8:ft=python
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2024-12-27T17:33:41+0100
# Last modified: 2024-12-27T17:34:39+0100

import zipapp

zipapp.create_archive(
    "src",
    target="lamprop",
    interpreter="/usr/bin/env python",
    main="console:main",
    compressed=True,
)
zipapp.create_archive(
    "src",
    target="lamprop-gui",
    interpreter="/usr/bin/env python",
    main="gui:main",
    compressed=True,
)
