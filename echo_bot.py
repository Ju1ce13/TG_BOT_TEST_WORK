import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from config import ECHO_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=ECHO_TOKEN)
dp = Dispatcher()

@dp.message()
async def handle_message(message: types.Message):
    await message.answer(message.text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())