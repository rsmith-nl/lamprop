.PHONY: help install dist clean backup

help:
	@echo "Use 'make install' as root to install py-lamprop."
	@echo "Use 'make dist' to create a software distribution."
	@echo "Use 'make clean' to remove all generated files."
	@echo "Use 'make backup' to create a complete backup."

install::
	@if [ `id -u` != 0 ]; then \
		echo "You must be root to install the program!"; \
		exit 1; \
	fi
	@python setup.py install

dist::
	@python setup.py sdist

clean::
	@rm -rf dist build py-lamprop-*.tar.gz

backup::
	@sh tools/genbackup
