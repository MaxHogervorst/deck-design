"""Euler-Bernoulli beam demand helper; no resistance approval."""
import numpy as np
def beam(points, supports, EI):
    xs = np.array(sorted(set((round(float(x), 8) for x in points))))
    n = len(xs)
    K = np.zeros((2 * n, 2 * n))
    elems = []
    for i in range(n - 1):
        L = xs[i + 1] - xs[i]
        ke = EI / L ** 3 * np.array([[12, 6 * L, -12, 6 * L], [6 * L, 4 * L * L, -6 * L, 2 * L * L], [-12, -6 * L, 12, -6 * L], [6 * L, 2 * L * L, -6 * L, 4 * L * L]])
        ix = np.arange(2 * i, 2 * i + 4)
        K[np.ix_(ix, ix)] += ke
        elems.append((L, ke, ix))
    fixed = np.array([2 * int(np.argmin(abs(xs - s))) for s in supports])
    free = np.array([j for j in range(2 * n) if j not in fixed])

    def uniform(qfun):
        f = np.zeros(2 * n)
        qs = []
        for i, (L, ke, ix) in enumerate(elems):
            q = qfun((xs[i] + xs[i + 1]) / 2)
            qs.append(q)
            f[ix] += q * np.array([L / 2, L * L / 12, L / 2, -L * L / 12])
        return (f, np.array(qs))

    def solve(F):
        if F.ndim == 1:
            F = F[:, None]
        D = np.zeros(F.shape)
        D[free] = np.linalg.solve(K[np.ix_(free, free)], F[free])
        R = (K @ D - F)[fixed]
        return (D, -R)

    def moments(D, Q):
        vals = []
        if Q.ndim == 1:
            Q = Q[:, None]
        for i, (L, ke, ix) in enumerate(elems):
            v = ke @ D[ix] - np.array([L / 2, L * L / 12, L / 2, -L * L / 12])[:, None] * Q[i]
            vals.extend([v[1], v[3]])
        return np.array(vals)
    return (xs, uniform, solve, moments)
