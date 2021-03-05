from matomo_import import (
    file_handling,
    sql_handling,
    settings
)
import yaml


def main():
    try:
        settings.init()
        reports = {}
        with open('secrets.yml', 'r') as f:
            reports = yaml.safe_load(f)['requests']

        data_objects = file_handling.set_files_for_sql_conversion(reports)
        sql_handling.fill_database(data_objects)
    finally:
        settings.close()


main()
