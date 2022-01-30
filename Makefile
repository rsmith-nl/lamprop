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
# Last modified: 2022-01-30T13:43:59+0100
.PHONY: clean check format test doc zip

.if make(zip)
TAGCOMMIT!=git rev-list --tags --max-count=1
TAG!=git describe --tags ${TAGCOMMIT}
.endif

all::
	@echo 'you can use the following commands:'
	@echo '* clean: remove all generated files.'
	@echo '* check: check all python files. (requires pylama)'
	@echo '* tags: regenerate tags file. (requires uctags)'
	@echo '* format: format the source. (requires black)'
	@echo '* test: run the built-in tests. (requires py.test)'
	@echo '* doc: build the documentation using LaTeX.'
	@echo '* zip: create a zipfile of the latest tagged version.'

clean::
	rm -f lamprop lamprop-gui backup-*.tar* lamprop-*.zip
	find . -type f -name '*.pyc' -delete
	find . -type d -name __pycache__ -delete
	cd doc && make clean

# The targets below are mostly for the maintainer.
check:: .IGNORE
	pylama lp/*.py test/*.py console.py gui.py tools/*.py

tags::
	uctags -R --languages=Python

format::
	black lp/*.py test/*.py console.py gui.py tools/*.py

test::
	py.test -v

doc::
	cd doc/; make

zip:: clean
	cd doc && make clean
	git checkout ${TAG}
	cd .. && zip -r lamprop-${TAG}.zip lamprop \
		-x 'lamprop/.git/*' '*/.pytest_cache/*' '*/__pycache__/*' '*/.cache/*'
	git checkout main
	mv ../lamprop-${TAG}.zip .
