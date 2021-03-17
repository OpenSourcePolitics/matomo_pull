from json import loads
from . import settings as s


def set_url(report_type, request_args={}):
    try:
        api_settings = s.secrets['api_settings']
        base_url_parameters = api_settings['url_parameters']
        base_url = api_settings['base_url']
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
    url = base_url
    for key, value in url_args.items():
        url += f"&{key}={value}"

    return url


def http_get(url):
    response = loads(s.http.request("GET", url).data.decode('utf-8'))
    if isinstance(response, dict) and response.get('result'):
        raise BaseException(f"Error in API call : {response['message']}")

    return response
