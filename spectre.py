
import requests
import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("APP_ID")
SECRET = os.getenv("SECRET")
account_id = os.getenv("account_id")
per_page = 1

url = "https://www.saltedge.com/api/v4/transactions"

payload = {'account_id': account_id,
           'per_page': per_page}

headers = {'Accept': 'application/json',
           'Content-Type': 'application/json',
           'App-id': APP_ID,
           'Secret': SECRET}

r = requests.get(url, params=payload, headers=headers)

print(r.status_code)

r.json()
