# file: __init__.py
# vim:fileencoding=utf-8:ft=python
#
# Copyright © 2015,2019 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# Created: 2015-05-16 16:57:52 +0200
# Last modified: 2019-01-01T00:21:29+0100
#
# SPDX-License-Identifier: BSD-2-Clause
"""Module for calculating fiber reinforced composites properties."""

from .html import out as html_output
from .latex import out as latex_output
from .parser import parse
from .text import out as text_output
from .core import fiber, resin, lamina, laminate
from .version import __version__
