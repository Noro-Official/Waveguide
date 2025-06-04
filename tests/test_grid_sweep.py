import sys
import subprocess
from pathlib import Path

import pandas as pd
import pytest


@pytest.mark.slow
def test_grid_sweep(tmp_path):
    pytest.importorskip("stim", reason="Stim not installed")

    script = Path(__file__).resolve().parents[1] / "scripts" / "run_grid_sweep.py"
    subprocess.run([
        sys.executable,
        str(script),
        "--shots",
        "100",
    ], cwd=tmp_path, check=True, timeout=60)

    csv_path = tmp_path / "results" / "epsilon_log.csv"
    assert csv_path.exists(), "results/epsilon_log.csv was not created"

    df = pd.read_csv(csv_path)
    expected_cols = ["N_r", "kappa2_kHz", "eps_log"]
    assert list(df.columns) == expected_cols, f"CSV columns are {list(df.columns)}, expected {expected_cols}"

    assert len(df) == 9, f"Expected 9 rows in CSV, found {len(df)}"

    expected_pairs = {(n, k) for n in [3, 5, 7] for k in [50, 150, 300]}
    actual_pairs = set(zip(df["N_r"], df["kappa2_kHz"]))
    assert actual_pairs == expected_pairs, f"Grid sweep missing or extra pairs: {actual_pairs}"

    for N_r, group in df.groupby("N_r"):
        ordered = group.sort_values("kappa2_kHz")["eps_log"].to_list()
        for a, b in zip(ordered, ordered[1:]):
            assert a >= b, f"eps_log not non-increasing for N_r={N_r}"

    assert df["eps_log"].gt(0).all() and df["eps_log"].lt(1).all(), "eps_log values must be in (0,1)"
