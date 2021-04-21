from matomo_import import (
    data_handling,
    sql_handling,
    settings
)


def exec():
    settings.init()

    data_objects = data_handling.set_data_objects_for_sql_conversion(
        settings.config['requests']
    )

    sql_handling.fill_database(data_objects)
