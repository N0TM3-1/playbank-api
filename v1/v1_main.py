from flask import Blueprint, request, jsonify
import v1.db_op as db

v1 = Blueprint('v1', __name__)

db.init()

@v1.route('/')
def root():
    return jsonify({'message':'hello'}), 200