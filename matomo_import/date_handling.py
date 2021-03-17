from datetime import timedelta, date
from . import settings as s


def get_date_range():
    rolling_date = s.secrets['api_settings']['start_date']
    end_date = s.secrets['api_settings']['end_date']

    if not isinstance(rolling_date, date) or not isinstance(end_date, date):
        raise TypeError("Date format is wrong")

    if end_date < rolling_date:
        raise ValueError("Start date and end date may be swaped !")

    date_range = []
    while rolling_date <= end_date:
        date_range.append(str(rolling_date))
        rolling_date += timedelta(1)

    return date_range
