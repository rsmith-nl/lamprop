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
# Last modified: 2021-05-25T15:58:00+0200

all::
	@echo 'you can use the following commands:'
	@echo '* clean: remove all generated files.'
	@echo '* check: check all python files. (requires pylama)'
	@echo '* tags: regenerate tags file. (requires uctags)'
	@echo '* format: format the source. (requires black)'
	@echo '* test: run the built-in tests. (requires py.test)'
	@echo '* doc: build the documentation using LaTeX.'

clean::
	rm -f lamprop lamprop-gui backup-*.tar*
	find . -type f -name '*.pyc' -delete
	find . -type d -name __pycache__ -delete

# The targets below are mostly for the maintainer.
check:: .IGNORE
	pylama lp/*.py test/*.py console.py gui.py tools/*.py

tags::
	uctags -R --verbose

format::
	black lp/*.py test/*.py console.py gui.py tools/*.py

test::
	py.test -v

doc::
	cd $(SUBDIR); make
