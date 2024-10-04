from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
import src.config as config
import src.db as db


user_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="🧑🏻‍💻Мой профиль")],
    [KeyboardButton(text="📅Расписание")],
    [KeyboardButton(text="🙋🏻‍♂️Записаться на занятие")],
    [KeyboardButton(text="🏠О нас")]
    ], resize_keyboard=True)


admin_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="🛠Панель администратора")],
    [KeyboardButton(text="📅Расписание")],
    [KeyboardButton(text="🏠О нас")],
    ], resize_keyboard=True)


admin_panel_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="📋Занятия")],
    [KeyboardButton(text="🙋🏻⬇️Выгрузить БД")],
    [KeyboardButton(text="👾Администраторы")],
    [KeyboardButton(text="◀️Главное меню")]
    ], resize_keyboard=True)


edit_admin_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🧑🏻‍🔧Добавить", callback_data="add_admin")],
    [InlineKeyboardButton(text="🚫Удалить", callback_data="delete_admin")]
    ])


db_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🙋🏻Пользователи", callback_data="users_data")],
    [InlineKeyboardButton(text="🪧Расписание", callback_data="shedule_data")],
    [InlineKeyboardButton(text="📋Занятия", callback_data="lessons_data")]
    ])


edit_children_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✏️Изменить", callback_data="edit_children_list")]
    ])


period_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Записаться на пробное занятие🤓")],
    [KeyboardButton(text="Записаться на постоянное посещение😎")],
    [KeyboardButton(text="◀️Главное меню")],
    ], resize_keyboard=True)


user_profile_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="🙋🏻‍♂️Мои занятия")],
    [KeyboardButton(text="◀️Главное меню")]
    ], resize_keyboard=True)


about_us_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="🧑🏻‍🏫Наши преподаватели")],
    [KeyboardButton(text="◀️Главное меню")]
    ], resize_keyboard=True)


def get_children_keyboard(children : list) -> InlineKeyboardMarkup:
    if len(children)>0:
        children_buttons = []
        for child in children:
            children_buttons.append([InlineKeyboardButton(text=child, callback_data=f"chouse_{child}")])
        children_keyboard = InlineKeyboardMarkup(inline_keyboard=children_buttons)
        return children_keyboard
    
    else:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="😭Нет записей", callback_data="no_children")]
        ])


def get_accept_keyboard(child : str):
    accept_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅Подтвердить", callback_data=f"delete_{child}")],
        [InlineKeyboardButton(text="☑️Отменить", callback_data=f"cancel_{child}")]
        ])
    
    return accept_keyboard


def get_week_keyboard() -> ReplyKeyboardMarkup:
    current_week = config.get_current_week()
    next_week = config.get_next_week()
    week_keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=f"Текущая неделя\n{current_week[0]}-{current_week[-1]}")],
        [KeyboardButton(text=f"Следующая неделя\n{next_week[0]}-{next_week[-1]}")],
        [KeyboardButton(text="❌Отмена")]
        ], resize_keyboard=True)

    return week_keyboard


def get_weekday_keyboard(current_week : list) -> ReplyKeyboardMarkup:
    weekday_buttons = []
    today = config.get_today()
    if not (today in current_week):
        today = config.switch_to_next_week(today)

    else:
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