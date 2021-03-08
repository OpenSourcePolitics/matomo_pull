import pytest
import matomo_import.settings as settings


def test_initialize_secrets_not_correct(tmpdir):
    dummy_file = tmpdir.join('dummy_secrets.yml')
    dummy_file.write("dummy_key: dummy_value")

    with pytest.raises(KeyError):
        settings.init(dummy_file.strpath)


def test_initialize_file_not_found():
    with pytest.raises(FileNotFoundError):
        settings.init('dummy_file.yml')


def test_initialize_all_correct(tmpdir):
    dummy_file = tmpdir.join('dummy_secrets.yml')
    dummy_file.write("""
        db_settings:
            db_provider: sqlite3
            db_name: dummy_database
        requests:
            dummy_table: None
    """)

    settings.init(dummy_file.strpath)

    assert 'connection' in dir(settings)
    assert 'http' in dir(settings)
    assert 'secrets' in dir(settings)
