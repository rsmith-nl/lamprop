#!/usr/bin/env python3
# file: setup.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2018-01-22 18:05:56 +0100
# Last modified: 2018-05-10T14:16:51+0200

from setuptools import setup
from lamprop.version import __version__

with open('README.rst') as f:
    ld = f.read()

name = 'lamprop'
setup(
    name=name,
    version=__version__,
    description='Calculates elastic properties of fibrous composites',
    author='Roland Smith',
    author_email='rsmith@xs4all.nl',
    license='BSD',
    url='https://github.com/rsmith-nl/lamprop',
    install_requires=['numpy>=1.10'],
    provides=[name],
    packages=[name],
    entry_points={
        'console_scripts': ['lamprop = lamprop.console:main'],
        'gui_scripts': ['lamprop-gui = lamprop.gui:main']
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Win32',
        'Environment :: X11 Applications',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Manufacturing',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering'
    ],
    long_description=ld
)
