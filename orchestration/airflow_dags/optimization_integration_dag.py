"""
Airflow DAG for UC-03: Optimization Engine Integration
Pulls PDE outputs, applies constraints, and runs energy optimization. Then optionally updates SCADA.
"""

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'metalworks',
    'start_date': days_ago(1),
    'retries': 2,
    'retry_delay': 300,  # 5 minutes
}

with DAG(
    'optimization_integration_dag',
    default_args=default_args,
    description='Energy optimization for UC-03 using PDE outputs + real-time constraints.',
    schedule_interval='@hourly',
) as dag:

    # 1. Retrieve PDE outputs from data lake
    fetch_pde_outputs = BashOperator(
        task_id='fetch_pde_outputs',
        bash_command='python scripts/fetch_pde_outputs.py --lake-tier gold',
    )

    # 2. Run optimization
    run_optimization = BashOperator(
        task_id='run_optimization',
        bash_command='python optimization/energy_optimize.py --pde_data pde_outputs.json',
    )

    # 3. Send recommended setpoints to SCADA
    update_scada = BashOperator(
        task_id='update_scada',
        bash_command='python scada/scada_client.py --setpoints recommended_setpoints.json',
    )

    fetch_pde_outputs >> run_optimization >> update_scada
