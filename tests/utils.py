import pytest
import yaml
import os
import matomo_import.settings as settings
from datetime import datetime

FILE_NAME = 'dummy_secrets.yml'
secrets_for_tests = {
    'db_settings': {
        'db_provider': 'sqlite3',
        'db_name': 'dummy_database'
    },
    'requests': {
        'dummy_table': {
            'url_parameters': {
                'method': 'an_api_method',
                'parameter': 'a_parameter_value'
            }
        }
    },
    'api_settings': {
        'start_date':  datetime.strptime('2021-01-01', '%Y-%m-%d').date(),
        'end_date':  datetime.strptime('2021-01-02', '%Y-%m-%d').date(),
        'url_parameters': {'dummy_arg': 'dummy_value'},
        'base_url': 'example.com'
    }
}

dummy_table_name = list(secrets_for_tests['requests'].keys())[0]
dummy_table_parameters = secrets_for_tests['requests'][dummy_table_name]


@pytest.fixture(scope="module", autouse=True)
def settings_setup():
    with open(FILE_NAME, 'w') as f:
        yaml.dump(secrets_for_tests, f)

    yield

    os.remove(FILE_NAME)
    os.remove(secrets_for_tests['db_settings']['db_name'])


@pytest.fixture(scope="function", autouse=True)
def settings_init():
    settings.init(FILE_NAME)


class DummyResponse:
    data = None

    def __init__(self, data):
        self.data = data


def dummy_correct_http_get(method, url):
    return DummyResponse(
        '[{"dummy_data":"value"}]'.encode('utf-8')
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
        ]""".encode('utf-8')
    )


def dummy_wrong_http_get(method, url):
    class DummyResponse:
        pass

    return DummyResponse()
