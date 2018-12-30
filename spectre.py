
import requests
import os

from dotenv import load_dotenv
from heroku import get_bank_accounts, get_logins, get_spectre_secrets

# Spectre API basic url
spectre_url = "https://www.saltedge.com/api/v4/"


load_dotenv()

APP_ID = os.getenv("APP_ID")
SECRET = os.getenv("SECRET")

# Spectre API basic headers
spectre_headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json',
                   'App-id': APP_ID,
                   'Secret': SECRET}

# Debugging
# account_id = os.getenv("account_id")
# customer_id = os.getenv("customer_id")
per_page = 1000
user_id = 1


def get_transactions(user_id, per_page):

    url = spectre_url + "transactions"

    account_ids = get_bank_accounts(user_id)

    total_transactions = []

    for account_id in account_ids:

        payload = {'account_id': account_id,
                   'per_page': per_page}

        try:
            r = requests.get(url, params=payload, headers=spectre_headers)
            account_transactions = r.json()["data"]
            # Consider any status other than 2xx an error
            if not r.status_code // 100 == 2:
                print("Error: Unexpected response {}".format(response))

        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)

        total_transactions = total_transactions + account_transactions

    return total_transactions


def get_accounts(user_id):

    url = spectre_url + "accounts"

    spectre_secrets = get_spectre_secrets(user_id)

    login_secret = spectre_secrets[0]
    customer_secret = spectre_secrets[1]

    account_headers = {'Customer-secret': customer_secret,
                       'Login-secret': login_secret}

    account_headers.update(spectre_headers)

    try:
        r = requests.get(url, headers=account_headers)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

    return r.json()["data"]


def refresh_login(user_id):

    logins = get_logins(user_id)

    for login in logins:

        url = spectre_url + "/logins/{}/refresh".format(login)

        try:
            r = requests.put(url, headers=spectre_headers)
            print(r.status_code)
            print(r.json())
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)

    return "Refreshed"
