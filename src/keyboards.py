from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup


main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Расписание")],
    [KeyboardButton(text="Записаться на занятие")],
    [KeyboardButton(text="О нас")]],
    resize_keyboard=True)
