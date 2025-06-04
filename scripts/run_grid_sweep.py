#!/usr/bin/env python
"""Run a grid sweep over ring count and cat-pump strength.

The script simulates a distance-3 rotated surface-code patch in ``Stim`` and
decodes each sample with ``PyMatching``.  A concentric-ring bias is modelled
using a depolarising error rate ``p_phys`` together with a biased bit-flip
channel.  The bias factor is defined as ``beta = kappa2 / 50e3`` (where
``kappa2`` is given in Hz).  Measurement bit-flip errors are applied with
probability ``p_phys / beta``.  Results from a parameter sweep are written to
``results/epsilon_log.csv`` and an accompanying scatter plot is saved to
``results/grid_sweep.png``.

Example
-------
Run with default settings::

    python scripts/run_grid_sweep.py --shots 10000 --show-plot
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, Sequence

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymatching as pm
import stim


def logical_error_rate(N_r: int, kappa2_hz: float, shots: int, p_phys: float = 1e-3) -> float:
    """Estimate the logical error rate for a biased surface-code instance.

    Parameters
    ----------
    N_r
        Number of concentric rings (used as the number of memory rounds).
    kappa2_hz
        Cat-pump strength in Hz controlling the bias factor ``beta``.
    shots
        Number of Monte-Carlo samples to draw from the circuit.
    p_phys
        Physical depolarising error probability applied to Clifford gates.

    Returns
    -------
    float
        Fraction of shots resulting in a logical failure.
    """
    beta = kappa2_hz / 50_000.0
    meas_flip = p_phys / beta
    circuit = stim.Circuit.generated(
        "surface_code:rotated_memory_x",
        distance=3,
        rounds=N_r,
        after_clifford_depolarization=p_phys,
        before_measure_flip_probability=meas_flip,
    )
    dem = circuit.detector_error_model(decompose_errors=True)
    matching = pm.Matching.from_detector_error_model(dem)
    sampler = circuit.compile_detector_sampler()
    dets, obs = sampler.sample(shots=shots, separate_observables=True)
    preds = matching.decode_batch(dets)
    failures = np.sum(np.any(preds != obs, axis=1))
    return failures / shots


def run_sweep(N_r_values: Sequence[int], kappa2_kHz: Sequence[float], shots: int) -> pd.DataFrame:
    """Evaluate the logical error rate over the parameter grid.

    Parameters
    ----------
    N_r_values
        Iterable of ring-count values.
    kappa2_kHz
        Iterable of cat-pump strengths in kilohertz.
    shots
        Number of circuit samples per grid point.

    Returns
    -------
    pandas.DataFrame
        Table containing ``N_r``, ``kappa2_kHz`` and ``eps_log`` columns.
    """
    records = []
    for N_r in N_r_values:
        for k2 in kappa2_kHz:
            eps_log = logical_error_rate(N_r, k2 * 1e3, shots)
            records.append({"N_r": N_r, "kappa2_kHz": k2, "eps_log": eps_log})
    return pd.DataFrame.from_records(records)


def main(argv: Sequence[str] | None = None) -> None:
    """Entry point for the grid sweep CLI."""
    parser = argparse.ArgumentParser(description="Run concentric-ring grid sweep")
    parser.add_argument(
        "--shots",
        type=int,
        default=int(1e4),
        help="Number of circuit shots per grid point",
    )
    parser.add_argument(
        "--show-plot",
        action="store_true",
        help="Display the result plot after running the sweep",
    )
    args = parser.parse_args(argv)

    if args.shots <= 0:
        raise SystemExit(1)

    N_r_values = [3, 5, 7]
    kappa2_values = [50.0, 150.0, 300.0]

    df = run_sweep(N_r_values, kappa2_values, args.shots)

    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    csv_path = results_dir / "epsilon_log.csv"
    df.to_csv(csv_path, index=False)

    fig, ax = plt.subplots()
    for N_r in N_r_values:
        sub = df[df["N_r"] == N_r]
        ax.scatter(sub["kappa2_kHz"], sub["eps_log"], label=f"N_r={N_r}")
    ax.set_xlabel("kappa2 (kHz)")
    ax.set_ylabel("eps_log")
    ax.set_title("Logical error rate sweep")
    ax.legend()
    fig.savefig(results_dir / "grid_sweep.png")
    if args.show_plot:
        plt.show()
    else:
        plt.close(fig)


if __name__ == "__main__":
    main()
