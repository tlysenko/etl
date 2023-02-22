'''
1. Get the file from S3
2. Transform the data
3. Put the file back to S3
'''

import pandas as pd
from datetime import datetime, timedelta
from airflow import DAG
from airflow.hooks.S3_hook import S3Hook
from airflow.operators.python_operator import PythonOperator
from io import StringIO
import yaml

# Get config

with open('./config.yaml') as cfg:
    config = yaml.safe_load(cfg)

AWS_CONN_ID = config['S3']['conn_id']
S3_BUCKET_NAME = config['S3']['bucket_name']
FILE_NAME = config['S3']['file_name']

### Helper functions

def get_file_from_s3(file_name=FILE_NAME,
                     s3_bucket_name=S3_BUCKET_NAME,
                     aws_conn_id=AWS_CONN_ID):

    s3_hook = S3Hook(aws_conn_id)
    print('file name', file_name)
    s3_object = s3_hook.get_key(file_name, s3_bucket_name)

    csv_string = s3_object.get()['Body'].read().decode('utf-8')

    df = pd.read_csv(StringIO(csv_string))
    return df

def put_file_to_s3(df,
                   file_name=FILE_NAME,
                   aws_bucket_name=S3_BUCKET_NAME,
                   aws_conn_id=AWS_CONN_ID):

    s3_hook = S3Hook(aws_conn_id)

    csv_string = StringIO(df.to_csv(index=False))

    s3_hook.load_string(
            string_data=csv_string.getvalue(),
            bucket_name=aws_bucket_name,
            replace=True,
            key='processed.csv'
        )
    return True

def transform(df):
    df.dropna(inplace=True)
    return df

### ETL function

def ETL(file_name=FILE_NAME,
        s3_bucket_name=S3_BUCKET_NAME,
        aws_conn_id=AWS_CONN_ID):

    df = get_file_from_s3(file_name,
                     s3_bucket_name=s3_bucket_name,
                     aws_conn_id=aws_conn_id)

    df = transform(df)

    put_file_to_s3(df,
                   file_name='transformed.csv',
                   aws_bucket_name=s3_bucket_name,
                   aws_conn_id=aws_conn_id)

### DAG

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 2, 20),
    'retries': 0,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    dag_id='csv_from_s3_to_s3_v01',
    default_args=default_args,
    description='Download CSV file from S3, clean, and write to S3',
    schedule_interval=None,
    tags=['cleaning']
)

task_etl = PythonOperator(task_id='ETL',
                                 python_callable=ETL,
                                 dag=dag)
