import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from config import BOT_TOKEN
from src.handlers import router
from aiogram.fsm.storage.memory import MemoryStorage
from db.database import init_db


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


async def main():
    logging.basicConfig(level=logging.INFO)
    dp.include_router(router)
    init_db()
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())