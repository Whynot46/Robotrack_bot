from aiogram.filters.command import Command
from aiogram import F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram import Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import src.keyboards as kb
import src.db as db


router = Router()


class State_class(StatesGroup):
    name = State()


@router.message(F.text, Command("start"))
async def start_loop(message: Message, bot: Bot):
    pass
            
        
@router.message(F.text == "/command")  
async def find_track(message: Message, bot: Bot, state = FSMContext):  
    pass
    

@router.callback_query(F.data)
async def track_callback(callback: CallbackQuery, bot: Bot):
    pass