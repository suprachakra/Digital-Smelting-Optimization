#!/bin/bash
#SBATCH --job-name=metalx_pde
#SBATCH --output=metalx_pde_output.log
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=4
#SBATCH --time=02:00:00

# Load modules if needed
module load fenics/2019.1.0

# Launch the HPC run
srun python run_hpc_simulation.py --nx 300 --ny 300 --time 100 --dt 1.0

