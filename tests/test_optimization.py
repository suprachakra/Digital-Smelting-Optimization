"""
test_optimization.py
Unit tests for optimization routines (energy_optimize, multi_objective, etc.)
"""

import pytest
from optimization.multi_objective import multi_objective_optimization
import numpy as np

def test_multi_objective_optimization():
    # Create dummy data
    time_steps = 10
    energy_data = np.ones(time_steps) * 100
    ghg_data = np.ones(time_steps) * 50
    anode_events = np.zeros(time_steps)
    weights = (0.5, 0.3, 0.2)

    x_sol, total_obj, result = multi_objective_optimization(energy_data, ghg_data, anode_events, weights)
    assert len(x_sol) == time_steps
    assert total_obj >= 0  # Weighted sum should be non-negative in this contrived example
    assert result.solver.status == 'ok' or 'aborted' not in result.solver.status

