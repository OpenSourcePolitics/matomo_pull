import pytest
import matomo_pull.settings as settings
import matomo_pull.utils as utils
from .conftest import (
    rdv_for_tests,
    settings_setup,
    settings_init,
    dummy_date
)


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
        settings.set_database_connection(),
        settings.sqlalchemy.engine.base.Engine
    )


def test_database_setup_wrong(settings_setup, monkeypatch):
    monkeypatch.setenv('POSTGRES_USER', 'dummy_value')

    with pytest.raises(ValueError):
        settings.set_database_connection()


def test_database_variables_wrongly_set(tmpdir, monkeypatch):
    with pytest.raises(KeyError):
        settings.set_mtm_vars()


def test_database_already_up_to_date(settings_setup, monkeypatch):
    from datetime import date, timedelta
    monkeypatch.setattr(
        settings,
        "update_start_date_regarding_database_state",
        dummy_date
    )
    settings.mtm_vars['end_date'] = date.today() - timedelta(days=1)
    with pytest.raises(utils.DatabaseAlreadyUpdatedError):
        settings.check_mtm_vars(settings.mtm_vars)


def test_database_creation(settings_setup):
    conn = settings.set_database_connection()
    conn.execute("create table visits(id int primary key not null, date date);")
    assert settings.is_database_created()

    conn.execute("drop table visits;")
    assert not settings.is_database_created()


def test_updating_dates(settings_init, settings_setup):
    from datetime import datetime, timedelta
    from random import randint
    last_update_date = datetime.now() - timedelta(days=randint(1, 100))
    conn = settings.set_database_connection()

    conn.execute(
        "create table visits(id int primary key not null, date timestamp);"
    )
    conn.execute(
        f"insert into visits(id,date) values(1, '{last_update_date}')"
    )

    vars = settings.check_mtm_vars(settings.mtm_vars)
    assert vars['start_date'] == last_update_date.date() + timedelta(days=1)

    conn.execute("drop table visits;")


def test_all_correct(settings_init, tmpdir):
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
    assert 'mtm_vars' in dir(settings)
