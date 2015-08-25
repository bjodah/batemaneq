#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from batemaneq import bateman_full


def solution3(u0=1.0, v0=0.7, w0=0.3, k0=1.0, k1=2.0, k2=3.0, tend=10.0,
              nt=100, plot=False, savefig='None'):
    """
    Example program calculating the trajectory of 3 coupled decays
    """
    tout = np.linspace(0, tend, nt)
    yout = np.asarray(bateman_full([u0, v0, w0], [k0, k1, k2],
                                   tout, exp=np.exp)).T
    if plot:
        import matplotlib.pyplot as plt
        plt.plot(tout, yout)
        if savefig == 'None':
            plt.show()
        else:
            plt.savefig(savefig)


if __name__ == '__main__':
    try:
        import argh
        argh.dispatch_command(solution3)
    except ImportError:
        solution3()
