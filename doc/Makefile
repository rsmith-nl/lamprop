# file: Makefile
# vim:fileencoding=utf-8:fdm=marker:ft=make
#
# Copyright © 2018 R.F. Smith <rsmith@xs4all.nl>
# Created: 2018-05-15T01:05:44+0200
# Last modified: 2018-05-15T01:08:47+0200
.SUFFIXES:
.PHONY: clean

VERSION!=awk '/GITHash/ {print(substr($$0, 15, 40));}' vc.tex

DOCSRC= lamprop-manual.tex
DOCPDF = ${DOCSRC:.tex=.pdf}
LMKARGS=-bibtex -pdfxe -silent -file-line-error -halt-on-error

all:  ${DOCPDF}

${DOCPDF}: *.tex
	-latexmk ${LMKARGS} ${DOCSRC} 2>&1

clean::
	latexmk -c
