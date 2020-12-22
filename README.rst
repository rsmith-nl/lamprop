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

As of version 2020-12-22. the internals have been updated to use

* Halpin-Tsai approximation for E2 and to help calculate Ez,
* periodic micromechanics model for single plies and
* first order shear deformation theory for laminates.

This helps yield better data for FEA.


This program can _not_ calculate the strength of composite laminates;
because there are many different failure modes, strengths of composite
laminates cannot readily be calculated from the strengths of the separate
materials that form the laminate. These strengths have to be determined
from tests.

The program has options for producing LaTeX and HTML output in addition to
plain text output.

The program and its file format are documented by a manual. This can be found
in the ``doc`` subdirectory.

There are basically two versions of this program; a console version primarily
meant for POSIX operating systems and a GUI version primarily meant for
ms-windows.

You can try both versions without installing them first, with the following
invocations in a shell from the root directory of the repository.

Use ``python console -h`` for the console version, and ``python gui`` for the
GUI version.


Of note
-------

As of version 3 (2017-02-25), support for old style fiber properties (which
also specified properties in the radial direction of the fiber) has been
removed from the code.
In the ``tools`` subdirectory of the source distribution a script called
``convert-lamprop.py`` has been provided to convert old-style lamprop files to
the new format.

On 2020-10-03, lamprop has switched to using the release date as the version.
So 4.2 became 2020-03-13.

The installed scripts are an archive of compiled Python bytecode.
This means that you have to re-install lamprop after updating Python to a new
version.


Requirements
------------

This program requires at least Python 3.6. It is *not* compatible with Python 2!
It has no library requirments outside of the Python standard library.
This version was developed and tested using Python 3.7 and 3.9.


Developers
++++++++++

You will need py.test_ to run the provided tests. Code checks are done using
pylama_. Both should be invoked from the root directory of the repository.

.. _py.test: https://docs.pytest.org/
.. _pylama: http://pylama.readthedocs.io/en/latest/


Installation
------------

To install it for the local user, run::

    python setup.py install

This will install it in the user path for Python scripts.
For POSIX operating systems this is ususally ``~/.local/bin``.
For ms-windows this is the ``Scripts`` directory of your Python installation
or another local directory.
Make sure that this directory is in your ``$PATH`` environment variable.

On a UNIX-like operating system, you can run ``make install`` as root instead
for a system-wide install. This will additionally install the manual.
By default, this install is done in the ``/usr/local/`` tree.
Change the PREFIX variable in the Makefile in case you want to install
somewhere else.


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

