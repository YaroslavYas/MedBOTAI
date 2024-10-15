import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import types, F


from variables import TOKEN
from openai_message import OpenAIMessage

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Привет! Отправь мне текст или фото, и я помогу тебе.")


@dp.message(F.photo)
async def handle_photo(message: types.Message):
    photo = message.photo[-1]
    file_info = await message.bot.get_file(photo.file_id)
    file = await message.bot.download_file(file_info.file_path)
    await message.answer(OpenAIMessage().send_image(file))


@dp.message()
async def text_message_handler(message: Message) -> None:
    await message.answer(OpenAIMessage().send_message(message.text))


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

