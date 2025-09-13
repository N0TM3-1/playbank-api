from flask import Blueprint, request, jsonify
import db_op as db

v1 = Blueprint('v1', __name__)

@v1.route('/hello')
def hello():
    return 'Hello from v1'

@v1.route('/users', methods=['GET','POST'])
def users():
    if request.method == 'GET':
        return jsonify({'message':'GET request in development...'}), 200
    elif request.method=='POST':
        data = request.get_json()
        username = data['username']
        password = data['password']
        if db.create_user(username, password) != True:
            return jsonify({'message':'User created successfully'}), 210