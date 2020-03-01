#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Tested with boost 1.59, GCC 4.8.3

import io
import os
import re
import shutil
import sys
from setuptools import setup
from setuptools.command.build_ext import build_ext
from setuptools.extension import Extension


pkg_name = 'batemaneq'

# Cythonize .pyx file if it exists (not in source distribution)
ext_modules = []


def _path_under_setup(*args):
    return os.path.join(os.path.dirname(__file__), *args)

USE_CYTHON = os.path.exists(_path_under_setup(
    pkg_name, '_bateman_double.pyx'))

if len(sys.argv) > 1 and '--help' not in sys.argv[1:] and sys.argv[1] not in (
            '--help-commands', 'egg_info', 'clean', '--version'):
    import numpy as np
    ext = '.pyx' if USE_CYTHON else '.cpp'
    sources = ['src/bateman_double.cpp', 'batemaneq/_bateman_double'+ext]
    ext_modules = [
        Extension('batemaneq._bateman_double', sources, language='c++',
                  include_dirs=[np.get_include(), './include'])
    ]
    if USE_CYTHON:
        from Cython.Build import cythonize
        ext_modules = cythonize(ext_modules, include_path=['./include'])

RELEASE_VERSION = os.environ.get('BATEMANEQ_RELEASE_VERSION', '')

# http://conda.pydata.org/docs/build.html#environment-variables-set-during-the-build-process
CONDA_BUILD = os.environ.get('CONDA_BUILD', '0') == '1'
if CONDA_BUILD:
    try:
        RELEASE_VERSION = 'v' + io.open('__conda_version__.txt', 'rt',
                                        encoding='utf-8').readline().rstrip()
    except IOError:
        pass

release_py_path = _path_under_setup(pkg_name, '_release.py')

if len(RELEASE_VERSION) > 1 and RELEASE_VERSION[0] == 'v':
    TAGGED_RELEASE = True
    __version__ = RELEASE_VERSION[1:]
else:
    TAGGED_RELEASE = False
    # read __version__ attribute from release.py:
    exec(io.open(release_py_path, encoding='utf-8').read())


class BuildExt(build_ext):
    """A custom build extension for adding compiler-specific options."""
    c_opts = {
        'msvc': ['/EHsc'],
        'unix': [],
    }

    def build_extensions(self):
        ct = self.compiler.compiler_type
        opts = self.c_opts.get(ct, [])
        if ct == 'unix':
            opts.append('-DVERSION_INFO="%s"' % self.distribution.get_version())
            opts.append('-std=c++11')
            if sys.platform == 'darwin' and re.search("clang", self.compiler.compiler[0]) is not None:
                opts += ['-stdlib=libc++', '-mmacosx-version-min=10.7']
        elif ct == 'msvc':
            opts.append('/DVERSION_INFO=\\"%s\\"' % self.distribution.get_version())
        for ext in self.extensions:
            ext.extra_compile_args = opts
        build_ext.build_extensions(self)

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

with io.open(_path_under_setup(pkg_name, '__init__.py'),
             'rt', encoding='utf-8') as f:
    short_description = f.read().split('"""')[1].split('\n')[1]
assert 10 < len(short_description) < 255
long_description = io.open(_path_under_setup('README.rst'),
                           encoding='utf-8').read()
assert len(long_description) > 100

setup_kwargs = dict(
    name=pkg_name,
    version=__version__,
    description=short_description,
    long_description=long_description,
    classifiers=classifiers,
    author='Björn Dahlgren',
    author_email='bjodah@DELETEMEgmail.com',
    license='BSD',
    url='https://github.com/bjodah/' + pkg_name,
    packages=[pkg_name] + tests,
    install_requires=['numpy'] + (['cython'] if USE_CYTHON else []),
    setup_requires=['numpy'] + (['cython'] if USE_CYTHON else []),
    ext_modules=ext_modules,
    cmdclass={'build_ext': BuildExt},
    zip_safe=False,
)

if __name__ == '__main__':
    try:
        if TAGGED_RELEASE:
            # Same commit should generate different sdist
            # depending on tagged version (set BATEMANEQ_RELEASE_VERSION)
            # this will ensure source distributions contain the correct version
            shutil.move(release_py_path, release_py_path+'__temp__')
            io.open(release_py_path, 'wt', encoding='utf-8').write(
                "__version__ = '{}'\n".format(__version__))
        setup(**setup_kwargs)
    finally:
        if TAGGED_RELEASE:
            shutil.move(release_py_path+'__temp__', release_py_path)
