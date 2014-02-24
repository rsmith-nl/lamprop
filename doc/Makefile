.PHONY: all install dist clean backup check refresh
.SUFFIXES: .1 .5 .pdf

all: lamprop.1.pdf lamprop.5.pdf

lamprop.1.pdf: lamprop.1
	mandoc -Tps $> >$*.ps
	epspdf $*.ps
	rm -f $*.ps

lamprop.5.pdf: lamprop.5
	mandoc -Tps $> >$*.ps
	epspdf $*.ps
	rm -f $*.ps

clean::
	rm -f *.ps *.pdf
