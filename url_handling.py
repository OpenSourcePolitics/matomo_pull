import settings as s


def set_url(report_type, request_args={}):
    api_settings = s.secrets['api_settings']
    url_args = api_settings['url_parameters'].copy()
    url_args.update(s.secrets['requests'][report_type]['url_parameters'])
    url_args.update(request_args)
    if not url_args.get('date'):
        url_args['date'] = (
            f"{api_settings['start_date']},{api_settings['end_date']}"
        )
    url = api_settings['base_url']
    for key, value in url_args.items():
        url += f"&{key}={value}"

    return url
