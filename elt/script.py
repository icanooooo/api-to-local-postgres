import requests
import csv

url = 'https://api.coincap.io/v2/assets'

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}
response = requests.request("GET", url, headers=headers, data=())
myjson = response.json()
csvheader = ['symbol', 'name', 'price(usd)', 'supply', 'maxSupply']

data = []

for x in myjson['data']:
    listing = [x['symbol'], x['name'], x['priceUsd'], x['supply'], x['maxSupply']]
    data.append(listing)

with open('crypto.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    writer.writerow(csvheader)
    writer.writerows(data)

