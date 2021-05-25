Reversing laminates with comments
#################################

:date: 2021-05-25
:tags: lamprop, symmetric
:author: Roland Smith

.. Last modified: 2021-05-25T08:49:23+0200
.. vim:spelllang=en

.. PELICAN_END_SUMMARY

The lamprop file format has the ``s:`` operator to make a laminate symmetric.

If the laminate is just a list of ``Lamina``, then we just add a reversed copy
of the list at the end of it.
But now that I want to be able to use comments in the lamina list, it becomes
more complicated.

Consider the following::

    layers = ["a", 1, 2, "b", 3, 4, "symm"]

For now, we will say that the numbers are lamina, and the strings are
comments.

First, we need to determine where the strings are positioned in the list::

    idx = [n for n, v in enumerate(layers) if isinstance(v, str)]

In this case, ``idx`` has the value ``[0, 3, 6]``.
To manipulate the list, we need to make this into a list of reversed pairs, like this::

    pairs = list(zip(idx[:-1], idx[1:]))[::-1]

This will have the value ``[(3, 6), (0, 3)]``.
Let's now construct the list extension::

    extension = []
    for s, e in pairs:
        extension += [layers[s]]+layers[s+1:e][::-1]

This yields ``['b', 4, 3, 'a', 2, 1]`` for ``extension``.

Note that this *only* works well if the list start and ends with a string!
So if necessary, we will add strings at the beginning and end of ``layers``.
