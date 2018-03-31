# file: Makefile
# vim:fileencoding=utf-8:fdm=marker:ft=make
#
# NOTE: This Makefile is only useful on UNIX-like operating systems!
#       It will *not* work on ms-windows!
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2018-01-21 22:44:51 +0100
# Last modified: 2018-03-31 16:20:01 +0200

.PHONY: all install uninstall clean check test

# Installation locations
PREFIX=/usr/local
BINDIR=$(PREFIX)/bin
MANDIR=$(PREFIX)/man
PKGPATH!=python3 -c "import sys; print([p for p in sys.path if p.endswith('site-packages')][0])"

# Leave these two as they are.
SUBDIR=doc
DISTFILES=README.rst

# Default target.
all::
	@echo "use 'make install' the program"
	@echo "use 'make clean' to remove generated files."
	@echo "use 'make check' to run pylama."
	@echo "use 'make test' to run the test suite using py.test."

# Install lamprop and its documentation.
install:
	python3 setup.py install
	rm -rf build dist lamprop.egg-info
# Install the manual page.
	gzip -c doc/lamprop.1 >lamprop.1.gz
	gzip -c doc/lamprop.5 >lamprop.5.gz
	install -d $(MANDIR)/man1
	install -d $(MANDIR)/man5
	install -m 644 lamprop.1.gz $(MANDIR)/man1
	install -m 644 lamprop.5.gz $(MANDIR)/man5
	rm -f lamprop.1.gz lamprop.5.gz

# Remove an installed lamprop completely
uninstall::
	rm -rf $(PKGPATH)/lamprop*.egg
	rm -rf $(BINDIR)/lamprop*

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
	py.test-3.6 -v
