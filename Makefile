.PHONY: all install dist clean backup
.SUFFIXES: .ps .pdf .py

#beginskip
PROG = lamprop
ALL = ${PROG}.1 ${PROG}.1.pdf ${PROG}.5 ${PROG}.5.pdf lpver.py

all: ${ALL} .git/hooks/post-commit tools/replace.sed
#endskip
BASE=/usr/local
MANDIR=$(BASE)/man
BINDIR=$(BASE)/bin

install: ${PROG}.1 setup.py ${PROG}.py
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
	gzip -k ${PROG}.1
	install -m 644 ${PROG}.1.gz $(MANDIR)/man1
	rm -f ${PROG}.1.gz

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
	rm -rf dist build backup-*.tar.gz *.pyc ${ALL} MANIFEST lpver.py

backup:  ${ALL}
# Generate a full backup.
	sh tools/genbackup

.git/hooks/post-commit: tools/post-commit
	install -m 755 $> $@

tools/replace.sed: .git/index
	tools/post-commit

lpver.py: lpver.in.py
	sed -f tools/replace.sed lpver.in.py >$@

${PROG}.1: ${PROG}.1.in tools/replace.sed
	sed -f tools/replace.sed ${PROG}.1.in >$@

${PROG}.1.pdf: ${PROG}.1
	mandoc -Tps $> >$*.ps
	epspdf $*.ps
	rm -f $*.ps

${PROG}.5: ${PROG}.5.in tools/replace.sed
	sed -f tools/replace.sed ${PROG}.5.in >$@

${PROG}.5.pdf: ${PROG}.5
	mandoc -Tps $> >$*.ps
	epspdf $*.ps
	rm -f $*.ps
#endskip
