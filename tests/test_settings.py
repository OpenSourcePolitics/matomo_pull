import pytest
import os
import matomo_pull.settings as settings
from tests.utils import rdv_for_tests, settings_setup  # noqa


def test_config_file_not_correct(tmpdir):
    dummy_file = tmpdir.join('dummy_config.yml')
    dummy_file.write("dummy_key: dummy_value")

    with pytest.raises(KeyError):
        settings.init(dummy_file.strpath)


def test_config_file_not_found():
    with pytest.raises(FileNotFoundError):
        settings.init('dummy_file.yml')


def test_database_setup(settings_setup):
    assert isinstance(
        settings.set_database_connection(
            vars={
                'POSTGRES_USER': os.environ['POSTGRES_USER'],
                'POSTGRES_PASSWORD': os.environ['POSTGRES_PASSWORD'],
                'POSTGRES_HOST': os.environ['POSTGRES_HOST'],
                'POSTGRES_PORT': os.environ['POSTGRES_PORT'],
                'db_name': os.environ['db_name']
            }
        ),
        settings.sqlalchemy.engine.base.Engine
    )


def test_database_setup_wrong(settings_setup):
    with pytest.raises(ValueError):
        settings.set_database_connection(
            vars={
                'POSTGRES_USER': os.environ['POSTGRES_USER'] + 'dummy',
                'POSTGRES_PASSWORD': os.environ['POSTGRES_PASSWORD'],
                'POSTGRES_HOST': os.environ['POSTGRES_HOST'],
                'POSTGRES_PORT': os.environ['POSTGRES_PORT'],
                'db_name': os.environ['db_name']
            }
        )


def test_database_variables_wrongly_set(tmpdir, monkeypatch):
    with pytest.raises(KeyError):
        settings.set_remote_database_variables()


def test_postgres_variables_wrongly_set():
    with pytest.raises(ValueError):
        settings.set_database_connection()


def test_all_correct(tmpdir):
    dummy_file = tmpdir.join('dummy_config.yml')
    dummy_file.write("""
        base_url_parameters:
            dummy_param: None
        requests:
            dummy_table: None
    """)

    settings.init(dummy_file.strpath, rdv_for_tests)

    assert 'connection' in dir(settings)
    assert 'http' in dir(settings)
    assert 'config' in dir(settings)
    assert 'remote_database_variables' in dir(settings)
