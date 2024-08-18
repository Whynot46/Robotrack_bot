import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from src.handlers import router
from src.config import API_TOKEN


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())


async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

                
if __name__ == "__main__":
    try:
        print('Bot is running...')
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')