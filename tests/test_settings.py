import pytest
import sqlite3
import matomo_import.settings as settings


def test_initialize_config_file_not_correct(tmpdir):
    dummy_file = tmpdir.join('dummy_config.yml')
    dummy_file.write("dummy_key: dummy_value")

    with pytest.raises(KeyError):
        settings.init(dummy_file.strpath)


def test_initialize_config_file_not_found():
    with pytest.raises(FileNotFoundError):
        settings.init('dummy_file.yml')


def test_initialize_database_setup(monkeypatch):
    monkeypatch.setenv('DB_NAME', 'dummy_database')

    assert isinstance(
        settings.set_database_connection(),
        sqlite3.Connection
    )

    monkeypatch.delenv('DB_NAME')

    with pytest.raises(KeyError):
        settings.set_database_connection()


def test_env_variables_wrongly_set(monkeypatch):
    monkeypatch.delenv('DB_NAME', False)

    with pytest.raises(KeyError):
        settings.set_env_variables()


def test_initialize_all_correct(tmpdir):
    dummy_file = tmpdir.join('dummy_config.yml')
    dummy_file.write("""
        base_url_parameters:
            dummy_param: None
        requests:
            dummy_table: None
    """)

    settings.init(dummy_file.strpath)

    assert 'connection' in dir(settings)
    assert 'http' in dir(settings)
    assert 'config' in dir(settings)
