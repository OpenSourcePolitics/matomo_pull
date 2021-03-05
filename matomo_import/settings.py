import urllib3
import sqlite3
import yaml
from os import remove


def init():
    set_http_manager()
    set_database()


def set_database():
    global connection, secrets
    with open('secrets.yml', 'r') as f:
        secrets = yaml.safe_load(f)
        connection = sqlite3.connect(secrets["api_settings"]["db_path"])


def set_http_manager():
    global http
    http = urllib3.PoolManager()


def http_get(uri):
    r = http.request("GET", uri)
    return r.data.decode('utf-8')


def close():
    files = []
    for element, values in secrets['requests'].items():
        files.append(values['file'])
    # files = ['visits.json', 'pages.json', 'referrers.json']
    for file in files:
        try:
            remove(file)
        except FileNotFoundError:
            print(f"File {file} wasn't found")
