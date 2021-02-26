from datetime import datetime, timedelta


def str_to_date(date_str):
    return datetime.strptime(date_str, "%d/%m/%Y").date()


def date_to_str(date):
    return date.strftime('%Y-%m-%d')


def get_date_range(start_date, end_date):
    rolling_date = str_to_date(start_date)
    end_date = str_to_date(end_date)
    date_range = []
    while rolling_date <= end_date:
        date_range.append(date_to_str(rolling_date))
        rolling_date += timedelta(1)

    return date_range
