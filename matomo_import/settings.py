import urllib3
import yaml


def init(settings_file='secrets.yml'):
    set_http_manager()
    set_secrets(settings_file)
    set_database()


def set_http_manager():
    global http
    http = urllib3.PoolManager()


def set_secrets(settings_file):
    global secrets
    with open(settings_file, 'r') as f:
        secrets = yaml.safe_load(f)


def set_database():
    if not secrets:
        raise ValueError("Secrets not defined !")
    global connection
    connection = specify_database_provider(secrets['db_settings'])


def specify_database_provider(
        db_settings={'db_provider': 'sqlite3', 'db_name': 'default'}
        ):
    if db_settings['db_provider'] == 'sqlite3':
        import sqlite3
        return sqlite3.connect(db_settings['db_name'])
    else:
        raise NotImplementedError("Database provider not handled")
