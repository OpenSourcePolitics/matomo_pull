import main

from .conftest import (  # noqa
    client,
    expired_token,
    invalid_token,
    valid_token,
    invalid_url,
    valid_url,
    set_sent_file,
    DUMMY_JWT_SECRET_KEY
)


def test_no_token_passed(client):
    response = client.get("/")

    assert response.status_code == 403
    assert response.data == b'{"message":"Missing token"}\n'


def test_token_has_expired(client, expired_token):
    url = f"/?token={expired_token}"

    response = client.get(url)
    assert response.data == b'{"message":"Token expired"}\n'


def test_token_signature_invalid(client, invalid_token):
    url = f"/?token={invalid_token}"

    response = client.get(url)
    assert response.data == b'{"message":"Invalid token"}\n'


def test_token_valid(client, valid_token):
    url = f"/?token={valid_token}"

    response = client.get(url)
    assert b'token' not in response.data
    assert response.data == b'{"message":"Invalid data"}\n'


def test_not_all_data_given(client, invalid_url):

    response = client.get(invalid_url)
    assert response.data == b'{"message":"Invalid data"}\n'


def test_database_variables_not_working(monkeypatch, client, valid_url):
    def failing_exec():
        raise Exception

    monkeypatch.setattr(main, "exec", failing_exec, raising=True)

    response = client.get(valid_url)
    assert response.status_code == 403
    assert response.data == (
        b'{"message":"Error executing script: recheck database variables"}\n'
    )


def test_all_clear(monkeypatch, client, valid_url, set_sent_file):
    def succeeding_exec(data={'db_name': 'dummy_database'}):
        return data

    monkeypatch.setattr(main, "exec", succeeding_exec, raising=False)

    response = client.get(valid_url)
    assert response.status_code == 200
