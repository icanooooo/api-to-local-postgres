from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
import subprocess

def getData():
    script_path = "../elt/script.py"
    result = subprocess.run(["python", script_path],
                            capture_output=True,
                            text=True)
    
    if result.returncode != 0:
        raise Exception(f"Script failed with error: {result.stderr}")
    else:
        print(result.stdout)


def my_task():
    print("hi this is a task")

with DAG('ingestToPostgres', start_date=datetime(2024, 1, 8),
         description='Test dag', tags=['test'],
         schedule='@daily', catchup=False):

    task_a = PythonOperator(task_id='moveCryptoSQL', python_callable=getData)
    
