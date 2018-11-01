=====================================================
Calculating elastic properties of composite laminates
=====================================================

The purpose of this program is to calculate some properties of
fiber-reinforced composite laminates. It calculates
- engineering properties like Ex, Ey, Gxy
- thermal properties CTE_x and CTE_y
- physical properties like density and laminate thickness
- stiffness and compliance matrices (ABD and abd)

Although these properties are not very difficult to calculate, (the relevant
equations and formulas can be readily found in the available composite
literature) the calculation is time-consuming and error-prone when done by
hand.

This program can _not_ calculate the strength of composite laminates;
because there are many different failure modes, strengths of composite
laminates cannot readily be calculated from the strengths of the separate
materials that form the laminate. These strengths have to be determined
from tests.

The program has options for producing LaTeX and HTML output in addition to
plain text output.

The program and its file format are documented by two manuals; lamprop.1 and
lamprop.5 respectively. If you install this program on UNIX-like systems with
'make install', these will be installed automatically. For users of other
systems, PDF versions are included in the distribution.

As of version 3, support for old style fiber properties (which also specified
properties in the radial direction of the fiber) has been removed from the
code. In the ``tools`` subdirectory of the source distribution a script called
``convert-lamprop.py`` has been provided to convert old-style lamprop files to
the new format.


Requirements
------------

This program requires Python (version 3), and the numpy module. This version
was developed and tested using Python 3.6 and numpy 1.11.2. But older versions
will probably work fine.

Developers
++++++++++

You will need py.test_ to run the provided tests. Code checks are done using
pylama_. Both should be invoked from the root directory of the repository.

.. _py.test: https://docs.pytest.org/
.. _pylama: http://pylama.readthedocs.io/en/latest/

There are basically two versions of this program; a console version (installed
as ``lamprop``) primarily meant for POSIX operating systems and a GUI version
(installed as ``lamprop-gui``) primarily meant for ms-windows.

You can try both versions without installing them first, with the following
invocations in a shell from the root directory of the repository.

Use ``python3 -m lamprop.console -h`` for the console version, and 
``python3 -m lamprop.gui`` for the GUI version.


Installation
------------

Run ``python3 setup.py install``. This will install both the module and the scripts
that use it.

Vim
+++

In the ``tools`` subdirectory you will find a vim_ syntax file for lamprop
files. If you want to use it, copy ``lamprop.vim`` to ``~/.vim/syntax``, and
set the filetype of your lamprop files to ``lamprop``.

.. _vim: http://www.vim.org

You can set the filetype by adding a modeline to your lamprop files:

.. code-block:: vim

    vim:ft=lamprop

This requires that modeline support is enabled. You should have the following
line in your ``vimrc``:

.. code-block:: vim

    set modeline

Alternatively, if you use the ``.lam`` extension for your lamprop files you
can use an autocommand in your ``vimrc``;

.. code-block:: vim

    autocmd BufNewFile,BufRead *.lam set filetype=lamprop

