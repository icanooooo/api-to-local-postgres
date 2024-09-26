from airflow import DAG
from datetime import datetime
from airflow.opertators.python import PythonOperator

def my_task():
    print("hi this is a task")

with DAG('my_dag', start_date=datetime(2024, 1, 8),
         description='Test dag', tags=['test'],
         schedule='@daily', catchup=False):

    task_a = PythonOperator(task_id='Podcast_Mas', python_callable=my_task)
    
