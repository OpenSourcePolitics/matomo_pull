import urllib3
import sqlite3
import os
import yaml


def init(data_file='config.yml', raw_database_variables={}):
    global http, config, remote_database_variables, connection
    http = set_http_manager()
    config = set_config(data_file)
    remote_database_variables = set_remote_database_variables(
        raw_database_variables
    )
    connection = set_database_connection()


def set_http_manager():
    return urllib3.PoolManager()


def set_config(config_file='config.yml'):
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)

    try:
        (
            config['base_url_parameters'], config['requests']
        )
    except KeyError:
        raise KeyError("Config file wrongly set")

    return config


def set_remote_database_variables(data={}):
    remote_database_variables = {
        'base_url': data['base_url'],
        'db_name': data['db_name'],
        'id_site': data['id_site'],
        'start_date': data['start_date'],
        'token_auth': data['token_auth'],
        'JWT_SECRET_KEY': os.environ['JWT_SECRET_KEY']
    }

    if (
        '' in remote_database_variables.values()
        or not remote_database_variables.values()
    ):
        raise KeyError(
            f"One or multiple configuration variables aren't set \n"
            f"Configuration variables : {remote_database_variables}"
        )

    return remote_database_variables


def set_database_connection():
    connection = sqlite3.connect(remote_database_variables['db_name'])

    return connection
