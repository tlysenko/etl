from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'tlysenko',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='postgres_operator_dag_v1_05',
    default_args=default_args,
    description='PostgresOperator DAG',
    start_date=datetime(2023, 2, 13, 3),
    schedule_interval='@daily') as dag:

    task_1 = PostgresOperator(
        task_id='create_posgtres_table',
        postgres_conn_id='postgres_localhost',
        sql=
        '''
            CREATE TABLE IF NOT EXISTS dag_runs (
            dt date,
            dag_id character varying(250),
            primary key (dt, dag_id)
            )
        '''
    )
    task_2 = PostgresOperator(
        task_id='insert_into_postgres_table',
        postgres_conn_id='postgres_localhost',
        sql= '''
            INSERT INTO dag_runs(dt, dag_id) values('{{ds}}', '{{dag.dag_id}}')
        ''')

    task_1 >> task_2