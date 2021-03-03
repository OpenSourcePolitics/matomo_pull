from datetime import timedelta
import settings as s


def date_to_str(date):
    return date.strftime('%Y-%m-%d')


def get_date_range():
    rolling_date = s.secrets['api_settings']['start_date']
    end_date = s.secrets['api_settings']['end_date']
    date_range = []
    while rolling_date <= end_date:
        date_range.append(date_to_str(rolling_date))
        rolling_date += timedelta(1)

    return date_range
