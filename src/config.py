import datetime


DB_PATH = "./db/Data.db"
API_TOKEN = "API_TOKEN"


def get_current_week():
    current_week =[]
    today = datetime.datetime.today()
    weekday = today.weekday()
    week_begin = today - datetime.timedelta(days=weekday) 
    current_week.append(week_begin.strftime("%d.%m.%Y"))
    for i in range(6):
        week_begin += datetime.timedelta(days=1)
        current_week.append(week_begin.strftime("%d.%m.%Y"))

    return current_week


def get_next_week(datetime):
    next_week =[]
    today = datetime.datetime.today()
    weekday = today.weekday()
    week_begin = today - datetime.timedelta(days=weekday) + datetime.timedelta(days=7)
    next_week.append(week_begin.strftime("%d.%m.%Y"))
    for i in range(6):
        week_begin += datetime.timedelta(days=1)
        next_week.append(week_begin.strftime("%d.%m.%Y"))

    return next_week