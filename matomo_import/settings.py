import urllib3
import sqlite3
import yaml
import sys
from os import remove


def init(settings_file='secrets.yml'):
    set_http_manager()
    set_database(settings_file)


def set_database(settings_file):
    global connection, secrets
    with open(settings_file, 'r') as f:
        secrets = yaml.safe_load(f)
        connection = sqlite3.connect(secrets["api_settings"]["db_path"])


def set_http_manager():
    global http
    http = urllib3.PoolManager()
