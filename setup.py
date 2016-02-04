#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Tested with boost GCC 4.8.3

import os
import shutil
import sys
from distutils.core import setup
from distutils.extension import Extension
import numpy as np


pkg_name = 'batemaneq'

# Cythonize .pyx file if it exists (not in source distribution)
ext_modules = []

if len(sys.argv) > 1 and '--help' not in sys.argv[1:] and sys.argv[1] not in (
            '--help-commands', 'egg_info', 'clean', '--version'):
    USE_CYTHON = os.path.exists('batemaneq/_bateman_double.pyx')
    ext = '.pyx' if USE_CYTHON else '.cpp'
    sources = ['src/bateman_double.cpp', 'batemaneq/_bateman_double'+ext]
    ext_modules = [
        Extension('batemaneq._bateman_double', sources, language='c++',
                  extra_compile_args=['-std=c++11'],
                  include_dirs=['./include'])
    ]
    if USE_CYTHON:
        from Cython.Build import cythonize
        ext_modules = cythonize(ext_modules, include_path=['./include'],
                                gdb_debug=True)

BATEMANEQ_RELEASE_VERSION = os.environ.get('BATEMANEQ_RELEASE_VERSION', '')

# http://conda.pydata.org/docs/build.html#environment-variables-set-during-the-build-process
CONDA_BUILD = os.environ.get('CONDA_BUILD', '0') == '1'
if CONDA_BUILD:
    try:
        BATEMANEQ_RELEASE_VERSION = 'v' + open(
            '__conda_version__.txt', 'rt').readline().rstrip()
    except IOError:
        pass

release_py_path = os.path.join(pkg_name, '_release.py')

if len(BATEMANEQ_RELEASE_VERSION) > 1 and BATEMANEQ_RELEASE_VERSION[0] == 'v':
    TAGGED_RELEASE = True
    __version__ = BATEMANEQ_RELEASE_VERSION[1:]
else:
    TAGGED_RELEASE = False
    # read __version__ attribute from release.py:
    exec(open(release_py_path).read())

classifiers = [
    "Development Status :: 4 - Beta",
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Mathematics',
]

tests = [
    'batemaneq.tests',
]

long_description = open('README.rst').read()
with open(os.path.join(pkg_name, '__init__.py')) as f:
    short_description = f.read().split('"""')[1]

setup_kwargs = dict(
    name=pkg_name,
    version=__version__,
    description=short_description,
    classifiers=classifiers,
    author='Björn Dahlgren',
    author_email='bjodah@DELETEMEgmail.com',
    license='BSD',
    url='https://github.com/bjodah/' + pkg_name,
    packages=[pkg_name] + tests,
    ext_modules=ext_modules,
    include_dirs=[np.get_include(), './include']
)

if __name__ == '__main__':
    try:
        if TAGGED_RELEASE:
            # Same commit should generate different sdist
            # depending on tagged version (set BATEMANEQ_RELEASE_VERSION)
            # this will ensure source distributions contain the correct version
            shutil.move(release_py_path, release_py_path+'__temp__')
            open(release_py_path, 'wt').write(
                "__version__ = '{}'\n".format(__version__))
        setup(**setup_kwargs)
    finally:
        if TAGGED_RELEASE:
            shutil.move(release_py_path+'__temp__', release_py_path)
