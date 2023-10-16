import pandas as pd
from . import settings as s


def fill_database(data_objects):
    for table_name, data_object in data_objects.items():
        convert_data_object_to_sql(
            table_name,
            s.config['requests'][table_name],
            data_object
        )


def convert_data_object_to_sql(table_name, table_params, data_object):
    df = pd.DataFrame(data_object)
    if table_params.get("need_transpose"):
        df = df.transpose()
        df = df.reset_index()
        df = df.rename(
            columns={"index": table_params.get("index_column_new_name")}
        )
    try:
        df['date'] = df['date'].apply(pd.to_datetime)
    except Exception:
        print(f'no date field currently for table {table_name}')
    finally:
        if s.is_database_created(table_name):
            res = s.connection.execute(
                f"select column_name from information_schema.columns"
                f" where table_name='{table_name}'"
            ).fetchall()
            database_cols = [i[0] for i in res]
            database_cols = list(set(database_cols) & set(df.columns.tolist()))
            df = df[database_cols]
        df.to_sql(
            table_name,
            s.connection,
            if_exists='append',
            schema='matomo'
        )
        print(table_name)
