from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
import src.config as config


main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Расписание")],
    [KeyboardButton(text="Записаться на занятие")],
    [KeyboardButton(text="О нас")]],
    resize_keyboard=True)


def get_week_keyboard() -> ReplyKeyboardMarkup:
    current_week = config.get_current_week()
    next_week = config.get_next_week()
    week_keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=f"Текущая неделя\n{current_week[0]}-{current_week[-1]}")],
        [KeyboardButton(text=f"Следующая неделя\n{next_week[0]}-{next_week[-1]}")]],
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

    return ReplyKeyboardMarkup(keyboard=weekday_buttons)
