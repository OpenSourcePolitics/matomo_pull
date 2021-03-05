import json
from .date_handling import get_date_range
from .url_handling import set_url, http_get


def set_report_from_url(file_name, parameters):
    data = []
    if parameters.get('date_range'):
        for day in get_date_range():
            url = set_url(file_name, {'date': day})
            raw_data = json.loads(http_get(url))
            current_parsed_data = parse_data(raw_data, day)
            data.extend(current_parsed_data)
    else:
        data = json.loads(http_get(set_url(file_name)))

    return data


def set_files_for_sql_conversion(reports_map):
    data_objects = {}
    for report_name, report_parameters in reports_map.items():
        data_objects[report_name] = set_report_from_url(
            report_name,
            report_parameters
        )
    return data_objects


def parse_data(raw_data, day):
    for entry in raw_data:
        entry['date'] = day
        if entry.get('subtable'):
            for sub_entry in entry['subtable']:
                sub_entry['sub_type'] = entry["label"]
                raw_data.append(sub_entry)
            entry.pop('subtable')

    return raw_data
