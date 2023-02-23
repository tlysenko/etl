import airflow.utils.dates
from airflow import DAG
from airflow.operators.python import PythonOperator
import logging

'''
Printing context variables to log
'''

dag = DAG(
    dag_id="listing_context_variables_v01",
    start_date=airflow.utils.dates.days_ago(3),
    schedule_interval="@daily",
)


def print_context(ds, **kwargs):
    logging.info("Printing context variables:")
    for key, value in kwargs.items():
        logging.info(f"{key}: {value}")


task_print_context = PythonOperator(
    task_id="print_context", python_callable=print_context, dag=dag, provide_context=True
)

task_print_context

