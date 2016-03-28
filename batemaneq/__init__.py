# -*- coding: utf-8 -*-
"""
batemaneq provides a Python package for evaluating the Bateman equation
"""
from __future__ import absolute_import

from ._release import __version__
from .bateman import bateman_parent, bateman_full
from ._bateman_double import bateman_parent as bateman_parent_arr
from ._bateman_double import bateman_full as bateman_full_arr
