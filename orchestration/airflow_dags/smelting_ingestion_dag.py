"""
Airflow DAG for UC-01: Data Ingestion & ETL
Collects raw sensor data from SCADA or Kafka, cleans it, and stores it in the Data Lake (Bronze → Silver).
"""

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'metalworks',
    'start_date': days_ago(1),
    'retries': 1,
    'retry_delay': 300,  # 5 minutes
}

with DAG(
    'smelting_ingestion_dag',
    default_args=default_args,
    description='Data ingestion & ETL pipeline for MetalX smelting (UC-01).',
    schedule_interval='@hourly',
) as dag:

    # 1. Extract from Kafka/SCADA
    extract_data = BashOperator(
        task_id='extract_data',
        bash_command='python services/kafka_producer.py --extract-only',
    )

    # 2. Transform data (clean, validate, outlier detection)
    transform_data = BashOperator(
        task_id='transform_data',
        bash_command='python notebooks/1_data_exploration.ipynb --headless',
    )

    # 3. Load into Data Lake
    load_data = BashOperator(
        task_id='load_data',
        bash_command='python scripts/load_to_datalake.py',
    )

    extract_data >> transform_data >> load_data
