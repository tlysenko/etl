from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import BranchPythonOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2020, 1, 1)
}

def _choose_best_model():
    accuracy = 6
    if accuracy > 5:
        return 'accurate'
    return 'inaccurate'

with DAG('dag_branching_v02',
         schedule_interval='@daily',
         default_args=default_args,
         catchup=False) as dag:
    choose_best_model = BranchPythonOperator(
        task_id='choose_best_model',
        python_callable=_choose_best_model)
    accurate = DummyOperator(
        task_id='accurate')
    inaccurate = DummyOperator(
        task_id='inaccurate')

    choose_best_model >> [accurate, inaccurate]
