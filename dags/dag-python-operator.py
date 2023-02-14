from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'tlysenko',
    'retries': 5,
    'retry_delay': timedelta(minutes=2),

}


def greet(ti):
    first_name = ti.xcom_pull(task_ids='get_name', key='first_name')
    last_name = ti.xcom_pull(task_ids='get_name', key='last_name')
    age = ti.xcom_pull(task_ids='get_age', key='age')
    print(f'Hello World! My name is {first_name} {last_name} and I am {age} years old')


def get_name(ti): # ti is task instance
    ti.xcom_push(key='first_name', value='Jerry')
    ti.xcom_push(key='last_name', value='Fridman')


def get_age(ti):
    ti.xcom_push(key='age', value=33)


with DAG(
        dag_id='python_operator_dag_v1.7',
        description='PythonOperator DAG',
        default_args=default_args,
        start_date=datetime(2023, 2, 13, 3),
        schedule_interval='@daily'
) as dag:

    task_1 = PythonOperator(task_id='greet',
                            python_callable=greet)
    task_2 = PythonOperator(task_id='get_name',
                            python_callable=get_name)
    task_3 = PythonOperator(task_id='get_age',
                            python_callable=get_age)

    [task_3, task_2] >> task_1

    # task_3 = PythonOperator()
