import pytest
import matomo_pull.date_handling as dh
# from datetime import timedelta

from .utils import (  # noqa
    settings_setup,
    settings_init,
    settings
)


def test_wrong_database_variables_settings(monkeypatch):
    monkeypatch.setattr(
        settings,
        'remote_database_variables',
        {'start_date': 'dummy_value'},
        raising=False
    )

    with pytest.raises(ValueError):
        dh.get_date_range()


def test_start_date_and_end_date_swaped(monkeypatch):
    monkeypatch.setattr(
        settings,
        'remote_database_variables',
        {
            'end_date': '2000-01-01',
            'start_date': '2020-01-01'
        },
        raising=False
    )

    with pytest.raises(ValueError):
        dh.get_date_range()


def test_correct_date_range(monkeypatch):
    monkeypatch.setattr(
        settings,
        'remote_database_variables',
        {
            'start_date': '2020-01-01',
            'end_date': '2020-01-01'
        },
        raising=False
    )

    date_range = dh.get_date_range()

    assert len(date_range) == 1
