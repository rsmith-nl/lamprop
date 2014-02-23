# -*- coding: utf-8 -*-
# Installation script for lamprop.
# R.F. Smith <rsmith@xs4all.nl>
# $Date$

from setuptools import setup, find_packages

with open('README.txt') as f:
    ld = f.read()

name = 'lamprop'

setup(
    name=name,
    version='$Revision$'[11:-2],
    packages=find_packages(),
    scripts=['lamprop.py'],

    # This program requires numpy
    install_requires=['numpy>=1.7'],

    package_data={
        '': ['Makefile', 'lamprop.?', 'lamprop.?.pdf'],
        'test': ['hyer.lam'],
    },

    # Metadata
    author='Roland Smith',
    author_email='rsmith@xs4all.nl',
    description='Calculates elastic properties of fibrous composites',
    license='BSD',
    keywords="composites",
    url='http://rsmith.home.xs4all.nl/',
    classifiers=['Development Status :: 5 - Production/Stable',
                'Environment :: Console',
                'Intended Audience :: End Users/Desktop',
                'Intended Audience :: Manufacturing',
                'License :: OSI Approved :: BSD License',
                'Operating System :: OS Independent',
                'Programming Language :: Python :: 2.7',
                'Topic :: Scientific/Engineering'],
    long_description=ld
)
