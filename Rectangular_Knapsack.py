#!/usr/bin/env python

# k-staged RK problem algorithm

import numpy as np
import math
from operator import itemgetter


# Instance as Input - optimal solution for I: used for column generation
# W - bin width, H - bin height, w/h - strip width/height lists, v - y, k - number of cuts, m - nr of stripes
# returns the optimal k-staged solution for I
def SDP(W, H, w, h, v, k, m):
    # number of items smaller than width -> TODO: how to implement that bigger pieces be cut?
    r = sum(i <= W for i in w)
    s = sum(i <= H for i in h)
    p = w[w <= W]
    q = h[h <= H]

    V = np.matrix
    item = np.matrix
    guillotine = np.matrix
    position = np.matrix
    A = ''

    for i in range(1, r):  # type: int
        for j in range(1, s):
            V[0, i, j] = max(v[f] for f in range(1, m) if (w[f] <= p[i]) & (h[f] <= q[j]))
            item[0, i, j] = max(f for f in range(1, m) if (w[f] <= p[i]) & (h[f] <= q[j]) & (v[f] == V[0, i, j]))
            guillotine[0, i, j] = None

    if k % 2 == 0:
        A = 'H'
    else:
        A = 'V'

    for l in range(1, k):
        for i in range(2, r):
            for j in range(2, s):
                V[l,i,j] = V[l-1, i,j]
                guillotine[l,i,j] = 'P'
                if A == 'V':
                    n = max(f for f in range(1, s) if q[f] <= math.floor(q[j] / 2))
                    for y in range(1, n):
                        t = max(f for f in range(1, s) if q[f] <= q[j] - q[y])
                        if V[l, i, j] < V[l -1, i, y] + V[l, i, t]:
                            V[l, i, j] = V[l - 1, i, y] + V[l, i, t]
                            position[l, i, j] = q[y]
                            guillotine[l, i, j] = 'H'
                else:
                    n = max(f for f in range(1, r) if p[f] <= math.floor(p[i] / 2))
                    for x in range(1, n):
                        t = max(f for f in range(1, r) if p[f] <= p[i] - p[x])
                        if V[l, i, j] < V[l -1, x, j] + V[l, t, j]:
                            V[l, i, j] = V[l - 1, x, j] + V[l, t, j]
                            position[l, i, j] = p[x]
                            guillotine[l, i, j] = 'V'

        if A == 'V':
            A = 'H'
        else:
            A = 'V'
    # TODO: kaj naj returnam?? rabim optimalen stolpec.
    return
