from flask import jsonify

def error(error:str, message:str, code:int):
    return jsonify({'error':f'{error}', 'message':f'{message}'}), code