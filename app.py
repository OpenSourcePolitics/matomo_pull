from flask import Flask, jsonify, request, make_response, send_file
from functools import wraps
from datetime import datetime, timedelta
import jwt
import json
import os
from zipfile import ZipFile

import main
from matomo_import import settings

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

def check_for_token(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            request_args = json.loads(request.data.decode('utf-8'))
        except:
            return jsonify({'message':'Invalid passed data'})
        
        token = request_args.get('token')
        if not token:
            return jsonify({'message': 'Missing token'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], 'HS256')
        except :
            return jsonify({'message': 'Invalid token'}), 403
        return func(*args, **kwargs)
    return wrapped

@app.route('/')
@check_for_token
def data():
    settings.set_env_variables()
    zip_name = f"{os.environ['DB_NAME']}.zip"

    with ZipFile(zip_name, 'w') as zip_file:
        main.exec()
        zip_file.write(os.environ['DB_NAME'])

    return send_file(
        zip_name,
        "application/zip",
        as_attachment=True,
        attachment_filename="banane.zip"
    )


@app.route('/login', methods=['POST'])
def login():
    args = json.loads(request.data.decode('utf-8'))
    if args.get('username') == 'user' and args.get('password') == 'password':
        token = jwt.encode(
            {
                'user': request.args.get('user'),
                'exp': datetime.now() + timedelta(minutes=30)
            },
            app.config['SECRET_KEY'],
            'HS256'
        )
        return jsonify({'token': token})
    else:
        return jsonify({'message':'Unable to verify'})
