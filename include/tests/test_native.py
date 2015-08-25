# -*- coding: utf-8 -*-

import os
import subprocess


def test_native():
    cwd = os.path.dirname(__file__)
    if cwd == '':
        cwd = None
    p = subprocess.Popen(['make', '-B'], cwd=cwd)
    assert p.wait() == os.EX_OK

    p = subprocess.Popen(['make', '-B', 'MULTIPRECISION_DIGITS10=32'], cwd=cwd)
    assert p.wait() == os.EX_OK

if __name__ == '__main__':
    test_native()
