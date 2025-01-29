"""
mass_transfer_model.py
Implements a simplified mass transfer PDE for ionic concentration based on Fick's Law:
  dC/dt = div(D * grad(C)) - R_electrochemical
"""

import dolfin

class MassTransferModel:
    def __init__(self, domain_mesh, diffusion_coeff=0.01, electrochemical_rate=0.0):
        """
        diffusion_coeff    : D in the PDE
        electrochemical_rate : R_electrochemical (could be a function or constant)
        """
        self.mesh = domain_mesh
        self.diffusion_coeff = diffusion_coeff
        self.electrochemical_rate = electrochemical_rate

        # Function space
        self.V = dolfin.FunctionSpace(self.mesh, "P", 1)
        self.C = dolfin.Function(self.V, name="Concentration")
        self.C_n = dolfin.Function(self.V)

        # Time step
        self.dt = dolfin.Constant(1.0)

    def set_initial_condition(self, initial_conc):
        self.C.assign(dolfin.Constant(initial_conc))
        self.C_n.assign(self.C)

    def set_boundary_conditions(self, bc_value):
        bc_expr = dolfin.Constant(bc_value)
        self.bcs = [dolfin.DirichletBC(self.V, bc_expr, "on_boundary")]

    def step(self):
        # PDE in weak form
        C_trial = dolfin.TrialFunction(self.V)
        v = dolfin.TestFunction(self.V)
        
        D = self.diffusion_coeff
        R_e = self.electrochemical_rate

        F = ((C_trial - self.C_n)/self.dt)*v*dolfin.dx \
            + (-D*dolfin.dot(dolfin.grad(C_trial), dolfin.grad(v)))*dolfin.dx \
            + R_e*v*dolfin.dx
        
        a = dolfin.lhs(F)
        L = dolfin.rhs(F)

        C_new = dolfin.Function(self.V)
        dolfin.solve(a == L, C_new, self.bcs)

        self.C_n.assign(C_new)
        self.C.assign(C_new)
        return C_new

    def run_simulation(self, total_time=10, dt=1):
        self.dt.assign(dt)
        num_steps = int(total_time/dt)

        concentration_snapshots = []
        for step in range(num_steps):
            c_field = self.step()
            concentration_snapshots.append(c_field.copy(deep=True))
        return concentration_snapshots

