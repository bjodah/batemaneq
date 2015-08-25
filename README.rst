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
The Thorium series `decay chain <https://en.wikipedia.org/wiki/Decay_chain>`_ (with half-lives shorter than 1h excluded):

.. code:: python

   >>> from batemaneq import bateman_parent
   >>> from math import log
   >>> d = 1./365  # Th-232 Ra-228 Ac-228 Th-228
   >>> h = d/24    # Ra-224 Pb-212 Bi-212 (Pb-208)
   >>> Thalf = [1.405e10, 5.75, 6.25*h, 1.9116, 3.6319*d, 10.64*h, 60.55/60*h]
   >>> bateman_parent([log(2)/x for x in Thalf], 100)  # 100 years
   [0.9999999950665681, 4.0925028658312447e-10, 5.078051001187696e-14,
   1.3605575316895603e-10, 7.082081172329036e-13, 8.64484883194704e-14,
   8.199335787638167e-15]


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
