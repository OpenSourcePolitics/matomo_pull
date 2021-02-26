import pandas as pd
import settings


def convert_file_to_sql(file_name, params={}):
    df = pd.read_json(f"{file_name}.json")
    if params.get("need_transpose"):
        df = df.transpose()
        df = df.reset_index()
        df = df.rename(columns={"index": params.get("index_column_new_name")})
    df.to_sql(
        file_name.replace("_report", ""),
        settings.connection,
        if_exists='replace'
    )


def fill_database(reports_map):
    for name, parameters in reports_map.items():
        convert_file_to_sql(name, parameters)
