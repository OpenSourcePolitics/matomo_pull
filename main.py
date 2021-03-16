from matomo_import import (
    data_handling,
    sql_handling,
    settings
)
import yaml


def main():
    settings.init()
    reports = {}
    with open('secrets.yml', 'r') as f:
        reports = yaml.safe_load(f)['requests']

    data_objects = data_handling.set_data_objects_for_sql_conversion(
        reports
    )
    sql_handling.fill_database(data_objects)


main()
