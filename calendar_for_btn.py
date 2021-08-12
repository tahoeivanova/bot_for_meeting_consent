import time
import datetime
from datetime import datetime as dt
from calendar import Calendar


def today_is():
    return time.strftime("%a %d %Y", time.localtime())

def calendar_iterator(year=dt.today().year, month=dt.today().month):
    c = Calendar()
    weekdays = c.itermonthdates(year, month)
    return weekdays
    # return c.monthdatescalendar(year, month)

def nearest_7_days():
    weekdays = calendar_iterator()
    these_7_days = [date for date in weekdays if is_nearest_week_date(date)]
    return these_7_days

def is_nearest_week_date(date):
    if (date >= dt.today().date()) and (date <= dt.today().date() + datetime.timedelta(days=7)):
        return date

def iterate_over_hours(date, start=19,stop=23):
    chosen_date = datetime.datetime(year=date.year, month=date.month, day=date.day, hour=0, minute=0)
    hours_in_day = [chosen_date+datetime.timedelta(hours=n, minutes=m+30) for n in range(start, stop) for m in range(0, 60, 30)]
    return hours_in_day

def calendar_pretty(year=dt.today().year, month=dt.today().month):
    calendar = list(calendar_iterator(year, month))[0]
    return [y.strftime("%d")  for y in calendar]

def validate_data(data, strformat):
    try:
        dt.strptime(data, strformat)
        return True
    except ValueError as e:
        return None

if __name__ == '__main__':
    # these_7_days = nearest_7_days()
    date = nearest_7_days()[0]
    if date.weekday() == 5:
        print(date)
    # print(datetime.datetime(year=dt.today().year, month=dt.today().month, day=dt.today().day)+datetime.timedelta(hours=1))
    # hours = iterate_over_hours(date)
    # for datetime in hours:
    #     print(datetime.strftime("%H"))
    # print(dt.today().date() + datetime.timedelta(days=10))
