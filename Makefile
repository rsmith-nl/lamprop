.PHONY: all install uninstall dist clean check refresh test setver

# Installation locations
PREFIX=/usr/local
MANDIR=$(PREFIX)/man
BINDIR=$(PREFIX)/bin

# Leave these two as they are.
SUBDIR=doc
DISTFILES=README.rst

# Default target.
all: lamprop ${SUBDIR}

lamprop: src/__main__.py src/lamprop/*.py
	python3 build.py

${SUBDIR}::
	cd ${.TARGET}; make ${.TARGETS}

# Install lamprop and its documentation.
install: lamprop
# Install the zipped script.
	install -d ${BINDIR}
	install lamprop ${BINDIR}
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
	rm -f ${BINDIR}/lamprop $(MANDIR)/man1/lamprop.1* \
	$(MANDIR)/man5/lamprop.5*

clean: ${SUBDIR}
	rm -rf lamprop backup-*.tar*
	find . -type f -name '*.pyc' -delete
	find . -type d -name __pycache__ -delete

# The specifications below are for the maintainer only.
check:: .IGNORE
	pep8 src/__main__.py src/lamprop/*.py test/test*.py

refresh::
	.git/hooks/post-commit

tests::
	nosetests-3.5 -v -w test
