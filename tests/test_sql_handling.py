
import pytest
from matomo_import.sql_handling import (
    convert_data_object_to_sql,
    fill_database
)
import matomo_import.settings as settings
import yaml
import os

FILE_NAME = 'dummy_secrets.yml'
secrets_for_tests = {
    'db_settings': {
        'db_provider': 'sqlite3',
        'db_name': 'dummy_database'
    },
    'requests': {
        'dummy_table': {}
    }
}


@pytest.fixture(scope="session", autouse=True)
def set_test_settings():
    global cursor
    with open(FILE_NAME, 'w') as f:
        yaml.dump(secrets_for_tests, f)

    settings.init(FILE_NAME)

    cursor = settings.connection.cursor()

    yield

    os.remove(FILE_NAME)
    os.remove(secrets_for_tests['db_settings']['db_name'])


def test_data_object_corrupted():
    with pytest.raises(ValueError):
        convert_data_object_to_sql('dummy_value', 'dummy_table')


def test_data_object_is_correct(tmpdir):
    dummy_table_name = 'dummy_table'
    dummy_object = [{"label": "value"}]
    convert_data_object_to_sql(
        dummy_table_name,
        settings.secrets['requests'][dummy_table_name],
        dummy_object
    )

    assert cursor.execute(f"select * from {dummy_table_name}")


def test_table_need_transpose():
    dummy_table_name = 'dummy_table'
    dummy_object = [{"label": "value"}]
    dummy_column_name = 'dummy_index'
    settings.secrets['requests']['dummy_table'] = {
        'need_transpose': True,
        'index_column_new_name': dummy_column_name
    }

    convert_data_object_to_sql(
        dummy_table_name,
        settings.secrets['requests'][dummy_table_name],
        dummy_object
    )

    assert cursor.execute(f"select * from {dummy_table_name}")
    assert cursor.execute(
        f"select {dummy_column_name} from {dummy_table_name}"
    )


def test_fill_database():
    data_objects = {
        'table1': [{'label1': 'value1'}],
        'table2': [{'label2': 'value2'}]
    }
    settings.secrets['requests'] = {
        'table1': {},
        'table2': {}
    }

    fill_database(data_objects)

    for table_name in data_objects:
        assert cursor.execute(f"select * from {table_name}")