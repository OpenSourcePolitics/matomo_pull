import json
from datetime import date
from . import settings as s


def set_url(report_type, request_args={}):
    base_url_parameters = s.config['base_url_parameters']
    url_parameters = s.config['requests'][report_type]['url_parameters']

    url = set_basic_url_with_env_variables()
    url_args = base_url_parameters.copy()
    url_args.update(url_parameters)
    url_args.update(request_args)
    if not s.config['requests'][report_type].get('date_range'):
        start_date = s.remote_database_variables['start_date']
        end_date = s.remote_database_variables.get('end_date') or \
            date.today().strftime("%Y-%m-%d")
        url_args['date'] = f"{start_date},{end_date}"

    for key, value in url_args.items():
        url += f"&{key}={value}"

    return url


def set_basic_url_with_env_variables():
    url = (
        f"{s.remote_database_variables['base_url']}index.php?"
        f"&token_auth={s.remote_database_variables['token_auth']}"
        f"&idSite={s.remote_database_variables['id_site']}"
    )

    return url


def http_get(url):
    try:
        response = json.loads(s.http.request("GET", url).data.decode('utf-8'))
    except Exception:
        raise ValueError(f"Request returns unhandable data: {url}")

    if isinstance(response, dict) and response.get('result'):
        raise ValueError(f"Request returns error: {url}")

    return response
