import sys
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

module_path = '/opt/airflow/ETL'
sys.path.insert(0, module_path)

from extract import load_data_to_postgres

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

dag = DAG(
    'postgres_data_load',
    default_args=default_args,
    description='DAG to load weather data into DWH',
    schedule_interval='0 * * * *',
)

load_data_task = PythonOperator(
    task_id='load_data_to_postgres',
    python_callable=load_data_to_postgres,
    dag=dag,
)

load_data_task
