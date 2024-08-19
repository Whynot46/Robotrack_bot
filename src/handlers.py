from aiogram.filters.command import Command
from aiogram import F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram import Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import src.keyboards as kb
import src.db as db


router = Router()


class User_data(StatesGroup):
    child_name = State()
    child_age = State()
    parent_number = State()


@router.message(F.text, Command("start"))
async def start_loop(message: Message, bot: Bot, state = FSMContext):
    bot.send_message(message.chat.id,
                    "Привет! Я бот из Роботрека!\n"
                    "Хочешь просмотреть расписание?\n"
                    "Хочешь записаться на занятие?\n"
                    "Хочешь связаться с преподавателем?\n"
                    "На эти и многие другие вопросы я смогу ответить тебе здесь!")

    if not db.is_old(message.from_user.id):
        await state.set_state(User_data.child_name)
        bot.send_message(message.chat.id,
                    "Для начала давайте познакомимся!"
                    "Укажите ФИО ребёнка")
    else:
        bot.send_message(message.chat.id,
                    "Я Вас помню!\n"
                    "Давайте сразу же перейдём к интересующим Вас вопросам!")


@router.message(User_data.child_name)
async def get_name(message: Message,state = FSMContext):
    if message.text != "Главное меню":
        await state.update_data(child_name = message.text)
        await state.set_state(User_data.child_age)
        await message.answer("Сколько Вашему ребёнку полных лет?")
    else:
        await state.reset_state()
        bot.send_message(message.chat.id, "Главное меню", reply_markup=kb.main_keyboard)


@router.message(User_data.child_age)
async def get_name(message: Message,state = FSMContext):
    if message.text != "Главное меню":
        if message.text.isdigit():
            await state.update_data(child_age = message.text)
            await state.set_state(User_data.parent_number)
            await message.answer("Укажите контактный номер родителя")
        else:
            await state.set_state(User_data.child_age)
            await message.answer("Пожалуйста, введите возраст в цифрах")
    else:
        await state.reset_state()
        bot.send_message(message.chat.id, "Главное меню", reply_markup=kb.main_keyboard)


@router.message(User_data.parent_number)
async def get_name(message: Message,state = FSMContext):
    if message.text != "Главное меню":
        try:
            await state.update_data(parent_number = message.text)
            user_data = await state.get_data()
            db.add_new_user(message.from_user.id, message.from_user.username, user_data['child_name'], user_data['child_age'], user_data['parent_number'])
            await message.answer("Вы успешно зарегистрировались!", reply_markup=kb.main_keyboard)
        except Exception as error:
            await message.answer(f"Ошибка записи данных в базу данных, попробуйте чуть позже")
            print(f"|DB_ERROR| {error}")
    else:
        await state.reset_state()
        bot.send_message(message.chat.id, "Главное меню", reply_markup=kb.main_keyboard)


@router.message(F.text == "Расписание")  
async def get_shedule(message: Message, bot: Bot, state = FSMContext):  
    pass


@router.message(F.text == "Записаться на занятие")  
async def get_shedule(message: Message, bot: Bot, state = FSMContext):  
    pass


@router.message(F.text == "О нас")  
async def get_shedule(message: Message, bot: Bot, state = FSMContext):  
    pass


@router.callback_query(F.data)
async def track_callback(callback: CallbackQuery, bot: Bot):
    pass