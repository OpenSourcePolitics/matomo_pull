import pytest
import requests
import requests_mock
import matomo_import.url_handling as uh
import re

from .utils import (  # noqa
    settings_fixture,
    settings
)


def test_set_url_wrong_secrets():
    settings.secrets['requests'] = {'dummy_value': {}}

    with pytest.raises(KeyError):
        uh.set_url('dummy_value')


def test_set_url_not_date_range():
    dummy_table = list(settings.secrets['requests'].keys())[0]
    url = uh.set_url(dummy_table)

    assert re.findall(r"date=.{10},.{10}", url)


def test_set_url_date_range_set():
    dummy_table = list(settings.secrets['requests'].keys())[0]
    settings.secrets['requests'][dummy_table]['date_range'] = True

    url = uh.set_url(dummy_table)
    assert not re.findall(r"date=.{10},.{10}", url)


def test_return_consistent_url():
    settings.secrets['api_settings']['base_url'] = 'https://example.com/index.php?'
    dummy_table = list(settings.secrets['requests'].keys())[0]
    url = uh.set_url(dummy_table)

    assert re.match(r"https://((\w)+\.)+(\w)+/index\.php\?(&(\w)+=[a-zA-Z,-_.]+)+$", url)


def test_http_get_wrong_answer(monkeypatch):
    dummy_table = list(settings.secrets['requests'].keys())[0]
    url = uh.set_url(dummy_table)

    def dummy_return(method, url):
        class DummyResponse:
            pass

        return DummyResponse()

    monkeypatch.setattr(settings.http, 'request', dummy_return)

    with pytest.raises(AttributeError):
        uh.http_get(url)


def test_http_get_right_answer(monkeypatch):
    dummy_table = list(settings.secrets['requests'].keys())[0]
    url = uh.set_url(dummy_table)

    def dummy_return(method, url):
        class DummyResponse:
            data = None

            def __init__(self, data):
                self.data = data

        return DummyResponse('dummy_data'.encode('utf-8'))

    monkeypatch.setattr(settings.http, 'request', dummy_return)

    assert uh.http_get(url) == dummy_return('GET', url).data.decode('utf-8')
