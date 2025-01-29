"""
solver_utils.py
Helper methods for solver selection, logging, or advanced debug.
"""

import pyomo.environ as pyo

def get_solver(solver_name='ipopt'):
    """
    Return a configured solver instance.
    """
    solver = pyo.SolverFactory(solver_name)
    # Could configure solver options here
    # solver.options['tol'] = 1e-8
    return solver

