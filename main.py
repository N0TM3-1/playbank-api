import os
from dotenv import load_dotenv
from flask import Flask

from v1.v1_main import v1

load_dotenv()
APP_DEBUG: bool = os.getenv('DEBUG')

app = Flask(__name__)

app.register_blueprint(v1, url_prefix="/v1")

if __name__=='__main__':
    app.run(debug=APP_DEBUG)