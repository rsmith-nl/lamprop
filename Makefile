# file: Makefile
# vim:fileencoding=utf-8:fdm=marker:ft=make
#
# NOTE: This Makefile is only useful on UNIX-like operating systems!
#       It will *not* work on ms-windows!
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2018-01-21 22:44:51 +0100
# Last modified: 2018-12-02T16:15:18+0100

.PHONY: all install uninstall clean check test doc

# Installation locations
PREFIX:=/usr/local
BINDIR:=$(PREFIX)/bin
DOCDIR:=$(PREFIX)/share/doc/lamprop
PKGPATH!=python3 -c "import sys; print([p for p in sys.path if p.endswith('site-packages')][0])"

# Leave these two as they are.
SUBDIR:=doc
DISTFILES:=README.rst

# Default target.
all::
	@echo "use 'make install' the program"
	@echo "use 'make clean' to remove generated files."
	@echo "use 'make check' to run pylama."
	@echo "use 'make test' to run the test suite using py.test."
	@echo "use 'make doc' to build the documentation using LaTeX."

# Install lamprop and its documentation.
install:
	python3 setup.py install
	rm -rf build dist lamprop.egg-info
# Install the manual.
	mkdir -p $(DOCDIR)
	install -m 644 doc/lamprop-manual.pdf $(DOCDIR)

# Remove an installed lamprop completely
uninstall::
	rm -rf $(PKGPATH)/lamprop*.egg
	rm -rf $(BINDIR)/lamprop*
	rm -rf $(DOCDIR)/lamprop-manual.pdf

clean:
	rm -rf backup-*.tar*
	rm -rf build
	rm -rf dist
	rm -rf lamprop.egg-info
	find . -type f -name '*.pyc' -delete
	find . -type d -name __pycache__ -delete

# The specifications below are for the maintainer only.
check:: .IGNORE
	pylama

test::
	py.test-3.7 -v

doc::
	cd $(SUBDIR); make
