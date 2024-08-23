import requests
import pyscopg2

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

def main():
    api_url = 'https://api.coincap.io/v2/assets'
    fetch_data(api_url)

if __name__ == "__main__":
    main()