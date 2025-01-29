"""
thermal_model.py
Implements the thermal PDE model based on Fourier's Law:
  rho * c_p * dT/dt = div(k * grad(T)) + Q_electrical
"""

import dolfin  # Typically for FEniCS, or "import fenics" in older versions
import numpy as np

class ThermalModel:
    def __init__(self, domain_mesh, rho, cp, k, Q_electrical=0.0):
        """
        domain_mesh   : FEniCS mesh object
        rho, cp, k    : material properties (density, heat capacity, thermal conductivity)
        Q_electrical  : optional internal heat source term
        """
        self.mesh = domain_mesh
        self.rho = rho
        self.cp = cp
        self.k = k
        self.Q_electrical = Q_electrical
        
        # Function space
        self.V = dolfin.FunctionSpace(self.mesh, "P", 1)  # Simple CG1 element
        self.T = dolfin.Function(self.V, name="Temperature")  # solution
        self.T_n = dolfin.Function(self.V)  # previous time-step

        # Time step data
        self.dt = dolfin.Constant(1.0)  # default 1s, can be changed

    def set_initial_condition(self, initial_temperature):
        """
        Assign an initial temperature field.
        """
        self.T.assign(dolfin.Constant(initial_temperature))
        self.T_n.assign(self.T)

    def set_boundary_conditions(self, boundary_value):
        """
        Simple Dirichlet boundary condition for demonstration.
        boundary_value: float, e.g. T=700 at boundary
        """
        bc_expr = dolfin.Constant(boundary_value)
        self.bcs = [dolfin.DirichletBC(self.V, bc_expr, "on_boundary")]

    def step(self):
        """
        Formulate the weak form and solve one time step.
        """
        # Define test/trial functions
        T_trial = dolfin.TrialFunction(self.V)
        v = dolfin.TestFunction(self.V)

        # PDE parameters
        rho_cp = self.rho * self.cp
        k_val = self.k

        # PDE in weak form for time stepping
        # (rho_cp * (T - T_n)/dt )*v dx + ...
        # Implementation details may differ based on the solver method
        F = (rho_cp * (T_trial - self.T_n)/self.dt)*v*dolfin.dx \
            + k_val*dolfin.dot(dolfin.grad(T_trial), dolfin.grad(v))*dolfin.dx \
            - self.Q_electrical*v*dolfin.dx
        
        a = dolfin.lhs(F)  # left-hand side
        L = dolfin.rhs(F)  # right-hand side

        T_new = dolfin.Function(self.V)
        dolfin.solve(a == L, T_new, self.bcs)

        # Update for next step
        self.T_n.assign(T_new)
        self.T.assign(T_new)

        return T_new

    def run_simulation(self, total_time=10, dt=1):
        """
        Runs a simple forward simulation for total_time seconds.
        """
        self.dt.assign(dt)
        num_steps = int(total_time/dt)

        temperature_snapshots = []
        for step in range(num_steps):
            T_field = self.step()
            temperature_snapshots.append(T_field.copy(deep=True))
        return temperature_snapshots


