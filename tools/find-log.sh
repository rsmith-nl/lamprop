#!/bin/sh
# file: find-log.sh
# vim:fileencoding=utf-8:ft=sh
#
# Find all the lines in the source code where the Logging functions or Logger
# methods error or warning are used.
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2015-04-14 14:15:00 +0200
# Last modified: 2016-06-05 21:29:06 +0200

find src -type f -name '*.py' -exec egrep -H -B 1 '\.(error|warning)\(' {} \;
