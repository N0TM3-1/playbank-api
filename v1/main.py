from flask import Flask, Blueprint, request, jsonify
from . import db_op as db
from v1.users import users

v1 = Blueprint('v1', __name__, url_prefix='/v1')
v1.register_blueprint(users)