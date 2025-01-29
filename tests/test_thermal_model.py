"""
test_thermal_model.py
Unit tests for the ThermalModel in models/thermal_model.py
"""

import pytest
import dolfin
from models.thermal_model import ThermalModel

def test_thermal_model_initialization():
    mesh = dolfin.UnitSquareMesh(dolfin.MPI.comm_world, 10, 10)
    model = ThermalModel(mesh, rho=2700, cp=900, k=200, Q_electrical=0.5)
    assert model.rho == 2700
    assert model.cp == 900
    assert model.k == 200
    assert model.Q_electrical == 0.5

def test_thermal_model_run():
    mesh = dolfin.UnitSquareMesh(dolfin.MPI.comm_world, 10, 10)
    model = ThermalModel(mesh, rho=2700, cp=900, k=200, Q_electrical=0.0)
    model.set_initial_condition(700.0)
    model.set_boundary_conditions(700.0)

    results = model.run_simulation(total_time=2, dt=1)
    # We expect 2 snapshots
    assert len(results) == 2

    # Basic sanity check: final temperature shouldn't be drastically different
    final_temp = results[-1].vector().get_local().mean()
    assert final_temp > 695.0 and final_temp < 705.0, "Temperature out of expected range"

