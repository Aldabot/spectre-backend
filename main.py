from spectre import get_transactions, get_accounts, refresh_login
from heroku import insert_transactions, drop_transactions, insert_accounts, check_balance, drop_accounts

import os

from flask import Flask, jsonify, make_response
from flask import request

from dotenv import load_dotenv
load_dotenv()

per_page = 1000

user_id = 1

# Refresh account balances


def refresh_balances(user_id):
    refresh_login(user_id)
    drop_accounts(user_id)
    acccounts = get_accounts(user_id)
    insert_accounts(acccounts)


refresh_balances(user_id)


def refresh_transactions(user_id):
    refresh_login(user_id)
    drop_transactions(user_id)
    transactions = get_transactions(user_id, per_page)
    insert_transactions(transactions)


refresh_transactions(user_id)
