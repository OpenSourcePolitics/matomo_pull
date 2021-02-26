import file_handling
import sql_handling
import settings
import yaml


def main():
    try:
        settings.init()
        reports = {}
        with open('secrets.yml', 'r') as f:
            reports = yaml.safe_load(f)['requests']

        file_handling.set_files_for_sql_conversion(reports)
        sql_handling.fill_database(reports)
    finally:
        settings.close()


main()
