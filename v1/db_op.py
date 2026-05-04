import psycopg2
import os
from dotenv import load_dotenv
import logging

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')

conn = psycopg2.connect(
    host = DB_HOST,
    port=DB_PORT,
    database = DB_NAME,
    user = DB_USER,
    password = DB_PASS
)

cur = conn.cursor()

def init():
    try:
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(20) NOT NULL UNIQUE,
                        email varchar(255),
                        api_key BYTEA NOT NULL
                    )
                    ''')
    except psycopg2.Error as e:
        conn.rollback()
        logging.exception('PSYCOPG2.ERROR') # TODO Fix this
    else:
        conn.commit()

def add_user(username, email, api_key):
    try:
        cur.execute(
            '''INSERT INTO users (username, email, api_key) VALUES (%s, %s, %s)''',
            (username, email, api_key)
        )
    except psycopg2.errors.UniqueViolation as e:
        conn.rollback()
        return 'unique_violation'
    except psycopg2.Error as e:
        conn.rollback()
        logging.exception('PSYCOPG2.ERROR') # TODO Fix this
        return e
    else:
        conn.commit()
        return True
