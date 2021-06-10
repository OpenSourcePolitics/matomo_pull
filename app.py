from flask import Flask, jsonify, request, send_file
from functools import wraps
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
            jwt.decode(token, app.config['SECRET_KEY'], 'HS256')
        except jwt.exceptions.ExpiredSignatureError:
            return jsonify({'message': 'Token expired'}), 403
        except jwt.exceptions.InvalidSignatureError:
            return jsonify({'message': 'Invalid token'}), 403
        except Exception as e:
            return jsonify({'message': f"{type(e).__name__}:  {str(e)}"})
        return func(*args, **kwargs)
    return wrapped


def check_data(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            [
                request.args['base_url'],
                request.args['id_site'],
                request.args['start_date'],
                request.args['token_auth'],
                request.args['db_name']
            ]
        except Exception:
            return jsonify({'message': 'Invalid data'}), 403
        return func(*args, **kwargs)
    return wrapped


@app.route('/')
@check_for_token
@check_data
def index():
    data = request.args
    try:
        main.exec(data)
    except Exception:
        return jsonify(
            {'message': 'Error executing script: recheck database variables'}
        ), 403
    db_name = data['db_name']
    db_file = open(db_name, 'rb')
    return send_file(
        db_file,
        "application/xsqlite3",
        as_attachment=True,
        attachment_filename=db_name
    )


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=os.environ["PORT"])
