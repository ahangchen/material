import calendar
import datetime


def print_dates(start_date, end_date):
    for i in range((end_date - start_date).days):
        cur_date = start_date + datetime.timedelta(days=i)
        print("%d %d %d" % (cur_date.year, cur_date.month, cur_date.day))


# print_dates(datetime.date(2016, 2, 1), datetime.date(2016, 3, 2))
# print(datetime.date(2016, 3, 1) + datetime.timedelta(weeks=1, days=1))


def gen_calendar(year, month, day):
    cur_date = datetime.date(year, month, day)
    month_first = datetime.date(year, month, 1)
    calendar_first = month_first - datetime.timedelta(days=month_first.weekday())
    calendar_dates = []

    for i in range(6):
        week_dates = []
        for j in range(7):
            week_dates.append(calendar_first + datetime.timedelta(days=j + i * 7))
        calendar_dates.append(week_dates)

    for i in range(6):
        for j in range(7):
            print(calendar_dates[i][j])


def add_months(source_date, months):
    month = int(source_date.month) - 1 + months
    year = int(int(source_date.year) + month / 12)
    month = month % 12 + 1
    day = min(int(source_date.day), calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


print(add_months(datetime.date(2016, 2, 26), -1))