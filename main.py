import asyncio
import logging
import sys

from os import getenv
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from variables import TOKEN
from openai_message import OpenAIMessage

dp = Dispatcher()


@dp.message()
async def command_start_handler(message: Message) -> None:
    await message.answer(OpenAIMessage(message.text).send_message())

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

