from airflow.decorators import dag, task
from datetime import datetime, timedelta

default_args = {'owner': 'tlysenko',
                'retries': 5,
                'retry_delay': timedelta(minutes=2)}


@dag(dag_id='dag_with_task_flow_v1.4',
    default_args=default_args,
    start_date=datetime(2023, 2, 13, 3),
    schedule_interval='@daily')

def hello_world_etl():
    @task(multiple_outputs=True)
    def get_name():
        return {'first_name': 'Jerry', 'last_name': 'Fridman'}


    @task()
    def get_age():
        return 31


    @task()
    def greet(first_name, last_name,age):
        print(f'Hello World! I am {first_name} {last_name} and I am {age} years old')


    name_dict = get_name()
    age = get_age()
    greet(first_name=name_dict['first_name'], last_name=name_dict['last_name'], age=age)


greet_dag = hello_world_etl()