# -*- coding: utf-8 -*-
# Installation script for lamprop.
#
# R.F. Smith <rsmith@xs4all.nl>
# Time-stamp: <2011-03-27 14:56:40 rsmith>

from distutils.core import setup
import lpver

setup(name=lpver.name,
      version=lpver.version,
      description='Program to calculate elastic properties of fibrous composites',
      author='Roland Smith',
      author_email='rsmith@xs4all.nl',
      url='http://www.xs4all.nl/~rsmith/software/',
      license=lpver.license,
      scripts=['lamprop'],
      py_modules=['lpfile', 'lpouthtml', 'lpoutlatex',
                  'lpouttext', 'lptypes', 'lpver']
      )
