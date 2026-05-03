from flask import Blueprint, request, jsonify
from . import db_op as db

users = Blueprint('users', __name__, url_prefix='/users')

@users.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    if data:
        username=data.get('username')
        password=data.get('password')
        res = db.add_user(username, password)
        if res==True:
            return jsonify({'message':'User created successfuly'}), 201
        else:
            return jsonify({'message':'Internal Server Error'}), 500
    else:
        return jsonify({'error':'Bad Request', 'message':'No content received'}), 400