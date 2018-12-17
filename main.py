from spectre import get_transactions, get_accounts
from heroku import insert_transactions, drop_transactions, insert_accounts
import os
from dotenv import load_dotenv
load_dotenv()

account_id = os.getenv("account_id")
customer_id = os.getenv("customer_id")
per_page = 1000

acccounts = get_accounts(customer_id)

insert_accounts(acccounts)

transactions = get_transactions(account_id,per_page)

drop_transactions(account_id)

insert_transactions(transactions)
