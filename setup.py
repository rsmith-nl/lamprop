# -*- coding: utf-8 -*-
# Installation script for lamprop.
#
# R.F. Smith <rsmith@xs4all.nl>
# Time-stamp: <2011-09-25 13:27:38 rsmith>

from distutils.core import setup
import lpver

with open('README.txt') as file:
    ld = file.read()

setup(name=lpver.name,
      version=lpver.version,
      description='Program to calculate elastic properties of fibrous composites',
      author='Roland Smith',
      author_email='rsmith@xs4all.nl',
      url='http://www.xs4all.nl/~rsmith/software/',
      scripts=['lamprop'],
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
