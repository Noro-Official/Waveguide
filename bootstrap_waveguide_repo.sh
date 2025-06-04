#!/usr/bin/env bash
set -euo pipefail

# Create directory structure
mkdir -p src notebooks tests docs data/raw data/processed hardware .github/workflows

# Create Python package init
cat <<'PY' > src/__init__.py
"""Waveguide 3.0 core package."""
PY

# Create demo notebook
cat <<'NB' > notebooks/demo.ipynb
{"cells": [], "metadata": {}, "nbformat": 4, "nbformat_minor": 5}
NB

# Create test stub
cat <<'PYTEST' > tests/test_placeholder.py
import pytest

def test_placeholder():
    assert True
PYTEST

# Create Sphinx conf
cat <<'CONF' > docs/conf.py
project = 'Waveguide 3.0'
extensions = []
master_doc = 'index'
CONF

touch docs/Waveguide_manual.tex

# Create .gitattributes
cat <<'ATTR' > .gitattributes
*.csv filter=lfs diff=lfs merge=lfs -text
*.h5  filter=lfs diff=lfs merge=lfs -text
ATTR

# Data placeholders
mkdir -p hardware
for f in hardware/GDS.md hardware/COMSOL.md hardware/s-parameters.md; do
    echo "Placeholder for $f" > "$f"
done

# GitHub Actions workflow
cat <<'YML' > .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt || true
      - name: Run tests
        run: pytest
      - name: Build LaTeX
        run: |
          cd docs && latexmk -pdf Waveguide_manual.tex
        if: always()
YML

# README (>=100 chars)
cat <<'MD' > README.md
# Waveguide 3.0

Badges go here.

Waveguide 3.0 explores novel cat-code lattices for robust quantum computation. This repository contains Python tools, simulation notebooks, and hardware models. Contributions welcome!
MD

# LICENSE
cat <<'MIT' > LICENSE
MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
MIT

# CITATION.cff
cat <<'CFF' > CITATION.cff
cff-version: 1.2.0
title: Waveguide 3.0
version: 0.1.0
authors:
  - family-names: Doe
    given-names: Jane
message: Please cite this work if used.
CFF

# AGENTS.md
cat <<'AG' > AGENTS.md
## Instructions for Codex Agents
- Install dependencies: `conda env create -f environment.yml`
- Run tests with `pytest`
AG

# environment.yml
cat <<'ENV' > environment.yml
name: waveguide
channels: [conda-forge]
dependencies:
  - python=3.11
  - stim
  - qutip-gpu
  - pytest
ENV

# .gitignore
cat <<'GI' > .gitignore
__pycache__/
*.pyc
.ipynb_checkpoints/
.env
.vscode/
*.pdf
.DS_Store
GI

# Initialize Git repo
if [ ! -d .git ]; then
  git init -b main
fi
git lfs install >/dev/null 2>&1 || true

git add .
git commit -m "feat: repo scaffold"

if [ -n "${GH_REMOTE:-}" ]; then
  git remote add origin "$GH_REMOTE" || true
  git push -u origin main
fi

echo -e "\e[32mWaveguide 3.0 repository bootstrap complete.\e[0m"
