'''
An end to end ETL pipeline using Airflow
 - take CSV file
 - Clean it
 - send it to Postgres
'''

# TODO: make it work. 
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


import pandas as pd

def t1_read_csv():
    url = 'https://github.com/datasciencedojo/datasets/blob/master/titanic.csv'
    df = pd.read_csv(url, error_bad_lines=False)
    return df

def t2_clean_data(df):
    df = df.dropna()
    return df

with DAG(
    dag_id='dag_e2e_etl_v01',
    description='ETL pipeline',
    start_date=datetime(2023, 2, 13, 3),
    schedule_interval='@daily') as dag:

    task_1 = PythonOperator(
        task_id='t1_read_csv',
        python_callable=t1_read_csv
    )

    task_2 = PythonOperator(
        task_id='t2_clean_data',
        python_callable=t2_clean_data,
        op_kwargs={'df': '{{ task_instance.xcom_pull(task_ids="t1_read_csv") }}'},

    )


task_1 >> task_2 #>> task_3