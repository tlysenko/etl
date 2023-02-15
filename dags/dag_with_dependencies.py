from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


default_args = {
    'owner': 'tlysenko',
    'retries': 5,
    'retry_delay': timedelta(minutes=2),
}
def get_sklearn():
    import sklearn
    print('sklearn version', sklearn.__version__)

with DAG(
        description='PythonOperator DAG',
        default_args=default_args,
        dag_id='Dag_with_dependencies_v1.0',
        start_date=datetime(2023, 2, 13, 3),
        schedule_interval='@daily'
) as dag:
    task_1 = PythonOperator(task_id='get_sklearn',python_callable=get_sklearn)

task_1

