import requests
import psycopg2
import time
import datetime

# Function for fetching Data from API
def fetch_data(url):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    } # ?
    response = requests.request("GET", url, headers=headers, data=())

    if response.status_code == 200: # if Connection succedd
        print('Sucessfully Connected to API')
        myjson = response.json()
    else: # if response other than '200' (failed)
        print(f"failed to get response: {response.status_code}")

    return myjson

# Function to connect to db
def connect_to_db(max_retries=5, delay=10): 
    tries = 0
    
    while tries < max_retries:
        try:    
            connection = psycopg2.connect( #through this command
                    host="destination_pgres",
                    database="destination_db",
                    user="icanooo",
                    password="secret"
            )
            print("CONNECTED to database!!!")
            return connection
        except:
            tries += 1
            print('retrying....')
            time.sleep(15)

    print("Failure to connect :(")
    
# Function to insert data to postgresdb
def insert_data(connection, data):
    try:
        cursor = connection.cursor() # Creating cursor(?)

        # to check if table exist in database
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
        
        # To insert data from json format
        insert_query = '''
        INSERT INTO crypto_table (symbol, name, price_in_usd, supply, max_supply, insert_date)
        values (%s, %s, %s, %s, %s, %s);
        '''

        for item in data:
            cursor.execute(insert_query, (item['symbol'], item['name'], 
                                          float(item['priceUsd']) if item['priceUsd'] else None,
                                          float(item['supply']) if item['supply'] else None,
                                          float(item['maxSupply']) if item['maxSupply'] else None,
                                          datetime.datetime.now()
                                          )
                                        )
            print(f"inserting {item['name']}")

        connection.commit()
        cursor.close()
        connection.close()

        print("Job done")
    except psycopg2.Error as e:
        print(f"Error due to: {e}")
        return False

def main():
    api_url = 'https://api.coincap.io/v2/assets'
    alpha = fetch_data(api_url)
    data = alpha['data']

    if data:
        connect = connect_to_db()
        insert_data(connect, data)

if __name__ == "__main__":
    main()
