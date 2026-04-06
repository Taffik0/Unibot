from aiogram import Bot, Dispatcher, types
import asyncio

API_TOKEN = "7125067226:AAFUzHXjzImkmzZ7jUbAq-eZxOd4rVJM7yg"


async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    @dp.message()
    async def echo(message: types.Message):
        await message.answer(message.text)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

asyncio.run(main())
