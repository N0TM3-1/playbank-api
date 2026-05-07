import psycopg2, os, logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
handler = logging.FileHandler('log.log')
formatter = logging.Formatter('[%(asctime)s]: %(name)s - %(levelname)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')

def connect():
    conn = psycopg2.connect(
        host = DB_HOST,
        port=DB_PORT,
        database = DB_NAME,
        user = DB_USER,
        password = DB_PASS
    )

    cur = conn.cursor()
    return conn, cur

def disconnect(conn, cur):
    cur.close()
    conn.close()

def init():
    conn, cur = connect()
    try:
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(20) NOT NULL UNIQUE,
                        email varchar(255),
                        key_prefix varchar(16),
                        api_key BYTEA NOT NULL,
                        wallets INT[],
                        CONSTRAINT unique_key_prefix UNIQUE (key_prefix)
                    )
                    """)
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS wallets (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(20),
                    owner INT,
                    balance INT,
                    CONSTRAINT fk_owner FOREIGN KEY(owner) REFERENCES users(id)
                    )
                    """)
    except psycopg2.Error:
        conn.rollback()
        logger.exception('PSYCOPG2.ERROR')
        disconnect(conn, cur)
        return False
    else:
        conn.commit()
        disconnect(conn, cur)
        return True

def add_user(username, email, key_prefix, api_key):
    conn, cur = connect()
    try:
        cur.execute(
            """INSERT INTO users (username, email, key_prefix, api_key) VALUES (%s, %s, %s, %s)""",
            (username, email, key_prefix, api_key)
        )
    except psycopg2.errors.UniqueViolation as e:
        conn.rollback()
        disconnect(conn, cur)
        if e.diag.constraint_name == 'unique_key_prefix':
            return 'key_prefix_error'
        return 'unique_violation'
    except psycopg2.Error as e:
        conn.rollback()
        logger.exception('PSYCOPG2.ERROR')
        disconnect(conn, cur)
        return e
    else:
        conn.commit()
        disconnect(conn, cur)
        return True

def create_wallet(name, owner):
    pass