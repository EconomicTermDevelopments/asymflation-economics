# Asymflation: An Economic Framework

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Status: Active](https://img.shields.io/badge/Status-Active-blue.svg)
![Category: Macroeconomics](https://img.shields.io/badge/Category-asymflation-purple.svg)

## Overview
`Asymflation` is modeled as asymmetric inflation dynamics under cost shocks. The repository defines one canonical concept expression and one executable index pipeline. The mechanism focus is faster upward pass-through than downward adjustment in prices.

This Phase 2 package includes upgraded documentation, working code with type hints, a 200-row synthetic dataset, notebook examples, semantic metadata, and a working-paper source. The objective is to make the term usable in research and policy workflows immediately, while keeping assumptions transparent and editable.

The project is structured for reproducibility: dataset generation is deterministic, index computation is explicit, and documentation aligns with code variable names. That alignment is the core scaling strategy for the remaining terms.

The same structure is reusable for the rest of TERMPRODUCT: preserve file shape and validation gates, then swap mechanism channels, assumptions, and examples. This keeps cross-term comparisons reliable and makes rollout to the remaining terms faster.

## Installation
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Quick Start
```bash
python generation_script.py
python asymflation.py
```

## Documentation
- `DEFINITION.md`
- `docs/index.html`
- `paper.tex`

## Citation
Economic Research Collective (2026). "Asymflation: An Economic Framework."

## License
MIT License.
