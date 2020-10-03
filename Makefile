# file: Makefile
# vim:fileencoding=utf-8:fdm=marker:ft=make
#
# NOTE: This Makefile is only useful on UNIX-like operating systems!
#       It will *not* work on ms-windows! Building the documentation requires
#       a working LaTeX installation.
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2018-01-21 22:44:51 +0100
# Last modified: 2020-10-03T14:08:48+0200

.PHONY: all build uninstall dist clean check tags format test doc

# Installation locations
PREFIX:=/usr/local
BINDIR:=$(PREFIX)/bin
DOCDIR:=$(PREFIX)/share/doc/lamprop
PKGPATH!=python3 -c "import site; print(site.getsitepackages()[0])"

# Leave these two as they are.
SUBDIR:=doc
DISTFILES:=README.rst

# Default target.
all::
	@echo 'you can use the following commands:'
	@echo '* test: run the built-in tests.'
	@echo '* build: create the self-contained programs.'
	@echo '* install'
	@echo '* uninstall'
	@echo '* dist: create a distribution file.'
	@echo '* clean: remove all generated files.'
	@echo '* check: run pylama on all python files.'
	@echo '* tags: run uctags.'
	@echo '* format: format the source with yapf.'
	@echo '* doc: build the documentation using LaTeX.'

# Install lamprop and its documentation.
install: build
	@if [ `id -u` != 0 ]; then \
		echo "You must be root to install the software!"; \
		exit 1; \
	fi
# Install the programs
	install lamprop $(BINDIR)
	install lamprop-gui $(BINDIR)
# Install the manual.
	mkdir -p $(DOCDIR)
	install -m 644 doc/lamprop-manual.pdf $(DOCDIR)

build: lamprop

lamprop: console.py gui.py lp/*.py
	./build.py

# Remove an installed lamprop completely
uninstall::
	@if [ `id -u` != 0 ]; then \
		echo "You must be root to uninstall the software!"; \
		exit 1; \
	fi
	rm -rf $(BINDIR)/lamprop*
	rm -rf $(DOCDIR)/lamprop-manual.pdf

# Create distribution file. Use zip format to make deployment easier on windoze.
dist:
	python3 -B setup.py sdist --format=zip
	rm -f MANIFEST

clean:
	rm -f lamprop lamprop-gui backup-*.tar*
	find . -type f -name '*.pyc' -delete
	find . -type d -name __pycache__ -delete

# The targets below are mostly for the maintainer.
check:: .IGNORE
	pylama -i E501,E741,C901,W605 lp/*.py test/*.py console.py gui.py build.py tools/*.py

tags::
	uctags -R --verbose

format::
	yapf -i lp/*.py test/*.py console.py gui.py build.py tools/*.py

test::
	py.test -v

doc::
	cd $(SUBDIR); make
