import pytest
from sqlalchemy import text
from matomo_pull.sql_handling import (
    convert_data_object_to_sql,
    fill_database
)

from .conftest import settings


def test_data_object_corrupted():
    with pytest.raises(ValueError):
        convert_data_object_to_sql('dummy_value', {}, 'dummy_table')


def test_data_object_is_correct(settings_init):
    dummy_table_name = 'dummy_table'
    dummy_object = [{"label": "value"}]
    convert_data_object_to_sql(
        dummy_table_name,
        settings.config['requests'][dummy_table_name],
        dummy_object
    )

    conn = settings.connection.connect()
    assert conn.execute(text(f"select * from {dummy_table_name}"))


def test_table_need_transpose(settings_init):
    dummy_table_name = 'dummy_table'
    dummy_object = [{"label": "value"}]
    dummy_column_name = 'dummy_index'
    settings.config['requests']['dummy_table'] = {
        'need_transpose': True,
        'index_column_new_name': dummy_column_name
    }

    convert_data_object_to_sql(
        dummy_table_name,
        settings.config['requests'][dummy_table_name],
        dummy_object
    )

    conn = settings.connection.connect()
    assert conn.execute(text(f"select * from {dummy_table_name}"))
    assert conn.execute(
        text(f"select {dummy_column_name} from {dummy_table_name}")
    )


def test_fill_database(settings_init):
    data_objects = {
        'table1': [{'label1': 'value1'}],
        'table2': [{'label2': 'value2'}]
    }
    settings.config['requests'] = {
        'table1': {},
        'table2': {}
    }

    fill_database(data_objects)

    conn = settings.connection.connect()
    for table_name in data_objects:
        assert conn.execute(text(f"select * from {table_name}"))
