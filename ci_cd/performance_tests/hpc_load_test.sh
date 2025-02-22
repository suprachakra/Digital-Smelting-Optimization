#!/usr/bin/env bash
# hpc_load_test.sh
# 
# Purpose:
#   Run a series of PDE simulations at varying mesh sizes and record runtime & memory usage.
# Usage:
#   bash hpc_load_test.sh

set -e

# Read config (example approach)
CONFIG_FILE="perf_config.yaml"

# Extract parameters from the config (this is a simple placeholder)
MESH_SIZES=(50 100 200 500)
TIME_STEPS=10

# Create a results folder if not exists
mkdir -p benchmark_results

echo "Starting HPC load tests..."

for MESH in "${MESH_SIZES[@]}"; do
  echo "Running PDE solve with mesh=${MESH}x${MESH}, time_steps=${TIME_STEPS}"
  
  START_TIME=$(date +%s)
  
  # Example HPC run: Using srun or mpirun with HPC
  # srun -N2 -n4 python ../hpc_scripts/run_hpc_simulation.py --nx $MESH --ny $MESH --time $TIME_STEPS
  
  # For demonstration, we'll just echo
  echo "srun -N2 -n4 python run_hpc_simulation.py --nx $MESH --ny $MESH --time $TIME_STEPS"
  
  END_TIME=$(date +%s)
  RUNTIME=$((END_TIME - START_TIME))
  
  # Log the result
  echo "mesh=${MESH}x${MESH}, runtime=${RUNTIME}s" >> benchmark_results/perf_log.txt
  
  # Potential memory usage capture (using /usr/bin/time -v or similar)
  # /usr/bin/time -v ...
  
  echo "Completed mesh=${MESH}x${MESH}"
done

echo "All HPC load tests completed."
echo "Results stored in benchmark_results/perf_log.txt"
