from aiogram.filters.command import Command
from aiogram import F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile, ReplyKeyboardRemove
from aiogram import Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import src.keyboards as kb
import src.db as db
import src.config as config
import datetime
import re


router = Router()


class User_data(StatesGroup):
    child_name = State()
    child_age = State()
    parent_number = State()


class Lesson_record(StatesGroup):
    period = State()
    week = State()
    weekday = State()
    lesson = State()


@router.message(Command("start"))
async def start_loop(message: Message, bot: Bot, state = FSMContext):
    await message.answer("Привет! Я бот из Роботрека🤖\n"
                "Хочешь просмотреть расписание?\n"
                "Хочешь записаться на занятие?\n"
                "Хочешь связаться с преподавателем?\n"
                "На эти и многие другие вопросы я смогу ответить тебе здесь!")

    if not db.is_old(message.from_user.id):
        await state.set_state(User_data.child_name)
        await message.answer("Для начала давайте познакомимся😉\n"
                    "Укажите ФИО ребёнка", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Я Вас помню😄\n"
                    "Давайте сразу же перейдём к интересующим Вас вопросам!", reply_markup=kb.main_keyboard)


@router.message(User_data.child_name)
async def put_name(message: Message, state = FSMContext):
    await state.update_data(child_name = message.text)
    await state.set_state(User_data.child_age)
    await message.answer("Укажите дату рождения Вашего ребёнка\nФормат: ДД.ММ.ГГГГ")


@router.message(User_data.child_age)
async def put_birthdate(message: Message, state = FSMContext):
    if config.check_date(message.text):
        await state.update_data(child_age = message.text)
        await state.set_state(User_data.parent_number)
        await message.answer("Укажите контактный номер родителя")
    else:
        await state.set_state(User_data.child_age)
        await message.answer("😮Пожалуйста, введите дату рождения, согласно формату")


@router.message(User_data.parent_number)
async def put_parent_number(message: Message, state = FSMContext):
    phone_pattern = r'^(\+?7|8)[\s\-]?(\(?\d{3}\)?)?[\s\-]?(\d{3})[\s\-]?(\d{2})[\s\-]?(\d{2})$'
    if re.match(phone_pattern, message.text) is not None:
        await state.update_data(parent_number = message.text)
        user_data = await state.get_data()
        db.add_new_user(message.from_user.id, message.from_user.username, user_data['child_name'], user_data['child_age'], user_data['parent_number'])
        await state.set_state(None)
        await message.answer("✅Вы успешно зарегистрировались!", reply_markup=kb.main_keyboard)
    else:
        await state.set_state(User_data.parent_number)
        await message.answer("😮Пожалуйста, введите корректный номер телефона")


@router.message(Command("admin"))
async def open_admin_panel(message: Message, bot: Bot, state = FSMContext):
    if str(message.from_user.id) in config.ADMIN_ID:
        await message.answer("🛠Панель администратора")


@router.message(F.text == "🧑🏻‍💻Мой профиль")  
async def get_user_profile(message: Message, bot: Bot):  
    await message.answer(f"Профиль пользователя @{db.get_username(message.from_user.id)}\n"
                        f"ФИО ребёнка: {db.get_child_name(message.from_user.id)}\n"
                        f"ДР ребёнка: {db.get_child_birthday(message.from_user.id)} ({config.calculate_age(db.get_child_birthday(message.from_user.id))} лет)\n"
                        f"Номер родителя: {db.get_parent_number(message.from_user.id)}"
                        , reply_markup=kb.user_keyboard)


@router.message(F.text == "◀️Главное меню")  
async def get_shedule(message: Message, bot: Bot):  
    await message.answer("🏠Главное меню", reply_markup = kb.main_keyboard)


@router.message(F.text == "🙋🏻‍♂️Мои занятия")  
async def get_shedule(message: Message, bot: Bot):  
    await message.answer("Здесь будет список Ваших занятий", reply_markup = kb.main_keyboard)


@router.message(F.text == "🗓Расписание")  
async def get_shedule(message: Message, bot: Bot):  
    await message.answer_photo(caption=f"Расписание на 2024/2025 год", photo=FSInputFile("./img/shedule_2024-2025.png"), reply_markup=kb.main_keyboard)


@router.message(F.text == "🏠О нас")  
async def get_shedule(message: Message, bot: Bot, state = FSMContext):  
    await message.answer("Детский клуб робототехники Роботрек\n"
                        "Наш адрес - ул. Савушкина, 4, корп. 6 (офис 307, этаж 3)\n"
                        "Режим работы - Вт-Вс 10:00–20:00\n"
                        "TG - https://t.me/s/robotrackast\n"
                        "VK - https://vk.com/robotrackast\n"
                        , reply_markup=kb.about_us_keyboard)


@router.message(F.text == "🧑🏻‍🏫Наши преподаватели")  
async def get_shedule(message: Message, bot: Bot):  
    await message.answer("Здесь будет список наших преподавателей", reply_markup = kb.main_keyboard)


@router.message(F.text == "🙋🏻‍♂️Записаться на занятие")  
async def sign_up(message: Message, bot: Bot, state = FSMContext):
    await state.set_state(Lesson_record.period)
    await message.answer("Как часто вы собираетесь посещать занятие?", reply_markup = kb.period_keyboard)


@router.message(Lesson_record.period)
async def put_period(message: Message, state = FSMContext):
    if message.text != "❌Отмена":
        if message.text == "Записаться на пробное занятие🤓" or message.text == "Записаться на постоянное посещение😎":
            await state.update_data(period = message.text)
            await state.set_state(Lesson_record.week)
            await message.answer("Какая неделя Вас интересует?", reply_markup=kb.get_week_keyboard())
        else:
            await state.set_state(Lesson_record.period)
            await message.answer("😮Пожалуйста, выберите частоту посещения занятия из предложенного списка")
    else:
        await state.clear()
        await message.answer("❌Запись отменена", reply_markup=kb.main_keyboard)


@router.message(Lesson_record.week)
async def put_weekday(message: Message, state = FSMContext):
    if message.text != "❌Отмена":
        await state.update_data(Lesson_record = message.text)
        await state.set_state(Lesson_record.weekday)
        if message.text[:14] == "Текущая неделя":
            await message.answer("Выберите день недели", reply_markup=kb.get_weekday_keyboard(config.get_current_week()))
        else:
            await message.answer("Выберите день недели", reply_markup=kb.get_weekday_keyboard(config.get_next_week()))
    else:
        await state.clear()
        await message.answer("❌Запись отменена", reply_markup=kb.main_keyboard)


@router.message(Lesson_record.weekday)
async def put_weekday(message: Message, state = FSMContext):
    if message.text != "❌Отмена":
        await state.update_data(weekday = message.text)
        await state.set_state(Lesson_record.lesson)
        await message.answer(f"Расписание на {message.text}", reply_markup=kb.get_lessons_keyboard((message.text).split('\n')[0]))
    else:
        await state.clear()
        await message.answer("❌Запись отменена", reply_markup=kb.main_keyboard)


@router.message(Lesson_record.lesson)
async def put_lesson(message: Message, state = FSMContext):
    if message.text != "❌Отмена":
        await state.update_data(lesson = message.text)
        data = await state.get_data()
        weekday, date = (data['weekday']).split("\n")
        topic, time = (data['lesson']).split("\n")
        topic, age = topic.split(" ", maxsplit=1)
        if db.sign_up_to_lesson(date, time, topic, age, message.from_user.id): 
            await message.answer(f"✅Вы записаны на урок\n"
                                f"{topic} {time}\n"
                                f"{weekday} {date}", reply_markup=kb.main_keyboard)
        elif db.sign_up_to_lesson(date, time, topic, age, message.from_user.id) == False:
            await message.answer(f"😔К сожалению, на этом занятии нет свободен\nПопробуйте записаться на другой день", reply_markup=kb.admin_keyboard)
        elif db.sign_up_to_lesson(date, time, topic, age, message.from_user.id) == None:
            await message.answer("🙋🏻‍♂️Вы уже записаны на этот урок", reply_markup=kb.main_keyboard)
    else:
        await state.clear()
        await message.answer("❌Запись отменена", reply_markup=kb.main_keyboard)