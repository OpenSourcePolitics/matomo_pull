import settings
import json
from date_handling import get_date_range


def write_file(file_name, raw_data):
    with open(f"{file_name}.json", 'w', encoding='utf-8') as f:
        f.write(raw_data)


def set_report_from_url(file_name, parameters):
    url = parameters['url']
    if parameters.get('date_range'):
        parsed_data = []
        for day in get_date_range(parameters['start_date'], parameters['end_date']):
            url = parameters['url'].replace('date', f"date={day}")
            raw_data = json.loads(settings.http_get(url))
            current_parsed_data = parse_data(raw_data, day)
            parsed_data.extend(current_parsed_data)
        with open(f"{file_name}.json", "w", encoding='utf-8') as f:
            json.dump(parsed_data, f)
    else:
        raw_data = settings.http_get(url)
        write_file(file_name, raw_data)


def set_files_for_sql_conversion(reports_map):
    for report_name, report_parameters in reports_map.items():
        set_report_from_url(
            report_name,
            report_parameters
        )


def parse_data(raw_data, day):
    for entry in raw_data:
        entry['date'] = day
        if entry.get('subtable'):
            for sub_entry in entry['subtable']:
                sub_entry['sub_type'] = entry["label"]
                raw_data.append(sub_entry)
            entry.pop('subtable')

    return raw_data
