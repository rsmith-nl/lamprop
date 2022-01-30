# file: Makefile
# vim:fileencoding=utf-8:fdm=marker:ft=make
#
# Copyright © 2018 R.F. Smith <rsmith@xs4all.nl>
# Created: 2018-05-15T01:05:44+0200
# Last modified: 2022-01-30T12:34:22+0100
.SUFFIXES:
.PHONY: clean

DOCSRC:= lamprop-manual.tex
DOCPDF:= ${DOCSRC:.tex=.pdf}
LMKARGS:=-bibtex -pdfxe -silent -file-line-error -halt-on-error

all:  ${DOCPDF}

${DOCPDF}: ${DOCSRC} lman.bib
	-latexmk ${LMKARGS} ${DOCSRC} 2>&1

clean::
	latexmk -c >/dev/null 2>&1
