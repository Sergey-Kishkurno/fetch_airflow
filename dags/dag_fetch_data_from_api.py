from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from fetch_data import fetch_data


default_args = {
    'owner': "airflow",
    'email': ["airflow@airflow.com"],
    'email_on_failure': False,
    'retries': 1
}

dag = DAG(
    "dag_fetch_from_api",
    schedule_interval='@daily',
    start_date=datetime(2022, 1, 25, 1, 0),
    default_args=default_args
)


t1 = PythonOperator(
    task_id='Task1_fetch_data_from_api',
    dag=dag,
    python_callable=fetch_data
)


