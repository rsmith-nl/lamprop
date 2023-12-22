#!/bin/sh
# file: find-log.sh
# vim:fileencoding=utf-8:ft=sh
#
# Find all the lines in the source code where the Logging functions or Logger
# methods error, warning, debug or info are used.
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2015-04-14 14:15:00 +0200

find . -type f -name '*.py' -exec egrep -H -B 1 '\.(error|warning|debug|info)' {} \;
