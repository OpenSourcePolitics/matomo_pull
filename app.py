from flask import Flask, jsonify, request, send_file
from functools import wraps
from datetime import datetime
import jwt
import os
from zipfile import ZipFile

import main
from matomo_import import settings

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
                return jsonify({'message':'Invalid token'}) 
        except Exception:
            return jsonify({'message': 'Invalid token'}), 403
        return func(*args, **kwargs)
    return wrapped


@app.route('/')
@check_for_token
def data():
    settings.set_env_variables()
    main.exec()
    db_file = open(os.environ['DB_NAME'], 'rb')
    return send_file(
        db_file,
        "application/xsqlite3",
        as_attachment=True,
        attachment_filename=os.environ['DB_NAME']
    )
