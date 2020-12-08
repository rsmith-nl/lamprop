# file: Makefile
# vim:fileencoding=utf-8:fdm=marker:ft=make
#
# NOTE: This Makefile is only useful on UNIX-like operating systems!
#       It will *not* work on ms-windows! Building the documentation requires
#       a working LaTeX installation.
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2018-01-21 22:44:51 +0100
# Last modified: 2020-12-08T20:28:39+0100

.PHONY: all install dist clean check tags format test doc

# Default target.
all::
	@echo 'you can use the following commands:'
	@echo '* install'
	@echo '* clean: remove all generated files.'
	@echo '* check: run pylama on all python files.'
	@echo '* tags: run uctags.'
	@echo '* format: format the source with black.'
	@echo '* test: run the built-in tests.'
	@echo '* doc: build the documentation using LaTeX.'

# Install lamprop and its documentation.
install::
# Install the programs
	setup.py install

clean:
	rm -f lamprop lamprop-gui backup-*.tar*
	find . -type f -name '*.pyc' -delete
	find . -type d -name __pycache__ -delete

# The targets below are mostly for the maintainer.
check:: .IGNORE
	pylama lp/*.py test/*.py console.py gui.py build.py tools/*.py

tags::
	uctags -R --verbose

format::
	black lp/*.py test/*.py console.py gui.py build.py tools/*.py

test::
	py.test -v

doc::
	cd $(SUBDIR); make
