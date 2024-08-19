import datetime


DB_PATH = "./db/Data.db"
API_TOKEN = "7083391110:AAHXU4X4h2U-FuHm0vmJfy3mTQoBAiD_HKk"


def get_today():
    datetime_obj = datetime.datetime.today()
    return datetime_obj.strftime("%d.%m.%Y")


def switch_to_next_week(day : str) -> str:
    format = "%d.%m.%Y"
    datetime_obj = datetime.datetime.strptime(day, format)
    datetime_obj += datetime.timedelta(days=7)
    next_week_day = datetime_obj.strftime("%d.%m.%Y")

    return next_week_day


def get_weekday(day : str) -> str:
    week = ("Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье")
    format = "%d.%m.%Y"
    datetime_obj = datetime.datetime.strptime(day, format)
    weekday = datetime_obj.weekday()
    return f"{week[weekday]}\n{datetime_obj.strftime('%d.%m.%Y')}"
    


# def get_weekday_list(week : list) -> list:
#     weekday_list = []
#     for day in week:
#         weekday_list.append(f"{get_weekday(day)}\n{day}")
#     return weekday_list


def get_current_week() -> list:
    current_week =[]
    today = datetime.datetime.today()
    weekday = today.weekday()
    week_begin = today - datetime.timedelta(days=weekday) 
    current_week.append(week_begin.strftime("%d.%m.%Y"))
    for i in range(6):
        week_begin += datetime.timedelta(days=1)
        current_week.append(week_begin.strftime("%d.%m.%Y"))

    return current_week


def get_next_week() -> list:
    next_week =[]
    today = datetime.datetime.today()
    weekday = today.weekday()
    week_begin = today - datetime.timedelta(days=weekday) + datetime.timedelta(days=7)
    next_week.append(week_begin.strftime("%d.%m.%Y"))
    for i in range(6):
        week_begin += datetime.timedelta(days=1)
        next_week.append(week_begin.strftime("%d.%m.%Y"))

    return next_week