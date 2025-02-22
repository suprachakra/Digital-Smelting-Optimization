# Changelog

All notable changes to this project will be documented in this file.
We adhere to [Semantic Versioning](https://semver.org/).

## [0.1.0] - 2025-02-21
### Added
- Initial release of Digital Smelting Optimization codebase.
- PDE models for thermal, mass transfer, electrochemistry.
- HPC scripts (`run_hpc_simulation.py`, `run_sim.slurm`).
- Optimization engine (Pyomo-based single-objective and multi-objective).
- Basic Dockerfile for local dev.

### Changed
- N/A

### Fixed
- N/A

## [0.2.0] - YYYY-MM-DD
### Added
- `CHANGELOG.md`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md`.
- Centralized config in `config/` folder (app_config.yaml, hpc_config.yaml, constraints_config.yaml).
- Airflow DAGs in `orchestration/`.

### Changed
- PDE solver default mesh size from 50x50 to 100x100 for better accuracy.

### Fixed
- Minor bug in `energy_optimize.py` for throughput constraint.
