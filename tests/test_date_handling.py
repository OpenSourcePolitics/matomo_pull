import pytest
import matomo_import.date_handling as dh
from datetime import datetime
from .utils import (  # noqa
    settings_fixture,
    settings
)


def test_wrong_secrets_settings():
    settings.secrets['api_settings']['start_date'] = 'dummy value'

    with pytest.raises(AssertionError):
        dh.get_date_range()


def test_start_date_and_end_date_swaped():
    settings.secrets['api_settings']['start_date'] = (
        datetime.strptime('2021-02-01', '%Y-%m-%d').date()
    )
    settings.secrets['api_settings']['end_date'] = (
        datetime.strptime('2021-01-01', '%Y-%m-%d').date()
    )

    with pytest.raises(AssertionError):
        dh.get_date_range()


def test_correct_date_range():
    settings.secrets['api_settings']['start_date'] = (
        datetime.strptime('2021-01-01', '%Y-%m-%d').date()
    )

    settings.secrets['api_settings']['end_date'] = (
        datetime.strptime('2021-01-31', '%Y-%m-%d').date()
    )

    date_range = dh.get_date_range()

    assert len(date_range) == 31
