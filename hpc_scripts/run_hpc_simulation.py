"""
run_hpc_simulation.py
Example HPC parallel run script for PDE solving with FEniCS or fenics.
Usage:
  mpirun -np 4 python run_hpc_simulation.py --nx 200 --ny 200 --time 50 --dt 0.5
"""

import argparse
import dolfin  # or fenics
from models.thermal_model import ThermalModel

def main():
    parser = argparse.ArgumentParser(description="Run thermal PDE on HPC")
    parser.add_argument("--nx", type=int, default=100, help="mesh subdivisions in x")
    parser.add_argument("--ny", type=int, default=100, help="mesh subdivisions in y")
    parser.add_argument("--time", type=float, default=10.0, help="total simulation time")
    parser.add_argument("--dt", type=float, default=1.0, help="time step")
    args = parser.parse_args()

    # Create a distributed mesh
    mesh = dolfin.UnitSquareMesh(dolfin.MPI.comm_world, args.nx, args.ny)

    # Example: Thermal PDE with some dummy parameters
    rho = 2700.0
    cp = 900.0
    k = 200.0
    Q_electrical = 0.5

    model = ThermalModel(mesh, rho, cp, k, Q_electrical)
    model.set_initial_condition(700.0)
    model.set_boundary_conditions(700.0)

    # Run simulation
    results = model.run_simulation(total_time=args.time, dt=args.dt)

    # Print final average temperature
    final_temp_values = results[-1].vector().get_local()
    avg_temp = sum(final_temp_values)/len(final_temp_values)
    rank = dolfin.MPI.rank(dolfin.MPI.comm_world)
    if rank == 0:
        print(f"Final average temperature: {avg_temp:.2f} K (nx={args.nx}, ny={args.ny})")

if __name__ == "__main__":
    main()

