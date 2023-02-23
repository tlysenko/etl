import pandas as pd
from datetime import datetime, timedelta
from airflow import DAG
from airflow.hooks.S3_hook import S3Hook
from airflow.operators.python_operator import PythonOperator
from io import StringIO
import yaml

'''
1. Get the file from S3
2. Transform the file
3. Put the file back to S3
'''


class EtlJob:

    def __init__(self):
        self.SRC_FILE_NAME = None
        self.TGT_FILE_NAME = None
        self.AWS_CONN_ID = None
        self.S3_BUCKET_NAME = None

    def get_config(self):
        with open('./config.yaml') as cfg:
            config = yaml.safe_load(cfg)

        self.AWS_CONN_ID = config['S3']['conn_id']
        self.S3_BUCKET_NAME = config['S3']['bucket_name']
        self.SRC_FILE_NAME = config['S3']['file_name']
        self.TGT_FILE_NAME = 'processed.csv'

        return self.AWS_CONN_ID, self.S3_BUCKET_NAME, self.SRC_FILE_NAME, self.TGT_FILE_NAME

    def get_file_from_s3(self):

        s3_hook = S3Hook(self.AWS_CONN_ID)
        print('file name', self.SRC_FILE_NAME)
        s3_object = s3_hook.get_key(self.SRC_FILE_NAME, self.S3_BUCKET_NAME)

        csv_string = s3_object.get()['Body'].read().decode('utf-8')

        df = pd.read_csv(StringIO(csv_string))
        return df

    def put_file_to_s3(self, df):
        s3_hook = S3Hook(self.AWS_CONN_ID)
        csv_string = StringIO(df.to_csv(index=False))
        s3_hook.load_string(
                string_data=csv_string.getvalue(),
                bucket_name=self.S3_BUCKET_NAME,
                replace=True,
                key=self.TGT_FILE_NAME
            )
        return True

    @staticmethod
    def transform(df):
        df.dropna(inplace=True)
        return df

    def run_etl(self):
        self.get_config()
        df = self.get_file_from_s3()
        df = self.transform(df)
        self.put_file_to_s3(df)


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 2, 20),
    'retries': 0,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    dag_id='csv_from_s3_to_s3_v03',
    default_args=default_args,
    description='Download CSV file from S3, clean, and write to S3',
    schedule_interval=None
)

etl_job = EtlJob()

task_etl = PythonOperator(task_id='ETL',
                          python_callable=etl_job.run_etl,
                          dag=dag)
