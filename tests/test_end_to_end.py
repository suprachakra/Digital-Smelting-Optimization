"""
test_end_to_end.py
Integration test from data ingestion -> PDE -> optimization -> SCADA mock
This is a 'conceptual' test - you may need to adjust for actual local environment.
"""

import pytest
import os
import requests
from models.thermal_model import ThermalModel
import dolfin
import numpy as np

def test_end_to_end():
    # 1) Data ingestion - assume we read a small processed file
    data_file = os.path.join('data', 'processed', 'sensor_data_day1_cleaned.csv')
    assert os.path.exists(data_file), "Processed data file not found."

    # 2) PDE step (thermal)
    mesh = dolfin.UnitSquareMesh(dolfin.MPI.comm_world, 5, 5)
    model = ThermalModel(mesh, 2700, 900, 200, 0.1)
    model.set_initial_condition(700.0)
    model.set_boundary_conditions(700.0)
    results = model.run_simulation(total_time=1, dt=1)
    assert len(results) == 1, "Unexpected PDE result length."

    # 3) Simple optimization: we'll pretend we post to SCADA with final setpoints
    # For demonstration, just do a direct request to scada_mock
    scada_url = "http://localhost:5000/api/scada/setpoint"
    # We expect scada_mock.py is running
    payload = {"voltage": 4.3, "current": 120.0}
    try:
        r = requests.post(scada_url, json=payload)
        print("SCADA response:", r.json())
        assert r.status_code == 200, "SCADA override triggered or server not responding"
        assert r.json().get('status') == "OK"
    except requests.exceptions.ConnectionError:
        pytest.skip("SCADA mock not running on port 5000, skipping SCADA integration check.")

