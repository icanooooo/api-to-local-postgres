import requests
import psycopg2
import time

def fetch_data(url):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers, data=())

    if response.status_code == 200:
        print('Sucessfully Connected')
        myjson = response.json()
    else:
        print(f"failed to get response: {response.status_code}")

    return myjson

def connect_to_db(max_retries=5, delay=10):
    tries = 0
    
    while tries < max_retries:
        try:    
            connection = psycopg2.connect(
                    host="pg_crypto",
                    database="crypto_db",
                    user="icanooo",
                    password="rahasia"
            )
            print("CONNECTED !!!")
            return connection
        except:
            tries += 1
            print('retrying....')
            time.delay(10)

    print("Failure to connect :(")
    

def insert_data(connection, data):
    cursor = connection.cursor()

    create_table = '''
    CREATE TABLE IF NOT EXIST crypto_table (
        id SERIAL PRIMARY KEY,
        symbol VARCHAR(50),
        name VARCHAR(50),
        priceUsd DOUBLE PRECISION,
        supply FLOAT,
        maxSupply FLOAT
    );
    '''

    cursor.execute(create_table)
    
    insert_query = '''
    INSERT INTO (id, symbol, name, price(usd), supply, maxSupply)
    values (%s, %s, %s, %s, %s);
    '''

    for item in data['data']:
       cursor.execute(insert_query, (item['id'], item['symbol'], item['name'], item['priceUsd'],
                                     item['supply'], item['maxSupply'],))
    connection.commit()
    cursor.close()

def main():
    api_url = 'https://api.coincap.io/v2/assets'
    data = fetch_data(api_url)

    if data:
        connection = psycopg2.connect(
            host="pg_crypto",
            database="crypto_db",
            user="icanooo",
            password="rahasia"
        )

        connection = connect_to_db
        insert_data(connection, data)
        connection.close()

if __name__ == "__main__":
    main()