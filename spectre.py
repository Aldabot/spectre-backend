
import requests
import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("APP_ID")
SECRET = os.getenv("SECRET")


def get_transactions(account_id, per_page):

    url = "https://www.saltedge.com/api/v4/transactions"

    payload = {'account_id': account_id,
               'per_page': per_page}

    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json',
               'App-id': APP_ID,
               'Secret': SECRET}

    r = requests.get(url, params=payload, headers=headers)

    return r.json()["data"]


def get_accounts(customer_id):

    url = "https://www.saltedge.com/api/v4/accounts"

    from heroku import get_spectre_secrets
    spectre_secrets = get_spectre_secrets(customer_id)

    login_secret = spectre_secrets[0]
    customer_secret = spectre_secrets[1]

    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json',
               'App-id': APP_ID,
               'Secret': SECRET,
               'Customer-secret': customer_secret,
               'Login-secret': login_secret}

    r = requests.get(url, headers=headers)

    return r.json()["data"]
