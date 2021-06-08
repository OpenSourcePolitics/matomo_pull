import pytest
import yaml
import os
import matomo_import.settings as settings
from datetime import datetime

FILE_NAME = 'dummy_config.yml'
config_for_tests = {
    'base_url_parameters': {
        'start_date':  datetime.strptime('2021-01-01', '%Y-%m-%d').date(),
        'end_date':  datetime.strptime('2021-01-02', '%Y-%m-%d').date(),
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
    'db_name': 'dummy_database',
    'id_site': '1',
    'start_date': '2021-01-04',
    'token_auth': 'dummy_token'
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
    os.remove(rdv_for_tests['db_name'])


@pytest.fixture(scope="function", autouse=True)
def settings_init():
    settings.init(FILE_NAME, rdv_for_tests)


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
