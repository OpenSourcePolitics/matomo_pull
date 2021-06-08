from .date_handling import get_date_range
from .url_handling import set_url, http_get


def set_data_objects_for_sql_conversion(reports_map):
    data_objects = {}
    for table_name, table_parameters in reports_map.items():
        data_objects[table_name] = set_data_object_from_url(
            table_name,
            table_parameters
        )
    return data_objects


def set_data_object_from_url(table_name, parameters={}):
    data = []
    if parameters.get('date_range'):
        range = get_date_range()
        for day in range:
            url = set_url(table_name, {'date': day})
            raw_data = http_get(url)
            current_parsed_data = parse_range_data(raw_data, day)
            data.extend(current_parsed_data)
    else:
        data = http_get(set_url(table_name))

    return remove_empty_values(data) if isinstance(data, dict) else data


def parse_range_data(raw_data, day):
    for entry in raw_data:
        entry['date'] = day
        if entry.get('subtable'):
            for sub_entry in entry['subtable']:
                sub_entry['sub_type'] = entry["label"]
                raw_data.append(sub_entry)
            entry.pop('subtable')

    return raw_data


def remove_empty_values(d):
    dictionnary_updated = {}
    for k, v in d.items():
        if v:
            dictionnary_updated[k] = v

    return dictionnary_updated
