import json
import os
from . import settings as s


def set_url(report_type, request_args={}):
    try:
        api_settings = s.secrets['api_settings']
        base_url_parameters = api_settings['url_parameters']
        base_url = os.getenv('BASE_URL') or api_settings['base_url']
        url_parameters = s.secrets['requests'][report_type]['url_parameters']
    except KeyError:
        raise KeyError("Error in settings definition")

    url_args = base_url_parameters.copy()
    url_args.update(url_parameters)
    url_args.update(request_args)
    if not s.secrets['requests'][report_type].get('date_range'):
        url_args['date'] = (
            f"{api_settings['start_date']},{api_settings['end_date']}"
        )
    url = base_url + "index.php?"
    for key, value in url_args.items():
        url += f"&{key}={value}"

    return url


def http_get(url):
    try:
        response = json.loads(s.http.request("GET", url).data.decode('utf-8'))
    except Exception:
        raise ValueError(f"Request returns unhandable data: {url}")

    if isinstance(response, dict) and response.get('result'):
        raise ValueError(f"Request returns error: {url}")

    return response
