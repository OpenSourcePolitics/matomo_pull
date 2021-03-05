import pandas as pd
from . import settings as s


def convert_file_to_sql(data_object, table_name, params={}):
    df = pd.DataFrame(data_object)
    params = s.secrets['requests'][table_name]
    if params.get("need_transpose"):
        df = df.transpose()
        df = df.reset_index()
        df = df.rename(columns={"index": params.get("index_column_new_name")})
    df.to_sql(
        table_name.replace("_report", ""),
        s.connection,
        if_exists='replace'
    )


def fill_database(data_objects):
    for table_name, data_object in data_objects.items():
        convert_file_to_sql(data_object, table_name)
