from datetime import timedelta
from . import settings as s


def get_date_range():
    rolling_date = s.secrets['api_settings']['start_date']
    end_date = s.secrets['api_settings']['end_date']
    date_range = []
    while rolling_date <= end_date:
        date_range.append(str(rolling_date))
        rolling_date += timedelta(1)

    return date_range
