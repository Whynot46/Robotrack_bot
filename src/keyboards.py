from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
import src.config as config
import src.db as db


main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="🧑🏻‍💻Мой профиль")],
    [KeyboardButton(text="🗓Расписание")],
    [KeyboardButton(text="🙋🏻‍♂️Записаться на занятие")],
    [KeyboardButton(text="🏠О нас")]],
    resize_keyboard=True)


admin_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="🗓Расписание")],
    [KeyboardButton(text="🙋🏻⬇️Выгрузить БД")],
    [KeyboardButton(text="◀️Главное меню")]],
    resize_keyboard=True)


period_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Записаться на пробное занятие🤓")],
    [KeyboardButton(text="Записаться на постоянное посещение😎")],
    [KeyboardButton(text="◀️Главное меню")],],
    resize_keyboard=True)


admin_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Просмотр расписания")],
    [KeyboardButton(text="Выгрузить базу данных")]],
    resize_keyboard=True)


user_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="🙋🏻‍♂️Мои занятия")],
    [KeyboardButton(text="◀️Главное меню")]],
    resize_keyboard=True)


about_us_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="🧑🏻‍🏫Наши преподаватели")],
    [KeyboardButton(text="◀️Главное меню")]],
    resize_keyboard=True)


def get_week_keyboard() -> ReplyKeyboardMarkup:
    current_week = config.get_current_week()
    next_week = config.get_next_week()
    week_keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=f"Текущая неделя\n{current_week[0]}-{current_week[-1]}")],
        [KeyboardButton(text=f"Следующая неделя\n{next_week[0]}-{next_week[-1]}")],
        [KeyboardButton(text="❌Отмена")]],
        resize_keyboard=True)

    return week_keyboard


def get_weekday_keyboard(current_week : list) -> ReplyKeyboardMarkup:
    weekday_buttons = []
    today = config.get_today()
    if not (today in current_week):
        today = config.switch_to_next_week(today)

    while current_week[0] != today:
        current_week.pop(0)

    for weekday in current_week:
        weekday_buttons.append([KeyboardButton(text=config.get_weekday(weekday))])

    weekday_buttons.append([KeyboardButton(text="❌Отмена")])

    return ReplyKeyboardMarkup(keyboard=weekday_buttons, resize_keyboard=True)


def get_lessons_keyboard(weekday : str) -> ReplyKeyboardMarkup:
    lessons = db.get_lessons(weekday)
    lessons_buttons = []
    for lesson in lessons:
        lessons_buttons.append([KeyboardButton(text=f"{lesson[0]} {lesson[1]}\n{lesson[2]}")])

    lessons_buttons.append([KeyboardButton(text="❌Отмена")])
    
    return ReplyKeyboardMarkup(keyboard=lessons_buttons, resize_keyboard=True)