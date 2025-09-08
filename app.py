from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

@app.route("/hello", methods=['GET'])
def hello():
    return 'Hello there!\n'

if __name__ == '__main__':
    app.run(debug=True)