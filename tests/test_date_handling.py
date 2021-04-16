import pytest
import matomo_import.date_handling as dh
from datetime import datetime, timedelta

from .utils import (  # noqa
    settings_setup,
    settings_init,
    settings
)


def test_wrong_config_settings(monkeypatch):
    settings.env['START_DATE'] = 'dummy_value'

    with pytest.raises(ValueError):
        dh.get_date_range()


def test_start_date_and_end_date_swaped(monkeypatch):
    monkeypatch.setenv('END_DATE','2000-01-01')

    with pytest.raises(ValueError):
        dh.get_date_range()


def test_correct_date_range(monkeypatch):
    wanted_delta = 30
    start_date = dh.string_to_date(settings.env['START_DATE'])
    monkeypatch.setenv(
        'END_DATE',
        start_date + timedelta(wanted_delta - 1)
    )

    date_range = dh.get_date_range()

    assert len(date_range) == wanted_delta
