.PHONY: all install dist clean backup check refresh
.SUFFIXES: .ps .pdf .py

SUBDIR= doc

PROG= lamprop
#beginskip
PYFILES!=ls *.py

all: ${SUBDIR} lamprop
#endskip
SCRIPTNAME = lamprop.py
BASE=/usr/local
MANDIR=$(BASE)/man
BINDIR=$(BASE)/bin

lamprop: src/lamprop.py src/lamprop/*.py
	cd src; zip -q ../lamprop lamprop/*.py
	cp -p src/lamprop.py __main__.py
	zip -q lamprop __main__.py
	echo '#!/usr/bin/env python' >lamprop
	cat lamprop.zip >>lamprop
	chmod a+x lamprop
	rm -f lamprop.zip __main__.py

install: lamprop
	@if [ `id -u` != 0 ]; then \
		echo "You must be root to install the program!"; \
		exit 1; \
	fi
# Installt the zipped script.
	install lamprop ${BINDIR}
# Install the manual page.
	gzip -c doc/lamprop.1 >lamprop.1.gz
	gzip -c doc/lamprop.5 >lamprop.5.gz
	install -m 644 lamprop.1.gz $(MANDIR)/man1
	install -m 644 lamprop.5.gz $(MANDIR)/man5
	rm -f lamprop.1.gz lamprop.5.gz

#beginskip
dist: ${SUBDIR}
# Make simplified makefile.
	mv Makefile Makefile.org
	awk -f tools/makemakefile.awk Makefile.org >Makefile
# Create distribution file. Use zip format to make deployment easier on windoze.
	python setup.py sdist --format=zip
	mv Makefile.org Makefile
	rm -f lamprop.egg-info

clean: ${SUBDIR}
	rm -rf lamprop dist build backup-*.tar.gz *.pyc __pycache__ MANIFEST

check:: .IGNORE
	pylint --rcfile=tools/pylintrc src/lamprop.py src/lamprop/*.py

refresh::
	.git/hooks/post-commit

#endskip
