=========
batemaneq
=========

.. image:: http://hera.physchem.kth.se:8080/github.com/bjodah/batemaneq/status.svg?branch=master
   :target: http://hera.physchem.kth.se:8080/github.com/bjodah/batemaneq
   :alt: Build status

``batemaneq`` provides a C++ implementation of the Bateman equation,
and a `Python <http://www.python.org>`_ bidning thereof. 

Example
=======
A length 3 decay chain

.. code:: python

   >>> from batemaneq import bateman_parent
   >>> y = bateman_parent(...)


License
=======
The source code is Open Source and is released under the very permissive
"simplified (2-clause) BSD license". See ``LICENSE.txt`` for further details.
Contributors are welcome to suggest improvements at https://github.com/bjodah/batemaneq

Author
======
Björn I. Dahlgren, contact:

- gmail address: bjodah
- kth.se address: bda
