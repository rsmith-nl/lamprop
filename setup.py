# -*- coding: utf-8 -*-
# Installation script for lamprop.
# R.F. Smith <rsmith@xs4all.nl>
# $Date$

from distutils.core import setup

with open('README.txt') as f:
    ld = f.read()

name = 'lamprop'
setup(name=name,
      version='$Revision$'[11:-2],
      description='Calculates elastic properties of fibrous composites',
      author='Roland Smith',
      author_email='rsmith@xs4all.nl',
      url='http://rsmith.home.xs4all.nl/software/',
      scripts=['lamprop'],
      data_files=[('share/doc/lamprop', ['doc/lamprop.1.pdf',
                                         'doc/lamprop.5.pdf'])],
      requires=['numpy'],
      provides=[name],
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Environment :: Console',
                   'Intended Audience :: End Users/Desktop',
                   'Intended Audience :: Manufacturing',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2.7',
                   'Topic :: Scientific/Engineering'
                   ],
      long_description=ld
      )
