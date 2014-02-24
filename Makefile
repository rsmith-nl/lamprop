.PHONY: all install dist clean check refresh

# Installation locations
BASE=/usr/local
MANDIR=$(BASE)/man
BINDIR=$(BASE)/bin

# Leave these two as they are.
SUBDIR=doc
VER!=grep Revision src/__main__.py | cut -d ' ' -f 4
DISTFILES=Makefile README.txt

# Default target.
lamprop: src/__main__.py src/lamprop/*.py
	cd src; zip -q ../foo.zip __main__.py lamprop/*.py
	echo '#!/usr/bin/env python' >lamprop
	cat foo.zip >>lamprop
	chmod a+x lamprop
	rm -f foo.zip

install: lamprop
	@if [ `id -u` != 0 ]; then \
		echo "You must be root to install the program!"; \
		exit 1; \
	fi
# Install the zipped script.
	install lamprop ${BINDIR}
# Install the manual page.
	gzip -c doc/lamprop.1 >lamprop.1.gz
	gzip -c doc/lamprop.5 >lamprop.5.gz
	install -m 644 lamprop.1.gz $(MANDIR)/man1
	install -m 644 lamprop.5.gz $(MANDIR)/man5
	rm -f lamprop.1.gz lamprop.5.gz

dist: ${SUBDIR} lamprop
	rm -rf dist
	mkdir -p dist/lamprop-${VER}/src/lamprop
	ln lamprop dist/lamprop-${VER}
	for f in ${DISTFILES}; do \
		ln $$f dist/lamprop-${VER}/$${f} ; \
	done
	for f in $$(find src/ -type f -name '*.py'); do \
		ln $$f dist/lamprop-${VER}/$${f} ; \
	done
	mkdir -p dist/lamprop-${VER}/doc
	for f in $$(ls doc/lamprop.*); do \
		ln $$f dist/lamprop-${VER}/$${f} ; \
	done
	mkdir -p dist/lamprop-${VER}/test
	ln test/hyer.lam dist/lamprop-${VER}/test/hyer.lam
	cd dist; zip -r lamprop-${VER}.zip lamprop-${VER}
	rm -rf dist/lamprop-${VER}

clean: ${SUBDIR}
	rm -rf lamprop dist backup-*.tar.gz src/lamprop/*.pyc

check:: .IGNORE
	flake8 src/__main__.py src/lamprop/*.py

refresh::
	.git/hooks/post-commit
