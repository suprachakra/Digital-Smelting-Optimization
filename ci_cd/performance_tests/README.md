## Performance & Load Testing

This folder contains scripts and configurations for stress-testing PDE solves, optimization routines, and data ingestion rates. The goal is to ensure the system meets performance and scalability requirements, as outlined in our Non-Functional Requirements (NFRs).

### Contents

- `hpc_load_test.sh`: Shell script to run multiple PDE solves at increasing mesh sizes (e.g., 50x50 → 500x500) and record solver times/memory usage.
- `perf_config.yaml`: Configuration file specifying test parameters (mesh sizes, HPC node counts, etc.).
- `benchmark_results/`: (Optional) A folder to store CSV or JSON logs of each test run.

### How to Use

1. **Configure**: Update `perf_config.yaml` with desired mesh sizes, HPC node counts, and time steps.
2. **Run**: Execute `bash hpc_load_test.sh`. This script will:
   - Launch PDE solves on HPC or local cluster.
   - Log solver iteration counts, CPU usage, and memory usage.
3. **Analyze**: Review logs in `benchmark_results/` to identify performance bottlenecks. 
4. **CI/CD Integration**: You can trigger these tests manually or on a scheduled basis in your pipeline for performance regression checks.
