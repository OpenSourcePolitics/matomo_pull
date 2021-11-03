import pytest
import matomo_pull.data_handling as dh

from .utils import (  # noqa
    settings_setup,
    settings_init,
    settings,
    dummy_correct_http_get,
    dummy_correct_http_get_subtabled,
    dummy_table_name,
    dummy_table_parameters,
    rdv_for_tests
)


def test_set_data_object_from_url_wrong_parameters():
    with pytest.raises(KeyError):
        dh.set_data_object_from_url('non_existing_table')


def test_set_data_object_from_url_with_date_range(monkeypatch):
    rdv_for_tests.update(
        {
            'start_date': '2021-01-01',
            'end_date': '2021-01-30'
        }
    )
    monkeypatch.setattr(
        settings,
        'remote_database_variables',
        rdv_for_tests,
        raising=False
    )
    dummy_table_parameters.update({'date_range': True})

    monkeypatch.setattr(settings.http, 'request', dummy_correct_http_get)

    data = dh.set_data_object_from_url(
        dummy_table_name,
        dummy_table_parameters
    )

    assert len(data) == 30


def test_set_data_objects_for_sql_conversion_wrong_reports_map():
    reports_map = {'non_existing_table': {}}

    with pytest.raises(KeyError):
        dh.set_data_objects_for_sql_conversion(reports_map)


def test_set_data_objects_for_sql_conversion_correct_reports_map(monkeypatch):
    monkeypatch.setattr(settings.http, 'request', dummy_correct_http_get)
    reports_map = {dummy_table_name: dummy_table_parameters}

    data_objects = dh.set_data_objects_for_sql_conversion(reports_map)

    assert len(data_objects) == 1


def test_parse_range_data_has_subtable(monkeypatch):
    monkeypatch.setattr(
        settings.http, 'request', dummy_correct_http_get_subtabled
    )

    rdv_for_tests['end_date'] = rdv_for_tests['start_date']
    monkeypatch.setattr(
        settings,
        'remote_database_variables',
        rdv_for_tests,
        raising=False
    )

    dummy_table_parameters.update({'date_range': True})

    reports_map = {dummy_table_name: dummy_table_parameters}
    data_objects = dh.set_data_objects_for_sql_conversion(reports_map)

    assert len(data_objects[dummy_table_name]) == 3
