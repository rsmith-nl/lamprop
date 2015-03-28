RTF output in lamprop
#####################

:date: 2015-03-28
:tags:
:author: Roland Smith

Introduction
============

To make life easier on those who are stuck with windows, I wanted to implement
Rich Text Format output for lamprop, to make it easier to paste lamprop output
into MS-word.

Resources
=========

`RTF 1.5 specification`_.

.. _RTF 1.5 specification: http://www.biblioscape.com/rtf15_spec.htm


Design choices
==============

The HTML and LaTeX formats use nested tables. It seems that this is supported
in recent versions of RTF but because it is cumbersome for me to do testing on
MS-windows I decided to do a straight port to the plain text output.

Using unicode
=============

Since this seems to be supported in RTF, I want to use the same unicode
characters that I use in the plain text output when stdout is utf-8 capable.
So I needed the ordinals of those characters;

.. code-block:: python

    In [13]: def utfnum(s):
    ....:     v = ord(s)
    ....:     print('utf-8: {}, decimal: {:04d}, hex: {:04x}'.format(s, v, v))
    ....:

    In [14]: utfnum('³')
    utf-8: ³, decimal: 0179, hex: 00b3

    In [15]: utfnum('²')
    utf-8: ², decimal: 0178, hex: 00b2

    In [16]: utfnum('⁻')
    utf-8: ⁻, decimal: 8315, hex: 207b

    In [17]: utfnum('¹')
    utf-8: ¹, decimal: 0185, hex: 00b9

    In [18]: utfnum('ν')
    utf-8: ν, decimal: 0957, hex: 03bd

    In [19]: utfnum('α')
    utf-8: α, decimal: 0945, hex: 03b1

The windows-1252 codepage contains ² and ³. For the other characters we use
the following replacements or alternatives;

* “K⁻¹“ is replaced by “1/K“,
* “ν” has alternative “v”,
* “α” has alternative “a”.

So “α_x = 3.003e-05 K⁻¹” becomes
“\u945a_x = 3.003e-05 {\upr{1/K}{\*\ud{K\u8315\u185}}}”.

