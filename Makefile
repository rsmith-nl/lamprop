# file: Makefile
# vim:fileencoding=utf-8:fdm=marker:ft=make
#
# NOTE: This Makefile is only intended for developers.
#       It is only meant for UNIX-like operating systems.
#       Most of the commands require extra software.
#       Building the documentation requires a working LaTeX installation.
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2018-01-21 22:44:51 +0100
# Last modified: 2023-11-13T10:15:26+0100
.POSIX:
.PHONY: clean check format test doc zip
.SUFFIXES:

PROJECT:=lamprop

.if make(zip)
TAGCOMMIT!=git rev-list --tags --max-count=1
TAG!=git describe --tags ${TAGCOMMIT}
.endif

# For a Python program, help is the default target.
all::
	@echo "Command  Meaning"
	@echo "-------  -------"
	@sed -n -e '/##/s/:.*\#\#/\t/p' -e '/@sed/d' Makefile

clean:: ## remove all generated files.
	rm -f lamprop lamprop-gui
	rm -f backup-*.tar* ${PROJECT}-*.zip
	find . -type f -name '*.pyc' -delete
	find . -type d -name __pycache__ -delete
	cd doc && make clean

check:: .IGNORE ## check all python files. (requires pylama)
	pylama lp/*.py test/*.py console.py gui.py tools/*.py

tags:: ## regenerate tags file. (requires uctags)
	uctags -R --languages=Python

format:: ## format the source. (requires black)
	black lp/*.py test/*.py console.py gui.py tools/*.py

test:: ## run the built-in tests. (requires py.test)
	py.test -v

doc:: ## build the documentation using LaTeX.
	cd doc/; make

zip:: clean ## create a zip-file from the most recent tagged state of the repository.
	cd doc && make clean
	git checkout ${TAG}
	cd .. && zip -r ${PROJECT}-${TAG}.zip ${PROJECT} \
		-x '*/.git/*' '*/.pytest_cache/*' '*/__pycache__/*' '*/.cache/*'
	git checkout main
	mv ../${PROJECT}-${TAG}.zip .
