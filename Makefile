.PHONY: all install dist clean backup check refresh
.SUFFIXES: .ps .pdf .py

#beginskip
PROG = lamprop
ALL = ${PROG}.1.pdf ${PROG}.5.pdf
PYFILES!=ls *.py

all: ${ALL} ${PROG}.py .git/hooks/post-commit
#endskip
BASE=/usr/local
MANDIR=$(BASE)/man
BINDIR=$(BASE)/bin

install: ${ALL} ${PROG}.py
	@if [ `id -u` != 0 ]; then \
		echo "You must be root to install the program!"; \
		exit 1; \
	fi
# Let Python do most of the install work.
	python setup.py install
# Lose the extension; this is UNIX. :-)
	mv $(BINDIR)/${PROG}.py $(BINDIR)/${PROG}
	rm -rf build
#Install the manual page.
	gzip -c ${PROG}.1 >${PROG}.1.gz
	gzip -c ${PROG}.5 >${PROG}.5.gz
	install -m 644 ${PROG}.1.gz $(MANDIR)/man1
	install -m 644 ${PROG}.5.gz $(MANDIR)/man5
	rm -f ${PROG}.1.gz ${PROG}.5.gz

#beginskip
dist: ${ALL}
# Make simplified makefile.
	mv Makefile Makefile.org
	awk -f tools/makemakefile.awk Makefile.org >Makefile
# Create distribution file. Use zip format to make deployment easier on windoze.
	python setup.py sdist --format=zip
	mv Makefile.org Makefile
	rm -f MANIFEST

clean::
	rm -rf dist build backup-*.tar.gz *.pyc ${ALL} MANIFEST

backup:  ${ALL}
# Generate a full backup.
	sh tools/genbackup

check:: .IGNORE
	pylint -i y --rcfile=tools/pylintrc l*.py

.git/hooks/post-commit: tools/post-commit
	install -m 755 $> $@

${PROG}.1.pdf: ${PROG}.1
	mandoc -Tps $> >$*.ps
	epspdf $*.ps
	rm -f $*.ps

${PROG}.5.pdf: ${PROG}.5
	mandoc -Tps $> >$*.ps
	epspdf $*.ps
	rm -f $*.ps

refresh::
	rm -f ${PYFILES}
	git checkout ${PYFILES}

#endskip
