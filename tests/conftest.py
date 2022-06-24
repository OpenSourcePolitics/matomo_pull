import pytest
import yaml
import os
import jwt
import matomo_pull.settings as settings
from datetime import datetime, timedelta, date
from sqlalchemy import create_engine

FILE_NAME = 'dummy_config_file.yml'
DUMMY_JWT_SECRET_KEY = 'dummy_secret'
config_for_tests = {
    'base_url_parameters': {
        'start_date': datetime.strptime('2021-01-01', '%Y-%m-%d').date(),
        'end_date': datetime.strptime('2022-01-02', '%Y-%m-%d').date(),
    },
    'requests': {
        'dummy_table': {
            'url_parameters': {
                'method': 'an_api_method',
                'parameter': 'a_parameter_value'
            }
        }
    }
}
rdv_for_tests = {
    'base_url': 'https://example.com/',
    'db_name': 'postgres',
    'id_site': '1',
    'start_date': '2020-01-04',
    'end_date': '2030-01-01',
    'token_auth': 'dummy_token',
    'POSTGRES_USER': 'postgres',
    'POSTGRES_PASSWORD': 'postgres',
    'POSTGRES_HOST': 'localhost',
    'POSTGRES_PORT': '5432'
}
dummy_table_name = list(config_for_tests['requests'].keys())[0]
dummy_table_parameters = config_for_tests['requests'][dummy_table_name]


@pytest.fixture(scope="module", autouse=True)
def settings_setup():
    for k, v in rdv_for_tests.items():
        os.environ[k] = v

    with open(FILE_NAME, 'w') as f:
        yaml.dump(config_for_tests, f)

    yield

    os.remove(FILE_NAME)


@pytest.fixture(scope="function", autouse=True)
def settings_init():
    drop_database()
    settings.init(FILE_NAME, rdv_for_tests)

    yield


def drop_database():
    vars = rdv_for_tests
    connection = create_engine(
        f"postgresql://{vars['POSTGRES_USER']}:{vars['POSTGRES_PASSWORD']}"
        f"@{vars['POSTGRES_HOST']}:{vars['POSTGRES_PORT']}"
        f"/{vars['db_name']}"
    )
    for table_name in connection.table_names():
        connection.execute(f"drop table if exists {table_name};")


class DummyResponse:
    data = None

    def __init__(self, data):
        self.data = data.encode('utf-8')


def dummy_correct_http_get(method, url):
    return DummyResponse(
        '[{"dummy_data":"value"}]'
    )


def dummy_correct_http_get_subtabled(method, url):
    return DummyResponse(
        """[
            {
                "label": "Direct Entry"
            },
            {
                "label": "Websites",
                "subtable": [
                    {
                        "label": "sublabel"
                    }
                ]
            }
        ]"""
    )


def dummy_wrong_url_http_get(method, url):
    return DummyResponse(
        """{
                "result": "error",
                "error_info": "dummy informations"
        }"""
    )


def dummy_wrong_http_get(method, url):
    class DummyResponse:
        pass

    return DummyResponse()


def dummy_date(mtm_vars):
    return date.today()


@pytest.fixture
def client(scope="module", autouse=True):
    from app import app
    app.config['SECRET_KEY'] = DUMMY_JWT_SECRET_KEY
    return app.test_client()


@pytest.fixture
def expired_token():
    payload = {
        'exp': datetime.now() - timedelta(days=7)
    }
    token = jwt.encode(
        payload,
        DUMMY_JWT_SECRET_KEY,
    )
    return token


@pytest.fixture
def invalid_token():
    payload = {
        'exp': datetime.now() + timedelta(minutes=30)
    }
    token = jwt.encode(
        payload,
        DUMMY_JWT_SECRET_KEY + DUMMY_JWT_SECRET_KEY,
    )
    return token


@pytest.fixture
def valid_token():
    payload = {
        'exp': datetime.now() + timedelta(minutes=30)
    }
    token = jwt.encode(
        payload,
        DUMMY_JWT_SECRET_KEY,
    )
    return token


@pytest.fixture
def invalid_url(valid_token):
    return (
        f"/?token={valid_token}"
        "&site_id=dummy_site"
        "&token_auth=dummy_auth"
    )


@pytest.fixture
def valid_url(valid_token):
    return (
        f"/?token={valid_token}"
        "&id_site=dummy_site"
        "&token_auth=dummy_auth"
        "&base_url=dummy_url"
        "&start_date=dummy_date"
        "&db_name=dummy_name"
    )


@pytest.fixture
def set_sent_file():
    with open('dummy_name', 'wb'):
        yield

    os.remove('dummy_name')
