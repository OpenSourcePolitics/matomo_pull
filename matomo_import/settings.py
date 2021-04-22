import urllib3
import sqlite3
import os
import yaml
import dotenv


def init(config_file='config.yml'):
    global http, config, env, connection
    http = set_http_manager()
    config = set_config(config_file)
    env = set_env_variables()
    connection = set_database_connection()


def set_http_manager():
    return urllib3.PoolManager()


def set_config(config_file):
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)

    try:
        (
            config['base_url_parameters'], config['requests']
        )
    except KeyError:
        raise KeyError("Config file wrongly set")

    return config


def set_env_variables():
    dotenv.load_dotenv('.env', override=False)

    env = {
        'BASE_URL': os.environ['BASE_URL'],
        'DB_NAME': os.environ['DB_NAME'],
        'ID_SITE': os.environ['ID_SITE'],
        'START_DATE': os.environ['START_DATE'],
        'TOKEN_AUTH': os.environ['TOKEN_AUTH']
    }

    if '' in env.values() or not env.values():
        raise KeyError(
            f"One or multiple environment variables aren't set \n"
            f"Environment variables : {env}"
        )

    return env


def set_database_connection():
    connection = sqlite3.connect(os.environ['DB_NAME'])

    return connection
