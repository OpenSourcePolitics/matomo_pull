import pytest
import yaml
import os
import matomo_import.settings as settings

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
        'start_date': '2021-01-01',
        'end_date': '2021-01-31',
        'url_parameters': {'dummy_arg': 'dummy_value'},
        'base_url': 'example.com'
    }
}

@pytest.fixture(autouse=True)
def settings_fixture():
    with open(FILE_NAME, 'w') as f:
        yaml.dump(secrets_for_tests, f)

    settings.init(FILE_NAME)

    yield

    os.remove(FILE_NAME)
    os.remove(secrets_for_tests['db_settings']['db_name'])
