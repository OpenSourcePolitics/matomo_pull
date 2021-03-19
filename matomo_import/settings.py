import urllib3
import yaml


def init(settings_file='secrets.yml'):
    global http, secrets, connection
    http = set_http_manager()
    secrets = set_secrets(settings_file)
    connection = set_database_connection(secrets)


def set_http_manager():
    return urllib3.PoolManager()


def set_secrets(settings_file):
    with open(settings_file, 'r') as f:
        secrets = yaml.safe_load(f)

    return secrets


def set_database_connection(secrets):
    connection = specify_database_provider(secrets['db_settings'])

    return connection


def specify_database_provider(
        db_settings={'db_provider': 'sqlite3', 'db_name': 'default'}
        ):
    if db_settings['db_provider'] == 'sqlite3':
        import sqlite3
        return sqlite3.connect(db_settings['db_name'])
    else:
        raise NotImplementedError("Database provider not handled")
