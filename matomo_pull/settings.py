import urllib3
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
    connection = set_database_connection(remote_database_variables)


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
        'POSTGRES_USER': (
            os.environ.get('POSTGRES_USER') or data['POSTGRES_USER']
        ),
        'POSTGRES_PASSWORD': (
            os.environ.get('POSTGRES_PASSWORD') or data['POSTGRES_PASSWORD']
        ),
        'POSTGRES_HOST': (
            os.environ.get('POSTGRES_HOST') or data['POSTGRES_HOST']
        ),
        'POSTGRES_PORT': (
            os.environ.get('POSTGRES_PORT') or data['POSTGRES_PORT']
        )
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
    try:
        connection = sqlalchemy.create_engine(
            f"postgresql://{vars['POSTGRES_USER']}:{vars['POSTGRES_PASSWORD']}"
            f"@{vars['POSTGRES_HOST']}:{vars['POSTGRES_PORT']}"
            f"/{vars['db_name']}"
        )
        connection.connect()
    except Exception:
        raise ValueError(
            f"The Postgres database was wrongly configured."
            f"Available variables are {vars}."
        )

    return connection


def check_database():
    try:
        connection.execute("select * from visits")
        is_database_created = True
    except:
        is_database_created = False
    return is_database_created


def update_start_date_regarding_database_state(remote_database_variables):
    # import pdb; pdb.set_trace()
    if is_database_created:
        last_update = datetime.strptime(
            connection.execute("select date from visits order by date desc limit 1").fetchall()[0][0],
            '%Y-%m-%d'
        ).date()
    
        if last_update == date.today() - timedelta(days = 1):
            raise NotImplementedError("database already up to date")
        else:
            return last_update + timedelta(days = 1)
    else:
        remote_database_variables['start_date']


def update_end_date_regarding_database_state(remote_database_variables):
    return date.today() - timedelta(days = 1)
