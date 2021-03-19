import pandas as pd
from . import settings as s


def convert_data_object_to_sql(table_name, table_params, data_object):
    df = pd.DataFrame(data_object)
    if table_params.get("need_transpose"):
        df = df.transpose()
        df = df.reset_index()
        df = df.rename(
            columns={"index": table_params.get("index_column_new_name")}
        )
    df.to_sql(
        table_name,
        s.connection,
        if_exists='replace'
    )


def fill_database(data_objects):
    for table_name, data_object in data_objects.items():
        convert_data_object_to_sql(
            table_name,
            s.secrets['requests'][table_name],
            data_object
        )
