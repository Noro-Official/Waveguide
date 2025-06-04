"""Run a grid sweep over ring count and cat-pump strength.

This script simulates a rotated surface code patch using Stim and decodes
with PyMatching. The bias from concentric rings is modelled by varying the
measurement error probability based on the cat-pump parameter.
Results are saved to ``results/epsilon_log.csv`` and ``results/grid_sweep.png``.

Example
-------
    python scripts/run_grid_sweep.py --shots 1e4
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymatching as pm
import stim


def logical_error_rate(distance: int, kappa2: float, shots: int, p_phys: float = 1e-3) -> float:
    """Return the logical error rate for a single surface-code instance.

    Parameters
    ----------
    distance
        Code distance (also treated as the number of concentric rings).
    kappa2
        Cat-pump parameter in Hz used to bias measurement errors.
    shots
        Number of samples to draw from the noisy circuit.
    p_phys
        Physical depolarising error rate applied to each Clifford gate.

    Returns
    -------
    float
        Fraction of shots resulting in a logical error.
    """
    meas_flip = p_phys * 1e5 / kappa2
    circuit = stim.Circuit.generated(
        "surface_code:rotated_memory_x",
        distance=distance,
        rounds=distance,
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


def run_sweep(N_r_values: Iterable[int], kappa2_values: Iterable[float], shots: int) -> pd.DataFrame:
    """Run the grid sweep and return the aggregated results."""
    records = []
    for N_r in N_r_values:
        for k2 in kappa2_values:
            eps_log = logical_error_rate(N_r, k2, shots)
            records.append({"N_r": N_r, "kappa2_kHz": k2 / 1e3, "eps_log": eps_log})
    df = pd.DataFrame(records)
    return df


def main(argv: Iterable[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Run concentric-ring grid sweep")
    parser.add_argument("--shots", type=float, default=1e4, help="Number of circuit shots")
    args = parser.parse_args(argv)
    shots = int(args.shots)

    N_r_values = [3, 5, 7]
    kappa2_values = [50e3, 150e3, 300e3]

    df = run_sweep(N_r_values, kappa2_values, shots)

    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    csv_path = results_dir / "epsilon_log.csv"
    df.to_csv(csv_path, index=False)

    plt.figure()
    for N_r in N_r_values:
        sub = df[df["N_r"] == N_r]
        plt.scatter(sub["kappa2_kHz"], sub["eps_log"], label=f"N_r={N_r}")
    plt.xlabel("kappa2 (kHz)")
    plt.ylabel("Logical error rate")
    plt.legend()
    plt.savefig(results_dir / "grid_sweep.png")


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
