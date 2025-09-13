import psycopg2 as db
from dotenv import load_dotenv
import os

load_dotenv()

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
db_port = os.getenv('DB_PORT')


def connect():
    conn = db.connect(
        database = db_name,
        host = db_host,
        user = db_user,
        password = db_password,
        port = db_port
    )
    cur = conn.cursor()
    return conn, cur

def create_user(username, password):
    conn, cur = connect()
    try:
        cur.execute("INSERT INTO users(username, password) VALUES (%s, %s)", (username, password))
    except db.Error as e:
        return e
    else: return True