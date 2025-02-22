from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'metalx',
    'start_date': days_ago(1),
    'retries': 1,
}

with DAG(
    'smelting_etl',
    default_args=default_args,
    description='ETL pipeline for smelting sensor data',
    schedule_interval='@hourly',
) as dag:

    extract_data = BashOperator(
        task_id='extract_data',
        bash_command='python services/kafka_producer.py --extract-only',
    )

    transform_data = BashOperator(
        task_id='transform_data',
        bash_command='python notebooks/1_data_exploration.ipynb --headless',
    )

    load_data = BashOperator(
        task_id='load_data',
        bash_command='python scripts/load_to_datalake.py',
    )

    run_pde_sim = BashOperator(
        task_id='run_pde_simulation',
        bash_command='srun python hpc_scripts/run_hpc_simulation.py --nx 300 --ny 300',
    )

    # Dependencies
    extract_data >> transform_data >> load_data >> run_pde_sim
