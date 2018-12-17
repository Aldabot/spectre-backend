import os
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import Json

load_dotenv()

hostname = os.getenv('hostname')
username = os.getenv('username')
password = os.getenv('password')
database = os.getenv('database')
port = "5432"


def insert_transactions(data):
    for item in data:
        item['balance'] = Json(item['extra']['account_balance_snapshot'])

    with psycopg2.connect(database=database, user=username, password=password, host=hostname) as connect:
        with connect.cursor() as cursor:
            query = """
                INSERT into
                    saltedge_transaction
                    (id, account_id, amount, balance, description, made_on, currency_code)
                VALUES
                    (%(id)s, %(account_id)s, %(amount)s, %(balance)s, %(description)s, %(made_on)s, %(currency_code)s);
            """
            cursor.executemany(query, data)

        connect.commit()
    connect.close()


def drop_transactions(account_id):
    connect = psycopg2.connect(
        database=database, user=username, password=password, host=hostname)
    cur = connect.cursor()
    query = f""" DELETE FROM saltedge_transaction
     WHERE account_id = {account_id};"""
    cur.execute(query)
    connect.commit()
    connect.close()


def get_spectre_secrets(customer_id):
    connect = psycopg2.connect(
        database=database, user=username, password=password, host=hostname)
    cur = connect.cursor()
    query = f""" SELECT customer_secret,login_secret
    FROM saltedge_customer sc
    LEFT JOIN saltedge_login sl on sc.customer_id=sl.customer_id
    WHERE sc.customer_id = {customer_id};"""
    cur.execute(query)
    row = cur.fetchone()
    customer_secret = row[0]
    login_secret = row[1]
    connect.commit()
    connect.close()
    return login_secret, customer_secret


def insert_accounts(data):
    with psycopg2.connect(database=database, user=username, password=password, host=hostname) as connect:
        with connect.cursor() as cursor:
            query = """
                INSERT into
                    saltedge_account
                    (account_id, login_id, name, currency_code, balance, nature)
                VALUES
                    (%(id)s, %(login_id)s, %(name)s, %(currency_code)s, %(balance)s, %(nature)s);
            """
            cursor.executemany(query, data)
        connect.commit()
    connect.close()
