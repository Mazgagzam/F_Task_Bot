import asyncio
import logging

from aiogram import Bot, Dispatcher

from handler import router

logging.basicConfig(level=logging.INFO)

TOKEN = "6822419474:AAF7x_Bd7FEYQo-EuYZ_GsOKXak8-czC9Ik"


async def main():
    bot = Bot(token=TOKEN)

    dp = Dispatcher()

    dp.include_router(router)
    await dp.start_polling(bot)


asyncio.run(main())
