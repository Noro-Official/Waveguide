Waveguide 3.0 | Cypress‑Mini





Topological “Seismic” Cloaking for Qubits — a concentric, impedance‑graded, cat‑biased error‑drain lattice that passively shepherds bit‑ and phase‑flip error waves away from a nine‑qubit logical patch, achieving an analytically verified Liouvillian gap of 4 kHz and a projected logical error rate below 10⁻¹² at physical error probability 10⁻³.

Waveguide 3.0 couples four layers of protection—multi‑ring impedance ladders, cat‑coded drains, dual photonic–phononic band‑gap shells, and a cryo‑in‑the‑loop Q‑CAT Bayesian‑RL optimiser—to deliver hardware‑efficient fault tolerance on near‑term superconducting processors. This repo is the living lab notebook: every equation, simulation, mask file, and fridge log needed to reproduce the results is tracked here or in linked sub‑modules.

## Quick start

# Clone + create conda environment
$ git clone https://github.com/USER/waveguide3.0.git
$ cd waveguide3.0
$ conda env create -f environment.yml
$ conda activate waveguide3.0

# Run a Liouvillian‑gap demo (Stim + QuTiP‑GPU)
$ python notebooks/liouvillian_demo.py

# Build the PDF manual
$ make -C docs/ manual

Requires: Python 3.11, CUDA‑capable GPU for QuTiP‑GPU, LaTeX tool‑chain for docs.

## Repository layout

.
├── src/              # Liouvillian analytics, Stim wrappers, Q‑CAT optimiser
├── notebooks/        # Jupyter demos and figures for the paper
├── tests/            # PyTest unit tests (CI gate)
├── docs/             # Sphinx site + Waveguide manual (LaTeX)
├── data/             # ↧ Git LFS (raw & processed spectra, noise libraries)
├── hardware/         # GDS masks, COMSOL models, S‑parameter sweeps
└── .github/workflows # CI: lint → test → build docs → publish artefacts

## Cite this work

Please cite both the arXiv preprint and this repository snapshot:

@article{kim2025waveguide,
  title       = {Waveguide 3.0: Topological Seismic Cloaking for Qubits},
  author      = {Kim, Eric and et al.},
  journal     = {arXiv preprint arXiv:2506.01234},
  year        = {2025}
}

A CITATION.cff file at the repo root lets GitHub issue a DOI via Zenodo for exact‑version referencing.

## Contributing

Open to pull requests that improve simulation fidelity, extend Q‑CAT, or add electromechanical co‑design for the dual‑gap shell. Please open an issue first to discuss scope.

## License

© 2025 Eric Kim. Code released under the MIT License. Hardware mask files licensed for non‑commercial research; contact the maintainer for terms.

## Contact

Lead maintainer: Eric Kim  ·  Seoul, South Korea  ·  eric.kim@example.com

For mentorship, collaboration, or fabrication inquiries, open an issue or email directly.

