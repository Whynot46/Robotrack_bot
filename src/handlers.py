from aiogram.filters.command import Command
from aiogram import F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile, ReplyKeyboardRemove
from aiogram import Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import src.keyboards as kb
import src.db as db
import src.config as config
import re


router = Router()


class User_data(StatesGroup):
    child_name = State()
    child_age = State()
    parent_number = State()


class Week(StatesGroup):
    week = State()
    weekday = State()


@router.message(Command("start"))
async def start_loop(message: Message, bot: Bot, state = FSMContext):
    await message.answer("Привет! Я бот из Роботрека!\n"
                "Хочешь просмотреть расписание?\n"
                "Хочешь записаться на занятие?\n"
                "Хочешь связаться с преподавателем?\n"
                "На эти и многие другие вопросы я смогу ответить тебе здесь!")

    if not db.is_old(message.from_user.id):
        await state.set_state(User_data.child_name)
        await message.answer("Для начала давайте познакомимся!\n"
                    "Укажите ФИО ребёнка", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Я Вас помню!\n"
                    "Давайте сразу же перейдём к интересующим Вас вопросам!", reply_markup=kb.main_keyboard)


@router.message(User_data.child_name)
async def put_name(message: Message, state = FSMContext):
    await state.update_data(child_name = message.text)
    await state.set_state(User_data.child_age)
    await message.answer("Сколько Вашему ребёнку полных лет?")


@router.message(User_data.child_age)
async def put_age(message: Message, state = FSMContext):
    if message.text.isdigit():
        await state.update_data(child_age = message.text)
        await state.set_state(User_data.parent_number)
        await message.answer("Укажите контактный номер родителя")
    else:
        await state.set_state(User_data.child_age)
        await message.answer("Пожалуйста, введите возраст в цифрах")


@router.message(User_data.parent_number)
async def put_parent_number(message: Message, state = FSMContext):
    phone_pattern = r'^(\+?7|8)[\s\-]?(\(?\d{3}\)?)?[\s\-]?(\d{3})[\s\-]?(\d{2})[\s\-]?(\d{2})$'
    if re.match(phone_pattern, message.text) is not None:
        await state.update_data(parent_number = message.text)
        user_data = await state.get_data()
        db.add_new_user(message.from_user.id, message.from_user.username, user_data['child_name'], user_data['child_age'], user_data['parent_number'])
        await state.set_state(None)
        await message.answer("Вы успешно зарегистрировались!", reply_markup=kb.main_keyboard)
    else:
        await state.set_state(User_data.parent_number)
        await message.answer("Пожалуйста, введите корректный номер телефона")


@router.message(F.text == "Расписание")  
async def get_shedule(message: Message, bot: Bot):  
    await message.answer_photo(caption=f"Расписание на 2024/2025 год", photo=FSInputFile("./img/shedule_2024-2025.png"), reply_markup=kb.main_keyboard)


@router.message(F.text == "О нас")  
async def get_shedule(message: Message, bot: Bot, state = FSMContext):  
    await message.answer("Детский клуб робототехники Роботрек\n"
                        "Наш адрес - ул. Савушкина, 4, корп. 6 (офис 307, этаж 3)\n"
                        "Режим работы - Вт-Вс 10:00–20:00\n"
                        "VK - https://vk.com/robotrackast\n"
                        "TG - https://t.me/s/robotrackast")


@router.message(F.text == "Записаться на занятие")  
async def sign_up(message: Message, bot: Bot, state = FSMContext):
    await state.set_state(Week.week)
    await message.answer("Какая неделя Вас интересует?", reply_markup=kb.get_week_keyboard())


@router.message(Week.week)
async def put_weekday(message: Message,state = FSMContext):
    await state.update_data(week = message.text)
    await state.set_state(Week.weekday)
    if message.text[:14] == "Текущая неделя":
        await message.answer("Выберите день недели", reply_markup=kb.get_weekday_keyboard(config.get_current_week()))
    else:
        await message.answer("Выберите день недели", reply_markup=kb.get_weekday_keyboard(config.get_next_week()))


@router.message(Week.weekday)
async def put_weekday(message: Message,state = FSMContext):
    await state.update_data(weekday = message.text)
    await message.answer(f"Здесь будет расписание на {message.text}", reply_markup=kb.main_keyboard)


