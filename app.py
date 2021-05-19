from flask import Flask, jsonify, request, send_file
from functools import wraps
from datetime import datetime
import jwt
import os

import main

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['JWT_SECRET_KEY']


def check_for_token(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message': 'Missing token'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], 'HS256')
            if datetime.fromtimestamp(data['exp']) <= datetime.now():
                return jsonify({'message': 'Invalid token'})
        except Exception:
            return jsonify({'message': 'Invalid token'}), 403
        return func(*args, **kwargs)
    return wrapped


@app.route('/', methods=['POST'])
@check_for_token
def index():
    data = request.get_json()
    main.exec(data)

    db_name = data['db_name']
    db_file = open(db_name, 'rb')
    return send_file(
        db_file,
        "application/xsqlite3",
        as_attachment=True,
        attachment_filename=db_name
    )
