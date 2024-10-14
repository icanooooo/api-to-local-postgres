from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
import subprocess
import requests
import psycopg2
import time
import json

def fetch_api():
    headers = {
            'Accept':'application/json',
            'Content-Type': 'application/json'
    }
    
    url = "https://api.coincap.io/v2/assets"
    response = requests.request("GET", url, headers=headers, data=())

    if response.status_code == 200: #Connected Let's go:
        print("Sucessfully Connected to API")
        myjson = response.json()

        return myjson
    else:
        raise Exception(f"womp,womp: {response.status_code}")

def load_to_db(**kwargs):

    # Connecting to DB
    tries=0

    while tries < 5:
        try:
            connection = psycopg2.connect(
                host="destination_pgres",
                database="destination_db",
                user="icanooo",
                password="secret"
            )
            print("CONNECTED")
            break
        except:
            tries += 1
            print('retrying..')
            time.sleep(15)


    # Inserting data from API to DB
    try:
        cursor = connection.cursor()

        create_table = '''
        CREATE TABLE IF NOT EXISTS crypto_table (
            id SERIAL PRIMARY KEY,
            symbol VARCHAR(50),
            name VARCHAR(50),
            price_in_usd DOUBLE PRECISION,
            supply FLOAT,
            max_supply FLOAT,
            insert_date TIMESTAMP
        );
        '''
        cursor.execute(create_table)
        print("Table created <3")

        insert_query ='''
        INSERT INTO crypto_table (symbol, name, price_in_usd, supply, max_supply, insert_date)
        values (%s, %s, %s, %s, %s, %s);
        '''

        # Using kwargs
        ti = kwargs['ti']

        api_pull = ti.xcom_pull(task_ids='ingest_api')
        data = api_pull['data']
        
        for item in data:
            cursor.execute(insert_query, (item['symbol'], item['name'], 
                                          float(item['priceUsd']) if item['priceUsd'] else None,
                                          float(item['supply']) if item['supply'] else None,
                                          float(item['maxSupply']) if item['maxSupply'] else None,
                                          datetime.now()
                                          )
                                        )
            print(f"inserting {item['name']}")

        connection.commit()
        cursor.close()
        connection.close()

    except psycopg2.Error as e:
        print(f"Error due to: {e}")
        return False


with DAG('ingestToPostgres', start_date=datetime(2024, 1, 8),
         description='Test dag', tags=['test'],
         schedule='@daily', catchup=False):

    task_a = PythonOperator(task_id='ingest_api', python_callable=fetch_api)
    task_b = PythonOperator(task_id='inserting_db', python_callable=load_to_db)
    
    task_a >> task_b
