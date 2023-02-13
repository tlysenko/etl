from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'tlysenko',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='first_dag',
    default_args=default_args,
    description='My first DAG',
    start_date=datetime(2023, 2, 13, 3),
    schedule_interval='@daily',

) as dag:
    task_1 = BashOperator(
        task_id='task_1',
        bash_command='echo "Hello World!"')