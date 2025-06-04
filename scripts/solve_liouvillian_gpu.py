#!/usr/bin/env python
"""Solve coloured-noise Liouvillian on GPU.

This script constructs a time-convolutionless (TCL-2) Liouvillian using a
coloured-noise spectral density and computes its low-lying eigenvalues.
"""
from __future__ import annotations

import argparse
from typing import Iterable
import numpy as np
import qutip

try:
    import qutip.backends.cupy as qbc  # type: ignore
    HAS_GPU = True
except Exception:
    HAS_GPU = False

try:
    from qutip.krylov import eigs as krylov_eigs  # type: ignore
except Exception:  # pragma: no cover
    krylov_eigs = None

from qutip.qip.operations.gates import *  # noqa: F401,F403


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    """Parse the command line arguments."""
    parser = argparse.ArgumentParser(description="Solve Liouvillian eigenproblem")
    parser.add_argument("--ham", required=True, help="Hamiltonian expression")
    parser.add_argument("--A", type=float, default=1e-4, help="Spectral density amplitude")
    parser.add_argument("--alpha", type=float, default=1.0, help="Spectral density exponent")
    parser.add_argument("--wc", type=float, default=5.0, help="Cutoff frequency")
    parser.add_argument("--num_eval", type=int, default=10, help="Number of eigenvalues")
    return parser.parse_args(argv)


def spectral_density(w: float, A: float, alpha: float, wc: float) -> float:
    """Return the coloured-noise spectral density."""
    return A / (abs(w) ** alpha + wc ** alpha)


def build_liouvillian(H: qutip.Qobj, A: float, alpha: float, wc: float) -> qutip.Qobj:
    """Construct the TCL-2 Liouvillian with coloured noise."""
    energies = H.eigenenergies()
    w0 = float(np.max(energies) - np.min(energies))
    gamma = spectral_density(w0, A, alpha, wc)
    gamma_phi = spectral_density(0.0, A, alpha, wc)
    c_ops = [np.sqrt(gamma) * qutip.sigmam(), np.sqrt(gamma_phi) * qutip.sigmaz()]
    if HAS_GPU:
        H = qbc.to_gpu(H)
        c_ops = [qbc.to_gpu(c) for c in c_ops]
    L = qutip.liouvillian(H, c_ops)
    if HAS_GPU:
        L = qbc.to_gpu(L)
    return L


def dense_eigs(L: qutip.Qobj, k: int) -> tuple[np.ndarray, list[qutip.Qobj]]:
    """Compute eigenpairs using dense linear algebra."""
    vals, vecs = np.linalg.eig(L.full())
    idx = np.argsort(np.abs(vals))[:k]
    vals = vals[idx]
    vecs = vecs[:, idx]
    evecs = []
    dims = [[[L.dims[0][0][0]], [L.dims[0][1][0]]], [[1], [1]]]
    for i in range(vecs.shape[1]):
        qv = qutip.Qobj(vecs[:, i], dims=dims)
        evecs.append(qv)
    return vals, evecs


def compute_eigs(L: qutip.Qobj, k: int) -> tuple[np.ndarray, list[qutip.Qobj]]:
    """Return ``k`` smallest-magnitude eigenpairs of ``L``."""
    if krylov_eigs is not None:
        return krylov_eigs(L, k=k, sigma=0.0)
    return dense_eigs(L, k)


def main(argv: Iterable[str] | None = None) -> None:
    """Run the eigenproblem solver."""
    args = parse_args(argv)
    H = eval(args.ham)
    L = build_liouvillian(H, args.A, args.alpha, args.wc)
    vals, vecs = compute_eigs(L, args.num_eval)
    print(f"GPU enabled: {HAS_GPU}")
    print("index\tre(λ)\tim(λ)\tpurity")
    for i, (lam, vec) in enumerate(zip(vals, vecs)):
        op = qutip.vector_to_operator(vec)
        purity = float((op.dag() * op).tr().real)
        print(f"{i}\t{lam.real:.6e}\t{lam.imag:.6e}\t{purity:.6f}")


if __name__ == "__main__":
    main()
