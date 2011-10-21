.PHONY: help install dist clean backup
.SUFFIXES: .ps .pdf 

MANBASE=/usr/local/man

#beginskip
all: lamprop.1 lamprop.5 lpver.py .git/hooks/post-commit tools/replace.sed lamprop.1.pdf lamprop.5.pdf
#endskip
BINDIR=/usr/local/bin
install: lamprop.1 lamprop.5 lpver.py
	if [ `id -u` != 0 ]; then \
		echo "You must be root to install the program!"; \
		exit 1; \
	fi
	python setup.py install
	mv $(BINDIR)/lamprop.py $(BINDIR)/lamprop
	rm -rf build
	gzip -k lamprop.1 lamprop.5
	install -m 644 lamprop.1.gz $(MANBASE)/man1
	install -m 644 lamprop.5.gz $(MANBASE)/man5
	rm -f lamprop.1.gz lamprop.5.gz

#beginskip
dist: all lamprop.1 lamprop.1.pdf lamprop.5 lamprop.5.pdf
	mv Makefile Makefile.org
	awk -f tools/makemakefile.awk Makefile.org >Makefile
	python setup.py sdist --format=zip
	mv Makefile.org Makefile
	rm -f MANIFEST

clean::
	rm -rf dist backup-*.tar.gz *.pyc lamprop.1 lamprop.5 lamprop.1.pdf lamprop.5.pdf lpver.py MANIFEST

backup::
	sh tools/genbackup

.git/hooks/post-commit: tools/post-commit
	install -m 755 $> $@

lamprop.1: lamprop.1.in tools/replace.sed
	sed -f tools/replace.sed lamprop.1.in >$@

lamprop.5: lamprop.5.in tools/replace.sed
	sed -f tools/replace.sed lamprop.5.in >$@

lpver.py: lpver.in.py tools/replace.sed
	sed -f tools/replace.sed lpver.in.py > $@

tools/replace.sed: .git/index
	tools/post-commit

lamprop.1.pdf: lamprop.1
	mandoc -Tps $> >$*.ps
	epspdf $*.ps
	rm -f $*.ps

lamprop.5.pdf: lamprop.5
	mandoc -Tps $> >$*.ps
	epspdf $*.ps
	rm -f $*.ps
#endskip
