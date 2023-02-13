from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'tlysenko',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='first_dag_v3.3',
    default_args=default_args,
    description='My first DAG',
    start_date=datetime(2023, 2, 13, 3),
    schedule_interval='@daily'
) as dag:
    task_1 = BashOperator(
        task_id='task_1',
        bash_command='echo "Hello World!"')
    task_2 = BashOperator(
        task_id='task_2',
        bash_command='echo "It is the second task that follows task_1"')
    task_3 = BashOperator(
        task_id='task_3',
        bash_command='echo "It is the third task that f"')

#    task_1.set_downstream(task_2)
#    task_1.set_downstream(task_3)

#    task_1 >> task_2
#    task_1 >> task_3

    task_1 >> [task_2, task_3]