from datetime import datetime, timedelta, date
from . import settings as s


def get_date_range():
    rolling_date = s.mtm_vars['start_date']
    end_date = s.mtm_vars['end_date']

    if not isinstance(rolling_date, date) or not isinstance(end_date, date):
        raise TypeError("Date format is wrong")

    if end_date < rolling_date:
        raise ValueError("Start date and end date may be swaped !")

    date_range = []
    while rolling_date <= end_date:
        date_range.append(str(rolling_date))
        rolling_date += timedelta(1)

    return date_range


def string_to_date(date_string):
    return datetime.strptime(date_string, '%Y-%m-%d').date()
