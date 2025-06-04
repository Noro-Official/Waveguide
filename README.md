# Waveguide 3.0 | Cypress-Mini

[![CI](https://img.shields.io/github/actions/workflow/status/<USER>/waveguide3.0/ci.yml?label=CI&logo=github&style=flat-square)](../../actions)
[![Docs](https://img.shields.io/badge/docs-latest-brightgreen?style=flat-square&logo=read-the-docs)](https://<USER>.github.io/waveguide3.0/)
[![License](https://img.shields.io/github/license/<USER>/waveguide3.0?style=flat-square)](LICENSE)
[![DOI](https://zenodo.org/badge/<ZENODO_BADGE_ID>.svg)](https://doi.org/<DOI_LINK>)

*A topological “seismic-cloak” lattice for superconducting qubits, integrating concentric impedance-graded rings, cat-biased error drains, and a dual photonic-phononic exoskeleton—auto-tuned in-fridge by the **Q-CAT** RL agent.*

---

## Key Features

| Layer | Purpose | Status |
|-------|---------|--------|
| **Impedance-graded CPW rings** | Radially bias error propagation (wave-guide effect) | ✅ Design v1, Stim-verified |
| **Cat-coded drains** | Exponential suppression of bit-flips at sinks | ✅ Single-cavity demo |
| **Dual photonic & phononic shell** | Attenuate microwave + phonon loss (κ̃ ↓) | 🛠️ Coupon in fab |
| **Q-CAT optimiser** | RL + BO loop maximising Liouvillian gap | 🛠️ Simulator complete |
| **Noise-library JSON** | Markovian, 1/f, QP bursts, non-Markovian kernels | 🛠️ A/B/C models merged |

---



---

## Quick Start

```bash
# 1. Clone + create environment
git clone https://github.com/<USER>/waveguide3.0.git
cd waveguide3.0
conda env create -f environment.yml
conda activate waveguide3

# 2. Run unit tests
pytest -q

# 3. Reproduce main figure (Liouvillian spectrum)
jupyter notebook notebooks/liouvillian_gap_demo.ipynb
Tip: The LaTeX design manual (docs/Waveguide_manual.tex) builds automatically in CI; the latest PDF lives under the Docs badge above.
Contributing

Pull requests are welcome! Please open an issue first to discuss substantial changes.
All code is auto-linted and unit-tested in GitHub Actions—merge only if CI is green.

License

This project is licensed under the MIT License (see LICENSE).
Mask‐layout and COMSOL files remain © Waveguide Project until first tape-out; non-commercial research use is permitted.

Citation

If you use this project in academic work, please cite via the accompanying CITATION.cff or DOI badge above:

@software{waveguide3.0,
  author       = {Kim, Eric},
  title        = {Waveguide 3.0 – Cypress-Mini},
  year         = {2025},
  publisher    = {Zenodo},
  version      = {v0.1-sim},
  doi          = {<DOI_LINK>}
}
Acknowledgements
Waveguide 3.0 draws inspiration from seismic metamaterials, Kerr-cat QEC, and the autonomous-dissipation framework pioneered by Shruti Puri, Zaki Leghtas, and collaborators. We thank the open-source quantum community for Stim, PyMatching, and QuTiP-GPU.


Replace the placeholder fields—`<USER>`, `<ZENODO_BADGE_ID>`, and `<DOI_LINK>`—with your GitHub username and Zenodo details once available, then drop this file into the repo root. GitHub will render badges and links automatically.
