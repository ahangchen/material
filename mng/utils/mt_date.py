import calendar
from datetime import timedelta, date


def gen_calendar(year, month):
    month_first = date(year, month, 1)
    calendar_first = month_first - timedelta(days=month_first.weekday())
    calendar_dates = []

    for i in range(6):
        week_dates = []
        for j in range(7):
            week_date = calendar_first + timedelta(days=j + i * 7)
            date_items = [week_date.year, week_date.month, week_date.day]
            week_dates.append(date_items)

        calendar_dates.append(week_dates)

    return calendar_dates


def add_months(source_date, months):
    month = int(source_date.month) - 1 + months
    year = int(source_date.year + month / 12)
    month = month % 12 + 1
    day = min(source_date.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)