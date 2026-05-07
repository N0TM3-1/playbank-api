import os, sys
from dotenv import load_dotenv
from flask import Flask

from v1.main import v1
from v1 import db_op as db

load_dotenv()
APP_DEBUG: bool = os.getenv('DEBUG')

result = db.init()
if not result:
    print("Database initialization error, exiting")
    sys.exit()

app = Flask(__name__)

app.register_blueprint(v1)

if __name__=='__main__':
    app.run(debug=APP_DEBUG)