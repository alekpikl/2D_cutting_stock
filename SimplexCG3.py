#!/usr/bin/env python

import numpy as np
from scipy import linalg
from Rectangular_Knapsack import SDP

def SimplexCG3(W,H,V,b,w,h,d,m):

    """

    :type instance: Instance
    """
    f = []
    for i in range(1,m):
        for j in range(1, m):
            if (w[i]<=W[j]) & (d[i]<=H[j]):
                f[i] = j
                break

    # Number of all possible patterns (2^m)
    n = 2**m
    x = d
    B = np.identity(m)
    # TODO: Inicializiraj C - C je v bistvu permutiran V. values of the bin type used in patterns 
    C = np.ones((n,), dtype=int)
    Cb = C[1:m]

    # TODO: A to dela tko, da ni returna po while loopu? 
    while(1):
        # TODO: Solve y_t * B = Cb_t ==> B_t * y = Cb
        y = linalg.solve(np.transpose(B), Cb );
        # 4
        for i in range(1,b):
            # TODO: define k? define SDP return value!
            z = SDP(W[i], H[i], w, h, y, k );
            if y * z > C[i]:
                break
            if i == b:
                return B,f,x
        # Solve B * w = z
        w = linalg.solve(B, z)

        i = 1
        j = 1

        t = min(x[j] / w[j] for j in range(1,m) if w[j] > 0)  # type: int
        s = min(j for j in range(1, m) if w[j]/w[j] > t)

        f[j] = i

        for i in range(1, m):
            B[i,s] = z[i]
            if i == s:
                x[i] = t
            else:
                x[i] = x[i] - w[i] * t



