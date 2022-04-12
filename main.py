import requests
import json

api_request = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=5&convert=USD&CMC_PRO_API_KEY=5a904e6d-6c76-40bd-8dbb-a0b3e4c02471")

api = json.loads(api_request.content)

print(api)