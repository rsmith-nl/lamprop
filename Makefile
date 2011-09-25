.PHONY: help install dist clean backup
.SUFFIXES: .ps .pdf 

MANBASE=/usr/local/man

all: lamprop.1 lamprop.5 lpver.py .git/hooks/post-commit tools/replace.sed

install: lamprop.1 lamprop.5 lpver.py
	if [ `id -u` != 0 ]; then \
		echo "You must be root to install the program!"; \
		exit 1; \
	fi
	python setup.py install
	rm -rf build
	gzip -k lamprop.1 lamprop.5
	install -m 644 lamprop.1.gz $(MANBASE)/man1
	install -m 644 lamprop.5.gz $(MANBASE)/man5
	rm -f lamprop.1.gz lamprop.5.gz

dist: all lamprop.1 lamprop.1.pdf lamprop.5 lamprop.5.pdf
	python setup.py sdist

clean::
	rm -rf dist py-lamprop-*.tar.gz *.pyc lamprop.1 lamprop.5 lamprop.1.pdf lamprop.5.pdf lpver.py

backup::
	sh tools/genbackup

.git/hooks/post-commit: tools/post-commit
	install -m 755 $> $@

lamprop.1: lamprop.1.in tools/replace.sed
	sed -f tools/replace.sed lamprop.1.in >$@

lamprop.1.pdf: lamprop.1
	mandoc -Tps $> >$*.ps
	epspdf $*.ps
	rm -f $*.ps

lamprop.5: lamprop.5.in tools/replace.sed
	sed -f tools/replace.sed lamprop.5.in >$@

lamprop.5.pdf: lamprop.5
	mandoc -Tps $> >$*.ps
	epspdf $*.ps
	rm -f $*.ps

lpver.py: lpver.in.py tools/replace.sed
	sed -f tools/replace.sed lpver.in.py > $@

tools/replace.sed: .git/index
	tools/post-commit