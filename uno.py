import requests
import csv

url = 'https://api.coincap.io/v2/assets'

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}
response = requests.request("GET", url, headers=headers, data=())
myjson = response.json()

data = []

for x in myjson['data']:
    listing = [x['symbol'], x['name'], x['priceUsd'], x['supply'], x['maxSupply']]
    data.append(listing)

print(data)

