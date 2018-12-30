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


def drop_transactions(user_id):
    connect = psycopg2.connect(
        database=database, user=username, password=password, host=hostname)
    cur = connect.cursor()
    query = f"""DELETE FROM saltedge_transaction
        WHERE account_id in (
            SELECT sa.account_id from saltedge_customer sc
            LEFT JOIN saltedge_login sl on sc.customer_id=sl.customer_id
            LEFT JOIN saltedge_account sa on sa.login_id = sl.login_id
            WHERE sc.user_id ={user_id});"""
    cur.execute(query)
    connect.commit()
    connect.close()


def drop_accounts(user_id):
    connect = psycopg2.connect(
        database=database, user=username, password=password, host=hostname)
    cur = connect.cursor()
    query = f""" DELETE FROM saltedge_account sa
	WHERE sa.login_id in (
		select login_id
		from saltedge_login sl
		INNER JOIN saltedge_customer sc on sc.customer_id = sl.customer_id
		WHERE sc.user_id = {user_id});	"""
    cur.execute(query)
    connect.commit()
    connect.close()


def get_spectre_secrets(user_id):
    connect = psycopg2.connect(
        database=database, user=username, password=password, host=hostname)
    cur = connect.cursor()
    query = f"""SELECT sc.customer_secret, sl.login_secret, sc.customer_id
    FROM saltedge_customer sc
    LEFT JOIN saltedge_login sl on sc.customer_id=sl.customer_id
    LEFT JOIN saltedge_account sa on sa.login_id = sl.login_id
    WHERE sc.user_id = {user_id};"""
    cur.execute(query)
    row = cur.fetchone()
    customer_secret = row[0]
    login_secret = row[1]
    customer_id = row[2]
    connect.commit()
    connect.close()
    return login_secret, customer_secret


def get_accounts(user_id):
    connect = psycopg2.connect(
        database=database, user=username, password=password, host=hostname)
    cur = connect.cursor()
    query = f"""SELECT sa.account_id
    FROM saltedge_customer sc
    LEFT JOIN saltedge_login sl on sc.customer_id=sl.customer_id
    LEFT JOIN saltedge_account sa on sa.login_id = sl.login_id
    WHERE sc.user_id ={user_id};"""
    cur.execute(query)
    accounts = cur.fetchall()
    connect.commit()
    connect.close()
    accounts_list = list(map(lambda x: x[0], accounts))
    return accounts_list


def get_bank_accounts(user_id):
    connect = psycopg2.connect(
        database=database, user=username, password=password, host=hostname)
    cur = connect.cursor()
    query = f"""SELECT sa.account_id
    FROM saltedge_customer sc
    LEFT JOIN saltedge_login sl on sc.customer_id=sl.customer_id
    LEFT JOIN saltedge_account sa on sa.login_id = sl.login_id
    WHERE sa.nature = 'account' and sc.user_id ={user_id};"""
    cur.execute(query)
    accounts = cur.fetchall()
    connect.commit()
    connect.close()
    accounts_list = list(map(lambda x: x[0], accounts))
    return accounts_list


def check_balance(user_id):
    connect = psycopg2.connect(
        database=database, user=username, password=password, host=hostname)
    cur = connect.cursor()
    query = f"""SELECT sa.nature, right(sa."name",4) as "name", sa.balance
    FROM saltedge_customer sc
    LEFT JOIN saltedge_login sl on sc.customer_id = sl.customer_id
    LEFT JOIN saltedge_account sa on sa.login_id = sl.login_id
    WHERE sa.nature = 'account' and sc.user_id = {user_id};"""
    cur.execute(query)
    balance = cur.fetchall()
    connect.commit()
    connect.close()
    return balance


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


def get_logins(user_id):
    connect = psycopg2.connect(
        database=database, user=username, password=password, host=hostname)
    cur = connect.cursor()
    query = f"""SELECT sl.login_id
    FROM saltedge_customer sc
    LEFT JOIN saltedge_login sl on sc.customer_id = sl.customer_id
    WHERE sc.user_id = {user_id};"""
    cur.execute(query)
    logins = cur.fetchall()
    connect.commit()
    connect.close()
    logins_list = list(map(lambda x: x[0], logins))
    return logins_list
