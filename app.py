from flask import Flask, request, jsonify
import logging
from v1.main import v1

app = Flask(__name__)
app.register_blueprint(v1, url_prefix='/v1')

if __name__ == '__main__':
    app.run(debug=True)