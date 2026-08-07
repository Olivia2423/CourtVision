from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
import os

# Add project path so Airflow can find your script
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.transformation.spark_etl import run_spark_etl

default_args = {
    'owner': 'olivia_kuitchoua',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'courtvision_etl_pipeline',
    default_args=default_args,
    description='Orchestrates PySpark ETL and PostgreSQL warehouse load for CourtVision',
    schedule_interval='@weekly',
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:

    run_pyspark_etl_task = PythonOperator(
        task_id='run_pyspark_transformation',
        python_callable=run_spark_etl,
    )

    run_pyspark_etl_task