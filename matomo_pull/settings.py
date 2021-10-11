import urllib3
import sqlite3
import sqlalchemy
import os
import yaml


def init(data_file='config.yml', raw_database_variables={}):
    global http, config, remote_database_variables, connection
    http = set_http_manager()
    config = set_config(data_file)
    remote_database_variables = set_remote_database_variables(
        raw_database_variables
    )
    connection = set_database_connection(raw_database_variables)


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
        'end_date': data['end_date'],
        'token_auth': data['token_auth'],
        'JWT_SECRET_KEY': os.environ['JWT_SECRET_KEY'],
    }

    if (
        '' in remote_database_variables.values() or not
        remote_database_variables.values()
    ):
        raise KeyError(
            f"One or multiple configuration variables aren't set \n"
            f"Configuration variables : {remote_database_variables}"
        )

    return remote_database_variables


def set_database_connection(vars=None):
    if vars.get('POSTGRES_USER'):
        user = vars['POSTGRES_USER']
        password = vars['POSTGRES_PASSWORD']
        host = vars['POSTGRES_HOST']
        port = vars['POSTGRES_PORT']
        db_name = vars['db_name'].lower()
        
        connection = sqlalchemy.create_engine(
            f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
        )
        try:
            connection.connect()
        except:
            raise ValueError(
                "The Postgres database was wrongly configured. Available variables:"
                f"POSTGRES_USER: {user}"
                f"POSTGRES_SERVER: {host}"
                f"POSTGRES_PORT: {port}"
            )
    else:
        connection = sqlite3.connect(remote_database_variables['db_name'])

    return connection
