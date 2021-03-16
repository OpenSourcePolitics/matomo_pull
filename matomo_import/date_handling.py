from datetime import timedelta, date
from . import settings as s


def get_date_range():
    rolling_date = s.secrets['api_settings']['start_date']
    end_date = s.secrets['api_settings']['end_date']

    assert_error_msg = "Date format is wrong"
    assert isinstance(rolling_date, date), assert_error_msg
    assert isinstance(end_date, date), assert_error_msg

    assert rolling_date <= end_date, f"""
        Start date and end date may be swaped !\
        Start date: {rolling_date},end_date: {end_date}
    """

    date_range = []
    while rolling_date <= end_date:
        date_range.append(str(rolling_date))
        rolling_date += timedelta(1)

    return date_range
