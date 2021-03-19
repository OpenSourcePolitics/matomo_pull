import pytest
import matomo_import.url_handling as uh
import re


from .utils import (  # noqa
    settings_setup,
    settings_init,
    settings,
    dummy_correct_http_get,
    dummy_wrong_http_get,
    dummy_wrong_url_http_get
)


def test_set_url_wrong_secrets():
    settings.secrets['requests'] = {'dummy_value': {}}

    with pytest.raises(KeyError):
        uh.set_url('dummy_value')


def test_set_url_not_date_range(monkeypatch):
    dummy_table = list(settings.secrets['requests'].keys())[0]
    monkeypatch.delitem(
        settings.secrets['requests'][dummy_table],
        'date_range',
        False
    )
    url = uh.set_url(dummy_table)

    assert re.findall(r"date=.{10},.{10}", url)


def test_set_url_date_range_set():
    dummy_table = list(settings.secrets['requests'].keys())[0]
    settings.secrets['requests'][dummy_table]['date_range'] = True

    url = uh.set_url(dummy_table)
    assert not re.findall(r"date=.{10},.{10}", url)


def test_return_consistent_url():
    settings.secrets['api_settings']['base_url'] = (
        'https://example.com/index.php?'
    )
    dummy_table = list(settings.secrets['requests'].keys())[0]
    url = uh.set_url(dummy_table)

    assert re.match(
        r"https://((\w)+\.)+(\w)+/index\.php\?(&(\w)+=[a-zA-Z,-_.]+)+$",
        url
    )


def test_http_get_wrong_answer(monkeypatch):
    dummy_table = list(settings.secrets['requests'].keys())[0]
    url = uh.set_url(dummy_table)

    monkeypatch.setattr(settings.http, 'request', dummy_wrong_http_get)

    with pytest.raises(ValueError):
        uh.http_get(url)

    monkeypatch.setattr(settings.http, 'request', dummy_wrong_url_http_get)

    with pytest.raises(ValueError):
        uh.http_get(url)


def test_http_get_right_answer(monkeypatch):
    dummy_table = list(settings.secrets['requests'].keys())[0]
    url = uh.set_url(dummy_table)

    monkeypatch.setattr(settings.http, 'request', dummy_correct_http_get)

    assert uh.http_get(url) == (
        uh.json.loads(dummy_correct_http_get('GET', url).data.decode('utf-8'))
    )
