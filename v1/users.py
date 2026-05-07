from flask import Blueprint, request, jsonify
from email_validator import validate_email, EmailNotValidError
import secrets, base64, bcrypt
from . import db_op as db
from .error import error

users = Blueprint('users', __name__, url_prefix='/users')

def gen_key(): # Generate API key
    prefix = secrets.token_hex(8)
    key = secrets.token_bytes(32) # Generate random key
    user_key = base64.urlsafe_b64encode(key).decode('utf-8') # Decode to retreive the plaintext API key
    user_key = prefix+'_'+user_key
    db_key = bcrypt.hashpw(user_key.encode(), bcrypt.gensalt()) # Encode, salt and hash the API key for storing
    return prefix, user_key, db_key


def check_user(username, email):
    ### USERNAME VALIDATION ###
    if not username or not username.strip():
        return False, error('validation_error', 'Username is required and can not be empty', 400)
    if ' ' in username:
        return False, error('validation_error', 'Username must not contain spaces', 400)
    
    ### EMAIL VALIDATION ###
    try:
        validate_email(email, check_deliverability=False)
    except EmailNotValidError as e:
        return False, error('validation_error', f'Invalid email: {email}', 400)
    return True, ''

@users.route('', methods=['POST'])
def create_user():
    data = request.get_json(silent=True)
    if data:
        username=data.get('username') # Used for identification
        email = data.get('email') # Optional
        is_valid, validation_result = check_user(username, email)
        if not is_valid:
            return validation_result
        prefix, api_key, db_key = gen_key()
        res = db.add_user(username, email, prefix, db_key)
        if res==True:
            return jsonify({'api_key':f'{api_key}'}), 201
        elif res == 'unique_violation':
            return error('conflict', f'User {username} already exists', 409)
        elif res == 'key_prefix_error':
            while res == 'key_prefix_error':
                prefix, api_key, db_key = gen_key()
                res = db.add_user(username, email, prefix, db_key)
                return jsonify({'api_key':f'{api_key}'}), 201
        else:
            return error('database_error', 'Database operation failed', 500)
    else:
        return error('bad_request', 'Missing or invalid JSON', 400)