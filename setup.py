# -*- coding: utf-8 -*-
# Installation script for lamprop.
#
# R.F. Smith <rsmith@xs4all.nl>
# Time-stamp: <2011-12-18 14:12:02 rsmith>

from distutils.core import setup
import lpver

with open('README.txt') as f:
    ld = f.read()

setup(name=lpver.name,
      version=lpver.version,
      description='Calculates elastic properties of fibrous composites',
      author='Roland Smith',
      author_email='rsmith@xs4all.nl',
      url='http://www.xs4all.nl/~rsmith/software/',
      scripts=['lamprop.py'],
#      data_files=[('share/doc/lamprop', ['lamprop.1.pdf', 'lamprop.5.pdf'])],
      requires=['numpy'],
      provides=[lpver.name],
      py_modules=['lpfile', 'lpouthtml', 'lpoutlatex',
                  'lpouttext', 'lptypes', 'lpver'],
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Environment :: Console',
                   'Intended Audience :: End Users/Desktop',
                   'Intended Audience :: Manufacturing',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2.7',
                   'Topic :: Scientific/Engineering'
                   ],
      long_description = ld
      )
