
import pytest
from matomo_import.sql_handling import (
    convert_data_object_to_sql,
    fill_database
)

from .utils import (  # noqa
    settings_setup,
    settings_init,
    settings
)


def test_data_object_corrupted():
    with pytest.raises(ValueError):
        convert_data_object_to_sql('dummy_value', {}, 'dummy_table')


def test_data_object_is_correct():
    dummy_table_name = 'dummy_table'
    dummy_object = [{"label": "value"}]
    convert_data_object_to_sql(
        dummy_table_name,
        settings.config['requests'][dummy_table_name],
        dummy_object
    )

    cursor = settings.connection.cursor()
    assert cursor.execute(f"select * from {dummy_table_name}")


def test_table_need_transpose():
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

    cursor = settings.connection.cursor()
    assert cursor.execute(f"select * from {dummy_table_name}")
    assert cursor.execute(
        f"select {dummy_column_name} from {dummy_table_name}"
    )


def test_fill_database():
    data_objects = {
        'table1': [{'label1': 'value1'}],
        'table2': [{'label2': 'value2'}]
    }
    settings.config['requests'] = {
        'table1': {},
        'table2': {}
    }

    fill_database(data_objects)

    cursor = settings.connection.cursor()
    for table_name in data_objects:
        assert cursor.execute(f"select * from {table_name}")
